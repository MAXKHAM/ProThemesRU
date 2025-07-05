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
    
    # Кнопка "Показать еще"
    if len(templates) > 3:
        keyboard = [
            [InlineKeyboardButton("📄 Показать еще", callback_data='more_templates')],
            [InlineKeyboardButton("🔙 В главное меню", callback_data='back_to_main')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "Показаны первые 3 шаблона. Хотите увидеть остальные?",
            reply_markup=reply_markup
        )
    else:
        keyboard = [[InlineKeyboardButton("🔙 В главное меню", callback_data='back_to_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(
            "Это все доступные шаблоны. Выберите подходящий!",
            reply_markup=reply_markup
        )
    
    return TEMPLATES

async def view_template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Детальный просмотр шаблона"""
    query = update.callback_query
    await query.answer()
    
    template_id = int(query.data.split('_')[1])
    template = template_manager.get_template_by_id(template_id)
    
    if not template:
        await query.message.reply_text("❌ Шаблон не найден")
        return TEMPLATES
    
    keyboard = [
        [
            InlineKeyboardButton("✅ Выбрать этот шаблон", callback_data=f'select_{template_id}'),
            InlineKeyboardButton("💰 Заказать", callback_data=f'order_{template_id}'),
        ],
        [
            InlineKeyboardButton("🔙 Назад к шаблонам", callback_data='templates'),
            InlineKeyboardButton("🏠 В главное меню", callback_data='back_to_main'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    detailed_caption = (
        f"🎨 <b>{template['name']}</b>\n\n"
        f"📂 <b>Категория:</b> {template['category']}\n"
        f"💵 <b>Цена:</b> {template['price']}\n\n"
        f"✨ <b>Особенности:</b>\n"
        f"{chr(10).join(['• ' + feature for feature in template['features']])}\n\n"
        f"📝 <b>Описание:</b>\n{template['description']}\n\n"
        f"🚀 <b>Что включено:</b>\n"
        f"• Адаптивный дизайн\n"
        f"• SEO-оптимизация\n"
        f"• Техническая поддержка\n"
        f"• Обучение работе с сайтом"
    )
    
    await query.message.reply_photo(
        photo=template["preview_image"],
        caption=detailed_caption,
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    
    return TEMPLATES

async def customize_template(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Конструктор сайта"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("🎨 Цветовая схема", callback_data='customize_colors'),
            InlineKeyboardButton("📝 Контент", callback_data='customize_content'),
        ],
        [
            InlineKeyboardButton("🖼️ Изображения", callback_data='customize_images'),
            InlineKeyboardButton("🔤 Шрифты", callback_data='customize_fonts'),
        ],
        [
            InlineKeyboardButton("📱 Адаптивность", callback_data='customize_responsive'),
            InlineKeyboardButton("⚡ Анимации", callback_data='customize_animations'),
        ],
        [
            InlineKeyboardButton("👁️ Предпросмотр", callback_data='preview_site'),
            InlineKeyboardButton("💾 Сохранить", callback_data='save_customization'),
        ],
        [
            InlineKeyboardButton("🔙 В главное меню", callback_data='back_to_main'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "🎨 <b>Конструктор сайта</b>\n\n"
        "Выберите, что хотите настроить:\n\n"
        "• <b>Цветовая схема</b> - измените цвета сайта\n"
        "• <b>Контент</b> - отредактируйте тексты и блоки\n"
        "• <b>Изображения</b> - загрузите свои фото\n"
        "• <b>Шрифты</b> - выберите стиль текста\n"
        "• <b>Адаптивность</b> - настройте для мобильных\n"
        "• <b>Анимации</b> - добавьте эффекты\n\n"
        "После настройки можете предварительно просмотреть результат!",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return CUSTOMIZATION

async def order_website(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Заказ сайта"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("🚀 Базовый (5000₽)", callback_data='order_basic'),
            InlineKeyboardButton("⭐ Про (8000₽)", callback_data='order_pro'),
        ],
        [
            InlineKeyboardButton("💎 Премиум (15000₽)", callback_data='order_premium'),
            InlineKeyboardButton("🏢 Корпоративный (25000₽)", callback_data='order_corporate'),
        ],
        [
            InlineKeyboardButton("🔙 В главное меню", callback_data='back_to_main'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "📦 <b>Выберите тарифный план:</b>\n\n"
        "🚀 <b>Базовый (5000₽)</b>\n"
        "• 1-2 страницы\n"
        "• Адаптивный дизайн\n"
        "• Базовая SEO-оптимизация\n"
        "• Срок: 3-5 дней\n\n"
        "⭐ <b>Про (8000₽)</b>\n"
        "• 3-5 страниц\n"
        "• Продвинутый дизайн\n"
        "• Формы обратной связи\n"
        "• Срок: 5-7 дней\n\n"
        "💎 <b>Премиум (15000₽)</b>\n"
        "• 5-10 страниц\n"
        "• Уникальный дизайн\n"
        "• Анимации и эффекты\n"
        "• Срок: 7-10 дней\n\n"
        "🏢 <b>Корпоративный (25000₽)</b>\n"
        "• Неограниченное количество страниц\n"
        "• Полная кастомизация\n"
        "• Техническая поддержка 24/7\n"
        "• Срок: 10-14 дней",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return ORDER

async def show_pricing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать цены"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("📦 Заказать", callback_data='order'),
            InlineKeyboardButton("💬 Консультация", callback_data='consultation'),
        ],
        [
            InlineKeyboardButton("🔙 В главное меню", callback_data='back_to_main'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "💰 <b>Наши цены</b>\n\n"
        "🚀 <b>Базовый пакет - 5000₽</b>\n"
        "• Лендинг-страница\n"
        "• Адаптивный дизайн\n"
        "• Базовая SEO-оптимизация\n"
        "• 1 месяц поддержки\n\n"
        "⭐ <b>Про пакет - 8000₽</b>\n"
        "• Многостраничный сайт\n"
        "• Продвинутый дизайн\n"
        "• Формы обратной связи\n"
        "• 3 месяца поддержки\n\n"
        "💎 <b>Премиум пакет - 15000₽</b>\n"
        "• Полнофункциональный сайт\n"
        "• Уникальный дизайн\n"
        "• Анимации и эффекты\n"
        "• 6 месяцев поддержки\n\n"
        "🏢 <b>Корпоративный - от 25000₽</b>\n"
        "• Индивидуальная разработка\n"
        "• Полная кастомизация\n"
        "• Техподдержка 24/7\n"
        "• 12 месяцев поддержки\n\n"
        "💡 <b>Дополнительные услуги:</b>\n"
        "• SEO-продвижение: от 5000₽/мес\n"
        "• Техподдержка: от 2000₽/мес\n"
        "• Обновления: от 1000₽/мес",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return SELECTING_ACTION

async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать помощь"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("📞 Связаться с поддержкой", callback_data='support'),
            InlineKeyboardButton("📧 Написать на email", callback_data='email_support'),
        ],
        [
            InlineKeyboardButton("🔙 В главное меню", callback_data='back_to_main'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "❓ <b>Помощь и поддержка</b>\n\n"
        "🤖 <b>Как пользоваться ботом:</b>\n"
        "1. Выберите шаблон из каталога\n"
        "2. Настройте его под свои нужды\n"
        "3. Закажите разработку\n"
        "4. Получите готовый сайт\n\n"
        "📞 <b>Связаться с нами:</b>\n"
        "• Telegram: @prothemes_support\n"
        "• Email: support@prothemes.ru\n"
        "• Телефон: +7 (999) 123-45-67\n\n"
        "⏰ <b>Время работы:</b>\n"
        "Пн-Пт: 9:00 - 18:00 (МСК)\n"
        "Сб-Вс: 10:00 - 16:00 (МСК)\n\n"
        "💡 <b>Часто задаваемые вопросы:</b>\n"
        "• Сколько времени занимает разработка?\n"
        "• Можно ли изменить дизайн после оплаты?\n"
        "• Предоставляете ли вы хостинг?\n"
        "• Есть ли гарантия на работу сайта?",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return SELECTING_ACTION

async def show_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Показать контакты"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("📞 Позвонить", callback_data='call_us'),
            InlineKeyboardButton("💬 Написать в Telegram", callback_data='telegram_contact'),
        ],
        [
            InlineKeyboardButton("📧 Email", callback_data='email_contact'),
            InlineKeyboardButton("🌐 Наш сайт", callback_data='website'),
        ],
        [
            InlineKeyboardButton("🔙 В главное меню", callback_data='back_to_main'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(
        "📞 <b>Наши контакты</b>\n\n"
        "🏢 <b>ProThemesRU</b>\n"
        "Создание профессиональных сайтов\n\n"
        "📱 <b>Telegram:</b> @prothemes_support\n"
        "📧 <b>Email:</b> info@prothemes.ru\n"
        "📞 <b>Телефон:</b> +7 (999) 123-45-67\n"
        "🌐 <b>Сайт:</b> https://prothemes.ru\n\n"
        "📍 <b>Адрес:</b>\n"
        "г. Москва, ул. Примерная, д. 123\n"
        "Бизнес-центр "Технопарк"\n\n"
        "⏰ <b>Время работы:</b>\n"
        "Понедельник - Пятница: 9:00 - 18:00\n"
        "Суббота: 10:00 - 16:00\n"
        "Воскресенье: выходной\n\n"
        "💬 <b>Онлайн-консультации:</b>\n"
        "Круглосуточно через бота",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )
    return SELECTING_ACTION

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
                CallbackQueryHandler(customize_template, pattern='^customization$'),
                CallbackQueryHandler(order_website, pattern='^order$'),
                CallbackQueryHandler(show_pricing, pattern='^pricing$'),
                CallbackQueryHandler(show_help, pattern='^help$'),
                CallbackQueryHandler(show_contacts, pattern='^contacts$'),
            ],
            TEMPLATES: [
                CallbackQueryHandler(view_template, pattern='^view_\d+$'),
                CallbackQueryHandler(show_templates, pattern='^templates$'),
                CallbackQueryHandler(back_to_main, pattern='^back_to_main$'),
            ],
            CUSTOMIZATION: [
                CallbackQueryHandler(customize_template, pattern='^customize_'),
                CallbackQueryHandler(back_to_main, pattern='^back_to_main$'),
            ],
            ORDER: [
                CallbackQueryHandler(order_website, pattern='^order_'),
                CallbackQueryHandler(back_to_main, pattern='^back_to_main$'),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )
    
    application.add_handler(conv_handler)
    application.add_error_handler(error_handler)
    
    # Запуск бота
    logger.info("Запуск телеграм бота...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()