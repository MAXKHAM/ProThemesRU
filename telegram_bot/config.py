#!/usr/bin/env python3
"""
ProThemesRU - Конфигурация Telegram бота
"""

import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class Config:
    """Конфигурация приложения"""
    
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'your_bot_token_here')
    TELEGRAM_ADMIN_CHAT_ID = os.environ.get('TELEGRAM_ADMIN_CHAT_ID', 'your_admin_chat_id_here')
    
    # API Configuration
    API_BASE_URL = os.environ.get('API_BASE_URL', 'https://pro-themes-ru.vercel.app')
    WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'https://pro-themes-ru.vercel.app/webhook')
    
    # Database Configuration
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///bot_database.db')
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'telegram_bot.log')
    
    # Features
    ENABLE_WEBHOOK = os.environ.get('ENABLE_WEBHOOK', 'true').lower() == 'true'
    ENABLE_POLLING = os.environ.get('ENABLE_POLLING', 'false').lower() == 'true'
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY', 'prothemesru-bot-secret-key-2024')
    
    # Environment
    ENVIRONMENT = os.environ.get('ENVIRONMENT', 'production')
    
    # Port (for Railway)
    PORT = int(os.environ.get('PORT', 8000))
    
    # Templates
    TEMPLATES = {
        '01': {'name': 'Gaming Template', 'price': 5000, 'category': 'gaming'},
        '02': {'name': 'Business Template', 'price': 3000, 'category': 'business'},
        '03': {'name': 'Portfolio Template', 'price': 4000, 'category': 'portfolio'},
        '04': {'name': 'E-commerce Template', 'price': 6000, 'category': 'ecommerce'},
        '05': {'name': 'Blog Template', 'price': 2500, 'category': 'blog'}
    }
    
    # Referral Program
    REFERRAL_COMMISSION = 0.10  # 10%
    MIN_WITHDRAWAL = 1000  # 1000₽
    
    # Support
    SUPPORT_EMAIL = 'support@prothemesru.com'
    SUPPORT_TELEGRAM = '@ProThemesRU_Support'
    WEBSITE_URL = 'https://pro-themes-ru.vercel.app'

class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    ENABLE_WEBHOOK = False
    ENABLE_POLLING = True

class ProductionConfig(Config):
    """Конфигурация для продакшена"""
    DEBUG = False
    LOG_LEVEL = 'INFO'
    ENABLE_WEBHOOK = True
    ENABLE_POLLING = False

# Выбираем конфигурацию в зависимости от окружения
def get_config():
    """Получить конфигурацию в зависимости от окружения"""
    env = os.environ.get('ENVIRONMENT', 'production')
    
    if env == 'development':
        return DevelopmentConfig()
    else:
        return ProductionConfig()

# Создаем экземпляр конфигурации
config = get_config() 