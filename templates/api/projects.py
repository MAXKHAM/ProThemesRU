from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import Project, Block, ProjectBlock, db
from datetime import datetime

projects_bp = Blueprint('projects', __name__)

@projects_bp.route('/api/projects', methods=['GET'])
@login_required
def get_projects():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'created_at': project.created_at.isoformat(),
        'status': project.status,
        'blocks_count': len(project.blocks)
    } for project in projects])

@projects_bp.route('/api/projects/new', methods=['POST'])
@login_required
def create_project():
    data = request.json
    project = Project(
        name=data.get('name', 'Новый проект'),
        description=data.get('description', ''),
        user_id=current_user.id,
        content=data.get('content', '')
    )
    db.session.add(project)
    db.session.commit()
    return jsonify({
        'id': project.id,
        'name': project.name
    })

@projects_bp.route('/api/projects/<int:project_id>', methods=['GET'])
@login_required
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    blocks = ProjectBlock.query.filter_by(project_id=project_id).order_by(ProjectBlock.order).all()
    return jsonify({
        'id': project.id,
        'name': project.name,
        'description': project.description,
        'blocks': [{
            'id': block.block_id,
            'type': block.block.type,
            'name': block.block.name,
            'order': block.order,
            'settings': block.settings
        } for block in blocks]
    })
        } for block in blocks]
    })

@projects_bp.route('/api/projects/<int:project_id>/blocks', methods=['POST'])
@login_required
def add_block_to_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.json
    block_type = data.get('type')
    block = Block.query.filter_by(type=block_type).first()
    
    if not block:
        return jsonify({'error': 'Block not found'}), 404
    
    # Получаем максимальный порядок
    max_order = db.session.query(db.func.max(ProjectBlock.order))\
        .filter_by(project_id=project_id).scalar() or 0
    
    project_block = ProjectBlock(
        project_id=project_id,
        block_id=block.id,
        order=max_order + 1,
        settings=data.get('settings', {})
    )
    
    db.session.add(project_block)
    db.session.commit()
    
    return jsonify({
        'id': project_block.id,
        'type': block.type,
        'name': block.name,
        'order': project_block.order,
        'settings': project_block.settings
    })

@projects_bp.route('/api/projects/<int:project_id>/blocks/<int:block_id>', methods=['PUT'])
@login_required
def update_block_settings(project_id, block_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    project_block = ProjectBlock.query.get_or_404(block_id)
    if project_block.project_id != project_id:
        return jsonify({'error': 'Block not found'}), 404
    
    data = request.json
    project_block.settings = data.get('settings', {})
    project_block.order = data.get('order', project_block.order)
    db.session.commit()
    
    return jsonify({
        'id': project_block.id,
        'settings': project_block.settings,
        'order': project_block.order
    })

@projects_bp.route('/api/projects/<int:project_id>/publish', methods=['POST'])
@login_required
def publish_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.user_id != current_user.id:
        return jsonify({'error': 'Access denied'}), 403
    
    project.status = 'published'
    project.updated_at = datetime.utcnow()
    db.session.commit()
    
    # TODO: Добавить логику публикации сайта
    return jsonify({
        'status': 'success',
        'message': 'Проект опубликован'
    })
