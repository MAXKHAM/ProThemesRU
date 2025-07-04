from flask import Blueprint

constructor_bp = Blueprint('constructor', __name__)

from app.constructor import routes 