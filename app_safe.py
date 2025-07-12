import os
import sys
from flask import Flask, jsonify

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'safe-secret-key')

# Try to import optional dependencies
try:
    from flask_cors import CORS
    CORS(app)
    CORS_AVAILABLE = True
except ImportError:
    CORS_AVAILABLE = False
    print("Warning: Flask-CORS not available")

try:
    from flask_sqlalchemy import SQLAlchemy
    from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
    from werkzeug.security import generate_password_hash, check_password_hash
    from datetime import datetime, timedelta
    
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///prothemesru.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
    
    # Initialize extensions
    db = SQLAlchemy(app)
    jwt = JWTManager(app)
    
    # Models
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password_hash = db.Column(db.String(255), nullable=False)
        role = db.Column(db.String(20), default='user')
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        is_active = db.Column(db.Boolean, default=True)
        name = db.Column(db.String(255))
        phone = db.Column(db.String(20))
        company = db.Column(db.String(255))

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
        price = db.Column(db.Float, nullable=False)
        downloads = db.Column(db.Integer, default=0)
        rating = db.Column(db.Float, default=0.0)
        status = db.Column(db.String(20), default='active')
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Create database tables
    with app.app_context():
        db.create_all()
    
    DB_AVAILABLE = True
    print("Database and JWT extensions loaded successfully")
    
except Exception as e:
    DB_AVAILABLE = False
    print(f"Warning: Database/JWT extensions not available: {e}")

# Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'ProThemesRU - Safe Version',
        'status': 'success',
        'version': '1.0.0',
        'database': 'connected' if DB_AVAILABLE else 'not available',
        'cors': 'enabled' if CORS_AVAILABLE else 'not available'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Safe API is working',
        'database': 'connected' if DB_AVAILABLE else 'not available',
        'cors': 'enabled' if CORS_AVAILABLE else 'not available'
    })

@app.route('/api/test')
def test():
    return jsonify({
        'test': 'success',
        'message': 'Safe endpoint working'
    })

# Auth routes (only if DB is available)
if DB_AVAILABLE:
    @app.route('/api/auth/register', methods=['POST'])
    def register():
        try:
            from flask import request
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
        except Exception as e:
            return jsonify({'error': f'Registration failed: {str(e)}'}), 500

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        try:
            from flask import request
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
        except Exception as e:
            return jsonify({'error': f'Login failed: {str(e)}'}), 500

    @app.route('/api/templates', methods=['GET'])
    def get_templates():
        try:
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
        except Exception as e:
            return jsonify({'error': f'Templates failed: {str(e)}'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 