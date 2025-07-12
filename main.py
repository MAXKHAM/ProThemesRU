from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'ProThemesRU - Платформа для создания сайтов',
        'status': 'success',
        'version': '1.0.0',
        'bot': 'coming_soon'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'API работает',
        'bot': 'ready'
    })

@app.route('/api/test')
def test():
    return jsonify({
        'test': 'success',
        'message': 'Тестовая страница работает'
    })

@app.route('/api/bot/status')
def bot_status():
    return jsonify({
        'bot': 'development',
        'message': 'Бот в разработке',
        'eta': '24 hours'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
