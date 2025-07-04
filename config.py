import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_super_secret_key_here_change_it_in_production!'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    TELEGRAM_ADMIN_CHAT_ID = os.environ.get('TELEGRAM_ADMIN_CHAT_ID')
    PAYMENT_API_KEY_PUBLIC = os.environ.get('PAYMENT_API_KEY_PUBLIC')
    PAYMENT_API_KEY_SECRET = os.environ.get('PAYMENT_API_KEY_SECRET')
    PROJECT_NAME = "ProThemesRU"
    ADMIN_EMAIL = "admin@prothemes.ru"

class DevelopmentConfig(Config):
    DEBUG = True
    FLASK_ENV = 'development'

class ProductionConfig(Config):
    DEBUG = False
    FLASK_ENV = 'production'

config_by_name = dict(
    development=DevelopmentConfig,
    production=ProductionConfig,
    testing=TestConfig,
    default=DevelopmentConfig
)
