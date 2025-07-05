#!/usr/bin/env python3
"""
Скрипт для запуска Telegram-бота ProThemesRU
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Добавляем путь к проекту
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.telegram_bot import start_telegram_bot

if __name__ == "__main__":
    # Проверяем токен бота
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token or token == "7967424639:AAGaQBdm3_QDqvnh8K61uo8sUrVlHii7FS0":
        print("\n" + "="*80)
        print("!!! ВНИМАНИЕ: Установите переменную окружения TELEGRAM_BOT_TOKEN !!!")
        print("!!! Получите токен у @BotFather в Telegram !!!")
        print("!!! Создайте файл .env с содержимым: TELEGRAM_BOT_TOKEN=ваш_токен !!!")
        print("="*80 + "\n")
        sys.exit(1)
    
    print("Запуск Telegram-бота ProThemesRU...")
    print(f"Токен: {token[:10]}...")
    print("Нажмите Ctrl+C для остановки")
    
    try:
        start_telegram_bot()
    except KeyboardInterrupt:
        print("\nБот остановлен пользователем")
    except Exception as e:
        print(f"Ошибка запуска бота: {e}")
        sys.exit(1) 