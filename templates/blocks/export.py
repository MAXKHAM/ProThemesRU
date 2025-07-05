# Экспорт блоков в различные форматы

import json
import yaml
import csv
from pathlib import Path
from . import all_blocks, block_categories

class BlockExporter:
    """Класс для экспорта блоков в различные форматы"""
    
    def __init__(self, blocks=None, categories=None):
        self.blocks = blocks or all_blocks
        self.categories = categories or block_categories
    
    def export_to_json(self, file_path="blocks_export.json"):
        """Экспорт блоков в JSON формат"""
        export_data = {
            "metadata": {
                "version": "1.0",
                "total_blocks": len(self.blocks),
                "categories": self.categories
            },
            "blocks": self.blocks
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        return file_path
    
    def export_to_yaml(self, file_path="blocks_export.yaml"):
        """Экспорт блоков в YAML формат"""
        export_data = {
            "metadata": {
                "version": "1.0",
                "total_blocks": len(self.blocks),
                "categories": self.categories
            },
            "blocks": self.blocks
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(export_data, f, default_flow_style=False, allow_unicode=True)
        
        return file_path
    
    def export_to_csv(self, file_path="blocks_export.csv"):
        """Экспорт блоков в CSV формат"""
        with open(file_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Заголовки
            writer.writerow(['ID', 'Название', 'Категория', 'HTML', 'CSS', 'Свойства'])
            
            # Данные
            for block_id, block_data in self.blocks.items():
                writer.writerow([
                    block_id,
                    block_data.get('name', ''),
                    block_data.get('category', ''),
                    block_data.get('html', ''),
                    block_data.get('css', ''),
                    ', '.join(block_data.get('properties', []))
                ])
        
        return file_path
    
    def export_by_category(self, output_dir="exports"):
        """Экспорт блоков по категориям"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        exported_files = []
        
        for category in self.categories.keys():
            category_blocks = {k: v for k, v in self.blocks.items() 
                             if v.get('category') == category}
            
            if category_blocks:
                # JSON для категории
                json_file = output_path / f"{category}_blocks.json"
                with open(json_file, 'w', encoding='utf-8') as f:
                    json.dump(category_blocks, f, ensure_ascii=False, indent=2)
                exported_files.append(str(json_file))
                
                # HTML файл с примерами
                html_file = output_path / f"{category}_examples.html"
                self._create_html_examples(category_blocks, html_file)
                exported_files.append(str(html_file))
        
        return exported_files
    
    def _create_html_examples(self, blocks, file_path):
        """Создание HTML файла с примерами блоков"""
        html_content = f"""
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Примеры блоков</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .block-example {{ margin: 30px 0; padding: 20px; border: 1px solid #ddd; border-radius: 5px; }}
        .block-title {{ font-size: 1.2em; font-weight: bold; margin-bottom: 10px; color: #333; }}
        .block-category {{ color: #666; margin-bottom: 15px; }}
        .block-preview {{ margin: 15px 0; }}
        .block-code {{ background: #f5f5f5; padding: 15px; border-radius: 5px; overflow-x: auto; }}
        .block-properties {{ margin-top: 15px; }}
        .property-tag {{ display: inline-block; background: #007bff; color: white; padding: 2px 8px; border-radius: 3px; margin: 2px; font-size: 0.8em; }}
    </style>
</head>
<body>
    <h1>Примеры блоков</h1>
"""
        
        for block_id, block_data in blocks.items():
            html_content += f"""
    <div class="block-example">
        <div class="block-title">{block_data.get('name', 'Без названия')}</div>
        <div class="block-category">Категория: {block_data.get('category', 'Не указана')}</div>
        <div class="block-preview">
            {block_data.get('html', '')}
        </div>
        <div class="block-code">
            <strong>HTML:</strong><br>
            <pre>{block_data.get('html', '')}</pre>
        </div>
        <div class="block-code">
            <strong>CSS:</strong><br>
            <pre>{block_data.get('css', '')}</pre>
        </div>
        <div class="block-properties">
            <strong>Свойства:</strong><br>
            {''.join([f'<span class="property-tag">{prop}</span>' for prop in block_data.get('properties', [])])}
        </div>
    </div>
"""
        
        html_content += """
</body>
</html>
"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    def export_for_frontend(self, output_dir="frontend_blocks"):
        """Экспорт блоков в формате для фронтенда"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Создание JavaScript файла с блоками
        js_content = "// Блоки для фронтенда\n\n"
        js_content += "export const blocks = {\n"
        
        for block_id, block_data in self.blocks.items():
            js_content += f"  '{block_id}': {{\n"
            js_content += f"    name: '{block_data.get('name', '')}',\n"
            js_content += f"    category: '{block_data.get('category', '')}',\n"
            js_content += f"    html: `{block_data.get('html', '')}`,\n"
            js_content += f"    css: `{block_data.get('css', '')}`,\n"
            js_content += f"    properties: {json.dumps(block_data.get('properties', []))}\n"
            js_content += "  },\n"
        
        js_content += "};\n\n"
        js_content += f"export const categories = {json.dumps(self.categories, ensure_ascii=False)};\n"
        
        js_file = output_path / "blocks.js"
        with open(js_file, 'w', encoding='utf-8') as f:
            f.write(js_content)
        
        return str(js_file)

# Функции для быстрого экспорта
def export_all_formats(output_dir="exports"):
    """Экспорт блоков во всех форматах"""
    exporter = BlockExporter()
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    files = []
    
    # JSON
    json_file = exporter.export_to_json(output_path / "all_blocks.json")
    files.append(json_file)
    
    # YAML
    yaml_file = exporter.export_to_yaml(output_path / "all_blocks.yaml")
    files.append(yaml_file)
    
    # CSV
    csv_file = exporter.export_to_csv(output_path / "all_blocks.csv")
    files.append(csv_file)
    
    # По категориям
    category_files = exporter.export_by_category(output_path / "by_category")
    files.extend(category_files)
    
    # Для фронтенда
    frontend_file = exporter.export_for_frontend(output_path / "frontend")
    files.append(frontend_file)
    
    return files 