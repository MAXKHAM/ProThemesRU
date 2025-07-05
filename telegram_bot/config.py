import os
from dotenv import load_dotenv

# ВАЖНО: .env должен быть в кодировке UTF-8 без BOM!
load_dotenv()

def parse_list_env(var):
    return [x for x in os.getenv(var, '').split(',') if x.strip()]

class BotConfig:
    """Конфигурация телеграм бота"""
    
    # Основные настройки
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID')
    
    # API настройки
    API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:5000')
    
    # Настройки логирования
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = 'telegram_bot.log'
    
    # Настройки базы данных
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot_database.db')
    
    # Настройки Redis (для кэширования)
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
    
    # Настройки платежей
    PAYMENT_API_KEY = os.getenv('PAYMENT_API_KEY')
    PAYMENT_SECRET_KEY = os.getenv('PAYMENT_SECRET_KEY')
    
    # Настройки уведомлений
    ENABLE_ADMIN_NOTIFICATIONS = os.getenv('ENABLE_ADMIN_NOTIFICATIONS', 'true').lower() == 'true'
    
    # Настройки шаблонов
    TEMPLATES_FILE = os.getenv('TEMPLATES_FILE', '../design_templates.json')
    
    # Настройки лимитов
    MAX_TEMPLATES_PER_USER = int(os.getenv('MAX_TEMPLATES_PER_USER', '10'))
    MAX_CUSTOMIZATIONS_PER_USER = int(os.getenv('MAX_CUSTOMIZATIONS_PER_USER', '5'))
    
    # Настройки таймаутов
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', '3600'))  # 1 час
    
    # Настройки безопасности
    ALLOWED_USERS = parse_list_env('ALLOWED_USERS')
    BLOCKED_USERS = parse_list_env('BLOCKED_USERS')
    
    @classmethod
    def validate(cls):
        """Проверка конфигурации"""
        errors = []
        
        if not cls.TELEGRAM_TOKEN:
            errors.append("TELEGRAM_BOT_TOKEN не установлен")
        
        if not cls.ADMIN_CHAT_ID:
            errors.append("TELEGRAM_ADMIN_CHAT_ID не установлен")
        
        return errors

class TemplatesConfig:
    """Конфигурация шаблонов"""
    
    # Категории шаблонов
    CATEGORIES = {
        'business': 'Бизнес',
        'portfolio': 'Портфолио',
        'ecommerce': 'E-commerce',
        'blog': 'Блог',
        'landing': 'Лендинг',
        'corporate': 'Корпоративный'
    }
    
    # Ценовые категории
    PRICE_CATEGORIES = {
        'basic': {'name': 'Базовый', 'price': 5000, 'currency': '₽'},
        'pro': {'name': 'Про', 'price': 8000, 'currency': '₽'},
        'premium': {'name': 'Премиум', 'price': 15000, 'currency': '₽'},
        'corporate': {'name': 'Корпоративный', 'price': 25000, 'currency': '₽'}
    }
    
    # Особенности шаблонов
    FEATURES = [
        'Адаптивный дизайн',
        'SEO-оптимизация',
        'Формы обратной связи',
        'Галерея работ',
        'Анимации',
        'Контактная форма',
        'Каталог товаров',
        'Корзина',
        'Онлайн-оплата',
        'Блог',
        'Новости',
        'Многоязычность'
    ]

class MessagesConfig:
    """Конфигурация сообщений"""
    
    # Приветственные сообщения
    WELCOME_MESSAGE = """
Привет, {name}! 🌟

Я помогу вам создать профессиональный сайт.
Выберите действие:
    """
    
    # Сообщения об ошибках
    ERROR_MESSAGES = {
        'template_not_found': '❌ Шаблон не найден',
        'api_error': '❌ Ошибка при загрузке данных',
        'payment_error': '❌ Ошибка при оплате',
        'general_error': '❌ Произошла ошибка. Попробуйте снова'
    }
    
    # Сообщения успеха
    SUCCESS_MESSAGES = {
        'template_selected': '✅ Шаблон выбран успешно!',
        'order_created': '✅ Заказ создан успешно!',
        'payment_success': '✅ Оплата прошла успешно!'
    }

# Экспорт конфигураций
config = BotConfig()
templates_config = TemplatesConfig()
messages_config = MessagesConfig() 