import aiohttp
import json
import logging
import asyncio
from typing import List, Dict, Optional
from config import OPENROUTER_API_KEY, OPENROUTER_MODEL


async def get_model_info(model_id: str) -> Dict:
    """
    Получение подробной информации о конкретной модели
    """
    try:
        url = "https://openrouter.ai/api/v1/models"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()

                    for model in data.get("data", []):
                        if model["id"] == model_id:
                            return {
                                "id": model_id,
                                "name": model.get("name", model_id),
                                "description": model.get("description", ""),
                                "context_length": model.get("context_length", 0),
                                "pricing": model.get("pricing", {}),
                                "architecture": model.get("architecture", {}),
                                "top_provider": model.get("top_provider", {}),
                                "permissions": model.get("permissions", []),
                            }

                    logging.warning(f"⚠️ Модель {model_id} не найдена")
                    return {}

                else:
                    error_text = await response.text()
                    logging.error(f"❌ Ошибка при получении списка моделей: {response.status}")
                    return {}

    except Exception as e:
        logging.error(f"❌ Ошибка при получении информации о модели {model_id}: {e}")
        return {}


async def get_available_models(limit: int = 50) -> List[str]:
    """
    Получение списка доступных моделей через OpenRouter
    """
    try:
        url = "https://openrouter.ai/api/v1/models"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=30) as response:
                if response.status == 200:
                    data = await response.json()
                    models = [model["id"] for model in data.get("data", [])]
                    return sorted(models)[:limit]
                else:
                    logging.error(f"❌ Не удалось получить список моделей: {response.status}")
                    return []

    except Exception as e:
        logging.error(f"❌ Ошибка при получении списка моделей: {e}")
        return []


async def get_popular_models() -> List[Dict]:
    """
    Получение списка популярных моделей с основной информацией
    """
    popular_model_ids = [
        "openai/gpt-3.5-turbo",
        "openai/gpt-4",
        "openai/gpt-4-turbo",
        "anthropic/claude-3-sonnet",
        "anthropic/claude-3-haiku",
        "google/gemini-pro",
        "meta-llama/llama-3-70b-instruct",
        "mistralai/mistral-7b-instruct"
    ]

    popular_models = []
    for model_id in popular_model_ids:
        info = await get_model_info(model_id)
        if info:
            popular_models.append(info)
        await asyncio.sleep(0.1)

    return popular_models


async def switch_model(new_model: str) -> bool:
    """
    Смена текущей модели
    """
    try:
        available_models = await get_available_models()

        if new_model in available_models:
            # Обновляем глобальную переменную
            from config import OPENROUTER_MODEL
            global OPENROUTER_MODEL
            OPENROUTER_MODEL = new_model
            logging.info(f"✅ Модель изменена на: {new_model}")
            return True
        else:
            logging.warning(f"⚠️ Модель {new_model} не найдена")
            return False

    except Exception as e:
        logging.error(f"❌ Ошибка при смене модели: {e}")
        return False


async def ai_generate(messages: List[Dict[str, str]]) -> str:
    """
    Генерация ответа с помощью моделей через OpenRouter API
    """
    try:
        if not messages:
            logging.warning("⚠️ Получен пустой список сообщений")
            return "Пожалуйста, напишите ваш запрос."

        if messages and messages[-1]['role'] != 'user':
            logging.warning("⚠️ Последнее сообщение не от пользователя")
            return "Ошибка формата запроса."

        logging.info(f"🔧 Начало генерации через OpenRouter. Сообщений: {len(messages)}")

        prompt_debug = "\n".join([f"{msg['role']}: {msg['content'][:50]}..." for msg in messages[-3:]])
        logging.debug(f"🔧 Структура промпта:\n{prompt_debug}")

        url = "https://openrouter.ai/api/v1/chat/completions"

        # Форматируем сообщения для OpenRouter
        formatted_messages = []
        for msg in messages:
            formatted_message = {
                "role": msg["role"],
                "content": [
                    {
                        "type": "text",
                        "text": msg["content"]
                    }
                ]
            }
            formatted_messages.append(formatted_message)

        payload = {
            "model": OPENROUTER_MODEL,
            "messages": formatted_messages,
            "temperature": 0.7,
            "max_tokens": 4000,
            "top_p": 0.9,
            "frequency_penalty": 0.1,
            "presence_penalty": 0.1,
            "stream": False
        }

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/your-telegram-ai-bot",
            "X-Title": "Telegram AI Assistant"
        }

        logging.debug(f"🔧 Отправка запроса к OpenRouter, модель: {OPENROUTER_MODEL}")

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers, timeout=120) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logging.error(f"❌ Ошибка OpenRouter: HTTP {response.status} - {error_text}")

                    if response.status == 401:
                        raise Exception("Неверный API ключ OpenRouter.")
                    elif response.status == 402:
                        raise Exception("Недостаточно средств на счету OpenRouter.")
                    elif response.status == 429:
                        raise Exception("Превышен лимит запросов к OpenRouter.")
                    elif response.status == 400:
                        try:
                            error_data = json.loads(error_text)
                            error_message = error_data.get('error', {}).get('message', 'Неизвестная ошибка')
                            raise Exception(f"Ошибка запроса: {error_message}")
                        except:
                            raise Exception(f"Ошибка запроса: {error_text}")
                    else:
                        raise Exception(f"Ошибка OpenRouter: HTTP {response.status}")

                response_data = await response.json()

        if not response_data.get("choices"):
            logging.error("❌ OpenRouter вернуло пустой список choices")
            return "Извините, не удалось сгенерировать ответ."

        choice = response_data["choices"][0]
        message = choice.get("message", {})

        response_content = ""
        content = message.get("content")

        if isinstance(content, str):
            response_content = content
        elif isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
            response_content = " ".join(text_parts)
        else:
            response_content = str(content) if content else ""

        if not response_content or not response_content.strip():
            logging.warning("⚠️ OpenRouter вернуло пустой ответ")
            return "Извините, не удалось сгенерировать содержательный ответ."

        if "usage" in response_data:
            usage = response_data["usage"]
            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)
            total_tokens = usage.get('total_tokens', 0)

            estimated_cost = (prompt_tokens * 0.50 / 1_000_000) + (completion_tokens * 1.50 / 1_000_000)

            logging.info(f"🔧 Использовано токенов: prompt={prompt_tokens}, "
                         f"completion={completion_tokens}, total={total_tokens}, "
                         f"примерная стоимость: ${estimated_cost:.6f}")

        if "model" in response_data:
            logging.info(f"🔧 Использована модель: {response_data['model']}")

        logging.info(f"✅ Ответ сгенерирован. Длина: {len(response_content)} символов")
        return response_content.strip()

    except aiohttp.ClientError as e:
        logging.error(f"🔥 Ошибка подключения к OpenRouter: {str(e)}")
        raise Exception("Не удалось подключиться к OpenRouter API.")

    except asyncio.TimeoutError:
        logging.error("🔥 Таймаут при подключении к OpenRouter")
        raise Exception("Таймаут при подключении к OpenRouter.")

    except json.JSONDecodeError as e:
        logging.error(f"🔥 Ошибка парсинга JSON от OpenRouter: {str(e)}")
        raise Exception("Ошибка обработки ответа от сервера.")

    except Exception as e:
        logging.error(f"🔥 Ошибка в ai_generate: {str(e)}", exc_info=True)
        raise