# Интеграция блоков с конструктором сайтов

import json
from typing import Dict, List, Any, Optional
from . import all_blocks, get_blocks_by_category, get_block_by_id

class BlockConstructor:
    """Класс для работы с блоками в конструкторе"""
    
    def __init__(self):
        self.available_blocks = all_blocks
        self.current_page_blocks = []
        self.block_history = []
        self.max_history = 50
    
    def add_block_to_page(self, block_id: str, position: int = None) -> Dict[str, Any]:
        """Добавление блока на страницу"""
        block_data = get_block_by_id(block_id)
        if not block_data:
            raise ValueError(f"Блок с ID '{block_id}' не найден")
        
        # Создание копии блока для страницы
        page_block = {
            'id': f"{block_id}_{len(self.current_page_blocks)}",
            'block_id': block_id,
            'name': block_data['name'],
            'category': block_data['category'],
            'html': block_data['html'],
            'css': block_data['css'],
            'properties': block_data['properties'].copy(),
            'custom_properties': {},
            'position': position or len(self.current_page_blocks),
            'visible': True,
            'locked': False
        }
        
        # Добавление в указанную позицию или в конец
        if position is not None and 0 <= position <= len(self.current_page_blocks):
            self.current_page_blocks.insert(position, page_block)
            # Обновление позиций
            for i, block in enumerate(self.current_page_blocks):
                block['position'] = i
        else:
            self.current_page_blocks.append(page_block)
        
        # Добавление в историю
        self._add_to_history('add', page_block)
        
        return page_block
    
    def remove_block_from_page(self, block_id: str) -> bool:
        """Удаление блока со страницы"""
        for i, block in enumerate(self.current_page_blocks):
            if block['id'] == block_id:
                removed_block = self.current_page_blocks.pop(i)
                # Обновление позиций
                for j, block in enumerate(self.current_page_blocks):
                    block['position'] = j
                
                self._add_to_history('remove', removed_block)
                return True
        
        return False
    
    def move_block(self, block_id: str, new_position: int) -> bool:
        """Перемещение блока на новую позицию"""
        if new_position < 0 or new_position >= len(self.current_page_blocks):
            return False
        
        for i, block in enumerate(self.current_page_blocks):
            if block['id'] == block_id:
                if i == new_position:
                    return True
                
                # Перемещение блока
                moved_block = self.current_page_blocks.pop(i)
                self.current_page_blocks.insert(new_position, moved_block)
                
                # Обновление позиций
                for j, block in enumerate(self.current_page_blocks):
                    block['position'] = j
                
                self._add_to_history('move', moved_block, {'old_position': i, 'new_position': new_position})
                return True
        
        return False
    
    def update_block_property(self, block_id: str, property_name: str, property_value: Any) -> bool:
        """Обновление свойства блока"""
        for block in self.current_page_blocks:
            if block['id'] == block_id:
                old_value = block['custom_properties'].get(property_name)
                block['custom_properties'][property_name] = property_value
                
                self._add_to_history('update_property', block, {
                    'property': property_name,
                    'old_value': old_value,
                    'new_value': property_value
                })
                return True
        
        return False
    
    def duplicate_block(self, block_id: str) -> Optional[Dict[str, Any]]:
        """Дублирование блока"""
        for block in self.current_page_blocks:
            if block['id'] == block_id:
                # Создание копии блока
                duplicated_block = block.copy()
                duplicated_block['id'] = f"{block['block_id']}_{len(self.current_page_blocks)}"
                duplicated_block['position'] = len(self.current_page_blocks)
                
                self.current_page_blocks.append(duplicated_block)
                self._add_to_history('duplicate', duplicated_block, {'original_id': block_id})
                
                return duplicated_block
        
        return None
    
    def toggle_block_visibility(self, block_id: str) -> bool:
        """Переключение видимости блока"""
        for block in self.current_page_blocks:
            if block['id'] == block_id:
                old_visible = block['visible']
                block['visible'] = not block['visible']
                
                self._add_to_history('toggle_visibility', block, {
                    'old_visible': old_visible,
                    'new_visible': block['visible']
                })
                return True
        
        return False
    
    def lock_unlock_block(self, block_id: str) -> bool:
        """Блокировка/разблокировка блока"""
        for block in self.current_page_blocks:
            if block['id'] == block_id:
                old_locked = block['locked']
                block['locked'] = not block['locked']
                
                self._add_to_history('lock_unlock', block, {
                    'old_locked': old_locked,
                    'new_locked': block['locked']
                })
                return True
        
        return False
    
    def get_page_html(self) -> str:
        """Генерация HTML страницы"""
        html_parts = ['<!DOCTYPE html>', '<html lang="ru">', '<head>', '<meta charset="UTF-8">']
        
        # CSS стили
        css_styles = []
        for block in self.current_page_blocks:
            if block['visible'] and block['css']:
                css_styles.append(block['css'])
        
        if css_styles:
            html_parts.append('<style>')
            html_parts.extend(css_styles)
            html_parts.append('</style>')
        
        html_parts.append('</head>')
        html_parts.append('<body>')
        
        # HTML контент
        for block in self.current_page_blocks:
            if block['visible']:
                html_parts.append(block['html'])
        
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        return '\n'.join(html_parts)
    
    def get_page_structure(self) -> List[Dict[str, Any]]:
        """Получение структуры страницы"""
        return [
            {
                'id': block['id'],
                'name': block['name'],
                'category': block['category'],
                'position': block['position'],
                'visible': block['visible'],
                'locked': block['locked'],
                'properties': block['custom_properties']
            }
            for block in self.current_page_blocks
        ]
    
    def save_page(self, file_path: str) -> bool:
        """Сохранение страницы в файл"""
        try:
            page_data = {
                'blocks': self.current_page_blocks,
                'html': self.get_page_html(),
                'structure': self.get_page_structure()
            }
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(page_data, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Ошибка сохранения страницы: {e}")
            return False
    
    def load_page(self, file_path: str) -> bool:
        """Загрузка страницы из файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                page_data = json.load(f)
            
            if 'blocks' in page_data:
                self.current_page_blocks = page_data['blocks']
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Ошибка загрузки страницы: {e}")
            return False
    
    def undo(self) -> bool:
        """Отмена последнего действия"""
        if not self.block_history:
            return False
        
        last_action = self.block_history.pop()
        action_type = last_action['type']
        
        if action_type == 'add':
            # Удаляем добавленный блок
            return self.remove_block_from_page(last_action['block']['id'])
        elif action_type == 'remove':
            # Возвращаем удаленный блок
            return self.add_block_to_page(last_action['block']['block_id'], last_action['block']['position'])
        elif action_type == 'move':
            # Возвращаем блок на исходную позицию
            old_position = last_action['metadata']['old_position']
            return self.move_block(last_action['block']['id'], old_position)
        elif action_type == 'update_property':
            # Возвращаем старое значение свойства
            property_name = last_action['metadata']['property']
            old_value = last_action['metadata']['old_value']
            return self.update_block_property(last_action['block']['id'], property_name, old_value)
        
        return False
    
    def _add_to_history(self, action_type: str, block: Dict[str, Any], metadata: Dict[str, Any] = None):
        """Добавление действия в историю"""
        history_entry = {
            'type': action_type,
            'block': block,
            'metadata': metadata or {}
        }
        
        self.block_history.append(history_entry)
        
        # Ограничение размера истории
        if len(self.block_history) > self.max_history:
            self.block_history.pop(0)
    
    def get_blocks_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Получение блоков по категории"""
        category_blocks = get_blocks_by_category(category)
        return [
            {
                'id': block_id,
                'name': block_data['name'],
                'category': block_data['category'],
                'preview_html': block_data['html'][:100] + '...' if len(block_data['html']) > 100 else block_data['html']
            }
            for block_id, block_data in category_blocks.items()
        ]
    
    def search_blocks(self, query: str) -> List[Dict[str, Any]]:
        """Поиск блоков"""
        from . import search_blocks
        
        found_blocks = search_blocks(query)
        return [
            {
                'id': block_id,
                'name': block_data['name'],
                'category': block_data['category'],
                'preview_html': block_data['html'][:100] + '...' if len(block_data['html']) > 100 else block_data['html']
            }
            for block_id, block_data in found_blocks.items()
        ]

# Глобальный экземпляр конструктора
constructor = BlockConstructor() 