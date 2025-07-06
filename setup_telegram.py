#!/usr/bin/env python3
"""
Скрипт для настройки Telegram вебхука
"""

import os
import sys
from app.telegram_bot.routes import set_telegram_webhook
from config import Config

def main():
    print("🤖 Настройка Telegram вебхука...")
    
    # Проверяем токен
    if not Config.TELEGRAM_BOT_TOKEN or 'your_telegram_bot_token' in Config.TELEGRAM_BOT_TOKEN:
        print("❌ Ошибка: TELEGRAM_BOT_TOKEN не настроен!")
        print("📝 Добавьте в config.py или установите переменную окружения:")
        print("   TELEGRAM_BOT_TOKEN=your_actual_bot_token")
        return False
    
    # Проверяем публичный URL
    if '127.0.0.1' in Config.PUBLIC_APP_URL:
        print("⚠️  Предупреждение: Используется localhost URL")
        print("📝 Для работы вебхука нужен публичный URL")
        print("💡 Используйте ngrok или другой туннель:")
        print("   ngrok http 5000")
        print("   Затем установите PUBLIC_APP_URL=https://your-ngrok-url.ngrok.io")
        return False
    
    try:
        set_telegram_webhook()
        print("✅ Вебхук успешно настроен!")
        return True
    except Exception as e:
        print(f"❌ Ошибка настройки вебхука: {e}")
        return False

if __name__ == '__main__':
    main() 