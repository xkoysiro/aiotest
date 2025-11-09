import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, CHAT_ID
from app.logging_setup   import setup_logging
from app.handlers import router as main_router
from app.handlers import cleanup_inactive_contexts


async def main():
    """Основная функция запуска бота"""
    # Инициализация бота и диспетчера
    bot = Bot(token=TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    # Настройка логирования
    telegram_handler = setup_logging(bot)

    try:
        # Регистрация роутеров
        dp.include_router(main_router)

        # Запуск фоновых задач
        asyncio.create_task(cleanup_inactive_contexts())

        logging.info("✅ Бот запускается...")

        # Запуск поллинга
        await dp.start_polling(bot)

    except Exception as e:
        logging.error(f"❌ Критическая ошибка при запуске бота: {e}")
    finally:
        # Корректное завершение
        await bot.session.close()
        logging.info("✅ Бот остановлен")


if __name__ == "__main__":
    asyncio.run(main())