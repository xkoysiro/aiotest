import aiohttp
import json
import logging
from config import LM_STUDIO_URL


async def ai_generate(text: str):
    """
    Генерация ответа с помощью локальной модели через LM Studio
    """
    try:
        # Проверяем входные данные
        if not text or not text.strip():
            logging.warning("⚠️ Получен пустой запрос")
            return "Пожалуйста, напишите ваш запрос."

        logging.info(f"🔧 Начало генерации через LM Studio. Длина текста: {len(text)} символов")
        logging.debug(f"🔧 Текст запроса: {text}")

        # URL LM Studio (памятка: обычно это http://localhost:1234/v1)
        url = f"{LM_STUDIO_URL}/chat/completions"

        # Данные для запроса
        payload = {
            "model": "local-model",
            "messages": [
                {
                    "role": "user",
                    "content": text
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1000,
            "stream": False
        }

        headers = {
            "Content-Type": "application/json"
        }

        # Отправляем запрос к LM Studio
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logging.error(f"❌ Ошибка LM Studio: HTTP {response.status} - {error_text}")
                    raise Exception(f"LM Studio error: HTTP {response.status}")

                response_data = await response.json()
                logging.debug(f"🔧 Полный ответ LM Studio: {json.dumps(response_data, ensure_ascii=False)[:500]}...")

        # Извлекаем ответ
        if not response_data.get("choices"):
            logging.error("❌ LM Studio вернуло пустой список choices")
            return "Извините, не удалось сгенерировать ответ."

        response_content = response_data["choices"][0]["message"]["content"]

        if not response_content:
            logging.warning("⚠️ LM Studio вернуло пустой ответ")
            return "Извините, не удалось сгенерировать содержательный ответ."

        # Логируем информацию об использовании токенов
        if "usage" in response_data:
            usage = response_data["usage"]
            logging.info(f"🔧 Использовано токенов: {usage.get('total_tokens', 'N/A')}")

        logging.info(f"✅ Ответ сгенерирован через LM Studio. Длина: {len(response_content)} символов")
        logging.debug(f"🔧 Содержание ответа: {response_content}")

        return response_content

    except aiohttp.ClientError as e:
        logging.error(f"🔥 Ошибка подключения к LM Studio: {str(e)}")
        raise Exception("Не удалось подключиться к локальной модели. Убедитесь, что LM Studio запущен.")

    except Exception as e:
        logging.error(f"🔥 Ошибка в ai_generate: {str(e)}", exc_info=True)
        raise