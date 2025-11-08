from config import TOKEN
from app.handlers import router
from app.logging_setup import setup_logging
import asyncio
import logging
from aiogram import Bot, Dispatcher

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def main():
    # Настраиваем логирование ДО включения роутера
    setup_logging(bot)

    # Логируем запуск бота
    logging.info("🚀 Бот запущен и готов к работе")

    # Включаем роутер
    dp.include_router(router)

    # Запускаем поллинг
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("🛑 Бот остановлен пользователем")
    except Exception as e:
        logging.critical(f"💥 Критическая ошибка: {e}")