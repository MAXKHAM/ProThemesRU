#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстрация возможностей системы блоков ProThemesRU
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from site_blocks import (
    all_blocks, 
    get_blocks_by_category, 
    get_block_by_id,
    get_all_categories,
    get_blocks_count
)
from site_blocks.constructor import constructor
from site_blocks.export import export_all_formats

def demo_basic_usage():
    """Демонстрация базового использования"""
    print("🎯 ДЕМОНСТРАЦИЯ: Базовое использование")
    print("=" * 50)
    
    # Показать все доступные блоки
    print(f"📦 Всего доступно блоков: {len(all_blocks)}")
    
    # Показать категории
    categories = get_all_categories()
    print(f"📂 Категории: {', '.join(categories)}")
    
    # Показать количество по категориям
    counts = get_blocks_count()
    print("📊 Количество блоков по категориям:")
    for category, count in counts.items():
        if category != 'total':
            print(f"   {category}: {count}")
    
    print(f"   Итого: {counts['total']}")
    print()

def demo_block_examples():
    """Демонстрация примеров блоков"""
    print("🎨 ДЕМОНСТРАЦИЯ: Примеры блоков")
    print("=" * 50)
    
    # Показать примеры из каждой категории
    for category in get_all_categories():
        blocks = get_blocks_by_category(category)
        if blocks:
            print(f"\n📁 {category.upper()}:")
            for block_id, block_data in list(blocks.items())[:3]:  # Показать первые 3
                print(f"   • {block_data['name']} (ID: {block_id})")
                print(f"     HTML: {block_data['html'][:50]}...")
                print(f"     Свойства: {', '.join(block_data['properties'])}")
    
    print()

def demo_constructor_usage():
    """Демонстрация использования конструктора"""
    print("🔨 ДЕМОНСТРАЦИЯ: Использование конструктора")
    print("=" * 50)
    
    # Очистить страницу
    constructor.current_page_blocks = []
    
    # Создать простую страницу
    print("Создаем простую страницу...")
    
    # Добавляем блоки
    header = constructor.add_block_to_page('header')
    print(f"✅ Добавлен {header['name']}")
    
    hero = constructor.add_block_to_page('hero_section')
    print(f"✅ Добавлен {hero['name']}")
    
    about = constructor.add_block_to_page('about_section')
    print(f"✅ Добавлен {about['name']}")
    
    contact_form = constructor.add_block_to_page('contact_form')
    print(f"✅ Добавлен {contact_form['name']}")
    
    footer = constructor.add_block_to_page('footer')
    print(f"✅ Добавлен {footer['name']}")
    
    # Настраиваем блоки
    print("\nНастраиваем блоки...")
    constructor.update_block_property(hero['id'], 'title', 'Добро пожаловать в ProThemesRU!')
    constructor.update_block_property(hero['id'], 'subtitle', 'Создавайте потрясающие сайты за минуты')
    constructor.update_block_property(hero['id'], 'button-text', 'Начать создание')
    
    constructor.update_block_property(about['id'], 'title', 'О нашей платформе')
    constructor.update_block_property(about['id'], 'content', 'ProThemesRU - это современная платформа для создания веб-сайтов без навыков программирования.')
    
    # Показываем структуру
    print(f"\n📋 Структура страницы ({len(constructor.current_page_blocks)} блоков):")
    for block in constructor.current_page_blocks:
        print(f"   {block['position'] + 1}. {block['name']} ({block['category']})")
    
    # Генерируем HTML
    html = constructor.get_page_html()
    print(f"\n📄 Сгенерирован HTML ({len(html)} символов)")
    
    # Сохраняем страницу
    constructor.save_page('demo_page.json')
    print("💾 Страница сохранена в demo_page.json")
    
    print()

def demo_advanced_features():
    """Демонстрация продвинутых возможностей"""
    print("🚀 ДЕМОНСТРАЦИЯ: Продвинутые возможности")
    print("=" * 50)
    
    # Дублирование блока
    if constructor.current_page_blocks:
        original_block = constructor.current_page_blocks[0]
        duplicated = constructor.duplicate_block(original_block['id'])
        print(f"🔄 Дублирован блок: {duplicated['name']}")
    
    # Перемещение блока
    if len(constructor.current_page_blocks) > 2:
        constructor.move_block(constructor.current_page_blocks[1]['id'], 0)
        print("↔️ Блок перемещен на первую позицию")
    
    # Переключение видимости
    if constructor.current_page_blocks:
        block = constructor.current_page_blocks[0]
        constructor.toggle_block_visibility(block['id'])
        print(f"👁️ Видимость блока '{block['name']}' переключена")
    
    # Блокировка блока
    if constructor.current_page_blocks:
        block = constructor.current_page_blocks[0]
        constructor.lock_unlock_block(block['id'])
        print(f"🔒 Блок '{block['name']}' заблокирован")
    
    # Отмена действия
    constructor.undo()
    print("↩️ Последнее действие отменено")
    
    print()

