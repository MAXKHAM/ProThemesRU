from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///prothemesru.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)

# Initialize extensions
db = SQLAlchemy(app)
jwt = JWTManager(app)
CORS(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    elements = db.Column(db.Text)
    canvas_settings = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    published_url = db.Column(db.String(255))

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, default=0.0)
    downloads = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()
    
    # Create default templates if they don't exist
    if not Template.query.first():
        templates = [
            Template(name='Бизнес сайт', category='business', price=0.0),
            Template(name='Портфолио', category='portfolio', price=0.0),
            Template(name='Интернет-магазин', category='ecommerce', price=0.0),
            Template(name='Блог', category='blog', price=0.0),
            Template(name='Лендинг', category='landing', price=0.0)
        ]
        for template in templates:
            db.session.add(template)
        db.session.commit()

# Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'ProThemesRU - Полнофункциональная платформа',
        'status': 'success',
        'version': '1.0.0',
        'api_url': 'https://pro-themes-ru-maxkhams-projects.vercel.app',
        'features': [
            'Визуальный конструктор сайтов',
            'Готовые шаблоны',
            'Telegram бот',
            'Платежная система',
            'Админ панель'
        ]
    })

@app.route('/api/health')
def health():
    try:
        templates_count = Template.query.count()
        users_count = User.query.count()
        return jsonify({
            'status': 'healthy',
            'message': 'API работает',
            'database': 'connected',
            'templates_count': templates_count,
            'users_count': users_count,
            'api_url': 'https://pro-themes-ru-maxkhams-projects.vercel.app'
        })
    except Exception as e:
        return jsonify({
            'status': 'healthy',
            'message': 'API работает',
            'database': 'error',
            'error': str(e),
            'api_url': 'https://pro-themes-ru-maxkhams-projects.vercel.app'
        })

# Auth routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    })

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.isoformat()
        }
    })

# Sites routes
@app.route('/api/sites', methods=['GET'])
@jwt_required()
def get_sites():
    user_id = get_jwt_identity()
    sites = Site.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'sites': [{
            'id': site.id,
            'name': site.name,
            'created_at': site.created_at.isoformat(),
            'updated_at': site.updated_at.isoformat(),
            'is_published': site.is_published,
            'published_url': site.published_url
        } for site in sites]
    })

@app.route('/api/sites', methods=['POST'])
@jwt_required()
def create_site():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Site name is required'}), 400
    
    site = Site(
        user_id=user_id,
        name=data['name'],
        elements=data.get('elements', ''),
        canvas_settings=data.get('canvas_settings', '')
    )
    
    db.session.add(site)
    db.session.commit()
    
    return jsonify({
        'message': 'Site created successfully',
        'site': {
            'id': site.id,
            'name': site.name,
            'created_at': site.created_at.isoformat()
        }
    }), 201

@app.route('/api/sites/<int:site_id>', methods=['GET'])
@jwt_required()
def get_site(site_id):
    user_id = get_jwt_identity()
    site = Site.query.filter_by(id=site_id, user_id=user_id).first()
    
    if not site:
        return jsonify({'error': 'Site not found'}), 404
    
    return jsonify({
        'site': {
            'id': site.id,
            'name': site.name,
            'elements': site.elements,
            'canvas_settings': site.canvas_settings,
            'created_at': site.created_at.isoformat(),
            'updated_at': site.updated_at.isoformat(),
            'is_published': site.is_published,
            'published_url': site.published_url
        }
    })

@app.route('/api/sites/<int:site_id>', methods=['PUT'])
@jwt_required()
def update_site(site_id):
    user_id = get_jwt_identity()
    site = Site.query.filter_by(id=site_id, user_id=user_id).first()
    
    if not site:
        return jsonify({'error': 'Site not found'}), 404
    
    data = request.get_json()
    
    if data.get('name'):
        site.name = data['name']
    if data.get('elements'):
        site.elements = data['elements']
    if data.get('canvas_settings'):
        site.canvas_settings = data['canvas_settings']
    
    site.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Site updated successfully',
        'site': {
            'id': site.id,
            'name': site.name,
            'updated_at': site.updated_at.isoformat()
        }
    })

# Templates routes
@app.route('/api/templates', methods=['GET'])
def get_templates():
    templates = Template.query.filter_by(status='active').all()
    
    return jsonify({
        'templates': [{
            'id': template.id,
            'name': template.name,
            'category': template.category,
            'price': template.price,
            'downloads': template.downloads,
            'rating': template.rating,
            'created_at': template.created_at.isoformat()
        } for template in templates]
    })

@app.route('/api/templates/<int:template_id>', methods=['GET'])
def get_template(template_id):
    template = Template.query.get(template_id)
    
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    return jsonify({
        'template': {
            'id': template.id,
            'name': template.name,
            'category': template.category,
            'price': template.price,
            'downloads': template.downloads,
            'rating': template.rating,
            'created_at': template.created_at.isoformat()
        }
    })

# Admin routes
@app.route('/api/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user or user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    return jsonify({
        'dashboard': {
            'total_users': User.query.count(),
            'total_sites': Site.query.count(),
            'total_templates': Template.query.count(),
            'active_users': User.query.filter_by(is_active=True).count(),
            'published_sites': Site.query.filter_by(is_published=True).count()
        }
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 