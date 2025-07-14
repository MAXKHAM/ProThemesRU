#!/usr/bin/env python3
"""
ProThemesRU - Обновленная версия Telegram бота
Полнофункциональный бот для создания сайтов с поддержкой переменных окружения
"""

import os
import json
import requests
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Импортируем конфигурацию
from config import config

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, config.LOG_LEVEL),
    filename=config.LOG_FILE
)
logger = logging.getLogger(__name__)

# Имитация базы данных пользователей
users_db = {}
projects_db = {}

class ProThemesRUBot:
    def __init__(self):
        """Инициализация бота"""
        if not config.TELEGRAM_BOT_TOKEN or config.TELEGRAM_BOT_TOKEN == 'your_bot_token_here':
            raise ValueError("TELEGRAM_BOT_TOKEN не установлен! Проверьте переменные окружения.")
        
        self.application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()
        
        logger.info("ProThemesRU Bot инициализирован")
        logger.info(f"API Base URL: {config.API_BASE_URL}")
        logger.info(f"Webhook URL: {config.WEBHOOK_URL}")
        logger.info(f"Environment: {config.ENVIRONMENT}")
    
    def setup_handlers(self):
        """Настройка обработчиков команд"""
        # Основные команды
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("templates", self.templates_command))
        self.application.add_handler(CommandHandler("create", self.create_command))
        self.application.add_handler(CommandHandler("profile", self.profile_command))
        self.application.add_handler(CommandHandler("projects", self.projects_command))
        self.application.add_handler(CommandHandler("support", self.support_command))
        self.application.add_handler(CommandHandler("referral", self.referral_command))
        
        # Обработчики для inline кнопок
        self.application.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Обработчик текстовых сообщений
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        logger.info("Обработчики команд настроены")
    
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
            'projects': [],
            'referral_code': f"REF{chat_id}"
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
/referral - Реферальная программа
/support - Поддержка

