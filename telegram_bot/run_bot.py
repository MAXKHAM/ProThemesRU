#!/usr/bin/env python3
"""
ProThemesRU Telegram Bot - Background Worker
Runs the bot in polling mode for Render worker dyno
"""

import os
import logging
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
import json

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')

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
                },
                {
                    "id": 2,
                    "name": "Креативное Агентство",
                    "category": "agency",
                    "price": 12000,
                    "description": "Стильный сайт для креативных агентств"
                },
                {
                    "id": 3,
                    "name": "Премиум E-commerce",
                    "category": "ecommerce",
                    "price": 25000,
                    "description": "Полнофункциональный интернет-магазин"
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

async def main():
    """Main function"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not configured!")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(CommandHandler('templates', templates_command))
    application.add_handler(CommandHandler('blocks', blocks_command))
    application.add_handler(CommandHandler('styles', styles_command))
    application.add_handler(CommandHandler('constructor', constructor_command))
    application.add_handler(CommandHandler('order', order_command))
    application.add_handler(CommandHandler('pricing', pricing_command))
    application.add_handler(CommandHandler('help', help_command))
    
    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    # Add error handler
    application.add_error_handler(error_handler)
    
    # Start polling
    logger.info("Starting bot in polling mode...")
    await application.initialize()
    await application.start()
    await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    asyncio.run(main()) 