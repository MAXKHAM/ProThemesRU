import telebot
from flask import Blueprint, request, current_app, jsonify
from config import Config
from app.models import User, GeneratedSite
from app import db

telegram_bp = Blueprint('telegram', __name__)

# Инициализация бота
bot = telebot.TeleBot(Config.TELEGRAM_BOT_TOKEN)

# Пример обработчика команды /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_id = message.from_user.id
    # Здесь можно проверить пользователя в БД, предложить регистрацию/вход
    bot.reply_to(message, f"Привет, {message.from_user.first_name}! Я ваш помощник по конструктору сайтов. Используйте меня для уведомлений или поддержки.")
    # Можно отправить ссылку на ваш сайт
    # bot.send_message(user_id, "Перейдите на наш сайт: http://127.0.0.1:5000/")

# Пример отправки уведомления из Flask-приложения
def send_site_generated_notification(telegram_id, site_url):
    try:
        bot.send_message(telegram_id, f"Ваш сайт по адресу {site_url} успешно сгенерирован!")
    except Exception as e:
        print(f"Ошибка отправки уведомления в Telegram: {e}")

# Функция для запуска бота (для отдельного процесса или потока)
def run_bot_polling():
    # Это блокирующая операция, поэтому ее лучше запускать в отдельном потоке/процессе
    # Или использовать вебхуки для продакшена
    print("Telegram Bot polling started...")
    bot.polling(none_stop=True)

# Вебхук для Telegram
@telegram_bp.route('/webhook', methods=['POST'])
def webhook():
    """Webhook для Telegram бота"""
    data = request.get_data()
    
    # Здесь будет логика обработки сообщений от Telegram
    return jsonify({'status': 'ok'})

# Функция для установки вебхука
def set_telegram_webhook():
    webhook_url = f"{Config.PUBLIC_APP_URL}/telegram_bot/telegram_webhook"
    try:
        bot.set_webhook(url=webhook_url)
        print(f"Webhook set to: {webhook_url}")
    except Exception as e:
        print(f"Error setting webhook: {e}")

@telegram_bp.route('/bot/status')
def bot_status():
    """Статус бота"""
    return jsonify({
        'status': 'running',
        'message': 'Telegram bot is active'
    }) 