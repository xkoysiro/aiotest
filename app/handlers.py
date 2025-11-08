from aiogram import Router, types
from aiogram.filters import Command
import logging
import asyncio
from app.text_generate import ai_generate

router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    logging.info(f"👤 Пользователь {message.from_user.id} запустил бота")
    await message.answer("Добро пожаловать! Напишите ваш запрос.")


@router.message()
async def handle_user_message(message: types.Message):
    """Обработчик всех сообщений пользователя"""
    global status_task
    user_id = message.from_user.id
    user_message = message.text

    if not user_message or not user_message.strip():
        logging.warning(f"⚠️ Пустое сообщение от пользователя {user_id}")
        await message.answer("Пожалуйста, напишите ваш запрос.")
        return

    logging.info(f"📨 Сообщение от {user_id}: {user_message}")

    # Отправляем начальное сообщение
    status_message = await message.answer("⏳ Обрабатываю ваш запрос...")

    try:
        # Задача для обновления статуса
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
                except:
                    break

                # Меняем статус каждые 3 цикла
                if dots == 0:
                    status_index = (status_index + 1) % len(statuses)

                await asyncio.sleep(2)  # Обновляем каждые 2 секунды

        # Запускаем обновление статуса
        status_task = asyncio.create_task(update_status())

        # Вызываем генерацию
        response = await ai_generate(user_message)

        # Останавливаем обновление статуса
        status_task.cancel()

        # Удаляем статус-сообщение и отправляем ответ
        await status_message.delete()
        await message.answer(response)

        logging.info(f"📤 Ответ отправлен пользователю {user_id}")

    except asyncio.CancelledError:
        # Это нормально при отмене статус-таска
        pass

    except Exception as e:
        # Останавливаем обновление статуса в случае ошибки
        try:
            status_task.cancel()
        except:
            pass

        try:
            await status_message.delete()
        except:
            pass

        logging.error(f"❌ Ошибка при обработке запроса от {user_id}: {e}")
        await message.answer("❌ Произошла ошибка при обработке вашего запроса. Попробуйте позже.")