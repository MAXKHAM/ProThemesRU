from flask import Blueprint, jsonify, request
from app.models import Template, Block, TemplateBlock, db
from datetime import datetime

templates_bp = Blueprint('templates', __name__)

@templates_bp.route('/api/templates', methods=['GET'])
def get_templates():
    category = request.args.get('category')
    templates = Template.query
    
    if category:
        templates = templates.filter_by(category=category)
    
    templates = templates.all()
    return jsonify([{
        'id': template.id,
        'name': template.name,
        'description': template.description,
        'preview_image': template.preview_image,
        'category': template.category,
        'features': template.features,
        'created_at': template.created_at.isoformat()
    } for template in templates])

@templates_bp.route('/api/templates/<int:template_id>', methods=['GET'])
def get_template(template_id):
    template = Template.query.get_or_404(template_id)
    blocks = TemplateBlock.query.filter_by(template_id=template_id).order_by(TemplateBlock.order).all()
    return jsonify({
        'id': template.id,
        'name': template.name,
        'description': template.description,
        'preview_image': template.preview_image,
        'category': template.category,
        'features': template.features,
        'blocks': [{
            'id': block.block_id,
            'type': block.block.type,
            'name': block.block.name,
            'order': block.order,
            'settings': block.settings
        } for block in blocks]
    })

@templates_bp.route('/api/templates/new', methods=['POST'])
@login_required
def create_template():
    data = request.json
    template = Template(
        name=data.get('name'),
        description=data.get('description'),
        preview_image=data.get('preview_image'),
        category=data.get('category'),
        features=data.get('features', {}),
        creator_id=current_user.id
    )
    db.session.add(template)
    db.session.commit()
    
    # Добавляем блоки
    blocks_data = data.get('blocks', [])
    for block_data in blocks_data:
        block = Block.query.get(block_data['id'])
        if block:
            template_block = TemplateBlock(
                template_id=template.id,
                block_id=block.id,
                order=block_data.get('order', 0),
                settings=block_data.get('settings', {})
            )
            db.session.add(template_block)
    
    db.session.commit()
    return jsonify({
        'id': template.id,
        'name': template.name
    })

@templates_bp.route('/api/templates/<int:template_id>/clone', methods=['POST'])
@login_required
def clone_template(template_id):
    template = Template.query.get_or_404(template_id)
    
    # Создаем новый шаблон
    new_template = Template(
        name=f"{template.name} (копия)",
        description=template.description,
        preview_image=template.preview_image,
        category=template.category,
        features=template.features,
        creator_id=current_user.id
    )
    db.session.add(new_template)
    db.session.commit()
    
    # Копируем блоки
    blocks = TemplateBlock.query.filter_by(template_id=template_id).all()
    for block in blocks:
        new_block = TemplateBlock(
            template_id=new_template.id,
            block_id=block.block_id,
            order=block.order,
            settings=block.settings
        )
        db.session.add(new_block)
    
    db.session.commit()
    return jsonify({
        'id': new_template.id,
        'name': new_template.name
    })

@templates_bp.route('/api/templates/<int:template_id>/preview', methods=['POST'])
def preview_template(template_id):
    template = Template.query.get_or_404(template_id)
    blocks = TemplateBlock.query.filter_by(template_id=template_id).order_by(TemplateBlock.order).all()
    
    preview_html = ''
    for block in blocks:
        block_html = block.block.html
        # Применяем настройки блока
        for key, value in block.settings.items():
            block_html = block_html.replace(f'{{{key}}}', str(value))
        preview_html += block_html
    
    return jsonify({
        'preview_html': preview_html,
        'styles': template.styles
    })
