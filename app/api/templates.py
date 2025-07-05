from flask import Blueprint

templates_bp = Blueprint('templates', __name__)

@templates_bp.route('/api/templates')
def get_templates():
    return {'templates': []}

@templates_bp.route('/api/templates/new', methods=['POST'])
def create_template():
    return {'success': True}
