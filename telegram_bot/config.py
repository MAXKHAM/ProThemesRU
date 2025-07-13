import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

# API Configuration
API_BASE_URL = os.environ.get('API_BASE_URL', 'https://pro-themes-ru-maxkhams-projects.vercel.app')

# Bot Settings
BOT_NAME = "ProThemesRU Bot"
BOT_DESCRIPTION = "Создавайте сайты прямо в Telegram!"

# API Endpoints
API_ENDPOINTS = {
    'health': f"{API_BASE_URL}/api/health",
    'templates': f"{API_BASE_URL}/api/templates",
    'register': f"{API_BASE_URL}/api/auth/register",
    'login': f"{API_BASE_URL}/api/auth/login",
    'sites': f"{API_BASE_URL}/api/sites"
}

# Error Messages
ERROR_MESSAGES = {
    'api_unavailable': 'Сервер временно недоступен. Попробуйте позже.',
    'network_error': 'Ошибка сети. Проверьте подключение.',
    'invalid_data': 'Неверные данные. Попробуйте еще раз.'
}

# Настройки логирования
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')

# Проверка обязательных переменных
def validate_config():
    """Проверяет корректность конфигурации"""
    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN не установлен в переменных окружения")
    
    if not API_BASE_URL:
        raise ValueError("API_BASE_URL не установлен в переменных окружения")
    
    return True 