# Система шаблонов для ProThemesRU

import os
from pathlib import Path

# Путь к шаблонам
TEMPLATES_PATH = Path(__file__).parent.parent.parent / "templates" / "blocks"

# Категории шаблонов
template_categories = {
    "business": "Бизнес сайты",
    "portfolio": "Портфолио",
    "blog": "Блоги",
    "ecommerce": "Интернет-магазины",
    "landing": "Лендинги",
    "corporate": "Корпоративные",
    "personal": "Персональные",
    "creative": "Креативные"
}

def get_available_templates():
    """Возвращает список доступных шаблонов"""
    templates = []
    
    if TEMPLATES_PATH.exists():
        for template_dir in TEMPLATES_PATH.iterdir():
            if template_dir.is_dir() and not template_dir.name.startswith('.'):
                template_info = {
                    "id": template_dir.name,
                    "name": template_dir.name.replace('_', ' ').title(),
                    "path": str(template_dir),
                    "category": "business",  # По умолчанию
                    "preview": None,
                    "files": []
                }
                
                # Поиск файлов шаблона
                for file_path in template_dir.rglob("*"):
                    if file_path.is_file():
                        template_info["files"].append(str(file_path.relative_to(template_dir)))
                        
                        # Поиск главной страницы
                        if file_path.name == "index.html":
                            template_info["main_file"] = str(file_path)
                        
                        # Поиск превью
                        if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png', '.gif']:
                            if 'preview' in file_path.name.lower() or 'screenshot' in file_path.name.lower():
                                template_info["preview"] = str(file_path)
                
                templates.append(template_info)
    
    return templates

def get_template_by_id(template_id):
    """Возвращает информацию о шаблоне по ID"""
    templates = get_available_templates()
    for template in templates:
        if template["id"] == template_id:
            return template
    return None

def get_templates_by_category(category):
    """Возвращает шаблоны по категории"""
    templates = get_available_templates()
    return [t for t in templates if t["category"] == category]

def search_templates(query):
    """Поиск шаблонов по названию"""
    query = query.lower()
    templates = get_available_templates()
    return [t for t in templates if query in t["name"].lower()]

def get_template_categories():
    """Возвращает список категорий шаблонов"""
    return template_categories

def get_template_content(template_id, file_name="index.html"):
    """Возвращает содержимое файла шаблона"""
    template = get_template_by_id(template_id)
    if not template:
        return None
    
    file_path = Path(template["path"]) / file_name
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Ошибка чтения файла: {e}"
    
    return None

def get_template_structure(template_id):
    """Возвращает структуру файлов шаблона"""
    template = get_template_by_id(template_id)
    if not template:
        return None
    
    structure = {
        "html_files": [],
        "css_files": [],
        "js_files": [],
        "image_files": [],
        "other_files": []
    }
    
    for file_path in template["files"]:
        if file_path.endswith('.html'):
            structure["html_files"].append(file_path)
        elif file_path.endswith('.css'):
            structure["css_files"].append(file_path)
        elif file_path.endswith('.js'):
            structure["js_files"].append(file_path)
        elif file_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg')):
            structure["image_files"].append(file_path)
        else:
            structure["other_files"].append(file_path)
    
    return structure 