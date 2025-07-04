from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.main import main_bp
from app.models import User
from app import db
import sys
import os

# Добавляем путь к системе блоков
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'site_blocks'))

try:
    from site_blocks import all_blocks, get_all_categories, get_blocks_count
    from site_blocks.constructor import constructor
    BLOCKS_AVAILABLE = True
except ImportError:
    BLOCKS_AVAILABLE = False
    all_blocks = {}
    get_all_categories = lambda: []
    get_blocks_count = lambda: {}
    constructor = None

@main_bp.route('/')
def index():
    """Главная страница"""
    return render_template('main/index.html')

@main_bp.route('/about')
def about():
    """Страница о проекте"""
    return render_template('main/about.html')

@main_bp.route('/contact')
def contact():
    """Контактная информация"""
    return render_template('main/contact.html')

@main_bp.route('/pricing')
def pricing():
    """Страница с тарифами"""
    return render_template('main/pricing.html')

@main_bp.route('/blocks-demo')
def blocks_demo():
    """Демонстрация системы блоков"""
    if not BLOCKS_AVAILABLE:
        flash('Система блоков недоступна', 'error')
        return redirect(url_for('main.index'))
    
    categories = get_all_categories()
    counts = get_blocks_count()
    
    # Группируем блоки по категориям
    blocks_by_category = {}
    for category in categories:
        blocks_by_category[category] = []
    
    for block_id, block_data in all_blocks.items():
        category = block_data.get('category', 'basic')
        if category in blocks_by_category:
            blocks_by_category[category].append({
                'id': block_id,
                'name': block_data.get('name', ''),
                'html': block_data.get('html', ''),
                'css': block_data.get('css', ''),
                'properties': block_data.get('properties', [])
            })
    
    return render_template('main/blocks_demo.html', 
                         blocks_by_category=blocks_by_category,
                         categories=categories,
                         counts=counts)

@main_bp.route('/blocks-api')
def blocks_api():
    """Страница с документацией API блоков"""
    return render_template('main/blocks_api.html')

@main_bp.route('/constructor-demo')
def constructor_demo():
    """Демонстрация конструктора"""
    if not BLOCKS_AVAILABLE or not constructor:
        flash('Конструктор недоступен', 'error')
        return redirect(url_for('main.index'))
    
    # Очищаем конструктор для демо
    constructor.current_page_blocks = []
    
    # Добавляем несколько блоков для демонстрации
    constructor.add_block_to_page('header')
    constructor.add_block_to_page('hero_section')
    constructor.add_block_to_page('about_section')
    constructor.add_block_to_page('footer')
    
    page_html = constructor.get_page_html()
    page_structure = constructor.get_page_structure()
    
    return render_template('main/constructor_demo.html',
                         page_html=page_html,
                         page_structure=page_structure,
                         available_blocks=all_blocks)

@main_bp.route('/api/blocks-info')
def blocks_info():
    """API endpoint для получения информации о блоках"""
    if not BLOCKS_AVAILABLE:
        return jsonify({'error': 'Система блоков недоступна'}), 500
    
    try:
        categories = get_all_categories()
        counts = get_blocks_count()
        
        blocks_list = []
        for block_id, block_data in all_blocks.items():
            blocks_list.append({
                'id': block_id,
                'name': block_data.get('name', ''),
                'category': block_data.get('category', ''),
                'properties': block_data.get('properties', [])
            })
        
        return jsonify({
            'total_blocks': len(all_blocks),
            'categories': categories,
            'counts': counts,
            'blocks': blocks_list
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/constructor/add-block', methods=['POST'])
def add_block_to_constructor():
    """API endpoint для добавления блока в конструктор"""
    if not BLOCKS_AVAILABLE or not constructor:
        return jsonify({'error': 'Конструктор недоступен'}), 500
    
    try:
        data = request.get_json()
        block_id = data.get('block_id')
        position = data.get('position')
        
        if not block_id:
            return jsonify({'error': 'block_id обязателен'}), 400
        
        block = constructor.add_block_to_page(block_id, position)
        return jsonify({
            'success': True,
            'block': block,
            'page_structure': constructor.get_page_structure()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/constructor/page-html')
def get_page_html():
    """API endpoint для получения HTML страницы"""
    if not BLOCKS_AVAILABLE or not constructor:
        return jsonify({'error': 'Конструктор недоступен'}), 500
    
    try:
        html = constructor.get_page_html()
        return jsonify({
            'html': html,
            'blocks_count': len(constructor.current_page_blocks)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/portfolio')
def portfolio():
    """Страница портфолио с шаблонами"""
    # Пример: получаем список шаблонов из templates/blocks
    import os
    templates_dir = os.path.join(os.path.dirname(__file__), '../../templates/blocks')
    try:
        template_folders = [f for f in os.listdir(templates_dir) if os.path.isdir(os.path.join(templates_dir, f))]
    except Exception:
        template_folders = []
    return render_template('main/portfolio.html', templates=template_folders) 