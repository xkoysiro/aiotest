from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject
import logging
import asyncio
from app.text_generate import ai_generate
from app.context_manager import UserContextManager

# Инициализация роутера и менеджера контекста
router = Router()
context_manager = UserContextManager(max_messages=15)


@router.message(Command("start"))
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    logging.info(f"👤 Пользователь {user_id} запустил бота")

    # Очищаем существующий контекст и создаем новый
    context_manager.clear_context(user_id)

    # Добавляем системное сообщение с инструкциями
    system_message = """Вы - полезный AI ассистент. Отвечайте на вопросы подробно и вежливо.
Поддерживайте контекст разговора и учитывайте предыдущие сообщения."""

    context_manager.add_message(user_id, 'system', system_message)

    welcome_text = """🤖 Добро пожаловать! 

Я ваш AI-помощник с памятью о нашем разговоре. 

Доступные команды:
/clear - очистить историю диалога
/history - показать историю
/context - информация о контексте

Напишите ваш вопрос или сообщение..."""

    await message.answer(welcome_text)


@router.message(Command("clear"))
async def clear_command(message: types.Message):
    """Очистка контекста диалога"""
    user_id = message.from_user.id
    if context_manager.clear_context(user_id):
        await message.answer("🧹 Контекст диалога очищен. Начните новый разговор.")
    else:
        await message.answer("ℹ️ Контекст уже пуст.")


@router.message(Command("history"))
async def history_command(message: types.Message):
    """Показывает текущую историю диалога"""
    user_id = message.from_user.id
    messages = context_manager.get_messages(user_id, include_system=False)

    if not messages:
        await message.answer("📝 История диалога пуста.")
        return

    # Показываем последние 8 сообщений
    recent_messages = messages[-8:]
    history_text = "📜 История диалога:\n\n"

    for i, msg in enumerate(recent_messages, 1):
        role_icon = "👤" if msg['role'] == 'user' else "🤖"
        # Обрезаем длинные сообщения для читаемости
        content = msg['content']
        if len(content) > 80:
            content = content[:80] + "..."

        history_text += f"{role_icon} {content}\n\n"

    stats = context_manager.get_context_stats(user_id)
    if stats:
        history_text += f"📊 Всего сообщений: {stats['total_messages']}"

    await message.answer(history_text)


@router.message(Command("context"))
async def context_command(message: types.Message):
    """Информация о текущем контексте"""
    user_id = message.from_user.id
    stats = context_manager.get_context_stats(user_id)

    if not stats:
        await message.answer("ℹ️ Контекст не создан. Начните диалог.")
        return

    context_info = f"""📊 Информация о контексте:

💬 Всего сообщений: {stats['total_messages']}
👤 Ваши сообщения: {stats['user_messages']}
🤖 Ответов бота: {stats['assistant_messages']}
⚙️ Системных: {stats['system_messages']}

🕐 Создан: {stats['created_at'].strftime('%H:%M %d.%m.%Y')}
⏰ Активность: {stats['last_activity'].strftime('%H:%M %d.%m.%Y')}"""

    await message.answer(context_info)


@router.message(F.text)
async def handle_user_message(message: types.Message):
    """Обработчик текстовых сообщений пользователя"""
    status_task = None
    user_id = message.from_user.id
    user_message = message.text.strip()

    # Проверка пустого сообщения
    if not user_message:
        await message.answer("Пожалуйста, напишите ваш запрос.")
        return

    logging.info(f"📨 Сообщение от {user_id}: {user_message}")

    try:
        # Добавляем сообщение пользователя в контекст ДО генерации
        context_manager.add_message(user_id, 'user', user_message)

        # Получаем форматированные сообщения для API
        messages_for_api = context_manager.get_formatted_messages(user_id)

        # Отправляем статусное сообщение
        status_message = await message.answer("⏳ Обрабатываю ваш запрос...")

        # Задача для анимированного статуса
        async def update_status():
            dots = 0
            statuses = [
                "⏳ Обрабатываю ваш запрос",
                "🤔 Анализирую содержание",
                "💭 Генерирую ответ",
                "📝 Форматирую результат"
            ]
            status_index = 0

            while True:
                dots = (dots + 1) % 4
                current_status = statuses[status_index] + "." * dots

                try:
                    await status_message.edit_text(current_status)
                except Exception as e:
                    logging.debug(f"Не удалось обновить статус: {e}")
                    break

                if dots == 0:
                    status_index = (status_index + 1) % len(statuses)

                await asyncio.sleep(1.5)

        # Запускаем обновление статуса
        status_task = asyncio.create_task(update_status())

        # Вызываем генерацию с контекстом
        response = await ai_generate(messages_for_api)

        # Останавливаем статус
        if status_task and not status_task.done():
            status_task.cancel()
            try:
                await status_task
            except asyncio.CancelledError:
                pass

        # Добавляем ответ ассистента в контекст ПОСЛЕ успешной генерации
        context_manager.add_message(user_id, 'assistant', response)

        # Удаляем статус и отправляем ответ
        await status_message.delete()

        # Разбиваем длинные ответы на части если нужно
        if len(response) > 4000:
            chunks = [response[i:i + 4000] for i in range(0, len(response), 4000)]
            for i, chunk in enumerate(chunks, 1):
                if len(chunks) > 1:
                    chunk = f"Часть {i}/{len(chunks)}:\n{chunk}"
                await message.answer(chunk)
        else:
            await message.answer(response)

        logging.info(f"✅ Ответ отправлен пользователю {user_id}")

    except asyncio.CancelledError:
        logging.debug("Статус задача отменена")

    except Exception as e:
        # Останавливаем статус при ошибке
        if status_task and not status_task.done():
            status_task.cancel()

        # Пытаемся удалить статус сообщение
        try:
            if 'status_message' in locals():
                await status_message.delete()
        except:
            pass

        error_msg = f"❌ Ошибка при обработке запроса: {str(e)}"
        logging.error(f"{error_msg} (пользователь: {user_id})")

        # Отправляем пользователю информативное сообщение об ошибке
        if "LM Studio" in str(e) or "подключ" in str(e).lower():
            await message.answer("🔌 Ошибка подключения к AI-модели.")
        elif "таймаут" in str(e).lower():
            await message.answer("⏰ Превышено время ожидания ответа от модели. Попробуйте позже.")
        else:
            await message.answer("❌ Произошла ошибка при обработке вашего запроса. Попробуйте еще раз.")


# Фоновая задача для очистки неактивных контекстов
async def cleanup_inactive_contexts():
    """Периодическая очистка неактивных контекстов"""
    while True:
        try:
            pruned_count = context_manager.prune_inactive_contexts(hours=24)
            if pruned_count > 0:
                logging.info(f"🧹 Удалено неактивных контекстов: {pruned_count}")
        except Exception as e:
            logging.error(f"Ошибка при очистке контекстов: {e}")

        await asyncio.sleep(3600)  # Проверка каждый час