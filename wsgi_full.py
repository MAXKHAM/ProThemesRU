#!/usr/bin/env python3
"""
WSGI entry point for ProThemesRU full application
"""

import os
import sys

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(__file__))

# Импортируем приложение
from app_full import app, db

# Создаем необходимые директории
os.makedirs('uploads', exist_ok=True)
os.makedirs('media', exist_ok=True)
os.makedirs('scraped_sites', exist_ok=True)

# Создаем таблицы базы данных
with app.app_context():
    db.create_all()

# Экспортируем приложение для Gunicorn
application = app

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 