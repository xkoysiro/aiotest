# 🤖 (RU) AI Telegram Bot with OpenRouter

Умный Telegram-бот с долгосрочной памятью диалога, работающий на мощных моделях через OpenRouter API с поддержкой инструментов (function calling).

## 🚀 Функционал

- 💬 **Интеллектуальный диалог** с AI-ассистентом
- 🧠 **Сохранение контекста** разговора (история до 20 сообщений)
- 🔧 **Инструменты AI** - поиск в интернете, работа с API, вычисления, уведомления
- 🔄 **Автоматическое управление памятью** - старые сообщения удаляются при превышении лимита
- 🎛 **Выбор разных LLM** через OpenRouter (GPT-4, Claude, Gemini, Llama и др.)
- 📊 **Статистика использования** - токены, стоимость запросов
- 🛡 **Безопасность** - локальное хранение контекста, защита ключей API

## 🛠 Технологии

- **Python 3.11+**
- **Aiogram 3.x** - современный фреймворк для Telegram ботов
- **OpenRouter API** - единый доступ к 100+ моделям (GPT-4, Claude, Llama и др.)
- **Aiohttp** - асинхронные HTTP запросы
- **Function Calling** - расширение возможностей нейросети через инструменты
- **In-memory хранилище** - быстрый доступ к контексту диалогов

## 🏗 Архитектура

```
telegram_ai_bot/
├── .env.example                 # Шаблон конфигурации (в репозитории)
├── .env                         # Локальная конфигурация (в .gitignore)
├── .gitignore                   # Игнорируемые файлы
├── run.py                       # Основной файл запуска (заменяет main.py)
├── config.py                    # Загрузка конфигурации
├── requirements.txt             # Зависимости проекта
├── README.md                    # Документация
├── app/                         # Основное приложение
│   ├── __init__.py
│   ├── handlers.py              # Обработчики сообщений и команд
│   ├── text_generate.py         # Интеграция с OpenRouter API
│   ├── context_manager.py       # Управление контекстом диалогов
│   ├── logging_setup.py         # Система логирования в Telegram
│   └── tools_templates.py       # Инструменты и шаблоны для работы с нейросетью
```

### Ключевые компоненты:

- **`run.py`** - Точка входа приложения, запуск бота (заменяет main.py)
- **`.env.example`** - Шаблон файла конфигурации
- **`app/tools_templates.py`** - Инструменты для расширения возможностей нейросети
- **`config.py`** - Управление конфигурацией, загрузка переменных окружения
- **`app/handlers.py`** - Все обработчики команд и сообщений Telegram
- **`app/text_generate.py`** - Интеграция с OpenRouter API, работа с моделями AI
- **`app/context_manager.py`** - Управление историей диалогов, кольцевой буфер сообщений
- **`app/logging_setup.py`** - Система логирования с отправкой в Telegram

## 🛠 `app/tools_templates.py` - Инструменты для расширения функциональности нейросети

Этот файл содержит готовые шаблоны инструментов (tools) для расширения возможностей нейросети через функцию вызовов (function calling). Инструменты позволяют AI-ассистенту взаимодействовать с внешними сервисами, базами данных и выполнять сложные операции.

### 🔧 Доступные инструменты:

- **🔍 `search_internet`** - Поиск актуальной информации в интернете (новости, погода, курсы валют)
- **🗄 `query_database`** - Запросы к базам данных (поиск пользователей, заказов, товаров)
- **🧮 `calculate_expression`** - Математические вычисления и конвертации единиц измерения
- **📁 `read_file_content`** - Работа с файлами и документами (чтение текстовых файлов, CSV, JSON)
- **🌐 `call_external_api`** - Интеграция с внешними API (погода, финансы, социальные сети)
- **📧 `send_notification`** - Отправка уведомлений (email, SMS, Telegram, push-уведомления)

### 🚀 Как использовать инструменты:

