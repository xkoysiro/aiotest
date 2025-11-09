import os
import sys


def load_env_file():
    """
    Загружает переменные из .env файла
    Возвращает словарь с переменными
    """
    env_vars = {}
    env_file_path = '.env'

    try:
        # Проверяем существование файла
        if not os.path.exists(env_file_path):
            print("⚠️ Файл .env не найден. Используются переменные окружения системы.")
            return env_vars

        # Читаем файл
        with open(env_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()

                # Пропускаем пустые строки и комментарии
                if not line or line.startswith('#'):
                    continue

                # Разделяем ключ и значение
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Убираем кавычки если есть
                    if (value.startswith('"') and value.endswith('"')) or (
                            value.startswith("'") and value.endswith("'")):
                        value = value[1:-1]

                    env_vars[key] = value

    except Exception as e:
        print(f"❌ Ошибка при чтении .env файла: {e}")

    return env_vars


def get_config_value(key, default=None):
    """
    Получает значение конфигурации в порядке приоритета:
    1. Переменная окружения системы
    2. .env файл
    3. Значение по умолчанию
    """
    # Сначала проверяем системные переменные окружения
    value = os.environ.get(key)
    if value is not None:
        return value

    # Затем проверяем .env файл
    env_vars = load_env_file()
    value = env_vars.get(key)
    if value is not None:
        return value

    # Возвращаем значение по умолчанию
    return default


# Загружаем все переменные один раз при импорте
_env_vars = load_env_file()


def get_config_value_cached(key, default=None):
    """
    Оптимизированная версия с кэшированием .env файла
    """
    # Системные переменные окружения (самый высокий приоритет)
    system_value = os.environ.get(key)
    if system_value is not None:
        return system_value

    # .env файл (второй приоритет)
    env_value = _env_vars.get(key)
    if env_value is not None:
        return env_value

    # Значение по умолчанию
    return default


# ============ КОНФИГУРАЦИЯ ПРИЛОЖЕНИЯ ============

# OpenRouter настройки
OPENROUTER_API_KEY = get_config_value_cached("OPENROUTER_API_KEY")
OPENROUTER_MODEL = get_config_value_cached("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")

# Telegram настройки
TELEGRAM_TOKEN = get_config_value_cached("TELEGRAM_TOKEN")
CHAT_ID = get_config_value_cached("CHAT_ID")

# Настройки приложения
MAX_CONTEXT_MESSAGES = int(get_config_value_cached("MAX_CONTEXT_MESSAGES", "20"))
REQUEST_TIMEOUT = int(get_config_value_cached("REQUEST_TIMEOUT", "120"))


# ============ ПРОВЕРКА ОБЯЗАТЕЛЬНЫХ ПЕРЕМЕННЫХ ============

def validate_config():
    """Проверяет наличие обязательных переменных конфигурации"""
    errors = []

    if not OPENROUTER_API_KEY:
        errors.append("OPENROUTER_API_KEY - не установлен")

    if not TELEGRAM_TOKEN:
        errors.append("TELEGRAM_TOKEN - не установлен")

    if errors:
        error_message = "❌ Ошибки конфигурации:\n" + "\n".join(f"  • {error}" for error in errors)
        error_message += "\n\n💡 Решение:"
        error_message += "\n  1. Создайте файл .env в корне проекта с переменными"
        error_message += "\n  2. Или установите переменные окружения системы"
        error_message += "\n  3. Пример .env файла:"
        error_message += "\n     OPENROUTER_API_KEY=your_key_here"
        error_message += "\n     TELEGRAM_TOKEN=your_token_here"
        error_message += "\n     OPENROUTER_MODEL=openai/gpt-3.5-turbo"

        print(error_message)
        sys.exit(1)

    # Выводим информацию о загруженной конфигурации
    print("✅ Конфигурация загружена успешно:")
    print(f"   • Модель: {OPENROUTER_MODEL}")
    print(f"   • Макс. сообщений: {MAX_CONTEXT_MESSAGES}")
    print(f"   • Таймаут запросов: {REQUEST_TIMEOUT} сек.")

    # Маскируем чувствительные данные при выводе
    masked_api_key = f"{OPENROUTER_API_KEY[:10]}..." if OPENROUTER_API_KEY and len(
        OPENROUTER_API_KEY) > 10 else "не установлен"
    masked_token = f"{TELEGRAM_TOKEN[:10]}..." if TELEGRAM_TOKEN and len(TELEGRAM_TOKEN) > 10 else "не установлен"

    print(f"   • API Key: {masked_api_key}")
    print(f"   • Telegram Token: {masked_token}")


# Автоматическая проверка при импорте модуля
if __name__ != "__main__":
    validate_config()


# ============ ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ ============

def show_current_config():
    """Показывает текущую конфигурацию (для отладки)"""
    config_info = {
        "OPENROUTER_API_KEY": f"{OPENROUTER_API_KEY[:10]}..." if OPENROUTER_API_KEY else "не установлен",
        "OPENROUTER_MODEL": OPENROUTER_MODEL,
        "TELEGRAM_TOKEN": f"{TELEGRAM_TOKEN[:10]}..." if TELEGRAM_TOKEN else "не установлен",
        "CHAT_ID": CHAT_ID or "не установлен",
        "MAX_CONTEXT_MESSAGES": MAX_CONTEXT_MESSAGES,
        "REQUEST_TIMEOUT": REQUEST_TIMEOUT
    }

    print("📋 Текущая конфигурация:")
    for key, value in config_info.items():
        print(f"  {key}: {value}")


def reload_config():
    """Перезагружает конфигурацию (полезно при изменении .env файла)"""
    global _env_vars, OPENROUTER_API_KEY, OPENROUTER_MODEL, TELEGRAM_TOKEN, CHAT_ID, MAX_CONTEXT_MESSAGES, REQUEST_TIMEOUT

    print("🔄 Перезагрузка конфигурации...")
    _env_vars = load_env_file()

    # Обновляем переменные
    OPENROUTER_API_KEY = get_config_value_cached("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = get_config_value_cached("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")
    TELEGRAM_TOKEN = get_config_value_cached("TELEGRAM_TOKEN")
    CHAT_ID = get_config_value_cached("CHAT_ID")
    MAX_CONTEXT_MESSAGES = int(get_config_value_cached("MAX_CONTEXT_MESSAGES", "20"))
    REQUEST_TIMEOUT = int(get_config_value_cached("REQUEST_TIMEOUT", "120"))

    validate_config()


# Если файл запущен напрямую - показываем конфигурацию
if __name__ == "__main__":
    show_current_config()