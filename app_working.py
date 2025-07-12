from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from datetime import datetime, timedelta

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///prothemesru.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MEDIA_FOLDER'] = 'media'
app.config['SCRAPED_FOLDER'] = 'scraped_sites'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MEDIA_FOLDER'], exist_ok=True)
os.makedirs(app.config['SCRAPED_FOLDER'], exist_ok=True)

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
    role = db.Column(db.String(20), default='user')  # user, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(255))  # Full name
    phone = db.Column(db.String(20))
    company = db.Column(db.String(255))

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    elements = db.Column(db.Text)  # JSON string
    canvas_settings = db.Column(db.Text)  # JSON string for canvas background
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    published_url = db.Column(db.String(255))

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    downloads = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, cancelled
    items = db.Column(db.Text)  # JSON string
    customer_info = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'ProThemesRU - Полнофункциональная платформа для создания сайтов',
        'status': 'success',
        'version': '1.0.0',
        'features': [
            'Визуальный конструктор сайтов',
            'Готовые шаблоны',
            'Адаптивный дизайн',
            'SEO оптимизация',
            'Telegram бот',
            'Платежная система',
            'Админ панель'
        ]
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'API работает корректно',
        'database': 'connected',
        'services': ['auth', 'templates', 'constructor', 'payments', 'admin'],
        'timestamp': datetime.now().isoformat()
    })

# Auth routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        name=data.get('name', ''),
        phone=data.get('phone', ''),
        company=data.get('company', '')
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.name,
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
    
    # Create access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'name': user.name,
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
            'name': user.name,
            'role': user.role,
            'created_at': user.created_at.isoformat()
        }
    })

# Site routes
@app.route('/api/sites', methods=['GET'])
@jwt_required()
def get_sites():
    user_id = get_jwt_identity()
    sites = Site.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'sites': [{
            'id': site.id,
            'name': site.name,
            'is_published': site.is_published,
            'created_at': site.created_at.isoformat(),
            'updated_at': site.updated_at.isoformat()
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
        elements=data.get('elements', '[]'),
        canvas_settings=data.get('canvas_settings', '{}')
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

# Template routes
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
            'status': template.status
        } for template in templates]
    })

# Admin routes
@app.route('/api/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get statistics
    total_users = User.query.count()
    total_projects = Site.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.amount)).filter_by(status='completed').scalar() or 0
    active_templates = Template.query.filter_by(status='active').count()
    
    return jsonify({
        'stats': {
            'total_users': total_users,
            'total_projects': total_projects,
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'active_templates': active_templates
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 