from app import db
from app.models import Template
from app import create_app

app = create_app()

with app.app_context():
    # Удаляем существующие шаблоны
    Template.query.delete()
    
    # Создаем тестовые шаблоны
    templates = [
        {
            'name': 'Business Landing',
            'description': 'Современный шаблон для бизнес-сайта с акцентом на профессиональность и надежность.',
            'image_url': '/static/img/templates/business_landing.jpg',
            'price': 999
        },
        {
            'name': 'Creative Portfolio',
            'description': 'Креативный шаблон для портфолио с современным дизайном и удобной навигацией.',
            'image_url': '/static/img/templates/creative_portfolio.jpg',
            'price': 1499
        },
        {
            'name': 'Online Store',
            'description': 'Шаблон для интернет-магазина с поддержкой каталога товаров и корзины.',
            'image_url': '/static/img/templates/online_store.jpg',
            'price': 1999
        },
        {
            'name': 'Video Catalog',
            'description': 'Современный шаблон для видеокаталога с поддержкой фильтров и поиска.',
            'image_url': '/static/img/templates/video_catalog.jpg',
            'price': 2499
        }
    ]
    
    # Добавляем шаблоны в базу данных
    for template_data in templates:
        template = Template(
            name=template_data['name'],
            description=template_data['description'],
            image_url=template_data['image_url'],
            price=template_data['price']
        )
        db.session.add(template)
    
    db.session.commit()
    print("Шаблоны успешно созданы!")
