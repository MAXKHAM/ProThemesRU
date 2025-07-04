
from flask import Blueprint
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app.models import User
from app import db

admin_bp = Blueprint('admin', __name__)

admin = Admin(name='ProThemesRU Admin', template_mode='bootstrap3')

def init_admin(app):
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
