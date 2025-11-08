"""
УНИВЕРСАЛЬНЫЕ ШАБЛОНЫ ДЛЯ СОЗДАНИЯ ИНСТРУМЕНТОВ (TOOLS)
Сохраните этот файл и импортируйте нужные шаблоны
"""
"""

🚀 КАК ИСПОЛЬЗОВАТЬ ЭТИ ШАБЛОНЫ:

1. Создайте файл tools_templates.py с этим кодом
2. Импортируйте нужные инструменты в ваш основной код:
from tools_templates import get_all_tools, process_tool_call

3. Замените заглушки на вашу реальную логику (API вызовы, БД запросы и т.д.)
4. Добавьте ваши токены в указанные места (там где комментарии "ТУТ БУДЕТ ВАШ ТОКЕН")
"""


import aiohttp
import json
import logging
from typing import Dict, List, Any, Optional

# =============================================================================
# 🎯 ШАБЛОН 1: ПОИСК ИНФОРМАЦИИ В ИНТЕРНЕТЕ
# =============================================================================

SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search_internet",
        "description": "Поиск актуальной информации в интернете по заданному запросу. Используй для вопросов о текущих событиях, новостях, погоде, курсах валют и другой актуальной информации.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Поисковый запрос для поиска в интернете"
                },
                "max_results": {
                    "type": "number",
                    "description": "Максимальное количество результатов (по умолчанию 3)"
                }
            },
            "required": ["query"]
        }
    }
}


async def search_internet(query: str, max_results: int = 3) -> Dict[str, Any]:
    """
    Универсальная функция поиска в интернете
    ЗАМЕНИТЕ ЭТУ РЕАЛИЗАЦИЮ на вызов реального API (Google Search, SerpAPI и т.д.)
    """
    try:
        # 🔧 ЗДЕСЬ ВАША РЕАЛЬНАЯ ЛОГИКА ПОИСКА:
        # Пример с заглушкой - замените на реальный API
        search_results = [
            {"title": f"Результат 1 по запросу '{query}'", "snippet": "Информация из интернета..."},
            {"title": f"Результат 2 по запросу '{query}'", "snippet": "Дополнительные данные..."}
        ]

        return {
            "status": "success",
            "query": query,
            "results": search_results[:max_results],
            "source": "internet_search"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Ошибка поиска: {str(e)}"
        }


# =============================================================================
# 🎯 ШАБЛОН 2: РАБОТА С БАЗОЙ ДАННЫХ
# =============================================================================

DATABASE_TOOL = {
    "type": "function",
    "function": {
        "name": "query_database",
        "description": "Выполнение запросов к базе данных для получения структурированной информации. Используй для поиска пользователей, заказов, товаров и других данных из БД.",
        "parameters": {
            "type": "object",
            "properties": {
                "table_name": {
                    "type": "string",
                    "description": "Название таблицы в базе данных"
                },
                "search_field": {
                    "type": "string",
                    "description": "Поле для поиска (например: name, email, id)"
                },
                "search_value": {
                    "type": "string",
                    "description": "Значение для поиска в указанном поле"
                },
                "limit": {
                    "type": "number",
                    "description": "Лимит результатов (по умолчанию 10)"
                }
            },
            "required": ["table_name", "search_field", "search_value"]
        }
    }
}


async def query_database(table_name: str, search_field: str, search_value: str, limit: int = 10) -> Dict[str, Any]:
    """
    Универсальная функция запроса к базе данных
    ЗАМЕНИТЕ на вашу реальную логику работы с БД (SQLite, PostgreSQL, MySQL)
    """
    try:
        # 🔧 ЗДЕСЬ ВАША РЕАЛЬНАЯ ЛОГИКА БАЗЫ ДАННЫХ:
        # Пример с заглушкой - замените на реальные SQL запросы
        mock_data = [
            {"id": 1, "name": "Пример пользователя", "email": "user@example.com"},
            {"id": 2, "name": "Другой пользователь", "email": "other@example.com"}
        ]

        return {
            "status": "success",
            "table": table_name,
            "search_criteria": f"{search_field} = {search_value}",
            "results": mock_data[:limit],
            "results_count": len(mock_data[:limit])
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Ошибка базы данных: {str(e)}"
        }


# =============================================================================
# 🎯 ШАБЛОН 3: МАТЕМАТИЧЕСКИЕ ВЫЧИСЛЕНИЯ
# =============================================================================

