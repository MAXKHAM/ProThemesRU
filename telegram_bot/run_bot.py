#!/usr/bin/env python3
"""
Скрипт для запуска Telegram бота ProThemesRU
"""

import os
import sys
from bot import main

if __name__ == "__main__":
    # Проверяем наличие токена
    if not os.environ.get('TELEGRAM_BOT_TOKEN'):
        print("❌ Ошибка: TELEGRAM_BOT_TOKEN не установлен!")
        print("💡 Установите переменную окружения TELEGRAM_BOT_TOKEN")
        sys.exit(1)
    
    # Проверяем URL API
    api_url = os.environ.get('API_BASE_URL')
    if not api_url or api_url == 'https://your-vercel-url.vercel.app':
        print("⚠️  Предупреждение: API_BASE_URL не настроен!")
        print("💡 Установите переменную окружения API_BASE_URL")
    
    print("🚀 Запуск Telegram бота ProThemesRU...")
    print(f"📡 API URL: {api_url}")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Ошибка запуска бота: {e}")
        sys.exit(1) 