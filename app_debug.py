from flask import Flask, jsonify
import os

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'debug-secret-key')

@app.route('/')
def home():
    return jsonify({
        'message': 'ProThemesRU - Debug Version',
        'status': 'success',
        'version': '1.0.0'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Debug API is working',
        'database': 'not connected (debug mode)'
    })

@app.route('/api/test')
def test():
    return jsonify({
        'test': 'success',
        'message': 'Debug endpoint working'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 