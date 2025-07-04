from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime

class TemplateBlock(BaseModel):
    id: str
    type: str  # 'header', 'footer', 'hero', 'features', 'pricing', 'contact', 'blog', 'portfolio', 'cta'
    content: Dict
    position: int
    settings: Dict = {}

class Template(BaseModel):
    id: str
    name: str
    description: str
    category: str  # 'business', 'portfolio', 'blog', 'landing', 'ecommerce'
    preview_image: str
    blocks: List[TemplateBlock]
    created_at: datetime
    updated_at: datetime
    is_featured: bool = False
    price: float
    features: List[str]
    tags: List[str]

    class Config:
        orm_mode = True

# Примерные шаблоны
EXAMPLE_TEMPLATES = [
    Template(
        id="business-1",
        name="Корпоративный сайт",
        description="Профессиональный шаблон для бизнеса",
        category="business",
        preview_image="templates/business-1.jpg",
        blocks=[
            TemplateBlock(
                id="header-1",
                type="header",
                content={
                    "logo": "logo.png",
                    "menu": ["Главная", "Услуги", "О нас", "Контакты"]
                },
                position=1
            ),
            TemplateBlock(
                id="hero-1",
                type="hero",
                content={
                    "title": "Ваш бизнес заслуживает лучшего",
                    "subtitle": "Профессиональные решения для вашего бизнеса",
                    "button_text": "Подробнее",
                    "button_link": "#about"
                },
                position=2
            ),
            TemplateBlock(
                id="features-1",
                type="features",
                content={
                    "items": [
                        {"icon": "🚀", "title": "Быстрый старт", "description": "Начните работу за 5 минут"},
                        {"icon": "🎨", "title": "Профессиональный дизайн", "description": "Современные решения"},
                        {"icon": "💰", "title": "Экономия", "description": "Снижение затрат на разработку"}
                    ]
                },
                position=3
            ),
            TemplateBlock(
                id="footer-1",
                type="footer",
                content={
                    "copyright": "© 2025 Все права защищены",
                    "social_links": [
                        {"icon": "facebook", "url": "#"},
                        {"icon": "instagram", "url": "#"},
                        {"icon": "linkedin", "url": "#"}
                    ]
                },
                position=4
            )
        ],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_featured=True,
        price=9990.0,
        features=["Адаптивный дизайн", "SEO оптимизация", "CRM интеграция"],
        tags=["business", "corporate", "professional"]
    ),
    Template(
        id="portfolio-1",
        name="Портфолио дизайнера",
        description="Стильный шаблон для портфолио",
        category="portfolio",
        preview_image="templates/portfolio-1.jpg",
        blocks=[
            TemplateBlock(
                id="header-2",
                type="header",
                content={
                    "logo": "logo.png",
                    "menu": ["Работы", "О проекте", "Контакты"]
                },
                position=1
            ),
            TemplateBlock(
                id="portfolio-1",
                type="portfolio",
                content={
                    "projects": [
                        {
                            "image": "project-1.jpg",
                            "title": "Проект 1",
                            "description": "Краткое описание проекта",
                            "link": "#"
                        },
                        {
                            "image": "project-2.jpg",
                            "title": "Проект 2",
                            "description": "Краткое описание проекта",
                            "link": "#"
                        }
                    ]
                },
                position=2
            ),
            TemplateBlock(
                id="contact-1",
                type="contact",
                content={
                    "title": "Свяжитесь со мной",
                    "form_fields": [
                        {"type": "text", "label": "Имя", "name": "name"},
                        {"type": "email", "label": "Email", "name": "email"},
                        {"type": "textarea", "label": "Сообщение", "name": "message"}
                    ]
                },
                position=3
            )
        ],
        created_at=datetime.now(),
        updated_at=datetime.now(),
        is_featured=True,
        price=7990.0,
        features=["Галерея работ", "Блог", "Контактная форма"],
        tags=["portfolio", "design", "creative"]
    )
]
