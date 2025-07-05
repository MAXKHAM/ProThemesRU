#!/usr/bin/env python3
"""
Запуск телеграм бота ProThemesRU
(Запускайте этот файл из папки telegram_bot)
"""

import sys
import os
import logging
from pathlib import Path

# Добавляем родительскую директорию в путь для импорта
sys.path.append(str(Path(__file__).parent.parent))

try:
    from config import BotConfig
    from bot import main
except ImportError as e:
    print(f"Ошибка импорта: {e}\nУбедитесь, что вы запускаете из папки telegram_bot и все зависимости установлены.")
    sys.exit(1)

def setup_logging():
    """Настройка логирования"""
    logging.basicConfig(
        level=getattr(logging, BotConfig.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(BotConfig.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_environment():
    """Проверка окружения"""
    errors = BotConfig.validate()
    
    if errors:
        print("❌ Ошибки конфигурации:")
        for error in errors:
            print(f"  - {error}")
        print("\nСоздайте файл .env с необходимыми переменными:")
        print("TELEGRAM_BOT_TOKEN=your_bot_token_here")
        print("TELEGRAM_ADMIN_CHAT_ID=your_admin_chat_id_here")
        return False
    
    return True

def main_wrapper():
    """Обертка для запуска бота"""
    print("🤖 Запуск телеграм бота ProThemesRU...")
    
    # Настройка логирования
    setup_logging()
    
    # Проверка окружения
    if not check_environment():
        sys.exit(1)
    
    print("✅ Конфигурация проверена успешно")
    print(f"📝 Логи будут записываться в: {BotConfig.LOG_FILE}")
    print(f"🔗 API URL: {BotConfig.API_BASE_URL}")
    
    try:
        # Запуск бота
        main()
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        logging.error(f"Критическая ошибка: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main_wrapper() 