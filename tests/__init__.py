from app import create_app, db
from app.models import User, SiteBlock, Site

def create_test_app():
    """Создает тестовое приложение"""
    app = create_app('testing')
    return app
