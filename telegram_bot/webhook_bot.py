#!/usr/bin/env python3
"""
Telegram бот для ProThemesRU с webhook поддержкой
Для деплоя на Vercel
"""

import os
import logging
import requests
import json
from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Flask приложение
app = Flask(__name__)

# Конфигурация
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
API_BASE_URL = os.environ.get('API_BASE_URL', 'https://prothemesru.vercel.app')
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'https://your-bot-domain.vercel.app/webhook')

class ProThemesRUBot:
    def __init__(self):
        self.api_url = API_BASE_URL
        logger.info(f"Бот инициализирован с API URL: {self.api_url}")
        
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

🌐 Веб-интерфейс: https://prothemesru.vercel.app
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
        elif query.data == "create_from_scratch":
            await self.create_from_scratch(update, context)
        elif query.data == "import_site":
            await self.import_site(update, context)
        elif query.data.startswith("create_from_template_"):
            template_id = query.data.split("_")[3]
            await self.create_from_template(update, context, template_id)
    
    async def show_templates(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать доступные шаблоны"""
        try:
            logger.info(f"Запрос шаблонов с API: {self.api_url}/api/templates")
            response = requests.get(f"{self.api_url}/api/templates", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                templates = data.get('templates', [])
                
                if not templates:
                    # Fallback templates если API не отвечает
                    templates = [
                        {
                            'id': 1,
                            'name': 'Королевский бизнес',
                            'category': 'business',
                            'price': 5000,
                            'rating': 4.9,
                            'downloads': 150
                        },
                        {
                            'id': 2,
                            'name': 'Золотое портфолио',
                            'category': 'portfolio',
                            'price': 3000,
                            'rating': 4.8,
                            'downloads': 89
                        },
                        {
                            'id': 3,
                            'name': 'Премиум магазин',
                            'category': 'ecommerce',
                            'price': 8000,
                            'rating': 4.7,
                            'downloads': 234
                        }
                    ]
                
                text = "📋 Доступные шаблоны:\n\n"
                keyboard = []
                
                for template in templates[:5]:  # Показываем первые 5
                    text += f"🎨 {template['name']}\n"
                    text += f"   Категория: {template['category']}\n"
                    text += f"   Цена: {'Бесплатно' if template.get('price', 0) == 0 else f'{template.get('price', 0)} ₽'}\n"
                    text += f"   Рейтинг: {template.get('rating', 0)}/5 ⭐\n\n"
                    
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
                logger.error(f"API вернул статус {response.status_code}")
                await self.send_error_message(update, context, "Ошибка загрузки шаблонов")
                
        except requests.exceptions.Timeout:
            logger.error("Таймаут при запросе к API")
            await self.send_error_message(update, context, "Сервер не отвечает. Попробуйте позже.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка сети: {e}")
            await self.send_error_message(update, context, "Ошибка подключения к серверу")
        except Exception as e:
            logger.error(f"Неожиданная ошибка: {e}")
            await self.send_error_message(update, context, "Произошла ошибка. Попробуйте позже.")
    
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
    
    async def create_from_scratch(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Создание сайта с нуля"""
        text = """
🎨 Создание сайта с нуля

Для создания сайта с нуля используйте наш веб-интерфейс:

🌐 https://prothemesru.vercel.app

Там вы найдете:
• Визуальный конструктор
• Готовые элементы
• Предварительный просмотр
• Сохранение проектов
        """
        
        keyboard = [
            [InlineKeyboardButton("🌐 Открыть конструктор", url="https://prothemesru.vercel.app")],
            [InlineKeyboardButton("🔙 Назад", callback_data="create_site")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_or_edit_message(update, context, text, reply_markup)
    
    async def import_site(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Импорт существующего сайта"""
        text = """
📤 Импорт существующего сайта

Для импорта сайта свяжитесь с нашей поддержкой:

📧 support@prothemesru.com
📱 @ProThemesRU_Bot

Мы поможем перенести ваш сайт на нашу платформу!
        """
        
        keyboard = [
            [InlineKeyboardButton("📧 Написать в поддержку", url="https://t.me/ProThemesRU_Bot")],
            [InlineKeyboardButton("🔙 Назад", callback_data="create_site")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_or_edit_message(update, context, text, reply_markup)
    
    async def select_template(self, update: Update, context: ContextTypes.DEFAULT_TYPE, template_id):
        """Выбор шаблона для создания сайта"""
        try:
            response = requests.get(f"{self.api_url}/api/templates/{template_id}", timeout=10)
            if response.status_code == 200:
                template = response.json().get('template', {})
            else:
                # Fallback template
                template = {
                    'id': template_id,
                    'name': f'Шаблон #{template_id}',
                    'category': 'business',
                    'price': 5000,
                    'rating': 4.8,
                    'downloads': 100
                }
            
            text = f"""
🎨 Выбран шаблон: {template['name']}

📋 Информация:
• Категория: {template['category']}
• Цена: {'Бесплатно' if template.get('price', 0) == 0 else f'{template.get('price', 0)} ₽'}
• Рейтинг: {template.get('rating', 0)}/5 ⭐
• Загрузок: {template.get('downloads', 0)}

✅ Готовы создать сайт на основе этого шаблона?
            """
            
            keyboard = [
                [InlineKeyboardButton("✅ Создать сайт", callback_data=f"create_from_template_{template_id}")],
                [InlineKeyboardButton("🔙 Выбрать другой", callback_data="templates")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await self.send_or_edit_message(update, context, text, reply_markup)
                
        except Exception as e:
            logger.error(f"Ошибка при выборе шаблона: {e}")
            await self.send_error_message(update, context, "Ошибка загрузки шаблона")
    
    async def create_from_template(self, update: Update, context: ContextTypes.DEFAULT_TYPE, template_id):
        """Создание сайта на основе шаблона"""
        text = f"""
🎉 Отлично! Создаем сайт на основе шаблона #{template_id}

Для завершения создания сайта:

1️⃣ Перейдите в веб-интерфейс
2️⃣ Выберите этот шаблон
3️⃣ Настройте контент
4️⃣ Опубликуйте сайт

🌐 https://prothemesru.vercel.app

Нужна помощь? Пишите в поддержку: @ProThemesRU_Bot
        """
        
        keyboard = [
            [InlineKeyboardButton("🌐 Открыть конструктор", url="https://prothemesru.vercel.app")],
            [InlineKeyboardButton("📱 Поддержка", url="https://t.me/ProThemesRU_Bot")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_or_edit_message(update, context, text, reply_markup)
    
    async def show_my_sites(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать сайты пользователя"""
        text = """
👤 Мои сайты

Для просмотра и управления вашими сайтами используйте веб-интерфейс:

🌐 https://prothemesru.vercel.app

Там вы сможете:
• Просматривать все сайты
• Редактировать их
• Публиковать изменения
• Управлять настройками

🔐 Войдите в систему для доступа к вашим проектам
        """
        
        keyboard = [
            [InlineKeyboardButton("🌐 Открыть веб-интерфейс", url="https://prothemesru.vercel.app")],
            [InlineKeyboardButton("🔙 Назад", callback_data="start")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_or_edit_message(update, context, text, reply_markup)
    
    async def send_or_edit_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, reply_markup=None):
        """Отправить или отредактировать сообщение"""
        query = update.callback_query
        if query:
            try:
                await query.edit_message_text(text=text, reply_markup=reply_markup)
            except Exception as e:
                logger.error(f"Ошибка редактирования сообщения: {e}")
                await query.message.reply_text(text=text, reply_markup=reply_markup)
        else:
            await update.message.reply_text(text=text, reply_markup=reply_markup)
    
    async def send_error_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE, error_text: str):
        """Отправить сообщение об ошибке"""
        text = f"❌ {error_text}\n\nПопробуйте позже или обратитесь в поддержку: @ProThemesRU_Bot"
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="start")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_or_edit_message(update, context, text, reply_markup)

# Создание экземпляра бота
bot = ProThemesRUBot()

# Создание приложения
if TELEGRAM_BOT_TOKEN:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("templates", bot.templates_command))
    application.add_handler(CommandHandler("my_sites", bot.my_sites_command))
    
    # Обработчик кнопок
    application.add_handler(CallbackQueryHandler(bot.button_handler))
else:
    application = None
    logger.error("TELEGRAM_BOT_TOKEN не установлен!")

@app.route('/')
def home():
    """Главная страница"""
    return jsonify({
        'message': 'ProThemesRU Telegram Bot',
        'status': 'running',
        'version': '1.0.0'
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook для Telegram"""
    if application is None:
        return jsonify({'error': 'Bot not initialized'}), 500
    
    try:
        # Получаем данные от Telegram
        update = Update.de_json(request.get_json(), application.bot)
        
        # Обрабатываем обновление
        application.process_update(update)
        
        return jsonify({'status': 'ok'})
    except Exception as e:
        logger.error(f"Ошибка в webhook: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/set-webhook', methods=['GET'])
def set_webhook():
    """Установка webhook"""
    if application is None:
        return jsonify({'error': 'Bot not initialized'}), 500
    
    try:
        # Устанавливаем webhook
        success = application.bot.set_webhook(url=WEBHOOK_URL)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': f'Webhook установлен: {WEBHOOK_URL}'
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Не удалось установить webhook'
            })
    except Exception as e:
        logger.error(f"Ошибка установки webhook: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Проверка здоровья сервиса"""
    return jsonify({
        'status': 'healthy',
        'bot_token': 'set' if TELEGRAM_BOT_TOKEN else 'not_set',
        'api_url': API_BASE_URL,
        'webhook_url': WEBHOOK_URL
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 