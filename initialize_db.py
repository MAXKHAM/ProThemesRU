from app import app, db
from app.models import User, Project, Template, Block

with app.app_context():
    # Удаляем существующую базу данных
    db.drop_all()
    # Создаем новую базу данных
    db.create_all()
    
    print("База данных успешно инициализирована!")