def demo_export_features():
    """Демонстрация функций экспорта"""
    print("📤 ДЕМОНСТРАЦИЯ: Функции экспорта")
    print("=" * 50)
    
    try:
        # Экспорт во всех форматах
        print("Экспортируем блоки во всех форматах...")
        files = export_all_formats('demo_exports')
        
        print(f"📁 Экспортировано файлов: {len(files)}")
        for file_path in files:
            file_size = os.path.getsize(file_path)
            print(f"   📄 {os.path.basename(file_path)} ({file_size} байт)")
        
        print("✅ Экспорт завершен успешно")
        
    except Exception as e:
        print(f"❌ Ошибка экспорта: {e}")
    
    print()

def demo_search_and_filter():
    """Демонстрация поиска и фильтрации"""
    print("🔍 ДЕМОНСТРАЦИЯ: Поиск и фильтрация")
    print("=" * 50)
    
    # Поиск блоков
    search_queries = ['форма', 'галерея', 'видео', 'социаль']
    
    for query in search_queries:
        found_blocks = constructor.search_blocks(query)
        print(f"🔍 Поиск '{query}': найдено {len(found_blocks)} блоков")
        for block in found_blocks[:2]:  # Показать первые 2
            print(f"   • {block['name']} ({block['category']})")
    
    # Фильтрация по категориям
    print(f"\n📂 Блоки по категориям:")
    for category in get_all_categories():
        category_blocks = constructor.get_blocks_by_category(category)
        print(f"   {category}: {len(category_blocks)} блоков")
    
    print()

def demo_custom_blocks():
    """Демонстрация создания пользовательских блоков"""
    print("🎨 ДЕМОНСТРАЦИЯ: Пользовательские блоки")
    print("=" * 50)
    
    # Создание пользовательского блока
    custom_block = {
        "name": "Пользовательский виджет",
        "category": "interactive",
        "html": """
        <div class="custom-widget">
            <h3>{title}</h3>
            <div class="widget-content">
                <p>{description}</p>
                <button class="widget-btn" style="background: {button_color}">{button_text}</button>
            </div>
        </div>
        """,
        "css": """
        .custom-widget {
            border: 2px solid #007bff;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
        }
        .widget-btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            color: white;
            cursor: pointer;
            font-size: 16px;
        }
        """,
        "properties": ["title", "description", "button_text", "button_color"]
    }
    
    # Добавление в систему
    from site_blocks.interactive import interactive_blocks
    interactive_blocks["custom_widget"] = custom_block
    
    print("✅ Создан пользовательский блок 'Пользовательский виджет'")
    print(f"   Категория: {custom_block['category']}")
    print(f"   Свойства: {', '.join(custom_block['properties'])}")
    
    # Добавление на страницу
    widget = constructor.add_block_to_page('custom_widget')
    constructor.update_block_property(widget['id'], 'title', 'Мой виджет')
    constructor.update_block_property(widget['id'], 'description', 'Это мой собственный виджет!')
    constructor.update_block_property(widget['id'], 'button_text', 'Нажми меня')
    constructor.update_block_property(widget['id'], 'button_color', '#28a745')
    
    print("✅ Пользовательский блок добавлен на страницу")
    
    print()

def run_demo():
    """Запуск полной демонстрации"""
    print("🎪 ДЕМОНСТРАЦИЯ СИСТЕМЫ БЛОКОВ PROTHEMESRU")
    print("=" * 60)
    print()
    
    demo_basic_usage()
    demo_block_examples()
    demo_constructor_usage()
    demo_advanced_features()
    demo_export_features()
    demo_search_and_filter()
    demo_custom_blocks()
    
    print("🎉 ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА!")
    print("=" * 60)
    print("📁 Созданные файлы:")
    print("   • demo_page.json - Сохраненная страница")
    print("   • demo_exports/ - Папка с экспортированными файлами")
    print()
    print("🚀 Система готова к использованию!")

if __name__ == "__main__":
    run_demo() 