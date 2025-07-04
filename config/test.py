from config import Config

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Используем память для тестов
    WTF_CSRF_ENABLED = False  # Отключаем CSRF для тестов
    SECRET_KEY = 'test-secret-key'
    DEBUG = True
