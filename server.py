from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Simple in-memory storage
users = {}
sites = {}
site_counter = 1

@app.route('/')
def home():
    return jsonify({
        'message': 'ProThemesRU - Полнофункциональная платформа',
        'status': 'success',
        'version': '1.0.0',
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
        'users_count': len(users),
        'sites_count': len(sites)
    })

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if data['username'] in users:
        return jsonify({'error': 'Username already exists'}), 400
    
    user_id = len(users) + 1
    users[data['username']] = {
        'id': user_id,
        'username': data['username'],
        'email': data['email'],
        'password': data['password'],
        'role': 'user',
        'created_at': datetime.now().isoformat()
    }
    
    return jsonify({
        'message': 'User registered successfully',
        'user': {
            'id': user_id,
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
    
    user = users.get(data['username'])
    
    if not user or user['password'] != data['password']:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    return jsonify({
        'message': 'Login successful',
        'user': {
            'id': user['id'],
            'username': user['username'],
            'email': user['email'],
            'role': user['role']
        }
    })

@app.route('/api/sites', methods=['GET'])
def get_sites():
    username = request.args.get('username')
    if not username or username not in users:
        return jsonify({'error': 'User not found'}), 404
    
    user_sites = [site for site in sites.values() if site['user_id'] == users[username]['id']]
    
    return jsonify({
        'sites': user_sites
    })

@app.route('/api/sites', methods=['POST'])
def create_site():
    data = request.get_json()
    
    if not data or not data.get('name') or not data.get('username'):
        return jsonify({'error': 'Site name and username required'}), 400
    
    if data['username'] not in users:
        return jsonify({'error': 'User not found'}), 404
    
    global site_counter
    site = {
        'id': site_counter,
        'user_id': users[data['username']]['id'],
        'name': data['name'],
        'elements': data.get('elements', '[]'),
        'created_at': datetime.now().isoformat(),
        'is_published': False
    }
    
    sites[site_counter] = site
    site_counter += 1
    
    return jsonify({
        'message': 'Site created successfully',
        'site': site
    }), 201

@app.route('/api/templates', methods=['GET'])
def get_templates():
    return jsonify({
        'templates': [
            {
                'id': 1,
                'name': 'Бизнес сайт',
                'category': 'business',
                'price': 0,
                'preview': 'business.jpg'
            },
            {
                'id': 2,
                'name': 'Портфолио',
                'category': 'portfolio',
                'price': 0,
                'preview': 'portfolio.jpg'
            },
            {
                'id': 3,
                'name': 'Интернет-магазин',
                'category': 'ecommerce',
                'price': 0,
                'preview': 'shop.jpg'
            }
        ]
    })

@app.route('/api/admin/dashboard')
def admin_dashboard():
    return jsonify({
        'stats': {
            'total_users': len(users),
            'total_sites': len(sites),
            'total_templates': 3
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False) 