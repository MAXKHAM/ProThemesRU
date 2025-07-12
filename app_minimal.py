from flask import Flask, jsonify
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

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
        'database': 'not connected',
        'services': ['basic', 'templates', 'constructor']
    })

@app.route('/api/templates')
def templates():
    return jsonify({
        'templates': [
            {
                'id': 1,
                'name': 'Бизнес-лендинг',
                'category': 'Бизнес',
                'price': 5000
            },
            {
                'id': 2,
                'name': 'Портфолио',
                'category': 'Портфолио',
                'price': 4000
            }
        ]
    })

@app.route('/api/status')
def status():
    return jsonify({
        'status': 'operational',
        'uptime': '99.9%',
        'version': '1.0.0'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 