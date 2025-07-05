from flask import Blueprint

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/users')
def get_users():
    return {'users': []}

@users_bp.route('/api/users/new', methods=['POST'])
def create_user():
    return {'success': True}
