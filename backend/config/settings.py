import os
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Базовые настройки
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Настройки базы данных
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./prothemes.db')

# Настройки кэширования изображений
IMAGE_CACHE_DIR = os.path.join(BASE_DIR, 'media', 'image_cache')
os.makedirs(IMAGE_CACHE_DIR, exist_ok=True)

# Настройки статических файлов
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Настройки безопасности
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False') == 'True'

# Настройки кэширования
CACHE_TYPE = 'redis'
CACHE_REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CACHE_DEFAULT_TIMEOUT = 300

# Настройки Redis
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Настройки Celery
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = REDIS_URL

# Настройки аналитики
GOOGLE_ANALYTICS_ID = os.getenv('GOOGLE_ANALYTICS_ID')
YANDEX_METRIKA_ID = os.getenv('YANDEX_METRIKA_ID')

# Настройки почты
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# Настройки логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Настройки CORS
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:3000').split(',')
CORS_ALLOW_CREDENTIALS = True

# Настройки JWT
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', SECRET_KEY)
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

# Настройки Redis для сессий
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'

# Настройки кэширования страниц
PAGE_CACHE_TIMEOUT = 3600

# Настройки CDN
CDN_URL = os.getenv('CDN_URL')
USE_CDN = CDN_URL is not None

# Настройки CDN для изображений
IMAGE_CDN_URL = os.getenv('IMAGE_CDN_URL')
USE_IMAGE_CDN = IMAGE_CDN_URL is not None

# Настройки оптимизации изображений
IMAGE_OPTIMIZATION = {
    'QUALITY': 85,
    'FORMAT': 'webp',
    'MAX_WIDTH': 1920,
    'MAX_HEIGHT': 1080,
}

# Настройки SEO
SEO_SETTINGS = {
    'DEFAULT_TITLE': 'ProThemesRU - Шаблоны сайтов',
    'DEFAULT_DESCRIPTION': 'Создайте сайт мечты с помощью наших шаблонов',
    'DEFAULT_KEYWORDS': [
        'шаблоны сайтов', 'конструктор сайтов', 'создание сайта',
        'сайт без кодирования', 'шаблоны для бизнеса', 'портфолио'
    ],
    'SOCIAL_IMAGE': '/static/images/social-preview.jpg'
}
