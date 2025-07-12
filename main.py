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
        'version': '1.0.0'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'API работает'
    })

@app.route('/api/test')
def test():
    return jsonify({
        'test': 'success',
        'message': 'Тестовая страница работает'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
