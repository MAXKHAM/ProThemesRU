import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env
load_dotenv()

from app import create_app, db

# Выбираем конфигурацию в зависимости от переменной окружения FLASK_ENV
config_name = os.environ.get('FLASK_ENV', 'default')
app = create_app(config_name)

# Создаем таблицы базы данных, если скрипт запущен напрямую
@app.cli.command('initdb')
def initdb_command():
    """Инициализирует базу данных."""
    db.create_all()
    print('Инициализирована база данных.')

if __name__ == '__main__':
    # Запуск приложения в режиме отладки
    # Для продакшена используйте Gunicorn или аналогичный сервер
    app.run(debug=True, host='0.0.0.0', port=5000) 