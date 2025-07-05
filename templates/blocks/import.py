# Импорт блоков из внешних источников

import json
import yaml
import csv
import requests
from pathlib import Path
from typing import Dict, List, Any

class BlockImporter:
    """Класс для импорта блоков из различных источников"""
    
    def __init__(self):
        self.imported_blocks = {}
        self.import_errors = []
    
    def import_from_json(self, file_path: str) -> Dict[str, Any]:
        """Импорт блоков из JSON файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if isinstance(data, dict):
                if 'blocks' in data:
                    blocks = data['blocks']
                else:
                    blocks = data
                
                self.imported_blocks.update(blocks)
                return blocks
            else:
                raise ValueError("Неверный формат JSON файла")
                
        except Exception as e:
            self.import_errors.append(f"Ошибка импорта из JSON {file_path}: {e}")
            return {}
    
    def import_from_yaml(self, file_path: str) -> Dict[str, Any]:
        """Импорт блоков из YAML файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if isinstance(data, dict):
                if 'blocks' in data:
                    blocks = data['blocks']
                else:
                    blocks = data
                
                self.imported_blocks.update(blocks)
                return blocks
            else:
                raise ValueError("Неверный формат YAML файла")
                
        except Exception as e:
            self.import_errors.append(f"Ошибка импорта из YAML {file_path}: {e}")
            return {}
    
    def import_from_csv(self, file_path: str) -> Dict[str, Any]:
        """Импорт блоков из CSV файла"""
        blocks = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    block_id = row.get('ID', '').strip()
                    if not block_id:
                        continue
                    
                    # Парсинг свойств
                    properties = []
                    if row.get('Свойства'):
                        properties = [p.strip() for p in row['Свойства'].split(',') if p.strip()]
                    
                    blocks[block_id] = {
                        'name': row.get('Название', ''),
                        'category': row.get('Категория', 'basic'),
                        'html': row.get('HTML', ''),
                        'css': row.get('CSS', ''),
                        'properties': properties
                    }
            
            self.imported_blocks.update(blocks)
            return blocks
            
        except Exception as e:
            self.import_errors.append(f"Ошибка импорта из CSV {file_path}: {e}")
            return {}
    
    def import_from_url(self, url: str) -> Dict[str, Any]:
        """Импорт блоков из URL"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Попытка парсинга как JSON
            try:
                data = response.json()
                if isinstance(data, dict) and 'blocks' in data:
                    blocks = data['blocks']
                else:
                    blocks = data
                
                self.imported_blocks.update(blocks)
                return blocks
                
            except json.JSONDecodeError:
                # Попытка парсинга как YAML
                try:
                    data = yaml.safe_load(response.text)
                    if isinstance(data, dict) and 'blocks' in data:
                        blocks = data['blocks']
                    else:
                        blocks = data
                    
                    self.imported_blocks.update(blocks)
                    return blocks
                    
                except yaml.YAMLError:
                    raise ValueError("Файл не является валидным JSON или YAML")
                    
        except Exception as e:
            self.import_errors.append(f"Ошибка импорта из URL {url}: {e}")
            return {}
    
    def import_from_directory(self, directory_path: str) -> Dict[str, Any]:
        """Импорт блоков из директории"""
        directory = Path(directory_path)
        if not directory.exists():
            self.import_errors.append(f"Директория не существует: {directory_path}")
            return {}
        
        all_blocks = {}
        
        # Поиск файлов блоков
        for file_path in directory.rglob("*"):
            if file_path.is_file():
                if file_path.suffix.lower() == '.json':
                    blocks = self.import_from_json(str(file_path))
                    all_blocks.update(blocks)
                elif file_path.suffix.lower() in ['.yaml', '.yml']:
                    blocks = self.import_from_yaml(str(file_path))
                    all_blocks.update(blocks)
                elif file_path.suffix.lower() == '.csv':
                    blocks = self.import_from_csv(str(file_path))
                    all_blocks.update(blocks)
        
        self.imported_blocks.update(all_blocks)
        return all_blocks
    
    def import_from_html_template(self, template_path: str) -> Dict[str, Any]:
        """Импорт блоков из HTML шаблона"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Извлечение блоков из HTML
            blocks = self._extract_blocks_from_html(html_content, template_path)
            self.imported_blocks.update(blocks)
            return blocks
            
        except Exception as e:
            self.import_errors.append(f"Ошибка импорта из HTML {template_path}: {e}")
            return {}
    
    def _extract_blocks_from_html(self, html_content: str, template_name: str) -> Dict[str, Any]:
        """Извлечение блоков из HTML контента"""
        blocks = {}
        
        # Поиск секций
        import re
        
        # Поиск header
        header_match = re.search(r'<header[^>]*>(.*?)</header>', html_content, re.DOTALL | re.IGNORECASE)
        if header_match:
            blocks[f"{template_name}_header"] = {
                'name': 'Header',
                'category': 'basic',
                'html': header_match.group(0),
                'css': '',
                'properties': ['text', 'background', 'padding']
            }
        
        # Поиск footer
        footer_match = re.search(r'<footer[^>]*>(.*?)</footer>', html_content, re.DOTALL | re.IGNORECASE)
        if footer_match:
            blocks[f"{template_name}_footer"] = {
                'name': 'Footer',
                'category': 'basic',
                'html': footer_match.group(0),
                'css': '',
                'properties': ['text', 'background', 'padding']
            }
        
        # Поиск секций
        section_matches = re.finditer(r'<section[^>]*>(.*?)</section>', html_content, re.DOTALL | re.IGNORECASE)
        for i, match in enumerate(section_matches):
            section_content = match.group(0)
            section_id = match.group(1).get('id', f'section_{i}')
            
            # Определение типа секции
            category = 'content'
            if 'hero' in section_content.lower() or 'banner' in section_content.lower():
                category = 'content'
            elif 'contact' in section_content.lower():
                category = 'content'
            elif 'about' in section_content.lower():
                category = 'content'
            
            blocks[f"{template_name}_{section_id}"] = {
                'name': f'Section {i+1}',
                'category': category,
                'html': section_content,
                'css': '',
                'properties': ['background', 'padding', 'text-color']
            }
        
        return blocks
    
    def validate_imported_blocks(self) -> List[str]:
        """Валидация импортированных блоков"""
        errors = []
        
        for block_id, block_data in self.imported_blocks.items():
            # Проверка обязательных полей
            if not isinstance(block_data, dict):
                errors.append(f"Блок {block_id}: должен быть словарем")
                continue
            
            if 'name' not in block_data:
                errors.append(f"Блок {block_id}: отсутствует поле 'name'")
            
            if 'category' not in block_data:
                errors.append(f"Блок {block_id}: отсутствует поле 'category'")
            
            if 'html' not in block_data:
                errors.append(f"Блок {block_id}: отсутствует поле 'html'")
            
            # Проверка категории
            valid_categories = ['basic', 'content', 'interactive', 'media', 'business', 'social']
            if 'category' in block_data and block_data['category'] not in valid_categories:
                errors.append(f"Блок {block_id}: недопустимая категория '{block_data['category']}'")
        
        return errors
    
    def get_import_summary(self) -> Dict[str, Any]:
        """Получение сводки импорта"""
        return {
            'total_imported': len(self.imported_blocks),
            'errors': len(self.import_errors),
            'import_errors': self.import_errors,
            'validation_errors': self.validate_imported_blocks(),
            'categories': self._count_by_category()
        }
    
    def _count_by_category(self) -> Dict[str, int]:
        """Подсчет блоков по категориям"""
        categories = {}
        for block_data in self.imported_blocks.values():
            category = block_data.get('category', 'unknown')
            categories[category] = categories.get(category, 0) + 1
        return categories

# Функции для быстрого импорта
def import_from_file(file_path: str) -> Dict[str, Any]:
    """Быстрый импорт из файла"""
    importer = BlockImporter()
    
    if file_path.endswith('.json'):
        return importer.import_from_json(file_path)
    elif file_path.endswith(('.yaml', '.yml')):
        return importer.import_from_yaml(file_path)
    elif file_path.endswith('.csv'):
        return importer.import_from_csv(file_path)
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {file_path}")

def import_from_directory(directory_path: str) -> Dict[str, Any]:
    """Быстрый импорт из директории"""
    importer = BlockImporter()
    return importer.import_from_directory(directory_path) 