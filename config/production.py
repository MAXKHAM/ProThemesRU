import os
from datetime import timedelta

class ProductionConfig:
    """Конфигурация для продакшена"""
    
    # Основные настройки
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    DEBUG = False
    TESTING = False
    
    # База данных
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://username:password@localhost/prothemesru'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT настройки
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=90)
    
    # Файловое хранилище
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'pdf', 'doc', 'docx'}
    
    # Email настройки
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    
    # Redis настройки
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Celery настройки
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'
    
    # Платежи
    STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    # AWS S3 (для файлового хранилища)
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.environ.get('AWS_REGION') or 'us-east-1'
    AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
    
    # Telegram Bot
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    TELEGRAM_ADMIN_ID = os.environ.get('TELEGRAM_ADMIN_ID')
    
    # Безопасность
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Логирование
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or 'logs/app.log'
    
    # Кэширование
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('CACHE_REDIS_URL') or 'redis://localhost:6379/1'
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Rate Limiting
    RATELIMIT_STORAGE_URL = os.environ.get('RATELIMIT_STORAGE_URL') or 'redis://localhost:6379/2'
    
    # Мониторинг
    SENTRY_DSN = os.environ.get('SENTRY_DSN')
    
    # Домены
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')
    
    # SSL/TLS
    SSL_REDIRECT = True
    
    # API настройки
    API_TITLE = 'ProThemesRU API'
    API_VERSION = 'v1'
    API_DESCRIPTION = 'API для платформы создания сайтов ProThemesRU'
    
    # Лимиты
    MAX_PROJECTS_PER_USER = 10
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    MAX_REQUESTS_PER_MINUTE = 100
    
    # Настройки шаблонов
    TEMPLATES_PER_PAGE = 12
    MAX_TEMPLATE_CATEGORIES = 20
    
    # Настройки конструктора
    MAX_ELEMENTS_PER_PROJECT = 100
    MAX_CANVAS_SIZE = 2000
    
    # Настройки экспорта
    EXPORT_FORMATS = ['html', 'zip', 'pdf']
    EXPORT_MAX_SIZE = 50 * 1024 * 1024  # 50MB 