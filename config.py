import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-very-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///prothemesru.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # YooKassa Payment Settings
    YOOKASSA_SHOP_ID = os.environ.get('YOOKASSA_SHOP_ID') or 'your_shop_id'
    YOOKASSA_SECRET_KEY = os.environ.get('YOOKASSA_SECRET_KEY') or 'your_secret_key'
    
    # Telegram Bot Settings
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN') or 'your_telegram_bot_token'
    PUBLIC_APP_URL = os.environ.get('PUBLIC_APP_URL') or 'http://127.0.0.1:5000'
    
    # Stripe Settings (alternative payment method)
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY') or 'sk_test_your_stripe_secret_key'
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY') or 'pk_test_your_stripe_publishable_key'
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET') or 'whsec_your_stripe_webhook_secret'
    
    # Session Settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # File Upload Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    
    # AI Settings
    AI_API_KEY = os.environ.get('AI_API_KEY') or 'your_ai_api_key'
    
    # Development Settings
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
