from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, Template, Project, db
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users', __name__)

@users_bp.route('/api/users/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already exists'}), 400

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    }), 201

@users_bp.route('/api/users/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()

    if user and check_password_hash(user.password_hash, data.get('password')):
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@users_bp.route('/api/users/profile', methods=['GET'])
@login_required
def get_profile():
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'created_at': current_user.created_at.isoformat(),
        'project_count': Project.query.filter_by(user_id=current_user.id).count(),
        'template_count': Template.query.filter_by(creator_id=current_user.id).count()
    })

@users_bp.route('/api/users/projects', methods=['GET'])
@login_required
def get_user_projects():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'status': project.status,
        'created_at': project.created_at.isoformat(),
        'blocks_count': len(project.blocks)
    } for project in projects])

@users_bp.route('/api/users/templates', methods=['GET'])
@login_required
def get_user_templates():
    templates = Template.query.filter_by(creator_id=current_user.id).all()
    return jsonify([{
        'id': template.id,
        'name': template.name,
        'description': template.description,
        'category': template.category,
        'created_at': template.created_at.isoformat(),
        'projects_count': len(template.projects)
    } for template in templates])

@users_bp.route('/api/users/upgrade', methods=['POST'])
@login_required
def upgrade_account():
    # TODO: Добавить логику повышения уровня аккаунта
    return jsonify({
        'status': 'success',
        'message': 'Account upgraded successfully'
    })
