from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

def create_app(config_name='default'):
    """Фабрика приложений Flask"""
    app = Flask(__name__)
    
    # Конфигурация
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    
    # Регистрация маршрутов
    with app.app_context():
        # Создаем таблицы базы данных
        db.create_all()
        
        # Регистрируем базовые маршруты
        @app.route('/')
        def index():
            return render_template('index.html')
        
        @app.route('/portfolio')
        def portfolio():
            return render_template('portfolio.html')
        
        @app.route('/about')
        def about():
            return render_template('about.html')
        
        @app.route('/login', methods=['GET', 'POST'])
        def login():
            if request.method == 'POST':
                user = User.query.filter_by(email=request.form.get('email')).first()
                if user and user.check_password(request.form.get('password')):
                    login_user(user)
                    return redirect(url_for('dashboard'))
                flash('Invalid email or password')
            return render_template('login.html')
        
        @app.route('/register', methods=['GET', 'POST'])
        def register():
            if request.method == 'POST':
                user = User(
                    username=request.form.get('username'),
                    email=request.form.get('email')
                )
                user.set_password(request.form.get('password'))
                db.session.add(user)
                db.session.commit()
                flash('Registration successful')
                return redirect(url_for('login'))
            return render_template('register.html')
        
        @app.route('/dashboard')
        @login_required
        def dashboard():
            projects = Project.query.filter_by(user_id=current_user.id).all()
            templates = Template.query.filter_by(creator_id=current_user.id).all()
            return render_template('dashboard.html', projects=projects, templates=templates)
        
        @app.route('/logout')
        @login_required
        def logout():
            logout_user()
            return redirect(url_for('index'))
    
    return app

# Создаем экземпляры расширений
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'

# Модели базы данных
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    projects = db.relationship('Project', backref='author', lazy=True)
    templates = db.relationship('Template', backref='creator', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='draft')
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    blocks = db.relationship('ProjectBlock', backref='project', lazy=True)
    settings = db.Column(db.JSON)

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    preview_image = db.Column(db.String(200))
    category = db.Column(db.String(50))
    features = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    projects = db.relationship('Project', backref='template', lazy=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blocks = db.relationship('TemplateBlock', backref='template', lazy=True)

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    html = db.Column(db.Text, nullable=False)
    styles = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи с проектами и шаблонами
    project_blocks = db.relationship('ProjectBlock', backref='block', lazy=True)
    template_blocks = db.relationship('TemplateBlock', backref='block', lazy=True)

class ProjectBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    block_id = db.Column(db.Integer, db.ForeignKey('block.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    settings = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TemplateBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False)
    block_id = db.Column(db.Integer, db.ForeignKey('block.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    settings = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
