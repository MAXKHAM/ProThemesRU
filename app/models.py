from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    telegram_id = db.Column(db.String(50), unique=True, nullable=True)
    ref_code = db.Column(db.String(50), unique=True, nullable=True)
    referred_by = db.Column(db.String(50), nullable=True)
    is_pro = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Связи с другими моделями
    orders = db.relationship('Order', backref='customer', lazy=True)
    user_sites = db.relationship('UserSite', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


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

class UserSite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    domain = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<UserSite {self.domain}>'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(20), default='pending')
    payment_method = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    transaction_id = db.Column(db.String(100), unique=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
    notes = db.Column(db.Text)

# Связи между моделями
db.Table('project_templates',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id')),
    db.Column('template_id', db.Integer, db.ForeignKey('template.id'))
)

db.Table('user_templates',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('template_id', db.Integer, db.ForeignKey('template.id'))
)
