#!/usr/bin/env python3
"""
Главный файл для запуска приложения ProThemesRU
"""

import os
from app import create_app
from config import config_by_name

# Определяем конфигурацию
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    print("🚀 Запуск ProThemesRU...")
    print(f"📋 Конфигурация: {config_name}")
    print("🌐 Приложение доступно по адресу: http://127.0.0.1:5000")
    print("🔧 Режим отладки: ВКЛЮЧЕН" if app.debug else "🔧 Режим отладки: ВЫКЛЮЧЕН")
    print("📱 Telegram бот: Настройте TELEGRAM_BOT_TOKEN в config.py")
    print("💳 Платежи: Настройте YOOKASSA_SHOP_ID и YOOKASSA_SECRET_KEY")
    print("\n" + "="*50)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.debug
    ) 