#!/usr/bin/env python3
"""
Telegram бот для ProThemesRU
Интеграция с API для создания и управления сайтами
"""

import os
import logging
import requests
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
API_BASE_URL = os.environ.get('API_BASE_URL', 'https://your-real-url-here.com')

class ProThemesRUBot:
    def __init__(self):
        self.api_url = API_BASE_URL
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        
        welcome_text = f"""
🎉 Добро пожаловать в ProThemesRU, {user.first_name}!

🚀 Создавайте профессиональные сайты прямо в Telegram!

📋 Доступные команды:
/start - Главное меню
/templates - Выбрать шаблон
/my_sites - Мои сайты
/help - Помощь
        """
        
        keyboard = [
            [InlineKeyboardButton("🏗️ Создать сайт", callback_data="create_site")],
            [InlineKeyboardButton("📋 Шаблоны", callback_data="templates")],
            [InlineKeyboardButton("👤 Мои сайты", callback_data="my_sites")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = """
❓ Помощь по использованию ProThemesRU Bot

🔧 Основные команды:
• /start - Главное меню
• /templates - Просмотр шаблонов
• /my_sites - Ваши сайты
• /help - Эта справка

🏗️ Создание сайта:
1. Нажмите "Создать сайт"
2. Выберите шаблон
3. Настройте параметры
4. Получите готовый сайт!

💡 Советы:
• Используйте готовые шаблоны для быстрого старта
• Все сайты адаптивны и SEO-оптимизированы
• Поддержка 24/7 в чате
        """
        
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="start")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(help_text, reply_markup=reply_markup)
    
    async def templates_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /templates"""
        await self.show_templates(update, context)
    
    async def my_sites_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /my_sites"""
        await self.show_my_sites(update, context)
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "start":
            await self.start(update, context)
        elif query.data == "create_site":
            await self.create_site_menu(update, context)
        elif query.data == "templates":
            await self.show_templates(update, context)
        elif query.data == "my_sites":
            await self.show_my_sites(update, context)
        elif query.data == "help":
            await self.help_command(update, context)
        elif query.data.startswith("template_"):
            template_id = query.data.split("_")[1]
            await self.select_template(update, context, template_id)
    
    async def show_templates(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать доступные шаблоны"""
        try:
            response = requests.get(f"{self.api_url}/api/templates")
            if response.status_code == 200:
                templates = response.json().get('templates', [])
                
                if not templates:
                    text = "📋 Шаблоны временно недоступны. Попробуйте позже."
                    keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="start")]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    await self.send_or_edit_message(update, context, text, reply_markup)
                    return
                
                text = "📋 Доступные шаблоны:\n\n"
                keyboard = []
                
                for template in templates[:5]:  # Показываем первые 5
                    text += f"🎨 {template['name']}\n"
                    text += f"   Категория: {template['category']}\n"
                    text += f"   Цена: {'Бесплатно' if template['price'] == 0 else f'${template['price']}'}\n\n"
                    
                    keyboard.append([
                        InlineKeyboardButton(
                            f"Выбрать {template['name']}", 
                            callback_data=f"template_{template['id']}"
                        )
                    ])
                
                keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="start")])
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await self.send_or_edit_message(update, context, text, reply_markup)
            else:
                await self.send_error_message(update, context, "Ошибка загрузки шаблонов")
                
        except Exception as e:
            logger.error(f"Ошибка при загрузке шаблонов: {e}")
            await self.send_error_message(update, context, "Ошибка подключения к серверу")
    
    async def create_site_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Меню создания сайта"""
        text = """
🏗️ Создание нового сайта

Выберите способ создания:

1️⃣ Шаблон - быстрый старт с готовым дизайном
2️⃣ С нуля - полная свобода творчества
3️⃣ Импорт - загрузите существующий сайт
        """
        
        keyboard = [
            [InlineKeyboardButton("📋 Выбрать шаблон", callback_data="templates")],
            [InlineKeyboardButton("🎨 Создать с нуля", callback_data="create_from_scratch")],
            [InlineKeyboardButton("📤 Импортировать", callback_data="import_site")],
            [InlineKeyboardButton("🔙 Назад", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_or_edit_message(update, context, text, reply_markup)
    
    async def select_template(self, update: Update, context: ContextTypes.DEFAULT_TYPE, template_id):
        """Выбор шаблона для создания сайта"""
        try:
            response = requests.get(f"{self.api_url}/api/templates/{template_id}")
            if response.status_code == 200:
                template = response.json().get('template', {})
                
                text = f"""
🎨 Выбран шаблон: {template['name']}

📋 Информация:
• Категория: {template['category']}
• Цена: {'Бесплатно' if template['price'] == 0 else f'${template['price']}'}
• Рейтинг: {template['rating']}/5
• Загрузок: {template['downloads']}

✅ Готовы создать сайт на основе этого шаблона?
                """
                
                keyboard = [
                    [InlineKeyboardButton("✅ Создать сайт", callback_data=f"create_from_template_{template_id}")],
                    [InlineKeyboardButton("🔙 Выбрать другой", callback_data="templates")],
                    [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await self.send_or_edit_message(update, context, text, reply_markup)
            else:
                await self.send_error_message(update, context, "Шаблон не найден")
                
        except Exception as e:
            logger.error(f"Ошибка при выборе шаблона: {e}")
            await self.send_error_message(update, context, "Ошибка загрузки шаблона")
    
    async def show_my_sites(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать сайты пользователя"""
        text = """
👤 Мои сайты

Для просмотра ваших сайтов необходимо войти в систему.

🔐 Войдите через веб-интерфейс:
https://your-real-url-here.com/login

После входа вы сможете:
• Просматривать все сайты
• Редактировать их
• Публиковать изменения
        """
        
        keyboard = [
            [InlineKeyboardButton("🌐 Открыть веб-интерфейс", url="https://your-real-url-here.com")],
            [InlineKeyboardButton("🔙 Назад", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_or_edit_message(update, context, text, reply_markup)
    
    async def send_or_edit_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, reply_markup=None):
        """Отправить или отредактировать сообщение"""
        query = update.callback_query
        if query:
            await query.edit_message_text(text=text, reply_markup=reply_markup)
        else:
            await update.message.reply_text(text=text, reply_markup=reply_markup)
    
    async def send_error_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE, error_text: str):
        """Отправить сообщение об ошибке"""
        text = f"❌ {error_text}\n\nПопробуйте позже или обратитесь в поддержку."
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="start")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_or_edit_message(update, context, text, reply_markup)

def main():
    """Запуск бота"""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN не установлен!")
        return
    
    # Создание приложения
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Создание экземпляра бота
    bot = ProThemesRUBot()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("templates", bot.templates_command))
    application.add_handler(CommandHandler("my_sites", bot.my_sites_command))
    
    # Обработчик кнопок
    application.add_handler(CallbackQueryHandler(bot.button_handler))
    
    # Запуск бота
    logger.info("Запуск ProThemesRU Telegram бота...")
    application.run_polling()

if __name__ == '__main__':
    main() 