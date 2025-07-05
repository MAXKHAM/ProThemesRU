#!/usr/bin/env python3
"""
Скрипт для загрузки дополнительных шаблонов и ресурсов
"""

import os
import requests
import json
import zipfile
import shutil
from pathlib import Path
from urllib.parse import urljoin
import time

class TemplateDownloader:
    """Загрузчик шаблонов и ресурсов"""
    
    def __init__(self):
        self.base_url = "https://api.github.com"
        self.templates_dir = Path("templates/blocks")
        self.static_dir = Path("static")
        self.downloaded_count = 0
        
    def download_free_templates(self):
        """Загрузка бесплатных шаблонов"""
        print("🎨 Загрузка бесплатных шаблонов...")
        
        # Список бесплатных шаблонов
        free_templates = [
            {
                "name": "Modern Business",
                "url": "https://github.com/StartBootstrap/startbootstrap-business-casual/archive/refs/heads/master.zip",
                "category": "business"
            },
            {
                "name": "Creative Portfolio",
                "url": "https://github.com/StartBootstrap/startbootstrap-creative/archive/refs/heads/master.zip",
                "category": "portfolio"
            },
            {
                "name": "Agency",
                "url": "https://github.com/StartBootstrap/startbootstrap-agency/archive/refs/heads/master.zip",
                "category": "agency"
            }
        ]
        
        for template in free_templates:
            try:
                self._download_template(template)
                self.downloaded_count += 1
                time.sleep(1)  # Пауза между загрузками
            except Exception as e:
                print(f"❌ Ошибка загрузки {template['name']}: {e}")
    
    def download_ui_components(self):
        """Загрузка UI компонентов"""
        print("🧱 Загрузка UI компонентов...")
        
        # Bootstrap компоненты
        bootstrap_url = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
        self._download_file(bootstrap_url, "static/css/bootstrap.min.css")
        
        # Font Awesome
        fontawesome_url = "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
        self._download_file(fontawesome_url, "static/css/fontawesome.min.css")
        
        # Google Fonts
        self._create_google_fonts_css()
    
    def download_images(self):
        """Загрузка изображений"""
        print("🖼️ Загрузка изображений...")
        
        # Создаем папки для изображений
        images_dir = self.static_dir / "images"
        images_dir.mkdir(parents=True, exist_ok=True)
        
        # Загружаем placeholder изображения
        placeholder_urls = [
            "https://via.placeholder.com/800x600/4A90E2/FFFFFF?text=Hero+Image",
            "https://via.placeholder.com/400x300/50C878/FFFFFF?text=Product",
            "https://via.placeholder.com/300x200/FF6B6B/FFFFFF?text=Service",
            "https://via.placeholder.com/200x200/9B59B6/FFFFFF?text=Avatar"
        ]
        
        for i, url in enumerate(placeholder_urls):
            filename = f"placeholder_{i+1}.jpg"
            self._download_file(url, f"static/images/{filename}")
    
    def _download_template(self, template):
        """Загрузка конкретного шаблона"""
        print(f"📥 Загрузка {template['name']}...")
        
        response = requests.get(template['url'], stream=True)
        response.raise_for_status()
        
        # Сохраняем во временный файл
        temp_file = f"temp_{template['name'].lower().replace(' ', '_')}.zip"
        with open(temp_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Распаковываем
        with zipfile.ZipFile(temp_file, 'r') as zip_ref:
            zip_ref.extractall(f"templates/blocks/{template['category']}")
        
        # Удаляем временный файл
        os.remove(temp_file)
        print(f"✅ {template['name']} загружен")
    
    def _download_file(self, url, filepath):
        """Загрузка файла"""
        response = requests.get(url)
        response.raise_for_status()
        
        # Создаем папки если нужно
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Загружен {filepath}")
    
    def _create_google_fonts_css(self):
        """Создание CSS с Google Fonts"""
        fonts_css = """
/* Google Fonts */
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
"""
        
        with open("static/css/fonts.css", 'w', encoding='utf-8') as f:
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
        
        # Загружаем изображения
        downloader.download_images()
        
        # Создаем индексы
        downloader.create_template_index()
        downloader.create_resources_list()
        
        print(f"\n🎉 Загрузка завершена!")
        print(f"📊 Загружено шаблонов: {downloader.downloaded_count}")
        print(f"📁 Проверьте папки:")
        print(f"   - templates/blocks/ (шаблоны)")
        print(f"   - static/ (ресурсы)")
        print(f"   - templates/template_index.json (индекс)")
        print(f"   - templates/resources.json (ресурсы)")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main() 