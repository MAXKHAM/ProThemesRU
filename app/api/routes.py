from flask import Blueprint, request, jsonify, current_app
from flask_restx import Api, Resource, Namespace
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash
import jwt
import datetime
import json
import os
from app.models import User, Block, Template

# Импортируем API блоков
try:
    from app.api.blocks import blocks_bp
except ImportError:
    blocks_bp = None

api_bp = Blueprint('api', __name__, url_prefix="/api")
api = Api(api_bp, version='1.0', title='ProThemesRU API',
          description='API для работы с конструктором сайтов и Telegram-ботом')

# Создаем namespace для аутентификации
auth_ns = Namespace('auth', description='Аутентификация API')
api.add_namespace(auth_ns)

# Создаем namespace для админки
admin_ns = Namespace('admin', description='Админские функции')
api.add_namespace(admin_ns)

# Создаем namespace для сайтов
sites_ns = Namespace('sites', description='Управление сайтами')
api.add_namespace(sites_ns)

# Создаем namespace для блоков
if blocks_bp:
    blocks_ns = Namespace('blocks', description='Управление блоками')
    api.add_namespace(blocks_ns)

# Файл для хранения данных сайта (в реальном проекте используйте базу данных)
SITE_DATA_FILE = 'site_data.json'

def generate_token(user_id):
    """Генерирует JWT токен для пользователя."""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def token_required(f):
    """Декоратор для проверки JWT токена."""
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            from app.models import User
            current_user = User.query.get(payload['user_id'])
            if not current_user:
                return jsonify({'message': 'Invalid token'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# --- АУТЕНТИФИКАЦИЯ ---
@auth_ns.route('/login')
class LoginAPI(Resource):
    def post(self):
        """Аутентификация пользователя и получение токена."""
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return {'message': 'Missing username or password'}, 400
        
        from app.models import User
        user = User.query.filter_by(username=data['username']).first()
        
        if user and user.check_password(data['password']):
            token = generate_token(user.id)
            return {
                'access_token': token,
                'user_id': user.id,
                'username': user.username,
                'is_pro': user.is_pro
            }
        else:
            return {'message': 'Invalid credentials'}, 401

# --- АДМИНСКИЕ ФУНКЦИИ ---
@admin_ns.route('/load_my_site_data')
class LoadSiteDataAPI(Resource):
    @token_required
    def get(self, current_user):
        """Загружает данные сайта из файла."""
        try:
            if os.path.exists(SITE_DATA_FILE):
                with open(SITE_DATA_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                return data
            else:
                return []
        except Exception as e:
            return {'error': str(e)}, 500

@admin_ns.route('/save_my_site_data')
class SaveSiteDataAPI(Resource):
    @token_required
    def post(self, current_user):
        """Сохраняет данные сайта в файл."""
        try:
            data = request.get_json()
            if not data:
                return {'error': 'No data provided'}, 400
            
            with open(SITE_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            return {'message': 'Site data saved successfully'}
        except Exception as e:
            return {'error': str(e)}, 500

# --- УПРАВЛЕНИЕ САЙТАМИ ---
@sites_ns.route('/export_site')
class ExportSiteAPI(Resource):
    @token_required
    def post(self, current_user):
        """Экспортирует сайт в ZIP-архив."""
        try:
            data = request.get_json()
            if not data or not data.get('elements'):
                return {'error': 'No site elements provided'}, 400
            
            # Здесь будет логика экспорта в ZIP
            # Пока возвращаем успешный ответ
            return {
                'message': 'Site exported successfully',
                'elements_count': len(data['elements'])
            }
        except Exception as e:
            return {'error': str(e)}, 500

@sites_ns.route('/publish_site')
class PublishSiteAPI(Resource):
    @token_required
    def post(self, current_user):
        """Публикует сайт."""
        try:
            data = request.get_json()
            if not data or not data.get('elements'):
                return {'error': 'No site elements provided'}, 400
            
            # Сохраняем данные сайта
            with open(SITE_DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(data['elements'], f, ensure_ascii=False, indent=2)
            
            return {'message': 'Site published successfully'}
        except Exception as e:
            return {'error': str(e)}, 500

# --- ОБЩИЕ API ---
@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'message': 'Hello from ProThemesRU API!'}

@api.route('/status')
class StatusAPI(Resource):
    def get(self):
        """Проверка статуса API."""
        return {
            'status': 'ok',
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'version': '1.0'
        }

@api_bp.route('/api/blocks', methods=['GET'])
def get_blocks():
    """Получить список всех блоков"""
    blocks = Block.query.all()
    return jsonify([{
        'id': block.id,
        'type': block.type,
        'name': block.name
    } for block in blocks])

@api_bp.route('/api/templates', methods=['GET'])
def get_templates():
    """Получить список всех шаблонов"""
    templates = Template.query.all()
    return jsonify([{
        'id': template.id,
        'name': template.name,
        'description': template.description,
        'category': template.category
    } for template in templates])
