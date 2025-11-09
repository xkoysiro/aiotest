from aiogram import Router, types, F
from aiogram.filters import Command, CommandObject
import logging
import asyncio

# Импорты всех нужных функций
from app.text_generate import (
    ai_generate,
    get_available_models,
    get_model_info,
    get_popular_models,
    switch_model
)
from app.context_manager import UserContextManager
from config import OPENROUTER_MODEL

router = Router()
context_manager = UserContextManager(max_messages=15)


@router.message(Command("start"))
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    logging.info(f"👤 Пользователь {user_id} запустил бота")

    context_manager.clear_context(user_id)

    system_message = f"""Вы - полезный AI ассистент. Отвечайте на вопросы подробно и вежливо.
Текущая модель: {OPENROUTER_MODEL}
Поддерживайте контекст разговора и учитывайте предыдущие сообщения."""

    context_manager.add_message(user_id, 'system', system_message)

    welcome_text = f"""🤖 Добро пожаловать! 

Я ваш AI-помощник с памятью о нашем разговоре. 
Текущая модель: `{OPENROUTER_MODEL}`

Доступные команды:
/clear - очистить историю диалога
/history - показать историю
/context - информация о контексте
/models - список доступных моделей
/model_info - информация о текущей модели
/switch_model - сменить модель

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

    recent_messages = messages[-8:]
    history_text = "📜 История диалога:\n\n"

    for i, msg in enumerate(recent_messages, 1):
        role_icon = "👤" if msg['role'] == 'user' else "🤖"
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


@router.message(Command("models"))
async def models_command(message: types.Message):
    """Показывает доступные модели и текущую модель"""
    try:
        status_msg = await message.answer("🔄 Получение списка моделей...")

        popular_models = await get_popular_models()

        if not popular_models:
            await status_msg.edit_text("❌ Не удалось получить список моделей")
            return

        models_text = f"🤖 **Текущая модель:** `{OPENROUTER_MODEL}`\n\n"
        models_text += "📚 **Популярные модели:**\n"

        for model in popular_models:
            status = "✅" if model["id"] == OPENROUTER_MODEL else "🔹"
            models_text += f"{status} `{model['id']}`\n"

        models_text += f"\n💡 Используйте `/switch_model название_модели` для смены"
        models_text += f"\n📊 Используйте `/model_info название_модели` для подробностей"

        await status_msg.edit_text(models_text, parse_mode="Markdown")

    except Exception as e:
        logging.error(f"❌ Ошибка в команде /models: {e}")
        try:
            await message.answer("❌ Ошибка при получении списка моделей")
        except:
            pass


@router.message(Command("model_info"))
async def model_info_command(message: types.Message, command: CommandObject):
    """Информация о текущей или указанной модели"""
    model_id = command.args or OPENROUTER_MODEL

    try:
        status_msg = await message.answer(f"🔄 Получение информации о модели `{model_id}`...")

        model_info = await get_model_info(model_id)

        if not model_info:
            await status_msg.edit_text(f"❌ Модель `{model_id}` не найдена")
            return

        info_text = f"🤖 **Модель:** `{model_id}`\n\n"

        if model_info.get("name"):
            info_text += f"**Название:** {model_info['name']}\n"

        if model_info.get("description"):
            info_text += f"**Описание:** {model_info['description']}\n"

        if model_info.get("context_length"):
            info_text += f"**Длина контекста:** {model_info['context_length']} токенов\n"

        pricing = model_info.get("pricing", {})
        if pricing.get("prompt") or pricing.get("completion"):
            prompt_price = pricing.get("prompt", 0)
            completion_price = pricing.get("completion", 0)
            info_text += f"**Цена:** ${prompt_price}/1M prompt, ${completion_price}/1M completion\n"

        top_provider = model_info.get("top_provider", {})
        if top_provider.get("name"):
            info_text += f"**Провайдер:** {top_provider['name']}\n"

        await status_msg.edit_text(info_text, parse_mode="Markdown")

    except Exception as e:
        logging.error(f"❌ Ошибка в команде /model_info: {e}")
        try:
            await status_msg.edit_text("❌ Ошибка при получении информации о модели")
        except:
            await message.answer("❌ Ошибка при получении информации о модели")


@router.message(Command("switch_model"))
async def switch_model_command(message: types.Message, command: CommandObject):
    """Смена модели AI"""
    user_id = message.from_user.id
    new_model = command.args

    if not new_model:
        await message.answer("❌ Укажите модель: `/switch_model openai/gpt-4`", parse_mode="Markdown")
        return

    try:
        status_msg = await message.answer(f"🔄 Переключаю на модель `{new_model}`...")

        success = await switch_model(new_model)

        if success:
            await status_msg.edit_text(f"✅ Модель изменена на: `{new_model}`", parse_mode="Markdown")

            context_manager.clear_context(user_id)
            system_message = f"""Вы - полезный AI ассистент. Отвечайте на вопросы подробно и вежливо.
Текущая модель: {new_model}
Поддерживайте контекст разговора и учитывайте предыдущие сообщения."""

            context_manager.add_message(user_id, 'system', system_message)

        else:
            await status_msg.edit_text(
                f"❌ Модель `{new_model}` не найдена или недоступна.\n"
                f"Используйте `/models` чтобы посмотреть доступные модели.",
                parse_mode="Markdown"
            )

    except Exception as e:
        logging.error(f"❌ Ошибка при смене модели: {e}")
        try:
            await status_msg.edit_text("❌ Ошибка при смене модели")
        except:
            await message.answer("❌ Ошибка при смене модели")


@router.message(F.text)
async def handle_user_message(message: types.Message):
    """Обработчик текстовых сообщений пользователя"""
    status_task = None
    user_id = message.from_user.id
    user_message = message.text.strip()

    if not user_message:
        await message.answer("Пожалуйста, напишите ваш запрос.")
        return

    logging.info(f"📨 Сообщение от {user_id}: {user_message}")

    try:
        context_manager.add_message(user_id, 'user', user_message)

        messages_for_api = context_manager.get_formatted_messages(user_id)

        status_message = await message.answer("⏳ Обрабатываю ваш запрос...")

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

        status_task = asyncio.create_task(update_status())

        response = await ai_generate(messages_for_api)

        if status_task and not status_task.done():
            status_task.cancel()
            try:
                await status_task
            except asyncio.CancelledError:
                pass

        context_manager.add_message(user_id, 'assistant', response)

        await status_message.delete()

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
        if status_task and not status_task.done():
            status_task.cancel()

        try:
            if 'status_message' in locals():
                await status_message.delete()
        except:
            pass

        error_msg = f"❌ Ошибка при обработке запроса: {str(e)}"
        logging.error(f"{error_msg} (пользователь: {user_id})")

        if "LM Studio" in str(e) or "подключ" in str(e).lower():
            await message.answer("🔌 Ошибка подключения к AI-модели.")
        elif "таймаут" in str(e).lower():
            await message.answer("⏰ Превышено время ожидания ответа от модели. Попробуйте позже.")
        else:
            await message.answer("❌ Произошла ошибка при обработке вашего запроса. Попробуйте еще раз.")


async def cleanup_inactive_contexts():
    """Периодическая очистка неактивных контекстов"""
    while True:
        try:
            pruned_count = context_manager.prune_inactive_contexts(hours=24)
            if pruned_count > 0:
                logging.info(f"🧹 Удалено неактивных контекстов: {pruned_count}")
        except Exception as e:
            logging.error(f"Ошибка при очистке контекстов: {e}")

        await asyncio.sleep(3600)