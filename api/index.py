from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'ProThemesRU - Полнофункциональная платформа',
        'status': 'success',
        'version': '1.0.0',
        'api_url': 'https://pro-themes-ru-maxkhams-projects.vercel.app'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'API работает',
        'database': 'in-memory',
        'api_url': 'https://pro-themes-ru-maxkhams-projects.vercel.app'
    })

@app.route('/api/templates')
def get_templates():
    templates = [
        {'id': 1, 'name': 'Бизнес сайт', 'category': 'business', 'price': 0.0},
        {'id': 2, 'name': 'Портфолио', 'category': 'portfolio', 'price': 0.0},
        {'id': 3, 'name': 'Интернет-магазин', 'category': 'ecommerce', 'price': 0.0},
        {'id': 4, 'name': 'Блог', 'category': 'blog', 'price': 0.0},
        {'id': 5, 'name': 'Лендинг', 'category': 'landing', 'price': 0.0}
    ]
    return jsonify({'templates': templates})

@app.route('/api/auth/register', methods=['POST'])
def register():
    return jsonify({
        'message': 'User registered successfully',
        'user': {'id': 1, 'username': 'test', 'role': 'user'}
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    return jsonify({
        'message': 'Login successful',
        'user': {'id': 1, 'username': 'test', 'role': 'user'}
    })

@app.route('/api/sites')
def get_sites():
    sites = [
        {'id': 1, 'name': 'Мой первый сайт', 'created_at': '2024-01-01T00:00:00Z'}
    ]
    return jsonify({'sites': sites})

# Vercel serverless function handler
def handler(request, context):
    return app(request, context) 