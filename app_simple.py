from flask import Flask, jsonify
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Enable CORS
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'ProThemesRU API is running!',
        'status': 'success',
        'version': '1.0.0'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'API is working correctly',
        'database': 'connected',
        'services': ['auth', 'templates', 'constructor', 'payments']
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

@app.route('/api/features')
def features():
    return jsonify({
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

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'operational',
        'uptime': '99.9%',
        'last_deploy': '2024-01-01T00:00:00Z',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 