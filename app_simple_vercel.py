from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# In-memory storage (для демонстрации)
users = {}
sites = {}
templates = [
    {
        'id': 1,
        'name': 'Бизнес сайт',
        'category': 'business',
        'price': 0.0,
        'downloads': 150,
        'rating': 4.5
    },
    {
        'id': 2,
        'name': 'Портфолио',
        'category': 'portfolio',
        'price': 0.0,
        'downloads': 89,
        'rating': 4.8
    },
    {
        'id': 3,
        'name': 'Интернет-магазин',
        'category': 'ecommerce',
        'price': 0.0,
        'downloads': 234,
        'rating': 4.6
    },
    {
        'id': 4,
        'name': 'Блог',
        'category': 'blog',
        'price': 0.0,
        'downloads': 67,
        'rating': 4.7
    },
    {
        'id': 5,
        'name': 'Лендинг',
        'category': 'landing',
        'price': 0.0,
        'downloads': 312,
        'rating': 4.9
    }
]

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
    return jsonify({
        'status': 'healthy',
        'message': 'API работает',
        'database': 'in-memory',
        'templates_count': len(templates),
        'users_count': len(users),
        'sites_count': len(sites),
        'api_url': 'https://pro-themes-ru-maxkhams-projects.vercel.app',
        'timestamp': datetime.utcnow().isoformat()
    })

# Auth routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    username = data['username']
    if username in users:
        return jsonify({'error': 'Username already exists'}), 400
    
    user_id = len(users) + 1
    users[username] = {
        'id': user_id,
        'username': username,
        'email': data['email'],
        'password': data['password'],  # В реальном проекте хешируйте!
        'role': 'user',
        'created_at': datetime.utcnow().isoformat()
    }
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user_id,
            'username': username,
            'email': data['email'],
            'role': 'user'
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
    
    username = data['username']
    password = data['password']
    
    if username not in users or users[username]['password'] != password:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    user = users[username]
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role']
        }
    })

# Sites routes
@app.route('/api/sites', methods=['GET'])
def get_sites():
    # В реальном проекте проверяйте токен
    user_id = request.args.get('user_id', 1)
    
    user_sites = [site for site in sites.values() if site['user_id'] == int(user_id)]
    
    return jsonify({
        'sites': user_sites
    })

@app.route('/api/sites', methods=['POST'])
def create_site():
    data = request.get_json()
    
    if not data or not data.get('name'):
        return jsonify({'error': 'Site name is required'}), 400
    
    site_id = len(sites) + 1
    user_id = data.get('user_id', 1)
    
    site = {
        'id': site_id,
        'user_id': user_id,
        'name': data['name'],
        'elements': data.get('elements', ''),
        'canvas_settings': data.get('canvas_settings', ''),
        'created_at': datetime.utcnow().isoformat(),
        'updated_at': datetime.utcnow().isoformat(),
        'is_published': False,
        'published_url': None
    }
    
    sites[site_id] = site
    
    return jsonify({
        'message': 'Site created successfully',
        'site': {
            'id': site_id,
            'name': data['name'],
            'created_at': site['created_at']
        }
    }), 201

# Templates routes
@app.route('/api/templates', methods=['GET'])
def get_templates():
    return jsonify({
        'templates': templates
    })

@app.route('/api/templates/<int:template_id>', methods=['GET'])
def get_template(template_id):
    template = next((t for t in templates if t['id'] == template_id), None)
    
    if not template:
        return jsonify({'error': 'Template not found'}), 404
    
    return jsonify({
        'template': template
    })

# Admin routes
@app.route('/api/admin/dashboard', methods=['GET'])
def admin_dashboard():
    return jsonify({
        'dashboard': {
            'total_users': len(users),
            'total_sites': len(sites),
            'total_templates': len(templates),
            'active_users': len(users),
            'published_sites': len([s for s in sites.values() if s['is_published']])
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 