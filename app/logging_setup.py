import logging
import sys
import asyncio
from aiogram import Bot
from aiogram.enums import ParseMode
from config import CHAT_ID


class TelegramLogHandler(logging.Handler):
    def __init__(self, bot: Bot, chat_id: int):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record):
        try:
            log_entry = self.format(record)
            # Отправляем в Telegram асинхронно
            asyncio.create_task(self.send_to_telegram(record.levelname, log_entry))
        except Exception as e:
            print(f"Ошибка в TelegramLogHandler: {e}")

    async def send_to_telegram(self, level: str, message: str):
        try:
            # Эмодзи для уровней логов
            emoji_map = {
                'DEBUG': '🐛',
                'INFO': 'ℹ️',
                'WARNING': '⚠️',
                'ERROR': '❌',
                'CRITICAL': '💥'
            }
            emoji = emoji_map.get(level, '📝')

            # Ограничиваем длину сообщения
            if len(message) > 3500:
                message = message[:3500] + "..."

            await self.bot.send_message(
                chat_id=self.chat_id,
                text=f"{emoji} **{level}**\n\n`{message}`",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            print(f"Не удалось отправить лог в Telegram: {e}")


def setup_logging(bot: Bot):
    """Настройка логирования с отправкой в Telegram"""
    # Создаем handler для Telegram
    telegram_handler = TelegramLogHandler(bot, CHAT_ID)
    telegram_handler.setLevel(logging.DEBUG)

    # Форматтер для логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    telegram_handler.setFormatter(formatter)

    # Добавляем handler к корневому логгеру
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # Очищаем существующие handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Добавляем наши handlers
    root_logger.addHandler(telegram_handler)

    # Вывод в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)