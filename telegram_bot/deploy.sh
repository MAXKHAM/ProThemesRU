#!/bin/bash

# Скрипт для быстрого деплоя Telegram Bot

echo "🚀 Запуск деплоя Telegram Bot ProThemesRU..."

# Проверка наличия токена
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ Ошибка: TELEGRAM_BOT_TOKEN не установлен"
    echo "Установите переменную окружения или добавьте в .env файл"
    exit 1
fi

# Проверка наличия admin chat id
if [ -z "$TELEGRAM_ADMIN_CHAT_ID" ]; then
    echo "❌ Ошибка: TELEGRAM_ADMIN_CHAT_ID не установлен"
    echo "Установите переменную окружения или добавьте в .env файл"
    exit 1
fi

echo "✅ Переменные окружения проверены"

# Установка зависимостей
echo "📦 Установка зависимостей..."
pip install -r requirements.txt

# Создание .env файла
echo "📝 Создание .env файла..."
cat > .env << EOF
TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
TELEGRAM_ADMIN_CHAT_ID=$TELEGRAM_ADMIN_CHAT_ID
API_BASE_URL=${API_BASE_URL:-http://localhost:5000}
LOG_LEVEL=${LOG_LEVEL:-INFO}
EOF

echo "✅ .env файл создан"

# Проверка конфигурации
echo "🔧 Проверка конфигурации..."
python -c "from config import BotConfig; print('✅ Конфигурация корректна')"

# Запуск бота
echo "🤖 Запуск бота..."
if [ "$USE_WEBHOOK" = "true" ]; then
    echo "🌐 Запуск с веб-хуками..."
    python webhook_bot.py
else
    echo "🔄 Запуск в режиме polling..."
    python bot.py
fi 