```python
from app.tools_templates import get_all_tools, process_tool_call

# Добавление инструментов в запрос к нейросети
payload = {
    "model": "gpt-4",
    "messages": messages,
    "tools": get_all_tools(),  # Все доступные инструменты
    "tool_choice": "auto"
}

# Обработка ответов с вызовами инструментов
for tool_call in response["tool_calls"]:
    result = await process_tool_call(tool_call)
```

### 💡 Особенности инструментов:

- **🔄 Универсальные шаблоны** - легко адаптируются под ваши нужды
- **⚡ Готовые схемы** - правильные JSON-схемы для function calling
- **🔧 Заглушки реализаций** - место для вашей бизнес-логики
- **🎯 Категоризация** - инструменты сгруппированы по назначению
- **🛡 Безопасность** - четкое разделение схем и реализаций

## 📦 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/xkoysiro/aiotest/tree/master
cd aiotest
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка окружения
```bash
# Скопируйте шаблон настроек
cp .env.example .env

# Отредактируйте .env файл, добавив ваши ключи:
# OPENROUTER_API_KEY=ваш_ключ_от_openrouter
# TELEGRAM_TOKEN=ваш_токен_бота_от_BotFather
```

### 4. Настройка инструментов (опционально)
Отредактируйте `app/tools_templates.py` чтобы добавить вашу логику:
- API ключи для внешних сервисов
- Подключение к вашей базе данных
- Интеграция с вашими системами

### 5. Запуск бота
```bash
python run.py
```

## ⚙️ Конфигурация

### Переменные окружения (.env):
```env
# Обязательные:
OPENROUTER_API_KEY=your_openrouter_api_key
TELEGRAM_TOKEN=your_telegram_bot_token

# Опциональные:
OPENROUTER_MODEL=openai/gpt-3.5-turbo  # Модель по умолчанию
CHAT_ID=your_chat_id                   # Для отправки логов в Telegram
MAX_CONTEXT_MESSAGES=20                # Максимум сообщений в истории
REQUEST_TIMEOUT=120                    # Таймаут запросов в секундах
```

### Поддерживаемые модели:
```python
# Популярные модели (автоматически определяются):
- openai/gpt-3.5-turbo
- openai/gpt-4
- openai/gpt-4-turbo
- anthropic/claude-3-sonnet
- anthropic/claude-3-haiku
- google/gemini-pro
- meta-llama/llama-3-70b-instruct
- mistralai/mistral-7b-instruct
```

## 🎯 Команды бота

- `/start` - начать диалог, инициализировать контекст
- `/clear` - очистить историю диалога
- `/history` - показать последние сообщения
- `/context` - информация о текущем контексте
- `/models` - список доступных моделей
- `/model_info [модель]` - подробности о модели
- `/switch_model [модель]` - сменить модель AI

## 🔧 Примеры использования

### Обычный диалог:
```
👤: Привет! Помоги написать письмо партнеру
🤖: Конечно! На какую тему письмо и какой тон предпочитаете?
```

### Использование инструментов:
```
👤: Какая сейчас погода в Москве?
🤖: [Использует инструмент поиска погоды]
✅ Погода в Москве: +20°C, солнечно

👤: Посчитай 25 * 4 + 100
🤖: [Использует инструмент вычислений]
✅ Результат: 25 * 4 + 100 = 200

👤: Найди информацию про искусственный интеллект
🤖: [Использует инструмент поиска в интернете]
✅ Нашел 3 статьи про ИИ...
```

### Работа с контекстом:
```
👤: Мы вчера обсуждали мой проект
🤖: Да, помню ваш проект по разработке AI-бота. Что хотели уточнить?
```

## 🔧 OpenRouter API

**Преимущества использования:**
- 📊 **Единый API** для 100+ моделей от разных провайдеров
- 💰 **Прозрачное ценообразование** - платите только за использованные токены
- 🚀 **Высокая доступность** - автоматическое переключение между провайдерами
- 🔄 **Быстрые обновления** - новые модели добавляются автоматически
- 🔧 **Function Calling** - поддержка инструментов и расширенной функциональности

