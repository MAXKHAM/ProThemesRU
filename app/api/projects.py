from flask import Blueprint

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/api/projects')
def get_projects():
    return {'projects': []}

@projects_bp.route('/api/projects/new', methods=['POST'])
def create_project():
    return {'success': True}
