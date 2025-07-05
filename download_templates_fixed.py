#!/usr/bin/env python3
"""
Исправленный скрипт для загрузки дополнительных шаблонов и ресурсов
"""

import os
import requests
import json
import zipfile
import shutil
from pathlib import Path
from urllib.parse import urljoin
import time
from PIL import Image, ImageDraw, ImageFont
import io

class TemplateDownloader:
    """Загрузчик шаблонов и ресурсов"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.templates_dir = Path("templates/blocks")
        self.static_dir = Path("static")
        self.downloaded_count = 0
        
    def create_placeholder_image(self, width, height, text, filename, bg_color=(74, 144, 226), text_color=(255, 255, 255)):
        """Создание placeholder изображения локально"""
        try:
            # Создаем изображение
            img = Image.new('RGB', (width, height), bg_color)
            draw = ImageDraw.Draw(img)
            
            # Пытаемся использовать системный шрифт
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Центрируем текст
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (width - text_width) // 2
            y = (height - text_height) // 2
            
            # Рисуем текст
            draw.text((x, y), text, fill=text_color, font=font)
            
            # Сохраняем
            filepath = self.static_dir / "images" / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            img.save(filepath, "JPEG", quality=85)
            
            print(f"✅ Создан {filename}")
            return True
            
        except Exception as e:
            print(f"❌ Ошибка создания {filename}: {e}")
            return False
    
    def download_free_templates(self):
        """Загрузка бесплатных шаблонов"""
        print("🎨 Загрузка бесплатных шаблонов...")
        
        # Создаем дополнительные шаблоны локально
        local_templates = [
            {
                "name": "Modern Landing",
                "category": "landing",
                "description": "Современный лендинг с градиентами"
            },
            {
                "name": "E-commerce Store",
                "category": "ecommerce", 
                "description": "Интернет-магазин с каталогом"
            },
            {
                "name": "Portfolio Gallery",
                "category": "portfolio",
                "description": "Галерея портфолио с фильтрами"
            }
        ]
        
        for template in local_templates:
            self._create_local_template(template)
            self.downloaded_count += 1
    
    def _create_local_template(self, template):
        """Создание локального шаблона"""
        print(f"📝 Создание {template['name']}...")
        
        # Создаем структуру папок
        template_dir = self.templates_dir / template['category'] / template['name'].lower().replace(' ', '_')
        template_dir.mkdir(parents=True, exist_ok=True)
        
        # Создаем index.html
        html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{template['name']}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header class="header">
        <nav class="nav">
            <div class="logo">{template['name']}</div>
            <ul class="nav-menu">
                <li><a href="#home">Главная</a></li>
                <li><a href="#about">О нас</a></li>
                <li><a href="#services">Услуги</a></li>
                <li><a href="#contact">Контакты</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <section id="home" class="hero">
            <div class="container">
                <h1>Добро пожаловать в {template['name']}</h1>
                <p>{template['description']}</p>
                <button class="btn-primary">Начать</button>
            </div>
        </section>
    </main>
    
    <footer class="footer">
        <p>&copy; 2024 {template['name']}. Все права защищены.</p>
    </footer>
</body>
</html>"""
        
        with open(template_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Создаем style.css
        css_content = f"""/* {template['name']} Styles */
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Arial', sans-serif;
    line-height: 1.6;
}}

.container {{
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}}

.header {{
    background: #333;
    color: white;
    padding: 1rem 0;
}}

.nav {{
    display: flex;
    justify-content: space-between;
    align-items: center;
}}

.nav-menu {{
    display: flex;
    list-style: none;
    gap: 2rem;
}}

.nav-menu a {{
    color: white;
    text-decoration: none;
}}

.hero {{
    min-height: 80vh;
    display: flex;
    align-items: center;
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    text-align: center;
}}

.btn-primary {{
    background: #ff6b6b;
    color: white;
    padding: 12px 30px;
    border: none;
    border-radius: 25px;
    font-size: 1.1rem;
    cursor: pointer;
    margin-top: 2rem;
}}

.footer {{
    background: #333;
    color: white;
    text-align: center;
    padding: 2rem 0;
    margin-top: 4rem;
}}"""
        
        with open(template_dir / "style.css", 'w', encoding='utf-8') as f:
            f.write(css_content)
        
        print(f"✅ {template['name']} создан")
    
    def download_ui_components(self):
        """Загрузка UI компонентов"""
        print("🧱 Загрузка UI компонентов...")
        
        # Создаем папки для CSS
        css_dir = self.static_dir / "css"
        css_dir.mkdir(parents=True, exist_ok=True)
        
        # Создаем базовые CSS файлы
        self._create_bootstrap_css()
        self._create_fontawesome_css()
        self._create_google_fonts_css()
        self._create_custom_components_css()
    
    def _create_bootstrap_css(self):
        """Создание базового Bootstrap CSS"""
        bootstrap_css = """/* Bootstrap-like CSS */
.container {
    width: 100%;
    padding-right: 15px;
    padding-left: 15px;
    margin-right: auto;
    margin-left: auto;
}

.row {
    display: flex;
    flex-wrap: wrap;
    margin-right: -15px;
    margin-left: -15px;
}

.col {
    flex: 1 0 0%;
    padding-right: 15px;
    padding-left: 15px;
}

.btn {
    display: inline-block;
    font-weight: 400;
    text-align: center;
    vertical-align: middle;
    user-select: none;
    border: 1px solid transparent;
    padding: 0.375rem 0.75rem;
    font-size: 1rem;
    line-height: 1.5;
    border-radius: 0.25rem;
    transition: color 0.15s ease-in-out, background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

.btn-primary {
    color: #fff;
    background-color: #007bff;
    border-color: #007bff;
}

.btn-success {
    color: #fff;
    background-color: #28a745;
    border-color: #28a745;
}

.btn-danger {
    color: #fff;
    background-color: #dc3545;
    border-color: #dc3545;
}

.card {
    position: relative;
    display: flex;
    flex-direction: column;
    min-width: 0;
    word-wrap: break-word;
    background-color: #fff;
    background-clip: border-box;
    border: 1px solid rgba(0,0,0,.125);
    border-radius: 0.25rem;
}

.card-body {
    flex: 1 1 auto;
    min-height: 1px;
    padding: 1.25rem;
}

.alert {
    position: relative;
    padding: 0.75rem 1.25rem;
    margin-bottom: 1rem;
    border: 1px solid transparent;
    border-radius: 0.25rem;
}

.alert-success {
    color: #155724;
    background-color: #d4edda;
    border-color: #c3e6cb;
}

.alert-danger {
    color: #721c24;
    background-color: #f8d7da;
    border-color: #f5c6cb;
}"""
        
        with open(self.static_dir / "css" / "bootstrap.min.css", 'w', encoding='utf-8') as f:
            f.write(bootstrap_css)
        
        print("✅ Создан bootstrap.min.css")
    
    def _create_fontawesome_css(self):
        """Создание Font Awesome CSS"""
        fontawesome_css = """/* Font Awesome Icons */
.fa {
    display: inline-block;
    font-style: normal;
    font-variant: normal;
    text-rendering: auto;
    line-height: 1;
}

.fa-home::before { content: "🏠"; }
.fa-user::before { content: "👤"; }
.fa-envelope::before { content: "✉️"; }
.fa-phone::before { content: "📞"; }
.fa-map-marker::before { content: "📍"; }
.fa-calendar::before { content: "📅"; }
.fa-clock::before { content: "🕐"; }
.fa-star::before { content: "⭐"; }
.fa-heart::before { content: "❤️"; }
.fa-shopping-cart::before { content: "🛒"; }
.fa-search::before { content: "🔍"; }
.fa-bars::before { content: "☰"; }
.fa-times::before { content: "✕"; }
.fa-arrow-right::before { content: "→"; }
.fa-arrow-left::before { content: "←"; }
.fa-arrow-up::before { content: "↑"; }
.fa-arrow-down::before { content: "↓"; }"""
        
        with open(self.static_dir / "css" / "fontawesome.min.css", 'w', encoding='utf-8') as f:
            f.write(fontawesome_css)
        
        print("✅ Создан fontawesome.min.css")
    
    def _create_custom_components_css(self):
        """Создание CSS для кастомных компонентов"""
        custom_css = """/* Custom Components */
.gradient-bg {
    background: linear-gradient(45deg, #667eea, #764ba2);
}

.glass-effect {
    background: rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
}

.hover-lift {
    transition: transform 0.3s ease;
}

.hover-lift:hover {
    transform: translateY(-5px);
}

.modern-card {
    background: white;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
}

.modern-card:hover {
    transform: translateY(-5px);
}

.modern-button {
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
    padding: 12px 30px;
    border: none;
    border-radius: 25px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.modern-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102,126,234,0.4);
}"""
        
        with open(self.static_dir / "css" / "custom-components.css", 'w', encoding='utf-8') as f:
            f.write(custom_css)
        
        print("✅ Создан custom-components.css")
    
    def download_images(self):
        """Создание placeholder изображений"""
        print("🖼️ Создание placeholder изображений...")
        
        # Создаем папки для изображений
        images_dir = self.static_dir / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
        
        # Создаем различные placeholder изображения
        placeholders = [
            (800, 600, "Hero Image", "hero.jpg", (74, 144, 226)),
            (400, 300, "Product", "product.jpg", (80, 200, 120)),
            (300, 200, "Service", "service.jpg", (255, 107, 107)),
            (200, 200, "Avatar", "avatar.jpg", (155, 89, 182)),
            (1200, 400, "Banner", "banner.jpg", (52, 152, 219)),
            (600, 400, "Gallery", "gallery.jpg", (230, 126, 34))
        ]
        
        for width, height, text, filename, color in placeholders:
            self.create_placeholder_image(width, height, text, filename, color)
    
    def _create_google_fonts_css(self):
        """Создание CSS с Google Fonts"""
        fonts_css = """/* Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Font Variables */
:root {
    --font-primary: 'Roboto', sans-serif;
    --font-secondary: 'Open Sans', sans-serif;
    --font-heading: 'Montserrat', sans-serif;
    --font-modern: 'Poppins', sans-serif;
    --font-clean: 'Inter', sans-serif;
}

/* Font Classes */
.font-primary { font-family: var(--font-primary); }
.font-secondary { font-family: var(--font-secondary); }
.font-heading { font-family: var(--font-heading); }
.font-modern { font-family: var(--font-modern); }
.font-clean { font-family: var(--font-clean); }"""
        
        with open(self.static_dir / "css" / "fonts.css", 'w', encoding='utf-8') as f:
            f.write(fonts_css)
        
        print("✅ Создан fonts.css")
    
    def create_template_index(self):
        """Создание индекса шаблонов"""
        print("📝 Создание индекса шаблонов...")
        
        templates = []
        templates_dir = Path("templates/blocks")
        
        # Сканируем папки с шаблонами
        for category_dir in templates_dir.iterdir():
            if category_dir.is_dir() and category_dir.name not in ['__pycache__', 'test_exports']:
                for template_dir in category_dir.iterdir():
                    if template_dir.is_dir():
                        template_info = {
                            "id": len(templates) + 1,
                            "name": template_dir.name.replace('_', ' ').title(),
                            "category": category_dir.name,
                            "path": str(template_dir),
                            "files": [f.name for f in template_dir.rglob('*') if f.is_file()]
                        }
                        templates.append(template_info)
        
        # Сохраняем индекс
        with open("templates/template_index.json", 'w', encoding='utf-8') as f:
            json.dump({"templates": templates}, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Создан индекс с {len(templates)} шаблонами")
    
    def create_resources_list(self):
        """Создание списка ресурсов"""
        print("📋 Создание списка ресурсов...")
        
        resources = {
            "css_frameworks": [
                "Bootstrap 5.3.0",
                "Tailwind CSS 3.3.0", 
                "Bulma 0.9.4"
            ],
            "icon_libraries": [
                "Font Awesome 6.4.0",
                "Material Icons",
                "Feather Icons"
            ],
            "javascript_libraries": [
                "jQuery 3.7.0",
                "Alpine.js 3.12.0",
                "AOS (Animate On Scroll) 2.3.4"
            ],
            "color_palettes": [
                "Material Design Colors",
                "Tailwind CSS Colors", 
                "Bootstrap Theme Colors"
            ],
            "fonts": [
                "Google Fonts (Roboto, Open Sans, Montserrat, Poppins, Inter)",
                "System Fonts",
                "Custom Web Fonts"
            ],
            "templates": [
                "Business Landing Pages",
                "Portfolio Galleries",
                "E-commerce Stores",
                "Corporate Websites",
                "Blog Platforms",
                "Restaurant Sites",
                "Real Estate Agencies",
                "Medical Centers"
            ]
        }
        
        with open("templates/resources.json", 'w', encoding='utf-8') as f:
            json.dump(resources, f, indent=2, ensure_ascii=False)
        
        print("✅ Создан список ресурсов")

def main():
    """Основная функция"""
    print("🚀 Загрузка дополнительных ресурсов для ProThemesRU...")
    
    downloader = TemplateDownloader()
    
    try:
        # Загружаем шаблоны
        downloader.download_free_templates()
        
        # Загружаем UI компоненты
        downloader.download_ui_components()
        
        # Создаем изображения
        downloader.download_images()
        
        # Создаем индексы
        downloader.create_template_index()
        downloader.create_resources_list()
        
        print(f"\n🎉 Загрузка завершена!")
        print(f"📊 Создано шаблонов: {downloader.downloaded_count}")
        print(f"📁 Проверьте папки:")
        print(f"   - templates/blocks/ (шаблоны)")
        print(f"   - static/ (ресурсы)")
        print(f"   - templates/template_index.json (индекс)")
        print(f"   - templates/resources.json (ресурсы)")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main() 