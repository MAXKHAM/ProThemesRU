from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Enable CORS
CORS(app)

# Routes
@app.route('/')
def home():
    return jsonify({
        'message': 'ProThemesRU - Тестовая версия',
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
        'database': 'not connected (test mode)',
        'services': ['auth', 'templates', 'constructor', 'payments', 'admin'],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/templates')
def templates():
    return jsonify({
        'templates': [
            {
                'id': 1,
                'name': 'Бизнес-лендинг',
                'category': 'Бизнес',
                'price': 5000,
                'description': 'Современный лендинг для бизнеса'
            },
            {
                'id': 2,
                'name': 'Портфолио',
                'category': 'Портфолио',
                'price': 4000,
                'description': 'Стильное портфолио для творческих людей'
            },
            {
                'id': 3,
                'name': 'E-commerce',
                'category': 'Магазин',
                'price': 8000,
                'description': 'Полнофункциональный интернет-магазин'
            }
        ]
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    return jsonify({
        'message': 'User registered successfully (test mode)',
        'user': {
            'id': 1,
            'username': data['username'],
            'email': data['email'],
            'role': 'user'
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    return jsonify({
        'message': 'Login successful (test mode)',
        'user': {
            'id': 1,
            'username': data['username'],
            'role': 'user'
        }
    })

@app.route('/api/sites', methods=['GET'])
def get_sites():
    return jsonify({
        'sites': [
            {
                'id': 1,
                'name': 'Мой первый сайт',
                'is_published': False,
                'created_at': datetime.now().isoformat()
            }
        ]
    })

@app.route('/api/admin/dashboard', methods=['GET'])
def admin_dashboard():
    return jsonify({
        'stats': {
            'total_users': 10,
            'total_projects': 25,
            'total_orders': 15,
            'total_revenue': 150000.0,
            'active_templates': 30
        }
    })

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'operational',
        'uptime': '99.9%',
        'version': '1.0.0',
        'mode': 'test'
    })

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