CALCULATOR_TOOL = {
    "type": "function",
    "function": {
        "name": "calculate_expression",
        "description": "Выполнение математических вычислений и решение уравнений. Используй для расчетов, конвертаций единиц измерения, статистических вычислений.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Математическое выражение для вычисления (например: 2+2*3, sqrt(16), 100 USD to RUB)"
                }
            },
            "required": ["expression"]
        }
    }
}


async def calculate_expression(expression: str) -> Dict[str, Any]:
    """
    Универсальная функция вычислений
    ДОБАВЬТЕ сюда вашу логику вычислений (eval, sympy, currency conversion)
    """
    try:
        # ⚠️ ВНИМАНИЕ: eval опасен для продакшена!
        # Используйте библиотеки like numexpr, sympy для безопасности
        result = eval(expression)

        return {
            "status": "success",
            "expression": expression,
            "result": result,
            "result_type": type(result).__name__
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Ошибка вычисления: {str(e)}",
            "expression": expression
        }


# =============================================================================
# 🎯 ШАБЛОН 4: РАБОТА С ФАЙЛАМИ И ДОКУМЕНТАМИ
# =============================================================================

FILE_TOOL = {
    "type": "function",
    "function": {
        "name": "read_file_content",
        "description": "Чтение содержимого файлов и документов. Используй для получения информации из текстовых файлов, CSV, JSON документов.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Путь к файлу или название документа"
                },
                "max_lines": {
                    "type": "number",
                    "description": "Максимальное количество строк для чтения (0 - весь файл)"
                }
            },
            "required": ["file_path"]
        }
    }
}


async def read_file_content(file_path: str, max_lines: int = 0) -> Dict[str, Any]:
    """
    Универсальная функция чтения файлов
    НАСТРОЙТЕ под вашу файловую систему или облачное хранилище
    """
    try:
        # 🔧 ЗДЕСЬ ВАША РЕАЛЬНАЯ ЛОГИКА РАБОТЫ С ФАЙЛАМИ:
        # Пример с заглушкой - замените на реальное чтение файлов
        mock_content = f"Содержимое файла {file_path}\n" + "\n".join([f"Строка {i}" for i in range(1, 10)])

        lines = mock_content.split('\n')
        if max_lines > 0:
            content = '\n'.join(lines[:max_lines])
        else:
            content = mock_content

        return {
            "status": "success",
            "file_path": file_path,
            "content": content,
            "lines_count": len(content.split('\n')),
            "file_size": len(content)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Ошибка чтения файла: {str(e)}"
        }


# =============================================================================
# 🎯 ШАБЛОН 5: API ИНТЕГРАЦИИ (ВНЕШНИЕ СЕРВИСЫ)
# =============================================================================

API_TOOL = {
    "type": "function",
    "function": {
        "name": "call_external_api",
        "description": "Вызов внешних API для получения данных от различных сервисов. Используй для получения погоды, курсов валют, котировок акций, данных с социальных сетей.",
        "parameters": {
            "type": "object",
            "properties": {
                "service_name": {
                    "type": "string",
                    "description": "Название сервиса (weather, currency, stocks, news, etc.)"
                },
                "endpoint": {
                    "type": "string",
                    "description": "Конечная точка API или действие"
                },
                "parameters": {
                    "type": "string",
                    "description": "Параметры запроса в формате JSON"
                }
            },
            "required": ["service_name", "endpoint"]
        }
    }
}


async def call_external_api(service_name: str, endpoint: str, parameters: str = "{}") -> Dict[str, Any]:
    """
    Универсальная функция вызова внешних API
    ДОБАВЬТЕ сюда ваши API ключи и логику вызовов
    """
    try:
        # 🔧 ЗДЕСЬ ВАША РЕАЛЬНАЯ ЛОГИКА API ВЫЗОВОВ:
        # Пример с заглушкой - замените на реальные API запросы

        # ТУТ БУДЕТ ВАШ ТОКЕН для внешних API
        API_TOKENS = {
            "weather": "YOUR_WEATHER_API_TOKEN",
            "currency": "YOUR_CURRENCY_API_TOKEN",
            "news": "YOUR_NEWS_API_TOKEN"
        }

        params_dict = json.loads(parameters) if parameters else {}

        # Пример реализации для разных сервисов
        if service_name == "weather":
            # Реализуйте вызов погодного API (OpenWeatherMap и т.д.)
            mock_data = {"temperature": 20, "condition": "sunny", "city": "Moscow"}
        elif service_name == "currency":
            # Реализуйте вызов валютного API
            mock_data = {"USD": 90.5, "EUR": 99.2, "timestamp": "2024-01-01"}
        else:
            mock_data = {"service": service_name, "endpoint": endpoint, "params": params_dict}

        return {
            "status": "success",
            "service": service_name,
            "endpoint": endpoint,
            "data": mock_data,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Ошибка API вызова: {str(e)}"
        }


