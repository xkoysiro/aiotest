import aiohttp
import json
import logging
from typing import List, Dict
from config import LM_STUDIO_URL
import asyncio


async def ai_generate(messages: List[Dict[str, str]]) -> str:
    """
    Генерация ответа с помощью локальной модели через LM Studio

    Args:
        messages: Список сообщений в формате [{"role": "user", "content": "текст"}]
    """
    try:
        if not messages:
            logging.warning("⚠️ Получен пустой список сообщений")
            return "Пожалуйста, напишите ваш запрос."

        # Проверяем, что последнее сообщение от пользователя
        if messages and messages[-1]['role'] != 'user':
            logging.warning("⚠️ Последнее сообщение не от пользователя")
            return "Ошибка формата запроса."

        logging.info(f"🔧 Начало генерации через LM Studio. Сообщений: {len(messages)}")

        # Логируем структуру промпта для отладки
        prompt_debug = "\n".join([f"{msg['role']}: {msg['content'][:50]}..." for msg in messages[-3:]])
        logging.debug(f"🔧 Структура промпта (последние 3):\n{prompt_debug}")

        url = f"{LM_STUDIO_URL}/chat/completions"

        payload = {
            "model": "local-model",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1000,
            "stream": False
        }

        headers = {"Content-Type": "application/json"}

        logging.debug(f"🔧 Отправка запроса к {url}")

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers,) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logging.error(f"❌ Ошибка LM Studio: HTTP {response.status} - {error_text}")

                    if response.status == 404:
                        raise Exception("LM Studio не доступен. Проверьте запущен ли сервер.")
                    elif response.status == 422:
                        raise Exception("Неверный формат запроса к LM Studio.")
                    else:
                        raise Exception(f"Ошибка LM Studio: HTTP {response.status}")

                response_data = await response.json()
                logging.debug(f"🔧 Получен ответ от LM Studio")

        if not response_data.get("choices"):
            logging.error("❌ LM Studio вернуло пустой список choices")
            logging.debug(f"🔧 Полный ответ: {response_data}")
            return "Извините, не удалось сгенерировать ответ."

        response_content = response_data["choices"][0]["message"]["content"]

        if not response_content or not response_content.strip():
            logging.warning("⚠️ LM Studio вернуло пустой ответ")
            return "Извините, не удалось сгенерировать содержательный ответ."

        # Логируем информацию об использовании токенов
        if "usage" in response_data:
            usage = response_data["usage"]
            logging.info(f"🔧 Использовано токенов: prompt={usage.get('prompt_tokens', 'N/A')}, "
                         f"completion={usage.get('completion_tokens', 'N/A')}, "
                         f"total={usage.get('total_tokens', 'N/A')}")

        logging.info(f"✅ Ответ сгенерирован. Длина: {len(response_content)} символов")
        return response_content.strip()

    except aiohttp.ClientError as e:
        logging.error(f"🔥 Ошибка подключения к LM Studio: {str(e)}")
        raise Exception("Не удалось подключиться к локальной модели.")

    except asyncio.TimeoutError:
        logging.error("🔥 Таймаут при подключении к LM Studio")
        raise Exception("Таймаут при подключении к модели. Попробуйте позже.")

    except Exception as e:
        logging.error(f"🔥 Ошибка в ai_generate: {str(e)}", exc_info=True)
        raise