import logging
import sys
import asyncio
from typing import Optional
from aiogram import Bot
from aiogram.enums import ParseMode
from config import CHAT_ID


class TelegramLogHandler(logging.Handler):
    def __init__(self, bot: Bot, chat_id: int, queue_size: int = 100):
        super().__init__()
        self.bot = bot
        self.chat_id = chat_id
        self.queue = asyncio.Queue(maxsize=queue_size)
        self.worker_task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()

    def start(self):
        """Запускает worker для обработки логов"""
        self.worker_task = asyncio.create_task(self._worker())

    def stop(self):
        """Останавливает worker"""
        self._stop_event.set()
        if self.worker_task:
            self.worker_task.cancel()

    async def _worker(self):
        """Фоновый worker для отправки логов"""
        while not self._stop_event.is_set():
            try:
                try:
                    record = await asyncio.wait_for(self.queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    continue

                await self._send_to_telegram(record)
                self.queue.task_done()

            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"❌ Ошибка в Telegram log worker: {e}")

    def emit(self, record):
        """Добавляет запись в очередь"""
        try:
            self.queue.put_nowait(record)
        except asyncio.QueueFull:
            print(f"⚠️ Очередь логов переполнена, сообщение потеряно: {self.format(record)}")
        except Exception as e:
            print(f"❌ Ошибка при добавлении лога в очередь: {e}")

    async def _send_to_telegram(self, record):
        """Отправляет конкретную запись в Telegram"""
        try:
            log_entry = self.format(record)
            level = record.levelname

            emoji_map = {
                'DEBUG': '🐛',
                'INFO': 'ℹ️',
                'WARNING': '⚠️',
                'ERROR': '❌',
                'CRITICAL': '💥'
            }
            emoji = emoji_map.get(level, '📝')

            if len(log_entry) > 3500:
                log_entry = log_entry[:3500] + "..."

            message_text = f"{emoji} **{level}**\n\n`{log_entry}`"

            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message_text,
                parse_mode=ParseMode.MARKDOWN,
                disable_notification=level in ['DEBUG', 'INFO']
            )

        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"❌ Не удалось отправить лог в Telegram: {e}")

    def close(self):
        """Корректное закрытие handler"""
        self.stop()
        super().close()


class LogFilter(logging.Filter):
    """Фильтр для исключения слишком частых повторяющихся сообщений"""

    def __init__(self):
        super().__init__()
        self.last_messages = {}

    def filter(self, record):
        message = record.getMessage()
        current_time = asyncio.get_event_loop().time()

        if message in self.last_messages:
            last_time = self.last_messages[message]
            if current_time - last_time < 60:
                return False

        self.last_messages[message] = current_time
        return True


def setup_logging(bot: Bot):
    """Настройка логирования с отправкой в Telegram"""

    telegram_handler = TelegramLogHandler(bot, CHAT_ID)
    telegram_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    telegram_handler.setFormatter(formatter)

    log_filter = LogFilter()
    telegram_handler.addFilter(log_filter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    root_logger.addHandler(telegram_handler)

    telegram_handler.start()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    console_handler.addFilter(log_filter)
    root_logger.addHandler(console_handler)

    logging.info("✅ Система логирования настроена с отправкой в Telegram")

    return telegram_handler


async def close_logging(telegram_handler: TelegramLogHandler):
    """Корректное закрытие системы логирования"""
    try:
        await asyncio.sleep(2)
        telegram_handler.stop()
        telegram_handler.close()
        logging.info("✅ Система логирования корректно остановлена")
    except Exception as e:
        print(f"❌ Ошибка при остановке логирования: {e}")