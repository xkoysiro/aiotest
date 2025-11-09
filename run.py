import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TELEGRAM_TOKEN
from app.logging_setup import setup_logging
from app.handlers import router as main_router
from app.handlers import cleanup_inactive_contexts


async def main():
    """Основная функция запуска бота"""
    bot = Bot(token=TELEGRAM_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    telegram_handler = setup_logging(bot)

    try:
        dp.include_router(main_router)

        asyncio.create_task(cleanup_inactive_contexts())

        logging.info("✅ Бот запускается...")

        await dp.start_polling(bot)

    except Exception as e:
        logging.error(f"❌ Критическая ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()
        logging.info("✅ Бот остановлен")


if __name__ == "__main__":
    asyncio.run(main())