**Как получить API ключ:**
1. Зарегистрируйтесь на [openrouter.ai](https://openrouter.ai/)
2. Перейдите в [API Keys](https://openrouter.ai/keys)
3. Создайте новый ключ
4. Добавьте его в `.env` файл

## 🐛 Отладка и логи

Бот отправляет логи в указанный Telegram чат:
- ✅ Успешные запросы
- ⚠️ Предупреждения (пустые сообщения и т.д.)
- ❌ Ошибки (проблемы с API, сетью и т.д.)
- 🔧 Использование инструментов

## 📞 Контакты

По вопросам сотрудничества и доработок - пишите в Telegram: [@RinKannnagi](https://t.me/RinKannnagi)

---

*🔄 Проект активно развивается. Следующие цели: персистентное хранилище, веб-админка, RAG-система, расширение инструментов.*

---

# 🤖 (ENG) AI Telegram Bot with OpenRouter

Smart Telegram bot with long-term dialogue memory, powered by multiple LLMs through OpenRouter API with function calling support.

## 🚀 Features

- 💬 **Intelligent dialogue** with AI assistant
- 🧠 **Context preservation** (up to 20 messages history)
- 🔧 **AI Tools** - internet search, API integration, calculations, notifications
- 🔄 **Automatic memory management** - old messages removed when limit exceeded
- 🎛 **Multiple LLM selection** via OpenRouter (GPT-4, Claude, Gemini, Llama, etc.)
- 📊 **Usage statistics** - tokens, request costs
- 🛡 **Security** - local context storage, API key protection

## 🏗 Architecture

```
telegram_ai_bot/
├── .env.example                 # Configuration template (in repository)
├── .env                         # Local configuration (in .gitignore)
├── .gitignore                   # Ignored files
├── run.py                       # Main launch file (replaces main.py)
├── config.py                    # Configuration loading
├── requirements.txt             # Project dependencies
├── README.md                    # Documentation
├── app/                         # Main application
│   ├── __init__.py
│   ├── handlers.py              # Message and command handlers
│   ├── text_generate.py         # OpenRouter API integration
│   ├── context_manager.py       # Dialogue context management
│   ├── logging_setup.py         # Telegram logging system
│   └── tools_templates.py       # AI tools and function calling templates
```

### Key Components:

- **`run.py`** - Application entry point, bot launch (replaces main.py)
- **`.env.example`** - Configuration file template
- **`app/tools_templates.py`** - AI tools for extended functionality
- **`config.py`** - Configuration management, environment variables loading
- **`app/handlers.py`** - All Telegram command and message handlers
- **`app/text_generate.py`** - OpenRouter API integration, AI models work
- **`app/context_manager.py`** - Dialogue history management, message circular buffer
- **`app/logging_setup.py`** - Logging system with Telegram notifications

## 🛠 `app/tools_templates.py` - AI Tools and Function Calling Templates

This file contains ready-to-use tool templates for extending AI capabilities through function calling. Tools allow AI assistant to interact with external services, databases and perform complex operations.

### 🔧 Available Tools:

- **🔍 `search_internet`** - Search for current information online (news, weather, exchange rates)
- **🗄 `query_database`** - Database queries (search users, orders, products)
- **🧮 `calculate_expression`** - Mathematical calculations and unit conversions
- **📁 `read_file_content`** - File and document operations (read text files, CSV, JSON)
- **🌐 `call_external_api`** - External API integration (weather, finance, social media)
- **📧 `send_notification`** - Notifications delivery (email, SMS, Telegram, push notifications)

### 🚀 How to use tools:

```python
from app.tools_templates import get_all_tools, process_tool_call

# Adding tools to AI request
payload = {
    "model": "gpt-4",
    "messages": messages,
    "tools": get_all_tools(),  # All available tools
    "tool_choice": "auto"
}

# Processing tool call responses
for tool_call in response["tool_calls"]:
    result = await process_tool_call(tool_call)
```

### 💡 Tool Features:

- **🔄 Universal templates** - easily adaptable to your needs
- **⚡ Ready schemas** - proper JSON schemas for function calling
- **🔧 Implementation stubs** - place for your business logic
- **🎯 Categorization** - tools grouped by purpose
- **🛡 Security** - clear separation of schemas and implementations

## 📦 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/xkoysiro/aiotest/tree/master
cd aiotest
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
```bash
# Copy configuration template
cp .env.example .env

# Edit .env file with your keys:
# OPENROUTER_API_KEY=your_openrouter_api_key
# TELEGRAM_TOKEN=your_telegram_bot_token
```

### 4. Configure Tools (Optional)
Edit `app/tools_templates.py` to add your logic:
- API keys for external services
- Connection to your database
- Integration with your systems

### 5. Run Bot
```bash
python run.py
```

## ⚙️ Configuration

### Environment Variables (.env):
```env
# Required:
OPENROUTER_API_KEY=your_openrouter_api_key
TELEGRAM_TOKEN=your_telegram_bot_token

# Optional:
OPENROUTER_MODEL=openai/gpt-3.5-turbo  # Default model
CHAT_ID=your_chat_id                   # For Telegram logs
MAX_CONTEXT_MESSAGES=20                # Max messages in history
REQUEST_TIMEOUT=120                    # Request timeout in seconds
```

### Supported Models:
```python
# Popular models (automatically detected):
- openai/gpt-3.5-turbo
- openai/gpt-4
- openai/gpt-4-turbo
- anthropic/claude-3-sonnet
- anthropic/claude-3-haiku
- google/gemini-pro
- meta-llama/llama-3-70b-instruct
- mistralai/mistral-7b-instruct
```

## 🎯 Bot Commands

- `/start` - start dialogue, initialize context
- `/clear` - clear dialogue history
- `/history` - show recent messages
- `/context` - current context information
- `/models` - list available models
- `/model_info [model]` - model details
- `/switch_model [model]` - change AI model

## 🔧 Usage Examples

### Regular Dialogue:
```
👤: Hi! Help me write an email to a partner
🤖: Of course! What's the email topic and preferred tone?
```

### Tool Usage:
```
👤: What's the weather in Moscow?
🤖: [Uses weather search tool]
✅ Weather in Moscow: +20°C, sunny

👤: Calculate 25 * 4 + 100
🤖: [Uses calculation tool]
✅ Result: 25 * 4 + 100 = 200

👤: Find information about artificial intelligence
🤖: [Uses internet search tool]
✅ Found 3 articles about AI...
```

### Context Work:
```
👤: We discussed my project yesterday
🤖: Yes, I remember your AI bot development project. What did you want to clarify?
```

## 🔧 OpenRouter API

**Advantages:**
- 📊 **Unified API** for 100+ models from different providers
- 💰 **Transparent pricing** - pay only for tokens used
- 🚀 **High availability** - automatic provider switching
- 🔄 **Fast updates** - new models added automatically
- 🔧 **Function Calling** - tools and extended functionality support

**How to get API key:**
1. Register at [openrouter.ai](https://openrouter.ai/)
2. Go to [API Keys](https://openrouter.ai/keys)
3. Create new key
4. Add it to `.env` file

## 🐛 Debugging and Logs

Bot sends logs to specified Telegram chat:
- ✅ Successful requests
- ⚠️ Warnings (empty messages, etc.)
- ❌ Errors (API issues, network problems, etc.)
- 🔧 Tool usage

## 📞 Contacts

For collaboration and customization inquiries - contact me on Telegram: [@RinKannnagi](https://t.me/RinKannnagi)

---

*🔄 Project actively developing. Next goals: persistent storage, web admin panel, RAG system, tools expansion.*
