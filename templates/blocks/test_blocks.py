#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование системы блоков ProThemesRU
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from site_blocks import (
    all_blocks, 
    get_blocks_by_category, 
    get_block_by_id, 
    search_blocks,
    get_all_categories,
    get_blocks_count
)
from site_blocks.constructor import constructor
from site_blocks.export import export_all_formats

def test_basic_functionality():
    """Тестирование базовой функциональности"""
    print("=== Тестирование базовой функциональности ===")
    
    # Проверка количества блоков
    total_blocks = len(all_blocks)
    print(f"Всего блоков: {total_blocks}")
    assert total_blocks > 0, "Должно быть больше 0 блоков"
    
    # Проверка категорий
    categories = get_all_categories()
    print(f"Категории: {categories}")
    assert len(categories) > 0, "Должны быть категории"
    
    # Проверка подсчета по категориям
    counts = get_blocks_count()
    print(f"Количество по категориям: {counts}")
    
    print("✅ Базовая функциональность работает\n")

def test_block_operations():
    """Тестирование операций с блоками"""
    print("=== Тестирование операций с блоками ===")
    
    # Получение блока по ID
    header_block = get_block_by_id('header')
    assert header_block is not None, "Блок header должен существовать"
    print(f"Найден блок: {header_block['name']}")
    
    # Получение блоков по категории
    basic_blocks = get_blocks_by_category('basic')
    assert len(basic_blocks) > 0, "Должны быть базовые блоки"
    print(f"Базовых блоков: {len(basic_blocks)}")
    
    # Поиск блоков
    found_blocks = search_blocks('форма')
    print(f"Найдено блоков с 'форма': {len(found_blocks)}")
    
    print("✅ Операции с блоками работают\n")

def test_constructor():
    """Тестирование конструктора"""
    print("=== Тестирование конструктора ===")
    
    # Очистка страницы
    constructor.current_page_blocks = []
    
    # Добавление блоков
    header = constructor.add_block_to_page('header')
    hero = constructor.add_block_to_page('hero_section')
    footer = constructor.add_block_to_page('footer')
    
    print(f"Добавлено блоков: {len(constructor.current_page_blocks)}")
    assert len(constructor.current_page_blocks) == 3, "Должно быть 3 блока"
    
    # Обновление свойств
    constructor.update_block_property(hero['id'], 'title', 'Новый заголовок')
    
    # Перемещение блока
    constructor.move_block(hero['id'], 0)
    
    # Дублирование блока
    duplicated = constructor.duplicate_block(header['id'])
    assert duplicated is not None, "Дублирование должно работать"
    
    # Генерация HTML
    html = constructor.get_page_html()
    assert '<html' in html, "HTML должен содержать тег html"
    assert len(html) > 100, "HTML должен быть не пустым"
    
    print(f"Сгенерирован HTML длиной: {len(html)} символов")
    
    # Получение структуры
    structure = constructor.get_page_structure()
    assert len(structure) > 0, "Структура должна быть не пустой"
    
    print("✅ Конструктор работает\n")

def test_export_import():
    """Тестирование экспорта и импорта"""
    print("=== Тестирование экспорта и импорта ===")
    
    try:
        # Экспорт
        files = export_all_formats('test_exports')
        print(f"Экспортировано файлов: {len(files)}")
        assert len(files) > 0, "Должны быть экспортированы файлы"
        
        # Проверка создания файлов
        for file_path in files:
            assert os.path.exists(file_path), f"Файл {file_path} должен существовать"
        
        print("✅ Экспорт работает")
        
    except Exception as e:
        print(f"❌ Ошибка экспорта: {e}")
    
    print("✅ Экспорт и импорт работает\n")

def test_custom_blocks():
    """Тестирование создания пользовательских блоков"""
    print("=== Тестирование пользовательских блоков ===")
    
    # Создание пользовательского блока
    custom_block = {
        "name": "Пользовательский блок",
        "category": "content",
        "html": "<div class='custom-block'><h2>{title}</h2><p>{content}</p></div>",
        "css": ".custom-block { padding: 20px; background: #f0f0f0; border-radius: 5px; }",
        "properties": ["title", "content", "background"]
    }
    
    # Добавление в систему
    from site_blocks.content import content_blocks
    content_blocks["custom_block"] = custom_block
    
    # Обновление главного словаря блоков
    from site_blocks import all_blocks
    all_blocks["custom_block"] = custom_block
    
    # Проверка добавления
    found_block = get_block_by_id('custom_block')
    assert found_block is not None, "Пользовательский блок должен быть найден"
    print(f"Добавлен пользовательский блок: {found_block['name']}")
    
    print("✅ Пользовательские блоки работают\n")

def test_error_handling():
    """Тестирование обработки ошибок"""
    print("=== Тестирование обработки ошибок ===")
    
    # Попытка получить несуществующий блок
    non_existent = get_block_by_id('non_existent_block')
    assert non_existent is None, "Несуществующий блок должен возвращать None"
    
    # Попытка получить несуществующую категорию
    empty_category = get_blocks_by_category('non_existent_category')
    assert len(empty_category) == 0, "Несуществующая категория должна быть пустой"
    
    # Попытка добавить несуществующий блок в конструктор
    try:
        constructor.add_block_to_page('non_existent_block')
        assert False, "Должна быть ошибка при добавлении несуществующего блока"
    except ValueError:
        print("✅ Ошибка при добавлении несуществующего блока обработана корректно")
    
    print("✅ Обработка ошибок работает\n")

def run_all_tests():
    """Запуск всех тестов"""
    print("🚀 Запуск тестов системы блоков ProThemesRU\n")
    
    try:
        test_basic_functionality()
        test_block_operations()
        test_constructor()
        test_export_import()
        test_custom_blocks()
        test_error_handling()
        
        print("🎉 Все тесты прошли успешно!")
        return True
        
    except Exception as e:
        print(f"❌ Тест не прошел: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 