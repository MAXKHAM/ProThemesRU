import logging
from telegram.ext import Application
from app.telegram_bot import start_telegram_bot

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    print("Запуск Telegram-бота...")
    try:
        start_telegram_bot()
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