🎯 Начните с просмотра шаблонов: /templates
        """
        
        keyboard = [
            [InlineKeyboardButton("📋 Шаблоны", callback_data="templates")],
            [InlineKeyboardButton("🚀 Создать сайт", callback_data="create")],
            [InlineKeyboardButton("👤 Профиль", callback_data="profile")],
            [InlineKeyboardButton("💰 Рефералы", callback_data="referral")],
            [InlineKeyboardButton("❓ Помощь", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
        logger.info(f"Пользователь {user.username} ({chat_id}) запустил бота")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /help"""
        help_text = f"""
📚 Справка по ProThemesRU

🔧 Основные команды:
/start - Главное меню
/help - Эта справка
/templates - Просмотр доступных шаблонов
/create - Создать новый сайт
/profile - Ваш профиль и настройки
/projects - Список ваших проектов
/referral - Реферальная программа
/support - Связаться с поддержкой

🎨 Шаблоны:
• Gaming - для игровых сайтов
• Business - для бизнеса
• Portfolio - для портфолио
• E-commerce - для интернет-магазинов
• Blog - для блогов

💰 Реферальная программа:
• Приглашайте друзей
• Получайте комиссию {config.REFERRAL_COMMISSION*100}% от первого заказа
• Минимальная сумма вывода: {config.MIN_WITHDRAWAL}₽

📞 Поддержка:
• Email: {config.SUPPORT_EMAIL}
• Telegram: {config.SUPPORT_TELEGRAM}
• Время работы: 24/7

🌐 Сайт: {config.WEBSITE_URL}
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
        text = "🎨 Доступные шаблоны:\n\n"
        
        keyboard = []
        for template_id, template in config.TEMPLATES.items():
            text += f"📋 {template['name']}\n"
            text += f"💰 Цена: {template['price']}₽\n"
            text += f"📝 Категория: {template['category']}\n\n"
            
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
    
    async def referral_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /referral"""
        chat_id = update.effective_chat.id
        user = users_db.get(chat_id, {})
        
        if not user:
            await update.message.reply_text("❌ Профиль не найден. Используйте /start для регистрации.")
            return
        
        referral_code = user.get('referral_code', f"REF{chat_id}")
        
        text = f"""
💰 Реферальная программа

🔗 Ваша реферальная ссылка:
https://t.me/ProThemesRUBot?start=ref_{referral_code}

📊 Статистика:
👥 Приглашено: 0 человек
💵 Заработано: 0₽
🎯 До вывода: {config.MIN_WITHDRAWAL}₽

💡 Как это работает:
1. Отправьте ссылку друзьям
2. Они регистрируются по вашей ссылке
3. Вы получаете {config.REFERRAL_COMMISSION*100}% от их первого заказа
4. Выводите заработанные деньги

📞 Вопросы? Обратитесь в поддержку: {config.SUPPORT_TELEGRAM}
        """
        
        keyboard = [
            [InlineKeyboardButton("📤 Поделиться ссылкой", switch_inline_query=f"ref_{referral_code}")],
            [InlineKeyboardButton("📊 Статистика", callback_data="referral_stats")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
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
🔗 Ваша ссылка: https://t.me/ProThemesRUBot?start=ref_{user.get('referral_code', f'REF{chat_id}')}
👥 Приглашено: 0 человек
💵 Заработано: 0₽

🎯 Статистика:
• Создано сайтов: {len(user.get('projects', []))}
• Активных проектов: {len([p for p in user.get('projects', []) if p.get('status') == 'active'])}
        """
        
        keyboard = [
            [InlineKeyboardButton("📊 Статистика", callback_data="statistics")],
            [InlineKeyboardButton("💰 Рефералы", callback_data="referral")],
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
        text = f"""
📞 Поддержка ProThemesRU

🆘 Если у вас возникли вопросы или проблемы:

📧 Email: {config.SUPPORT_EMAIL}
💬 Telegram: {config.SUPPORT_TELEGRAM}
🌐 Сайт: {config.WEBSITE_URL}

⏰ Время работы: 24/7

📋 Часто задаваемые вопросы:
• Как создать сайт? - Используйте /create
• Как выбрать шаблон? - Используйте /templates
• Как работает реферальная программа? - Используйте /referral

🔧 Техническая поддержка:
• Проблемы с ботом
• Ошибки в конструкторе
• Вопросы по оплате
• Настройка домена
        """
        
        keyboard = [
            [InlineKeyboardButton("📧 Написать в поддержку", url=f"https://t.me/{config.SUPPORT_TELEGRAM.replace('@', '')}")],
            [InlineKeyboardButton("🌐 Открыть сайт", url=config.WEBSITE_URL)],
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
        elif data == "referral":
            await self.referral_command(update, context)
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
        template = config.TEMPLATES.get(template_id)
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
        text = f"""
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
            [InlineKeyboardButton("🌐 Открыть конструктор", url=f"{config.WEBSITE_URL}/constructor")],
            [InlineKeyboardButton("📖 Инструкция", url=f"{config.WEBSITE_URL}/help")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    
    async def create_custom_site(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Создание кастомного сайта"""
        text = f"""
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
            [InlineKeyboardButton("📞 Связаться", url=f"https://t.me/{config.SUPPORT_TELEGRAM.replace('@', '')}")],
            [InlineKeyboardButton("📧 Email", url=f"mailto:{config.SUPPORT_EMAIL}")],
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
            await update.message.reply_text(f"🌐 Наш сайт: {config.WEBSITE_URL}\n\nСоздавайте сайты легко и быстро!")
        else:
            await update.message.reply_text(
                "Не понимаю команду. Используйте /help для просмотра доступных команд."
            )
    
    def run(self):
        """Запуск бота"""
        print("🤖 ProThemesRU Bot запускается...")
        print(f"🔗 API Base URL: {config.API_BASE_URL}")
        print(f"🔗 Webhook URL: {config.WEBHOOK_URL}")
        print(f"🌍 Environment: {config.ENVIRONMENT}")
        print(f"🔧 Debug: {config.DEBUG}")
        print("✅ Бот готов к работе!")
        
        # Запуск бота
        if config.ENABLE_WEBHOOK:
            print("🔗 Запуск в режиме webhook...")
            # Здесь будет код для webhook
        else:
            print("🔄 Запуск в режиме polling...")
            self.application.run_polling()

def main():
    """Главная функция"""
    try:
        bot = ProThemesRUBot()
        bot.run()
    except Exception as e:
        logger.error(f"Ошибка запуска бота: {e}")
        print(f"❌ Ошибка запуска бота: {e}")

if __name__ == '__main__':
    main() 