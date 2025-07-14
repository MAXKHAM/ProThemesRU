#!/usr/bin/env python3
"""
ProThemesRU - Финальная версия Telegram бота
Полнофункциональный бот для создания сайтов
"""

import os
import json
import requests
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Конфигурация
BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')
API_BASE_URL = os.environ.get('API_BASE_URL', 'https://your-site.vercel.app')

# Имитация базы данных пользователей
users_db = {}
projects_db = {}

class ProThemesRUBot:
    def __init__(self):
        self.application = Application.builder().token(BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("templates", self.templates_command))
        self.application.add_handler(CommandHandler("create", self.create_command))
        self.application.add_handler(CommandHandler("profile", self.profile_command))
        self.application.add_handler(CommandHandler("projects", self.projects_command))
        self.application.add_handler(CommandHandler("support", self.support_command))
        
        # Обработчики для inline кнопок
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Обработчик текстовых сообщений
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Сохраняем пользователя
        users_db[chat_id] = {
            'id': chat_id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'joined_at': datetime.now().isoformat(),
            'projects': []
        }
        
        welcome_text = f"""
🎉 Добро пожаловать в ProThemesRU, {user.first_name}!

🚀 Создавайте профессиональные сайты легко и быстро!

✨ Что вы можете делать:
• Выбирать из 25+ премиум шаблонов
• Создавать сайты через визуальный конструктор
• Получать готовый код для размещения
• Использовать реферальную программу

📋 Доступные команды:
/start - Главное меню
/help - Справка
/templates - Просмотр шаблонов
/create - Создать новый сайт
/profile - Ваш профиль
/projects - Ваши проекты
/support - Поддержка

🎯 Начните с просмотра шаблонов: /templates
        """
        
        keyboard = [
            [InlineKeyboardButton("📋 Шаблоны", callback_data="templates")],
            [InlineKeyboardButton("🚀 Создать сайт", callback_data="create")],
            [InlineKeyboardButton("👤 Профиль", callback_data="profile")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /help"""
        help_text = """
📚 Справка по ProThemesRU

🔧 Основные команды:
/start - Главное меню
/help - Эта справка
/templates - Просмотр доступных шаблонов
/create - Создать новый сайт
/profile - Ваш профиль и настройки
/projects - Список ваших проектов
/support - Связаться с поддержкой

🎨 Шаблоны:
• Gaming - для игровых сайтов
• Business - для бизнеса
• Portfolio - для портфолио
• E-commerce - для интернет-магазинов
• Blog - для блогов

💰 Реферальная программа:
• Приглашайте друзей
• Получайте комиссию 10% от первого заказа
• Минимальная сумма вывода: 1000₽

📞 Поддержка:
• Email: support@prothemesru.com
• Telegram: @ProThemesRU_Support
• Время работы: 24/7

🌐 Сайт: https://prothemesru.vercel.app
        """
        
        keyboard = [
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")],
            [InlineKeyboardButton("📞 Поддержка", callback_data="support")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(help_text, reply_markup=reply_markup)
    
    async def templates_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /templates"""
        await self.show_templates(update, context)
    
    async def show_templates(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать доступные шаблоны"""
        templates = {
            '01': {'name': 'Gaming Template', 'price': 5000, 'category': 'gaming', 'description': 'Современный дизайн для игровых сайтов'},
            '02': {'name': 'Business Template', 'price': 3000, 'category': 'business', 'description': 'Профессиональный дизайн для бизнеса'},
            '03': {'name': 'Portfolio Template', 'price': 4000, 'category': 'portfolio', 'description': 'Стильное портфолио для творческих людей'},
            '04': {'name': 'E-commerce Template', 'price': 6000, 'category': 'ecommerce', 'description': 'Полнофункциональный интернет-магазин'},
            '05': {'name': 'Blog Template', 'price': 2500, 'category': 'blog', 'description': 'Красивый блог для контент-мейкеров'}
        }
        
        text = "🎨 Доступные шаблоны:\n\n"
        
        keyboard = []
        for template_id, template in templates.items():
            text += f"📋 {template['name']}\n"
            text += f"💰 Цена: {template['price']}₽\n"
            text += f"📝 {template['description']}\n\n"
            
            keyboard.append([InlineKeyboardButton(
                f"Выбрать {template['name']}", 
                callback_data=f"select_template_{template_id}"
            )])
        
        keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
        else:
            await update.message.reply_text(text, reply_markup=reply_markup)
    
    async def create_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /create"""
        text = """
🚀 Создание нового сайта

Выберите один из способов:

1️⃣ Шаблонный сайт - быстрый старт с готовым дизайном
2️⃣ Конструктор - создание с нуля через визуальный редактор
3️⃣ Кастомный заказ - индивидуальная разработка

Какой вариант вам подходит?
        """
        
        keyboard = [
            [InlineKeyboardButton("📋 Шаблонный сайт", callback_data="create_template")],
            [InlineKeyboardButton("🔧 Конструктор", callback_data="create_constructor")],
            [InlineKeyboardButton("🎨 Кастомный заказ", callback_data="create_custom")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup)
    
    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /profile"""
        chat_id = update.effective_chat.id
        user = users_db.get(chat_id, {})
        
        if not user:
            await update.message.reply_text("❌ Профиль не найден. Используйте /start для регистрации.")
            return
        
        text = f"""
👤 Ваш профиль

📝 Имя: {user.get('first_name', 'Не указано')}
🆔 ID: {chat_id}
📅 Дата регистрации: {user.get('joined_at', 'Не указано')}
📊 Проектов создано: {len(user.get('projects', []))}

💰 Реферальная программа:
🔗 Ваша ссылка: https://t.me/ProThemesRUBot?start=ref_{chat_id}
👥 Приглашено: 0 человек
💵 Заработано: 0₽

🎯 Статистика:
• Создано сайтов: {len(user.get('projects', []))}
• Активных проектов: {len([p for p in user.get('projects', []) if p.get('status') == 'active'])}
        """
        
        keyboard = [
            [InlineKeyboardButton("📊 Статистика", callback_data="statistics")],
            [InlineKeyboardButton("💰 Рефералы", callback_data="referrals")],
            [InlineKeyboardButton("⚙️ Настройки", callback_data="settings")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup)
    
    async def projects_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /projects"""
        chat_id = update.effective_chat.id
        user = users_db.get(chat_id, {})
        
        if not user:
            await update.message.reply_text("❌ Профиль не найден. Используйте /start для регистрации.")
            return
        
        projects = user.get('projects', [])
        
        if not projects:
            text = "📋 У вас пока нет проектов.\n\nСоздайте первый сайт: /create"
            keyboard = [[InlineKeyboardButton("🚀 Создать сайт", callback_data="create")]]
        else:
            text = f"📋 Ваши проекты ({len(projects)}):\n\n"
            
            keyboard = []
            for i, project in enumerate(projects[:5], 1):  # Показываем первые 5
                text += f"{i}. {project.get('name', 'Без названия')}\n"
                text += f"   Статус: {project.get('status', 'Неизвестно')}\n"
                text += f"   Создан: {project.get('created_at', 'Не указано')}\n\n"
                
                keyboard.append([InlineKeyboardButton(
                    f"Открыть {project.get('name', 'Проект')}", 
                    callback_data=f"open_project_{project.get('id', i)}"
                )])
        
        keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="start")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup)
    
    async def support_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /support"""
        text = """
📞 Поддержка ProThemesRU

🆘 Если у вас возникли вопросы или проблемы:

📧 Email: support@prothemesru.com
💬 Telegram: @ProThemesRU_Support
🌐 Сайт: https://prothemesru.vercel.app

⏰ Время работы: 24/7

📋 Часто задаваемые вопросы:
• Как создать сайт? - Используйте /create
• Как выбрать шаблон? - Используйте /templates
• Как работает реферальная программа? - Используйте /help

🔧 Техническая поддержка:
• Проблемы с ботом
• Ошибки в конструкторе
• Вопросы по оплате
• Настройка домена
        """
        
        keyboard = [
            [InlineKeyboardButton("📧 Написать в поддержку", url="https://t.me/ProThemesRU_Support")],
            [InlineKeyboardButton("🌐 Открыть сайт", url="https://prothemesru.vercel.app")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text, reply_markup=reply_markup)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка нажатий на inline кнопки"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "start":
            await self.start_command(update, context)
        elif data == "help":
            await self.help_command(update, context)
        elif data == "templates":
            await self.show_templates(update, context)
        elif data == "create":
            await self.create_command(update, context)
        elif data == "profile":
            await self.profile_command(update, context)
        elif data == "support":
            await self.support_command(update, context)
        elif data.startswith("select_template_"):
            template_id = data.split("_")[-1]
            await self.select_template(update, context, template_id)
        elif data == "create_template":
            await self.create_template_site(update, context)
        elif data == "create_constructor":
            await self.create_constructor_site(update, context)
        elif data == "create_custom":
            await self.create_custom_site(update, context)
    
    async def select_template(self, update: Update, context: ContextTypes.DEFAULT_TYPE, template_id: str):
        """Выбор шаблона"""
        templates = {
            '01': {'name': 'Gaming Template', 'price': 5000},
            '02': {'name': 'Business Template', 'price': 3000},
            '03': {'name': 'Portfolio Template', 'price': 4000},
            '04': {'name': 'E-commerce Template', 'price': 6000},
            '05': {'name': 'Blog Template', 'price': 2500}
        }
        
        template = templates.get(template_id)
        if not template:
            await update.callback_query.edit_message_text("❌ Шаблон не найден")
            return
        
        text = f"""
🎨 Выбран шаблон: {template['name']}

💰 Стоимость: {template['price']}₽

📋 Что включено:
• Готовый HTML/CSS код
• Адаптивный дизайн
• SEO оптимизация
• Инструкция по установке
• 30 дней поддержки

🚀 Хотите создать сайт с этим шаблоном?
        """
        
        keyboard = [
            [InlineKeyboardButton("✅ Создать сайт", callback_data=f"buy_template_{template_id}")],
            [InlineKeyboardButton("👀 Предпросмотр", callback_data=f"preview_template_{template_id}")],
            [InlineKeyboardButton("📋 Другие шаблоны", callback_data="templates")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    
    async def create_template_site(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Создание сайта на основе шаблона"""
        text = """
📋 Создание шаблонного сайта

Выберите категорию шаблона:

🎮 Gaming - для игровых сайтов
💼 Business - для бизнеса
🎨 Portfolio - для портфолио
🛒 E-commerce - для магазинов
📝 Blog - для блогов
        """
        
        keyboard = [
            [InlineKeyboardButton("🎮 Gaming", callback_data="category_gaming")],
            [InlineKeyboardButton("💼 Business", callback_data="category_business")],
            [InlineKeyboardButton("🎨 Portfolio", callback_data="category_portfolio")],
            [InlineKeyboardButton("🛒 E-commerce", callback_data="category_ecommerce")],
            [InlineKeyboardButton("📝 Blog", callback_data="category_blog")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    
    async def create_constructor_site(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Создание сайта через конструктор"""
        text = """
🔧 Конструктор сайтов

Создайте сайт с нуля через визуальный редактор!

✨ Возможности:
• Drag-and-drop интерфейс
• Готовые блоки и компоненты
• Настройка цветов и шрифтов
• Добавление изображений
• SEO настройки

🌐 Откройте конструктор на сайте:
        """
        
        keyboard = [
            [InlineKeyboardButton("🌐 Открыть конструктор", url="https://prothemesru.vercel.app/constructor")],
            [InlineKeyboardButton("📖 Инструкция", url="https://prothemesru.vercel.app/help")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    
    async def create_custom_site(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Создание кастомного сайта"""
        text = """
🎨 Кастомная разработка

Создадим сайт специально для вас!

📋 Что включено:
• Индивидуальный дизайн
• Полная разработка
• Настройка под ваши нужды
• Техническая поддержка
• Обучение работе с сайтом

💰 Стоимость: от 15000₽

📞 Свяжитесь с нами для обсуждения проекта:
        """
        
        keyboard = [
            [InlineKeyboardButton("📞 Связаться", url="https://t.me/ProThemesRU_Support")],
            [InlineKeyboardButton("📧 Email", url="mailto:support@prothemesru.com")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений"""
        text = update.message.text
        chat_id = update.effective_chat.id
        
        # Простая обработка текста
        if "привет" in text.lower():
            await update.message.reply_text("Привет! 👋 Используйте /start для начала работы с ботом.")
        elif "спасибо" in text.lower():
            await update.message.reply_text("Пожалуйста! 😊 Если нужна помощь, используйте /help")
        elif "сайт" in text.lower():
            await update.message.reply_text("🌐 Наш сайт: https://prothemesru.vercel.app\n\nСоздавайте сайты легко и быстро!")
        else:
            await update.message.reply_text(
                "Не понимаю команду. Используйте /help для просмотра доступных команд."
            )
    
    def run(self):
        """Запуск бота"""
        print("🤖 ProThemesRU Bot запускается...")
        print(f"🔗 Webhook URL: {WEBHOOK_URL}")
        print("✅ Бот готов к работе!")
        
        # Запуск бота
        self.application.run_polling()

def main():
    """Главная функция"""
    if not BOT_TOKEN:
        print("❌ ОШИБКА: BOT_TOKEN не установлен!")
        return
    
    bot = ProThemesRUBot()
    bot.run()

if __name__ == '__main__':
    main() 