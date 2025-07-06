#!/usr/bin/env python3
"""
Скрипт для инициализации базы данных ProThemesRU
Создает примеры блоков и шаблонов для работы конструктора
"""

import os
import sys
from datetime import datetime

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Block, Template, Payment, GeneratedSite
from config import Config

def init_database():
    """Инициализация базы данных с примерами данных"""
    app = create_app('development')
    
    with app.app_context():
        # Создаем таблицы
        db.create_all()
        print("✅ Таблицы базы данных созданы")
        
        # Создаем примеры блоков
        blocks_data = [
            {
                'name': 'Заголовок сайта',
                'type': 'header',
                'html_content': '''
                <header class="bg-primary text-white text-center py-5">
                    <div class="container">
                        <h1 class="display-4">{{{title}}}</h1>
                        <p class="lead">{{{subtitle}}}</p>
                    </div>
                </header>
                ''',
                'css_content': '''
                .bg-primary { background-color: #007bff !important; }
                .display-4 { font-size: 2.5rem; font-weight: 300; }
                .lead { font-size: 1.25rem; font-weight: 300; }
                '''
            },
            {
                'name': 'Главный баннер',
                'type': 'hero',
                'html_content': '''
                <section class="hero-section text-center py-5" style="background: linear-gradient(135deg, {{{bg_color_1}}}, {{{bg_color_2}}});">
                    <div class="container">
                        <h1 class="hero-title">{{{hero_title}}}</h1>
                        <p class="hero-subtitle">{{{hero_subtitle}}}</p>
                        <a href="{{{cta_link}}}" class="btn btn-light btn-lg">{{{cta_text}}}</a>
                    </div>
                </section>
                ''',
                'css_content': '''
                .hero-section { min-height: 60vh; display: flex; align-items: center; }
                .hero-title { font-size: 3rem; margin-bottom: 1rem; color: white; }
                .hero-subtitle { font-size: 1.5rem; margin-bottom: 2rem; color: white; opacity: 0.9; }
                '''
            },
            {
                'name': 'Текстовый блок',
                'type': 'content',
                'html_content': '''
                <section class="content-section py-5">
                    <div class="container">
                        <div class="row">
                            <div class="col-lg-8 mx-auto">
                                <h2>{{{section_title}}}</h2>
                                <p>{{{content_text}}}</p>
                            </div>
                        </div>
                    </div>
                </section>
                ''',
                'css_content': '''
                .content-section { background-color: #f8f9fa; }
                .content-section h2 { color: #333; margin-bottom: 1.5rem; }
                .content-section p { font-size: 1.1rem; line-height: 1.6; color: #666; }
                '''
            },
            {
                'name': 'Карточки услуг',
                'type': 'cards',
                'html_content': '''
                <section class="services-section py-5">
                    <div class="container">
                        <h2 class="text-center mb-5">{{{services_title}}}</h2>
                        <div class="row">
                            <div class="col-md-4 mb-4">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <h5 class="card-title">{{{service_1_title}}}</h5>
                                        <p class="card-text">{{{service_1_desc}}}</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 mb-4">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <h5 class="card-title">{{{service_2_title}}}</h5>
                                        <p class="card-text">{{{service_2_desc}}}</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 mb-4">
                                <div class="card h-100">
                                    <div class="card-body text-center">
                                        <h5 class="card-title">{{{service_3_title}}}</h5>
                                        <p class="card-text">{{{service_3_desc}}}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
                ''',
                'css_content': '''
                .services-section { background-color: white; }
                .card { border: none; box-shadow: 0 2px 10px rgba(0,0,0,0.1); transition: transform 0.3s; }
                .card:hover { transform: translateY(-5px); }
                .card-title { color: #333; font-weight: 600; }
                .card-text { color: #666; }
                '''
            },
            {
                'name': 'Контактная форма',
                'type': 'contact',
                'html_content': '''
                <section class="contact-section py-5 bg-light">
                    <div class="container">
                        <div class="row">
                            <div class="col-lg-6 mx-auto">
                                <h2 class="text-center mb-4">{{{contact_title}}}</h2>
                                <form>
                                    <div class="mb-3">
                                        <input type="text" class="form-control" placeholder="{{{name_placeholder}}}" required>
                                    </div>
                                    <div class="mb-3">
                                        <input type="email" class="form-control" placeholder="{{{email_placeholder}}}" required>
                                    </div>
                                    <div class="mb-3">
                                        <textarea class="form-control" rows="5" placeholder="{{{message_placeholder}}}" required></textarea>
                                    </div>
                                    <button type="submit" class="btn btn-primary w-100">{{{submit_text}}}</button>
                                </form>
                            </div>
                        </div>
                    </div>
                </section>
                ''',
                'css_content': '''
                .contact-section { background-color: #f8f9fa; }
                .form-control { border: 1px solid #ddd; border-radius: 5px; padding: 12px; }
                .form-control:focus { border-color: #007bff; box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25); }
                .btn-primary { background-color: #007bff; border: none; padding: 12px; font-weight: 600; }
                '''
            },
            {
                'name': 'Подвал сайта',
                'type': 'footer',
                'html_content': '''
                <footer class="bg-dark text-white py-4">
                    <div class="container">
                        <div class="row">
                            <div class="col-md-6">
                                <h5>{{{company_name}}}</h5>
                                <p>{{{footer_description}}}</p>
                            </div>
                            <div class="col-md-6 text-md-end">
                                <p>{{{contact_info}}}</p>
                                <p>{{{copyright_text}}}</p>
                            </div>
                        </div>
                    </div>
                </footer>
                ''',
                'css_content': '''
                .bg-dark { background-color: #343a40 !important; }
                footer h5 { color: #fff; margin-bottom: 1rem; }
                footer p { color: #ccc; margin-bottom: 0.5rem; }
                '''
            }
        ]
        
        # Добавляем блоки в базу данных
        for block_data in blocks_data:
            existing_block = Block.query.filter_by(name=block_data['name']).first()
            if not existing_block:
                block = Block(**block_data)
                db.session.add(block)
                print(f"✅ Добавлен блок: {block_data['name']}")
            else:
                print(f"⏭️  Блок уже существует: {block_data['name']}")
        
        # Создаем примеры шаблонов
        templates_data = [
            {
                'name': 'Корпоративный сайт',
                'description': 'Профессиональный шаблон для бизнеса',
                'price': 0.0,
                'html_content': '''
                <!DOCTYPE html>
                <html lang="ru">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>{{{site_title}}}</title>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                    <style>{{{custom_css}}}</style>
                </head>
                <body>
                    {{{header_block}}}
                    {{{hero_block}}}
                    {{{content_block}}}
                    {{{services_block}}}
                    {{{contact_block}}}
                    {{{footer_block}}}
                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
                </body>
                </html>
                ''',
                'css_content': '''
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
                .hero-section { min-height: 60vh; }
                .card { transition: transform 0.3s; }
                .card:hover { transform: translateY(-5px); }
                '''
            },
            {
                'name': 'Лендинг страница',
                'description': 'Одностраничный сайт для продаж',
                'price': 0.0,
                'html_content': '''
                <!DOCTYPE html>
                <html lang="ru">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>{{{site_title}}}</title>
                    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                    <style>{{{custom_css}}}</style>
                </head>
                <body>
                    {{{hero_block}}}
                    {{{content_block}}}
                    {{{contact_block}}}
                    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
                </body>
                </html>
                ''',
                'css_content': '''
                body { font-family: 'Arial', sans-serif; }
                .hero-section { min-height: 80vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
                .btn-primary { background: linear-gradient(45deg, #667eea, #764ba2); border: none; }
                '''
            }
        ]
        
        # Добавляем шаблоны в базу данных
        for template_data in templates_data:
            existing_template = Template.query.filter_by(name=template_data['name']).first()
            if not existing_template:
                template = Template(**template_data)
                db.session.add(template)
                print(f"✅ Добавлен шаблон: {template_data['name']}")
            else:
                print(f"⏭️  Шаблон уже существует: {template_data['name']}")
        
        # Создаем тестового пользователя
        test_user = User.query.filter_by(username='admin').first()
        if not test_user:
            test_user = User(
                username='admin',
                email='admin@prothemesru.com',
                is_pro=True
            )
            test_user.set_password('admin123')
            db.session.add(test_user)
            print("✅ Создан тестовый пользователь: admin/admin123")
        else:
            print("⏭️  Тестовый пользователь уже существует")
        
        # Сохраняем все изменения
        db.session.commit()
        print("\n🎉 База данных успешно инициализирована!")
        print("\n📋 Что было создано:")
        print(f"   • {len(blocks_data)} блоков для конструктора")
        print(f"   • {len(templates_data)} шаблонов")
        print("   • Тестовый пользователь (admin/admin123)")
        print("\n🚀 Теперь вы можете:")
        print("   1. Запустить приложение: python run.py")
        print("   2. Войти как admin/admin123")
        print("   3. Использовать конструктор сайтов")

if __name__ == '__main__':
    init_database()
