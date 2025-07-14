#!/usr/bin/env python3
"""
ProThemesRU - Финальная версия основного приложения
Полнофункциональная платформа для создания сайтов
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_cors import CORS
import os
import json
import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'prothemesru-secret-key-2024')
CORS(app)

# Конфигурация
app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Имитация базы данных
users_db = {}
projects_db = {}
orders_db = {}
templates_db = {
    '01': {'name': 'Gaming Template', 'price': 5000, 'category': 'gaming'},
    '02': {'name': 'Business Template', 'price': 3000, 'category': 'business'},
    '03': {'name': 'Portfolio Template', 'price': 4000, 'category': 'portfolio'},
    '04': {'name': 'E-commerce Template', 'price': 6000, 'category': 'ecommerce'},
    '05': {'name': 'Blog Template', 'price': 2500, 'category': 'blog'}
}

@app.route('/')
def index():
    """Главная страница"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Проверка работоспособности API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'version': '2.0.0',
        'service': 'ProThemesRU API'
    })

@app.route('/api/templates')
def get_templates():
    """Получение списка шаблонов"""
    return jsonify({
        'success': True,
        'templates': templates_db,
        'total': len(templates_db)
    })

@app.route('/api/templates/<template_id>')
def get_template(template_id):
    """Получение конкретного шаблона"""
    if template_id in templates_db:
        return jsonify({
            'success': True,
            'template': templates_db[template_id]
        })
    return jsonify({'success': False, 'error': 'Template not found'}), 404

@app.route('/api/projects', methods=['GET', 'POST'])
def projects():
    """Управление проектами"""
    if request.method == 'POST':
        data = request.get_json()
        project_id = str(uuid.uuid4())
        projects_db[project_id] = {
            'id': project_id,
            'name': data.get('name', 'New Project'),
            'template': data.get('template'),
            'created_at': datetime.datetime.now().isoformat(),
            'status': 'draft'
        }
        return jsonify({
            'success': True,
            'project': projects_db[project_id]
        })
    else:
        return jsonify({
            'success': True,
            'projects': list(projects_db.values())
        })

@app.route('/api/projects/<project_id>', methods=['GET', 'PUT', 'DELETE'])
def project_detail(project_id):
    """Детали проекта"""
    if project_id not in projects_db:
        return jsonify({'success': False, 'error': 'Project not found'}), 404
    
    if request.method == 'GET':
        return jsonify({
            'success': True,
            'project': projects_db[project_id]
        })
    elif request.method == 'PUT':
        data = request.get_json()
        projects_db[project_id].update(data)
        return jsonify({
            'success': True,
            'project': projects_db[project_id]
        })
    elif request.method == 'DELETE':
        del projects_db[project_id]
        return jsonify({'success': True, 'message': 'Project deleted'})

@app.route('/api/orders', methods=['GET', 'POST'])
def orders():
    """Управление заказами"""
    if request.method == 'POST':
        data = request.get_json()
        order_id = str(uuid.uuid4())
        orders_db[order_id] = {
            'id': order_id,
            'project_id': data.get('project_id'),
            'template_id': data.get('template_id'),
            'amount': data.get('amount', 0),
            'status': 'pending',
            'created_at': datetime.datetime.now().isoformat()
        }
        return jsonify({
            'success': True,
            'order': orders_db[order_id]
        })
    else:
        return jsonify({
            'success': True,
            'orders': list(orders_db.values())
        })

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Регистрация пользователя"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if email in users_db:
        return jsonify({'success': False, 'error': 'User already exists'}), 400
    
    user_id = str(uuid.uuid4())
    users_db[email] = {
        'id': user_id,
        'email': email,
        'password_hash': generate_password_hash(password),
        'created_at': datetime.datetime.now().isoformat(),
        'referral_code': str(uuid.uuid4())[:8].upper()
    }
    
    return jsonify({
        'success': True,
        'user': {
            'id': user_id,
            'email': email,
            'referral_code': users_db[email]['referral_code']
        }
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Вход пользователя"""
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if email not in users_db:
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    user = users_db[email]
    if not check_password_hash(user['password_hash'], password):
        return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
    
    session['user_id'] = user['id']
    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'referral_code': user['referral_code']
        }
    })

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """Выход пользователя"""
    session.pop('user_id', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route('/api/user/profile')
def user_profile():
    """Профиль пользователя"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    # Найти пользователя по ID
    user = None
    for email, user_data in users_db.items():
        if user_data['id'] == user_id:
            user = user_data
            break
    
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'user': {
            'id': user['id'],
            'email': user['email'],
            'referral_code': user['referral_code'],
            'created_at': user['created_at']
        }
    })

@app.route('/api/analytics')
def analytics():
    """Аналитика"""
    return jsonify({
        'success': True,
        'analytics': {
            'total_users': len(users_db),
            'total_projects': len(projects_db),
            'total_orders': len(orders_db),
            'total_revenue': sum(order['amount'] for order in orders_db.values()),
            'templates_used': len(set(project['template'] for project in projects_db.values() if project.get('template')))
        }
    })

@app.route('/api/referral/<referral_code>')
def referral_info(referral_code):
    """Информация о реферальной программе"""
    # Найти пользователя по реферальному коду
    referrer = None
    for email, user_data in users_db.items():
        if user_data['referral_code'] == referral_code:
            referrer = user_data
            break
    
    if not referrer:
        return jsonify({'success': False, 'error': 'Invalid referral code'}), 404
    
    return jsonify({
        'success': True,
        'referral': {
            'code': referral_code,
            'referrer_email': referrer['email']
        }
    })

@app.route('/webhook', methods=['POST'])
def telegram_webhook():
    """Webhook для Telegram бота"""
    data = request.get_json()
    
    # Обработка сообщений от Telegram
    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')
        
        # Простая обработка команд
        if text == '/start':
            response = {
                'chat_id': chat_id,
                'text': 'Добро пожаловать в ProThemesRU! 🚀\n\nСоздавайте профессиональные сайты легко и быстро!'
            }
        elif text == '/help':
            response = {
                'chat_id': chat_id,
                'text': 'Доступные команды:\n/start - Начать\n/help - Справка\n/templates - Шаблоны\n/create - Создать сайт'
            }
        else:
            response = {
                'chat_id': chat_id,
                'text': 'Используйте /help для просмотра доступных команд'
            }
        
        # Отправляем ответ (в реальном приложении здесь был бы вызов Telegram API)
        return jsonify({'success': True, 'response': response})
    
    return jsonify({'success': True})

@app.errorhandler(404)
def not_found(error):
    """Обработка 404 ошибки"""
    return jsonify({'success': False, 'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Обработка 500 ошибки"""
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("🚀 ProThemesRU запускается...")
    print(f"📍 Порт: {port}")
    print(f"🔧 Режим отладки: {debug}")
    print("✅ Готово! Откройте http://localhost:5000")
    
    app.run(host='0.0.0.0', port=port, debug=debug) 