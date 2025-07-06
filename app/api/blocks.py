from flask import Blueprint, jsonify, request
from flask_restx import Api, Resource, fields
import sys
import os
from app.models import Block

# Добавляем путь к системе блоков
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'site_blocks'))

try:
    from site_blocks import (
        all_blocks, 
        get_blocks_by_category, 
        get_block_by_id, 
        search_blocks,
        get_all_categories,
        get_blocks_count
    )
    from site_blocks.constructor import constructor
except ImportError as e:
    print(f"Ошибка импорта системы блоков: {e}")
    # Fallback данные
    all_blocks = {}
    get_blocks_by_category = lambda x: {}
    get_block_by_id = lambda x: None
    search_blocks = lambda x: {}
    get_all_categories = lambda: []
    get_blocks_count = lambda: {}
    constructor = None

# Создаем Blueprint для API блоков
blocks_bp = Blueprint('blocks', __name__)
api = Api(blocks_bp, title='Blocks API', description='API для работы с блоками конструктора')

# Модели для документации API
block_model = api.model('Block', {
    'id': fields.String(description='ID блока'),
    'name': fields.String(description='Название блока'),
    'category': fields.String(description='Категория блока'),
    'html': fields.String(description='HTML код блока'),
    'css': fields.String(description='CSS стили блока'),
    'properties': fields.List(fields.String, description='Доступные свойства')
})

category_model = api.model('Category', {
    'name': fields.String(description='Название категории'),
    'display_name': fields.String(description='Отображаемое название'),
    'block_count': fields.Integer(description='Количество блоков в категории')
})

@blocks_bp.route('/', methods=['GET'])
def get_blocks():
    """Получить все блоки"""
    blocks = Block.query.all()
    return jsonify([{
        'id': block.id,
        'type': block.type,
        'name': block.name,
        'html': block.html
    } for block in blocks])

@blocks_bp.route('/<int:block_id>', methods=['GET'])
def get_block(block_id):
    """Получить конкретный блок"""
    block = Block.query.get_or_404(block_id)
    return jsonify({
        'id': block.id,
        'type': block.type,
        'name': block.name,
        'html': block.html,
        'styles': block.styles
    })

@api.route('/categories')
class CategoriesList(Resource):
    @api.doc('get_categories')
    @api.marshal_list_with(category_model)
    def get(self):
        """Получить все категории блоков"""
        try:
            categories = get_all_categories()
            counts = get_blocks_count()
            
            categories_list = []
            for category in categories:
                categories_list.append({
                    'name': category,
                    'display_name': category.replace('_', ' ').title(),
                    'block_count': counts.get(category, 0)
                })
            return categories_list
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/categories/<string:category>')
class CategoryBlocks(Resource):
    @api.doc('get_blocks_by_category')
    @api.marshal_list_with(block_model)
    def get(self, category):
        """Получить блоки по категории"""
        try:
            category_blocks = get_blocks_by_category(category)
            blocks_list = []
            for block_id, block_data in category_blocks.items():
                blocks_list.append({
                    'id': block_id,
                    'name': block_data.get('name', ''),
                    'category': block_data.get('category', ''),
                    'html': block_data.get('html', ''),
                    'css': block_data.get('css', ''),
                    'properties': block_data.get('properties', [])
                })
            return blocks_list
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/search')
class SearchBlocks(Resource):
    @api.doc('search_blocks')
    @api.marshal_list_with(block_model)
    def get(self):
        """Поиск блоков по названию"""
        try:
            query = request.args.get('q', '')
            if not query:
                return []
            
            found_blocks = search_blocks(query)
            blocks_list = []
            for block_id, block_data in found_blocks.items():
                blocks_list.append({
                    'id': block_id,
                    'name': block_data.get('name', ''),
                    'category': block_data.get('category', ''),
                    'html': block_data.get('html', ''),
                    'css': block_data.get('css', ''),
                    'properties': block_data.get('properties', [])
                })
            return blocks_list
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/constructor/page')
class PageConstructor(Resource):
    @api.doc('get_page_structure')
    def get(self):
        """Получить структуру текущей страницы"""
        try:
            if constructor:
                return {
                    'blocks': constructor.get_page_structure(),
                    'html': constructor.get_page_html()
                }
            else:
                return {'error': 'Конструктор недоступен'}, 500
        except Exception as e:
            return {'error': str(e)}, 500

    @api.doc('add_block_to_page')
    def post(self):
        """Добавить блок на страницу"""
        try:
            if not constructor:
                return {'error': 'Конструктор недоступен'}, 500
            
            data = request.get_json()
            block_id = data.get('block_id')
            position = data.get('position')
            
            if not block_id:
                return {'error': 'block_id обязателен'}, 400
            
            block = constructor.add_block_to_page(block_id, position)
            return {
                'success': True,
                'block': block,
                'page_structure': constructor.get_page_structure()
            }
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/constructor/page/<string:block_id>')
class PageBlockManagement(Resource):
    @api.doc('update_block_property')
    def put(self, block_id):
        """Обновить свойство блока"""
        try:
            if not constructor:
                return {'error': 'Конструктор недоступен'}, 500
            
            data = request.get_json()
            property_name = data.get('property_name')
            property_value = data.get('property_value')
            
            if not property_name:
                return {'error': 'property_name обязателен'}, 400
            
            success = constructor.update_block_property(block_id, property_name, property_value)
            if success:
                return {
                    'success': True,
                    'page_structure': constructor.get_page_structure()
                }
            else:
                return {'error': 'Блок не найден'}, 404
        except Exception as e:
            return {'error': str(e)}, 500

    @api.doc('remove_block_from_page')
    def delete(self, block_id):
        """Удалить блок со страницы"""
        try:
            if not constructor:
                return {'error': 'Конструктор недоступен'}, 500
            
            success = constructor.remove_block_from_page(block_id)
            if success:
                return {
                    'success': True,
                    'page_structure': constructor.get_page_structure()
                }
            else:
                return {'error': 'Блок не найден'}, 404
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/constructor/page/save')
class SavePage(Resource):
    @api.doc('save_page')
    def post(self):
        """Сохранить страницу"""
        try:
            if not constructor:
                return {'error': 'Конструктор недоступен'}, 500
            
            data = request.get_json()
            file_path = data.get('file_path', 'page.json')
            
            success = constructor.save_page(file_path)
            if success:
                return {'success': True, 'file_path': file_path}
            else:
                return {'error': 'Ошибка сохранения'}, 500
        except Exception as e:
            return {'error': str(e)}, 500

@api.route('/constructor/page/load')
class LoadPage(Resource):
    @api.doc('load_page')
    def post(self):
        """Загрузить страницу"""
        try:
            if not constructor:
                return {'error': 'Конструктор недоступен'}, 500
            
            data = request.get_json()
            file_path = data.get('file_path', 'page.json')
            
            success = constructor.load_page(file_path)
            if success:
                return {
                    'success': True,
                    'page_structure': constructor.get_page_structure(),
                    'html': constructor.get_page_html()
                }
            else:
                return {'error': 'Ошибка загрузки'}, 500
        except Exception as e:
            return {'error': str(e)}, 500 