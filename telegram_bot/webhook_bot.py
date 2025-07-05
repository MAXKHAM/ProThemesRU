#!/usr/bin/env python3
"""
Telegram Bot с поддержкой веб-хуков для деплоя на GitHub
"""

import os
import logging
import json
import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaDocument
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)
from telegram.constants import ParseMode
from dotenv import load_dotenv
import requests
import aiohttp
from PIL import Image
import io
from flask import Flask, request, jsonify

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('telegram_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Состояния диалога
SELECTING_ACTION, TEMPLATES, CUSTOMIZATION, ORDER, PAYMENT, FEEDBACK = range(6)

# Кнопки главного меню
MAIN_MENU = [
    [
        InlineKeyboardButton("📚 Шаблоны", callback_data='templates'),
        InlineKeyboardButton("🎨 Конструктор", callback_data='customization'),
    ],
    [
        InlineKeyboardButton("📦 Заказать", callback_data='order'),
        InlineKeyboardButton("💰 Цены", callback_data='pricing'),
    ],
    [
        InlineKeyboardButton("❓ Помощь", callback_data='help'),
        InlineKeyboardButton("📞 Контакты", callback_data='contacts'),
    ],
]

# API конфигурация
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
PORT = int(os.getenv('PORT', 8080))

# Хранилище данных пользователей (в продакшене использовать Redis/DB)
user_data = {}

class TemplateManager:
    """Менеджер для работы с шаблонами"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self) -> List[Dict]:
        """Загрузка шаблонов из локального файла"""
        try:
            with open('../design_templates.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Файл шаблонов не найден, используем демо-данные")
            return self._get_demo_templates()
    
    def _get_demo_templates(self) -> List[Dict]:
        """Демо-шаблоны"""
        return [
            {
                "id": 1,
                "name": "Бизнес-лендинг",
                "category": "Бизнес",
                "features": ["Адаптивный дизайн", "SEO-оптимизация", "Формы обратной связи"],
                "preview_image": "https://via.placeholder.com/300x200/4A90E2/FFFFFF?text=Бизнес-лендинг",
                "price": "5000₽",
                "description": "Современный лендинг для бизнеса"
            },
            {
                "id": 2,
                "name": "Портфолио",
                "category": "Портфолио",
                "features": ["Галерея работ", "Анимации", "Контактная форма"],
                "preview_image": "https://via.placeholder.com/300x200/50C878/FFFFFF?text=Портфолио",
                "price": "4000₽",
                "description": "Стильное портфолио для творческих людей"
            },
            {
                "id": 3,
                "name": "Интернет-магазин",
                "category": "E-commerce",
                "features": ["Каталог товаров", "Корзина", "Онлайн-оплата"],
                "preview_image": "https://via.placeholder.com/300x200/FF6B6B/FFFFFF?text=Магазин",
                "price": "8000₽",
                "description": "Полнофункциональный интернет-магазин"
            }
        ]
    
    def get_templates(self) -> List[Dict]:
        return self.templates
    
    def get_template_by_id(self, template_id: int) -> Optional[Dict]:
        return next((t for t in self.templates if t["id"] == template_id), None)

template_manager = TemplateManager()

class UserManager:
    """Менеджер пользователей"""
    
    def __init__(self):
        self.users = {}
    
    def add_user(self, user_id: int, user_data: Dict):
        self.users[user_id] = {
            "id": user_id,
            "created_at": datetime.now(),
            "last_activity": datetime.now(),
            "selected_template": None,
            "customization_data": {},
            "orders": [],
            **user_data
        }
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        return self.users.get(user_id)
    
    def update_user(self, user_id: int, data: Dict):
        if user_id in self.users:
            self.users[user_id].update(data)
            self.users[user_id]["last_activity"] = datetime.now()
    
    def get_user_stats(self) -> Dict:
        total_users = len(self.users)
        active_users = len([u for u in self.users.values() 
                          if (datetime.now() - u["last_activity"]).days < 7])
        return {"total": total_users, "active": active_users}

user_manager = UserManager()

# Flask приложение для веб-хуков
app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "bot": "ProThemesRU Telegram Bot",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработка веб-хуков от Telegram"""
    if request.method == 'POST':
        update = Update.de_json(request.get_json(), application.bot)
        application.process_update(update)
        return jsonify({"status": "ok"})

@app.route('/health')
def health():
    """Проверка здоровья приложения"""
    return jsonify({
        "status": "healthy",
        "users": user_manager.get_user_stats(),
        "templates": len(template_manager.get_templates())
    })

# Функции бота (те же, что и в bot.py)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало диалога"""
    user = update.effective_user
    
    # Регистрируем пользователя
    user_manager.add_user(user.id, {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username
    })
    
    logger.info(f"Пользователь {user.first_name} (ID: {user.id}) начал диалог")
    
    reply_markup = InlineKeyboardMarkup(MAIN_MENU)
    await update.message.reply_text(
        f"Привет, {user.first_name}! 🌟\n\n"
        "Я помогу вам создать профессиональный сайт.\n"
        "Выберите действие:",
        reply_markup=reply_markup
    )
    return SELECTING_ACTION

async def show_templates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать доступные шаблоны"""
    query = update.callback_query
    await query.answer()
    
    templates = template_manager.get_templates()
    
    if not templates:
        await query.message.reply_text("❌ Произошла ошибка при загрузке шаблонов")
        return SELECTING_ACTION
    
    # Показываем первые 3 шаблона
    for template in templates[:3]:
        keyboard = [
            [
                InlineKeyboardButton("👁️ Просмотр", callback_data=f'view_{template["id"]}'),
                InlineKeyboardButton("✅ Выбрать", callback_data=f'select_{template["id"]}'),
            ],
            [
                InlineKeyboardButton("💰 Цена: " + template["price"], callback_data=f'price_{template["id"]}'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        caption = (
            f"🎨 <b>{template['name']}</b>\n"
            f"📂 Категория: {template['category']}\n"
            f"✨ Особенности: {', '.join(template['features'])}\n"
            f"💵 Цена: {template['price']}\n\n"
            f"📝 {template['description']}"
        )
        
        await query.message.reply_photo(
            photo=template["preview_image"],
            caption=caption,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    
    keyboard = [[InlineKeyboardButton("🔙 В главное меню", callback_data='back_to_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "Это все доступные шаблоны. Выберите подходящий!",
        reply_markup=reply_markup
    )
    
    return TEMPLATES

async def back_to_main(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Возврат в главное меню"""
    query = update.callback_query
    await query.answer()
    
    reply_markup = InlineKeyboardMarkup(MAIN_MENU)
    await query.message.reply_text(
        "🏠 <b>Главное меню</b>\n\n"
        "Выберите действие:",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return SELECTING_ACTION

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(msg="Ошибка:", exc_info=context.error)
    
    if isinstance(update, Update):
        await update.effective_message.reply_text(
            "❌ Произошла ошибка. Пожалуйста, попробуйте снова или обратитесь в поддержку."
        )

async def send_admin_notification(message: str):
    """Отправка уведомления администратору"""
    if ADMIN_CHAT_ID:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                    json={
                        "chat_id": ADMIN_CHAT_ID,
                        "text": f"🔔 {message}",
                        "parse_mode": "HTML"
                    }
                ) as response:
                    if response.status != 200:
                        logger.error(f"Ошибка отправки уведомления админу: {response.status}")
        except Exception as e:
            logger.error(f"Ошибка отправки уведомления админу: {e}")

def setup_bot():
    """Настройка бота"""
    global application
    
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN не установлен!")
        return None
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Добавляем обработчики
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_ACTION: [
                CallbackQueryHandler(show_templates, pattern='^templates$'),
                CallbackQueryHandler(back_to_main, pattern='^back_to_main$'),
            ],
            TEMPLATES: [
                CallbackQueryHandler(show_templates, pattern='^templates$'),
                CallbackQueryHandler(back_to_main, pattern='^back_to_main$'),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)
    
    return application

def main():
    """Запуск бота с веб-хуками"""
    print("🤖 Запуск телеграм бота ProThemesRU с веб-хуками...")
    
    # Настройка бота
    bot_app = setup_bot()
    if not bot_app:
        return
    
    # Настройка веб-хука
    if WEBHOOK_URL:
        bot_app.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
        print(f"✅ Веб-хук установлен: {WEBHOOK_URL}/webhook")
    
    # Запуск Flask приложения
    print(f"🌐 Запуск веб-сервера на порту {PORT}")
    app.run(host='0.0.0.0', port=PORT, debug=False)

if __name__ == '__main__':
    main() 