import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from config import config_by_name

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
csrf = CSRFProtect()
cors = CORS()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    cors.init_app(app, resources={r"/ai/*": {"origins": "*"}})

    # Регистрируем основные blueprints
    from app.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/')
    
    from app.main.routes import main_bp
    app.register_blueprint(main_bp)
    
    from app.constructor_routes import constructor_bp
    app.register_blueprint(constructor_bp, url_prefix='/constructor')
    
    from app.payments.routes import payments_bp
    app.register_blueprint(payments_bp, url_prefix='/payments')
    
    from app.errors import errors_bp
    app.register_blueprint(errors_bp)

    # Регистрируем API Blueprint
    try:
        from app.api.routes import api_bp
        app.register_blueprint(api_bp)
    except ImportError:
        pass

    # Регистрируем API блоков
    try:
        from app.api.blocks import blocks_bp
        app.register_blueprint(blocks_bp, url_prefix='/api/blocks')
    except ImportError:
        pass

    # Регистрируем AI Blueprint
    try:
        from app.ai_routes import ai_bp
        app.register_blueprint(ai_bp, url_prefix='/ai')
    except ImportError:
        pass

    # Регистрируем Telegram Blueprint
    try:
        from app.telegram_bot.routes import telegram_bp
        app.register_blueprint(telegram_bp)
    except ImportError:
        pass

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/prothemesru.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('ProThemesRU startup')

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
