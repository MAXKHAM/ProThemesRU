from flask import Blueprint

ai_tools_bp = Blueprint('ai_tools', __name__)

from app.ai_tools import routes 