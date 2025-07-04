import os
import logging
from typing import Dict, List, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
    ConversationHandler,
)
from dotenv import load_dotenv
import requests
from datetime import datetime

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния диалога
SELECTING_ACTION, TEMPLATES, CUSTOMIZATION, ORDER = range(4)

# Кнопки клавиатуры
MAIN_MENU = [
    [
        InlineKeyboardButton("📚 Шаблоны", callback_data='templates'),
        InlineKeyboardButton("🎨 Конструктор", callback_data='customization'),
    ],
    [
        InlineKeyboardButton("📦 Заказать", callback_data='order'),
        InlineKeyboardButton("❓ Помощь", callback_data='help'),
    ],
]

# API конфигурация
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Начало диалога"""
    user = update.effective_user
    logger.info(f"Пользователь {user.first_name} начал диалог")
    
    reply_markup = InlineKeyboardMarkup(MAIN_MENU)
    await update.message.reply_text(
        f"Привет, {user.first_name}! 🌟\n"
        "Я помогу вам создать профессиональный сайт.\n"
        "Выберите действие:",
        reply_markup=reply_markup
    )
    return SELECTING_ACTION

async def show_templates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать доступные шаблоны"""
    query = update.callback_query
    await query.answer()
    
    try:
        response = requests.get(f'{API_BASE_URL}/api/templates')
        templates = response.json()['templates']
        
        for template in templates[:5]:  # Показываем первые 5 шаблонов
            keyboard = [
                [
                    InlineKeyboardButton("Изучить", callback_data=f'template_{template.id}'),
                    InlineKeyboardButton("Выбрать", callback_data=f'select_{template.id}'),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.message.reply_photo(
                photo=template.preview_image,
                caption=f"{template.name}\n"
                       f"Категория: {template.category}\n"
                       f"Особенности: {', '.join(template.features)}",
                reply_markup=reply_markup
            )
    except Exception as e:
        logger.error(f"Ошибка при получении шаблонов: {e}")
        await query.message.reply_text("Произошла ошибка при загрузке шаблонов")
    
    return TEMPLATES

async def customize_template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Конструктор сайта"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("Добавить блок", callback_data='add_block'),
            InlineKeyboardButton("Изменить цвета", callback_data='change_colors'),
        ],
        [
            InlineKeyboardButton("Добавить анимацию", callback_data='add_animation'),
            InlineKeyboardButton("Настроить шрифты", callback_data='set_fonts'),
        ],
        [
            InlineKeyboardButton("Предпросмотр", callback_data='preview'),
            InlineKeyboardButton("В главное меню", callback_data='back'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "Выберите действие для конструирования сайта:",
        reply_markup=reply_markup
    )
    return CUSTOMIZATION

async def order_website(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Заказ сайта"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("Базовый", callback_data='basic'),
            InlineKeyboardButton("Профессиональный", callback_data='pro'),
        ],
        [
            InlineKeyboardButton("Премиум", callback_data='premium'),
            InlineKeyboardButton("В главное меню", callback_data='back'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "Выберите тарифный план:",
        reply_markup=reply_markup
    )
    return ORDER

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Помощь"""
    await update.message.reply_text(
        "Доступные команды:\n"
        "/start - Начать диалог\n"
        "/help - Показать это сообщение\n"
        "\n"
        "Для создания сайта:\n"
        "1. Выберите шаблон\n"
        "2. Настройте его под свои нужды\n"
        "3. Закажите разработку"
    )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error(msg="Ошибка:", exc_info=context.error)
    
    if isinstance(update, Update):
        await update.effective_message.reply_text(
            "Произошла ошибка. Пожалуйста, попробуйте снова."
        )

def main() -> None:
    """Запуск бота"""
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Добавляем обработчики
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECTING_ACTION: [
                CallbackQueryHandler(show_templates, pattern='^templates$'),
                CallbackQueryHandler(customize_template, pattern='^customization$'),
                CallbackQueryHandler(order_website, pattern='^order$'),
                CallbackQueryHandler(help_command, pattern='^help$'),
            ],
            TEMPLATES: [
                CallbackQueryHandler(show_templates, pattern='^templates$'),
                CallbackQueryHandler(start, pattern='^back$'),
            ],
            CUSTOMIZATION: [
                CallbackQueryHandler(customize_template, pattern='^customization$'),
                CallbackQueryHandler(start, pattern='^back$'),
            ],
            ORDER: [
                CallbackQueryHandler(order_website, pattern='^order$'),
                CallbackQueryHandler(start, pattern='^back$'),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)
    
    # Запуск бота
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()