class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_super_secret_key_here_change_it_in_production!'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Telegram Bot Configuration
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    TELEGRAM_ADMIN_CHAT_ID = os.environ.get('TELEGRAM_ADMIN_CHAT_ID')
    
    # Flask Configuration
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
    DEBUG = os.environ.get('DEBUG', True)
    
    # API Configuration
    FLASK_API_BASE_URL = os.environ.get('FLASK_API_BASE_URL', 'http://127.0.0.1:5000/api')
    FLASK_PUBLIC_SITE_URL = os.environ.get('FLASK_PUBLIC_SITE_URL', 'http://127.0.0.1:5000/public')
    FLASK_EDITOR_URL = os.environ.get('FLASK_EDITOR_URL', 'http://localhost:3000')
