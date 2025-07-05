#!/usr/bin/env python3
"""
Улучшенный Telegram Bot ProThemesRU с расширенной библиотекой шаблонов и блоков
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
SELECTING_ACTION, TEMPLATES, CUSTOMIZATION, ORDER, PAYMENT, FEEDBACK, BLOCKS, STYLES = range(8)

# Кнопки главного меню
MAIN_MENU = [
    [
        InlineKeyboardButton("📚 Шаблоны", callback_data='templates'),
        InlineKeyboardButton("🧱 Блоки", callback_data='blocks'),
    ],
    [
        InlineKeyboardButton("🎨 Стили", callback_data='styles'),
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

class EnhancedTemplateManager:
    """Расширенный менеджер шаблонов"""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.categories = self._get_categories()
    
    def _load_templates(self) -> List[Dict]:
        """Загрузка шаблонов из расширенного файла"""
        try:
            with open('../templates/blocks/enhanced_templates.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('templates', [])
        except FileNotFoundError:
            logger.warning("Файл шаблонов не найден, используем демо-данные")
            return self._get_demo_templates()
    
    def _get_categories(self) -> Dict:
        """Получение категорий шаблонов"""
        try:
            with open('../templates/blocks/enhanced_templates.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('categories', {})
        except FileNotFoundError:
            return {}
    
    def _get_demo_templates(self) -> List[Dict]:
        """Демо-шаблоны"""
        return [
            {
                "id": 1,
                "name": "Современный бизнес-лендинг",
                "category": "business",
                "price": 5000,
                "currency": "₽",
                "features": ["Адаптивный дизайн", "SEO-оптимизация", "Формы обратной связи"],
                "description": "Современный лендинг для бизнеса",
                "preview_image": "https://via.placeholder.com/400x300/4A90E2/FFFFFF?text=Бизнес-лендинг",
                "tags": ["бизнес", "лендинг", "адаптивный"]
            }
        ]
    
    def get_templates(self, category: str = None) -> List[Dict]:
        """Получение шаблонов с фильтрацией по категории"""
        if category:
            return [t for t in self.templates if t.get('category') == category]
        return self.templates
    
    def get_template_by_id(self, template_id: int) -> Optional[Dict]:
        return next((t for t in self.templates if t["id"] == template_id), None)
    
    def get_categories(self) -> Dict:
        return self.categories

class BlocksManager:
    """Менеджер UI блоков"""
    
    def __init__(self):
        self.blocks = self._load_blocks()
    
    def _load_blocks(self) -> Dict:
        """Загрузка UI блоков"""
        try:
            with open('../templates/blocks/ui_components.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Файл блоков не найден")
            return {}
    
    def get_components(self, category: str = None) -> Dict:
        """Получение компонентов"""
        if category:
            return self.blocks.get('components', {}).get(category, {})
        return self.blocks.get('components', {})
    
    def get_animations(self) -> Dict:
        return self.blocks.get('animations', {})
    
    def get_color_schemes(self) -> Dict:
        return self.blocks.get('color_schemes', {})
    
    def get_typography(self) -> Dict:
        return self.blocks.get('typography', {})

class StylesManager:
    """Менеджер стилей"""
    
    def __init__(self):
        self.styles = self._load_styles()
    
    def _load_styles(self) -> Dict:
        """Загрузка стилей"""
        try:
            with open('../templates/blocks/styles_library.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning("Файл стилей не найден")
            return {}
    
    def get_gradients(self) -> Dict:
        return self.styles.get('gradients', {})
    
    def get_shadows(self) -> Dict:
        return self.styles.get('shadows', {})
    
    def get_effects(self) -> Dict:
        return self.styles.get('effects', {})
    
    def get_predefined_styles(self) -> Dict:
        return self.styles.get('predefined_styles', {})

# Инициализация менеджеров
template_manager = EnhancedTemplateManager()
blocks_manager = BlocksManager()
styles_manager = StylesManager()

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
    
    # Создаем кнопки для категорий
    categories = template_manager.get_categories()
    keyboard = []
    
    for cat_id, cat_info in categories.items():
        keyboard.append([InlineKeyboardButton(
            f"{cat_info.get('icon', '📁')} {cat_info.get('name', cat_id)}", 
            callback_data=f'category_{cat_id}'
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 В главное меню", callback_data='back_to_main')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "📚 <b>Выберите категорию шаблонов:</b>\n\n"
        "У нас есть шаблоны для различных типов сайтов:",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return TEMPLATES

async def show_category_templates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать шаблоны конкретной категории"""
    query = update.callback_query
    await query.answer()
    
    category = query.data.split('_')[1]
    templates = template_manager.get_templates(category)
    
    if not templates:
        await query.message.reply_text("❌ Шаблоны в этой категории не найдены")
        return TEMPLATES
    
    # Показываем первые 3 шаблона
    for template in templates[:3]:
        keyboard = [
            [
                InlineKeyboardButton("👁️ Просмотр", callback_data=f'view_{template["id"]}'),
                InlineKeyboardButton("✅ Выбрать", callback_data=f'select_{template["id"]}'),
            ],
            [
                InlineKeyboardButton(f"💰 {template['price']}{template['currency']}", callback_data=f'price_{template["id"]}'),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        caption = (
            f"🎨 <b>{template['name']}</b>\n"
            f"📂 Категория: {template.get('category', 'Не указана')}\n"
            f"✨ Особенности: {', '.join(template['features'][:3])}\n"
            f"💵 Цена: {template['price']}{template['currency']}\n\n"
            f"📝 {template['description']}"
        )
        
        await query.message.reply_photo(
            photo=template["preview_image"],
            caption=caption,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    
    keyboard = [[InlineKeyboardButton("🔙 Назад к категориям", callback_data='templates')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "Показаны первые 3 шаблона из категории. Выберите подходящий!",
        reply_markup=reply_markup
    )
    
    return TEMPLATES

async def show_blocks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать UI блоки"""
    query = update.callback_query
    await query.answer()
    
    components = blocks_manager.get_components()
    keyboard = []
    
    for component_type in components.keys():
        keyboard.append([InlineKeyboardButton(
            f"🧱 {component_type.title()}", 
            callback_data=f'blocks_{component_type}'
        )])
    
    keyboard.append([InlineKeyboardButton("🔙 В главное меню", callback_data='back_to_main')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "🧱 <b>UI Блоки и компоненты</b>\n\n"
        "Выберите тип компонентов для просмотра:",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return BLOCKS

async def show_block_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать блоки конкретной категории"""
    query = update.callback_query
    await query.answer()
    
    category = query.data.split('_')[1]
    components = blocks_manager.get_components(category)
    
    if not components:
        await query.message.reply_text("❌ Компоненты не найдены")
        return BLOCKS
    
    message_text = f"🧱 <b>{category.title()}</b>\n\n"
    
    for comp_id, comp_info in components.items():
        message_text += f"<b>{comp_info.get('name', comp_id)}</b>\n"
        message_text += f"HTML: <code>{comp_info.get('html', 'Не указан')}</code>\n\n"
    
    keyboard = [[InlineKeyboardButton("🔙 Назад к блокам", callback_data='blocks')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    
    return BLOCKS

async def show_styles(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать стили и эффекты"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🌈 Градиенты", callback_data='styles_gradients')],
        [InlineKeyboardButton("🌫️ Тени", callback_data='styles_shadows')],
        [InlineKeyboardButton("✨ Эффекты", callback_data='styles_effects')],
        [InlineKeyboardButton("🎨 Готовые стили", callback_data='styles_predefined')],
        [InlineKeyboardButton("🔙 В главное меню", callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "🎨 <b>Стили и эффекты</b>\n\n"
        "Выберите тип стилей для просмотра:",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return STYLES

async def show_style_category(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать стили конкретной категории"""
    query = update.callback_query
    await query.answer()
    
    category = query.data.split('_')[1]
    
    if category == 'gradients':
        styles = styles_manager.get_gradients()
        icon = "🌈"
    elif category == 'shadows':
        styles = styles_manager.get_shadows()
        icon = "🌫️"
    elif category == 'effects':
        styles = styles_manager.get_effects()
        icon = "✨"
    elif category == 'predefined':
        styles = styles_manager.get_predefined_styles()
        icon = "🎨"
    else:
        styles = {}
        icon = "📁"
    
    if not styles:
        await query.message.reply_text("❌ Стили не найдены")
        return STYLES
    
    message_text = f"{icon} <b>{category.title()}</b>\n\n"
    
    for style_id, style_info in styles.items():
        message_text += f"<b>{style_info.get('name', style_id)}</b>\n"
        message_text += f"CSS: <code>{style_info.get('css', 'Не указан')}</code>\n\n"
    
    keyboard = [[InlineKeyboardButton("🔙 Назад к стилям", callback_data='styles')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        message_text,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    
    return STYLES

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

def main() -> None:
    """Запуск бота"""
    if not TELEGRAM_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN не установлен!")
        return
    
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Добавляем обработчики
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_ACTION: [
                CallbackQueryHandler(show_templates, pattern='^templates$'),
                CallbackQueryHandler(show_blocks, pattern='^blocks$'),
                CallbackQueryHandler(show_styles, pattern='^styles$'),
                CallbackQueryHandler(back_to_main, pattern='^back_to_main$'),
            ],
            TEMPLATES: [
                CallbackQueryHandler(show_category_templates, pattern='^category_'),
                CallbackQueryHandler(show_templates, pattern='^templates$'),
                CallbackQueryHandler(back_to_main, pattern='^back_to_main$'),
            ],
            BLOCKS: [
                CallbackQueryHandler(show_block_category, pattern='^blocks_'),
                CallbackQueryHandler(show_blocks, pattern='^blocks$'),
                CallbackQueryHandler(back_to_main, pattern='^back_to_main$'),
            ],
            STYLES: [
                CallbackQueryHandler(show_style_category, pattern='^styles_'),
                CallbackQueryHandler(show_styles, pattern='^styles$'),
                CallbackQueryHandler(back_to_main, pattern='^back_to_main$'),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)
    
    # Запуск бота
    logger.info("Запуск улучшенного телеграм бота...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 