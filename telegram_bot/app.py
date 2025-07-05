#!/usr/bin/env python3
"""
ProThemesRU Telegram Bot - Main Application
Deployment-ready Flask application for Render
"""

import os
import logging
from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import asyncio
from threading import Thread
import json

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')

# Initialize bot
bot = Bot(token=BOT_TOKEN) if BOT_TOKEN else None

# Store bot application globally
bot_app = None

def load_templates():
    """Load templates from JSON files"""
    try:
        with open('templates/blocks/premium_templates.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.warning("Templates file not found, using default")
        return {
            "premium_templates": [
                {
                    "id": 1,
                    "name": "Современный SaaS Лендинг",
                    "category": "saas",
                    "price": 15000,
                    "description": "Премиум лендинг для SaaS продуктов"
                }
            ]
        }

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    welcome_text = f"""
🚀 Добро пожаловать в ProThemesRU, {user.first_name}!

🎨 Создайте профессиональный сайт за несколько минут!

Выберите действие:
/start - Главное меню
/templates - 📚 Шаблоны сайтов
/blocks - 🧱 UI компоненты  
/styles - 🎨 Стили и эффекты
/constructor - 🛠️ Конструктор сайтов
/order - 📦 Заказать сайт
/pricing - 💰 Цены и тарифы
/help - ❓ Помощь

💡 Начните с /templates чтобы посмотреть готовые шаблоны!
    """
    
    await update.message.reply_text(welcome_text)

async def templates_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /templates command"""
    templates = load_templates()
    
    response = "📚 **Доступные шаблоны:**\n\n"
    
    for template in templates.get('premium_templates', [])[:5]:  # Show first 5
        response += f"🎨 **{template['name']}**\n"
        response += f"📂 Категория: {template['category']}\n"
        response += f"💰 Цена: {template['price']} ₽\n"
        response += f"📝 {template['description']}\n\n"
    
    response += "💡 Используйте /order для заказа шаблона"
    
    await update.message.reply_text(response, parse_mode='Markdown')

async def blocks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /blocks command"""
    response = """🧱 **UI Компоненты и блоки:**

🎯 **Категории блоков:**
• 💼 Бизнес-блоки
• 🎨 Портфолио
• 🛒 E-commerce
• 🏢 Корпоративные
• 📝 Блог
• 🍽️ Рестораны
• 🏠 Недвижимость
• 🏥 Медицина

💡 **Доступно более 50 компонентов!**

🔧 Используйте /constructor для создания сайта
📦 Используйте /order для заказа
    """
    
    await update.message.reply_text(response, parse_mode='Markdown')

async def styles_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /styles command"""
    response = """🎨 **Современные стили и эффекты:**

🌈 **Градиенты:**
• Neon - Неоновые эффекты
• Sunset - Закатные тона
• Ocean - Морские оттенки
• Forest - Лесные цвета
• Fire - Огненные градиенты
• Aurora - Северное сияние

✨ **Эффекты:**
• Glass - Стеклянные элементы
• Hover - Анимации при наведении
• Scroll - Анимации при скролле
• Loading - Загрузочные анимации

🎯 **Кнопки:**
• Modern - Современные
• Neon - Неоновые
• Glass - Стеклянные

💡 **30+ готовых стилей!**
    """
    
    await update.message.reply_text(response, parse_mode='Markdown')

async def constructor_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /constructor command"""
    response = """🛠️ **Конструктор сайтов ProThemesRU**

🎯 **Возможности:**
• 🎨 Визуальный редактор
• 🧱 Drag & Drop блоки
• 📱 Адаптивный дизайн
• ⚡ Быстрая сборка
• 📤 Экспорт в HTML/CSS

🚀 **Начните создание:**
1. Выберите шаблон (/templates)
2. Настройте блоки (/blocks)
3. Примените стили (/styles)
4. Закажите готовый сайт (/order)

💡 **Создайте сайт за 10 минут!**
    """
    
    await update.message.reply_text(response, parse_mode='Markdown')

async def order_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /order command"""
    response = """📦 **Заказать сайт**

🎯 **Тарифы:**
• 🚀 **Старт** - 5,000 ₽
  - Лендинг страница
  - Адаптивный дизайн
  - 3 дня разработки

• 💼 **Бизнес** - 15,000 ₽
  - Многостраничный сайт
  - CMS система
  - SEO оптимизация
  - 7 дней разработки

• ⭐ **Премиум** - 25,000 ₽
  - E-commerce функционал
  - Интеграции
  - Аналитика
  - 14 дней разработки

📞 **Свяжитесь с нами:**
• Telegram: @ProThemesSupport
• Email: support@prothemes.ru
• Сайт: https://prothemes.ru

💡 Укажите в сообщении желаемый тариф!
    """
    
    await update.message.reply_text(response, parse_mode='Markdown')

async def pricing_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /pricing command"""
    response = """💰 **Цены и тарифы ProThemesRU**

🎯 **Создание сайтов:**
• 🚀 Лендинг: от 5,000 ₽
• 💼 Корпоративный: от 15,000 ₽
• 🛒 Интернет-магазин: от 25,000 ₽
• 🎨 Портфолио: от 8,000 ₽

📦 **Готовые шаблоны:**
• 📚 Базовые: 2,000 ₽
• ⭐ Премиум: 5,000 ₽
• 🏆 VIP: 10,000 ₽

🔧 **Дополнительные услуги:**
• 📱 Мобильная версия: +2,000 ₽
• 🔍 SEO оптимизация: +3,000 ₽
• 📊 Аналитика: +1,500 ₽
• 🚀 Ускорение: +50% к цене

💡 **Акции и скидки:**
• 🎉 Первый заказ: -20%
• 👥 Оптом: -15%
• ⏰ Срочно: +30%

📞 Закажите через /order
    """
    
    await update.message.reply_text(response, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    response = """❓ **Помощь по ProThemesRU**

🎯 **Основные команды:**
/start - Главное меню
/templates - Просмотр шаблонов
/blocks - UI компоненты
/styles - Стили и эффекты
/constructor - Создание сайта
/order - Заказать сайт
/pricing - Цены и тарифы
/help - Эта справка

💡 **Как создать сайт:**
1. Выберите шаблон (/templates)
2. Настройте блоки (/blocks)
3. Примените стили (/styles)
4. Закажите готовый сайт (/order)

📞 **Поддержка:**
• Telegram: @ProThemesSupport
• Email: support@prothemes.ru
• Сайт: https://prothemes.ru

🚀 **Готовы создать сайт? Начните с /start!**
    """
    
    await update.message.reply_text(response, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages"""
    message_type = update.message.chat.type
    text = update.message.text
    
    logger.info(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    
    if message_type == 'group':
        if '@ProThemesRUBot' in text:
            new_text = text.replace('@ProThemesRUBot', '').strip()
            response = f'Привет! Вы написали: "{new_text}"'
        else:
            return
    else:
        response = f'Вы написали: "{text}"\n\n💡 Используйте /start для главного меню'
    
    await update.message.reply_text(response)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f'Exception while handling an update: {context.error}')

def run_bot():
    """Run the bot in a separate thread"""
    global bot_app
    
    async def main():
        # Create application
        bot_app = Application.builder().token(BOT_TOKEN).build()
        
        # Add handlers
        bot_app.add_handler(CommandHandler('start', start_command))
        bot_app.add_handler(CommandHandler('templates', templates_command))
        bot_app.add_handler(CommandHandler('blocks', blocks_command))
        bot_app.add_handler(CommandHandler('styles', styles_command))
        bot_app.add_handler(CommandHandler('constructor', constructor_command))
        bot_app.add_handler(CommandHandler('order', order_command))
        bot_app.add_handler(CommandHandler('pricing', pricing_command))
        bot_app.add_handler(CommandHandler('help', help_command))
        
        # Add message handler
        bot_app.add_handler(MessageHandler(filters.TEXT, handle_message))
        
        # Add error handler
        bot_app.add_error_handler(error_handler)
        
        # Set webhook if URL is provided
        if WEBHOOK_URL:
            await bot_app.bot.set_webhook(url=WEBHOOK_URL)
            logger.info(f"Webhook set to {WEBHOOK_URL}")
        else:
            # Start polling
            await bot_app.initialize()
            await bot_app.start()
            await bot_app.run_polling(allowed_updates=Update.ALL_TYPES)
    
    # Run the bot
    asyncio.run(main())

# Flask routes
@app.route('/')
def home():
    """Home page"""
    return jsonify({
        "status": "success",
        "message": "ProThemesRU Telegram Bot is running!",
        "version": "1.0.0",
        "endpoints": {
            "webhook": "/webhook",
            "health": "/health",
            "status": "/status"
        }
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle webhook from Telegram"""
    if bot_app is None:
        return jsonify({"error": "Bot not initialized"}), 500
    
    try:
        # Process the update
        update = Update.de_json(request.get_json(), bot_app.bot)
        
        # Handle the update
        asyncio.create_task(bot_app.process_update(update))
        
        return jsonify({"status": "ok"})
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "bot_token": "configured" if BOT_TOKEN else "missing",
        "admin_chat_id": "configured" if ADMIN_CHAT_ID else "missing"
    })

@app.route('/status')
def status():
    """Status endpoint"""
    return jsonify({
        "status": "running",
        "bot": "active" if bot_app else "inactive",
        "webhook": "configured" if WEBHOOK_URL else "polling"
    })

if __name__ == '__main__':
    # Start bot in a separate thread
    if BOT_TOKEN:
        bot_thread = Thread(target=run_bot)
        bot_thread.daemon = True
        bot_thread.start()
        logger.info("Bot started in background thread")
    else:
        logger.error("BOT_TOKEN not configured!")
    
    # Run Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 