# =============================================================================
# 🎯 ШАБЛОН 6: УВЕДОМЛЕНИЯ И КОММУНИКАЦИИ
# =============================================================================

NOTIFICATION_TOOL = {
    "type": "function",
    "function": {
        "name": "send_notification",
        "description": "Отправка уведомлений, сообщений и напоминаний. Используй для отправки email, SMS, push-уведомлений или сообщений в мессенджеры.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "Текст сообщения для отправки"
                },
                "recipient": {
                    "type": "string",
                    "description": "Получатель (email, телефон, username)"
                },
                "channel": {
                    "type": "string",
                    "description": "Канал отправки (email, sms, telegram, push)"
                },
                "urgency": {
                    "type": "string",
                    "enum": ["low", "normal", "high"],
                    "description": "Срочность сообщения"
                }
            },
            "required": ["message", "recipient", "channel"]
        }
    }
}


async def send_notification(message: str, recipient: str, channel: str, urgency: str = "normal") -> Dict[str, Any]:
    """
    Универсальная функция отправки уведомлений
    НАСТРОЙТЕ интеграции с email, Telegram, SMS сервисами
    """
    try:
        # 🔧 ЗДЕСЬ ВАША РЕАЛЬНАЯ ЛОГИКА ОТПРАВКИ:
        # ТУТ БУДЕТ ВАШ ТОКЕН для Telegram бота, email сервера и т.д.

        notification_services = {
            "telegram": "YOUR_TELEGRAM_BOT_TOKEN",
            "email": "YOUR_SMTP_CREDENTIALS",
            "sms": "YOUR_SMS_API_TOKEN"
        }

        # Заглушка реализации
        logging.info(f"📧 Отправка {channel} уведомления для {recipient}: {message}")

        return {
            "status": "success",
            "channel": channel,
            "recipient": recipient,
            "message_preview": message[:50] + "...",
            "urgency": urgency,
            "sent_at": "2024-01-01T00:00:00Z"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Ошибка отправки уведомления: {str(e)}"
        }


# =============================================================================
# 🛠 УТИЛИТЫ ДЛЯ РАБОТЫ С ИНСТРУМЕНТАМИ
# =============================================================================

def get_all_tools() -> List[Dict]:
    """Возвращает все доступные инструменты"""
    return [
        SEARCH_TOOL,
        DATABASE_TOOL,
        CALCULATOR_TOOL,
        FILE_TOOL,
        API_TOOL,
        NOTIFICATION_TOOL
    ]


def get_tools_by_category(category: str) -> List[Dict]:
    """Возвращает инструменты по категории"""
    categories = {
        "search": [SEARCH_TOOL],
        "data": [DATABASE_TOOL, FILE_TOOL],
        "compute": [CALCULATOR_TOOL],
        "integration": [API_TOOL, NOTIFICATION_TOOL]
    }
    return categories.get(category, [])


async def process_tool_call(tool_call: Dict) -> Dict:
    """Универсальная обработка вызова инструмента"""
    function_name = tool_call["function"]["name"]
    arguments = json.loads(tool_call["function"]["arguments"])

    # 🔧 СВЯЗЫВАЕМ ИМЯ ФУНКЦИИ С РЕАЛЬНОЙ ФУНКЦИЕЙ
    function_mapping = {
        "search_internet": search_internet,
        "query_database": query_database,
        "calculate_expression": calculate_expression,
        "read_file_content": read_file_content,
        "call_external_api": call_external_api,
        "send_notification": send_notification
    }

    if function_name in function_mapping:
        result = await function_mapping[function_name](**arguments)
        return {
            "tool_call_id": tool_call["id"],
            "function_name": function_name,
            "result": result
        }
    else:
        return {
            "tool_call_id": tool_call["id"],
            "function_name": function_name,
            "result": {"status": "error", "message": f"Функция {function_name} не найдена"}
        }


# =============================================================================
# 📝 ПРИМЕР ИСПОЛЬЗОВАНИЯ В ВАШЕМ КОДЕ
# =============================================================================
"""
# В вашем основном файле:
from tools_templates import get_all_tools, process_tool_call

# Использование в ai_generate функции:
payload = {
    "model": "local-model",
    "messages": conversation_history,
    "tools": get_all_tools(),  # ← ВСЕ инструменты
    "tool_choice": "auto"
}

# Обработка tool calls:
tool_results = []
for tool_call in message["tool_calls"]:
    result = await process_tool_call(tool_call)
    tool_results.append(result)
"""