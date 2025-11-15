# 🤖 (RU) AI Telegram Bot with OpenRouter

Умный Telegram-бот с долгосрочной памятью диалога, работающий на мощных моделях через OpenRouter API.

## 🚀 Функционал

- 💬 Интеллектуальный диалог с AI-ассистентом
- 🧠 Сохранение контекста разговора (история сообщений)
- 🔄 Гибкая система промптов и настроек(в разработке)
- ⚙️ FSM (Finite State Machine) для сложных сценариев(в разработке)
- 🎛 Выбор разных LLM через OpenRouter(в разработке)

## 🛠 Технологии

- **Python 3.11+**
- **Aiogram 3.x** - современный фреймворк для Telegram ботов
- **OpenRouter API** - единый доступ к 100+ моделям (GPT-4, Claude, Llama и др.)
- **SQLite/PostgreSQL** - хранение данных и контекста (на данный момент не используется)
- **Docker** - контейнеризация (опционально)(на данный момент не используется)

## 📦 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/ваш-ник/ваш-репозиторий.git
cd your-bot-repo
```

### 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 3. Настройка окружения
Создайте файл `.env` используя `.env example` из репозитория.

### 4. Запуск бота
```bash
python run.py
```

## ⚙️ Конфигурация моделей

Бот поддерживает любые модели с OpenRouter:

```python
# Доступные модели (примеры)
MODELS = {
    "gpt-4": "openai/gpt-4",
    "claude-sonnet": "anthropic/claude-3-sonnet", 
    "llama-70b": "meta-llama/llama-3-70b-instruct",
    "mixtral": "mistralai/mixtral-8x7b-instruct"
}
```

## 🎯 Примеры использования

**Обычный диалог:**
```
👤: Привет! Помоги написать письмо партнеру
🤖: Конечно! На какую тему письмо и какой тон предпочитаете?
```

**Работа с контекстом:**
```
👤: Мы вчера обсуждали мой проект
🤖: Да, помню ваш проект по разработке AI-бота. Что хотели уточнить?
```

## 🔧 API OpenRouter

**Преимущества использования:**
- Единый API для 100+ моделей
- Гибкая настройка параметров
- Конкурентные цены
- Быстрое обновление моделей

## 📞 Контакты

По вопросам сотрудничества и доработок - пишите в Telegram: @RinKannnagi

---

*🔄 Проект активно развивается. Следующие цели: веб-админка, RAG-система, мультиязычность.*

---

# 🤖 (ENG) AI Telegram Bot with OpenRouter

Smart Telegram bot with long-term dialogue memory, powered by multiple LLMs through OpenRouter API.

## 🚀 Features

- 💬 Intelligent dialogue with AI assistant
- 🧠 Conversation context preservation (message history)
- 🔄 Flexible prompt and settings system (in development)
- ⚙️ FSM (Finite State Machine) for complex scenarios (in development)
- 🎛 Multiple LLM selection via OpenRouter (in development)

## 🛠 Technologies

- **Python 3.11+**
- **Aiogram 3.x** - modern Telegram bot framework
- **OpenRouter API** - unified access to 100+ models (GPT-4, Claude, Llama, etc.)
- **SQLite/PostgreSQL** - data and context storage (currently not used)
- **Docker** - containerization (optional, currently not used)

## 📦 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/your-username/your-repository.git
cd your-bot-repo
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Create `.env` file using `.env example` from repository.

### 4. Run Bot
```bash
python run.py
```

## ⚙️ Model Configuration

Bot supports any OpenRouter models:

```python
# Available models (examples)
MODELS = {
    "gpt-4": "openai/gpt-4",
    "claude-sonnet": "anthropic/claude-3-sonnet", 
    "llama-70b": "meta-llama/llama-3-70b-instruct",
    "mixtral": "mistralai/mixtral-8x7b-instruct"
}
```

## 🎯 Usage Examples

**Regular Dialogue:**
```
👤: Hi! Help me write an email to a partner
🤖: Of course! What's the email topic and preferred tone?
```

**Context Work:**
```
👤: We discussed my project yesterday
🤖: Yes, I remember your AI bot development project. What did you want to clarify?
```

## 🔧 OpenRouter API

**Advantages:**
- Single API for 100+ models
- Flexible parameter configuration
- Competitive pricing
- Fast model updates

## 📞 Contacts

For collaboration and customization inquiries - contact me on Telegram: @RinKannnagi

---

*🔄 Project actively developing. Next goals: web admin panel, RAG system, multilingual support.*
```
