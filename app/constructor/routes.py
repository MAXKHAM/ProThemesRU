from flask import render_template, send_file, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.constructor import constructor_bp
from app.models import Template, Block, UserSite
from app.utils.exporter import export_site_as_zip
import zipfile
import os
import json
from io import BytesIO
from app.constructor.blocks import HeaderBlock, HeroSectionBlock, TextBlock, ImageBlock, ButtonBlock, FooterBlock, WebsitePage, CalculatorBlock

@constructor_bp.route('/')
@login_required
def constructor():
    if not current_user.is_pro:
        flash('Доступ к конструктору только для PRO-пользователей.', 'warning')
        return redirect(url_for('main.index'))
    return render_template('constructor.html', title='Constructor')

@constructor_bp.route('/download_zip')
@login_required
def download_zip():
    if not current_user.is_pro:
        flash('Скачивание ZIP доступно только для PRO-пользователей.', 'warning')
        return redirect(url_for('constructor.constructor'))
    zip_path = 'example.zip'
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.writestr('example.txt', 'This is a sample file.')
    return send_file(zip_path, as_attachment=True, download_name='project.zip')

@constructor_bp.route('/generate_site', methods=['POST'])
@login_required
def generate_site():
    data = request.json
    
    # Создаем сайт
    site = WebsitePage(
        title=data.get('title', 'Новый сайт'),
        background_color=data.get('background_color', '#ffffff'),
        background_image=data.get('background_image'),
        font_family=data.get('font_family', 'Arial')
    )
    
    # Добавляем блоки
    blocks = data.get('blocks', [])
    for block_data in blocks:
        block_type = block_data.get('type')
        block_id = block_data.get('id')
        
        if block_type == 'header':
            site.add_block(
                HeaderBlock(
                    block_id=block_id,
                    logo_text=data.get('logo_text', 'Мой сайт'),
                    nav_items=data.get('nav_items', {})
                )
            )
        elif block_type == 'hero':
            site.add_block(
                HeroSectionBlock(
                    block_id=block_id,
                    title=block_data.get('title', 'Добро пожаловать'),
                    description=block_data.get('description', ''),
                    background_image=block_data.get('background_image')
                )
            )
        elif block_type == 'text':
            site.add_block(
                TextBlock(
                    block_id=block_id,
                    content=block_data.get('content', '')
                )
            )
        elif block_type == 'image':
            site.add_block(
                ImageBlock(
                    block_id=block_id,
                    image_url=block_data.get('image_url', ''),
                    alt_text=block_data.get('alt_text', '')
                )
            )
        elif block_type == 'button':
            site.add_block(
                ButtonBlock(
                    block_id=block_id,
                    text=block_data.get('text', 'Кнопка'),
                    link=block_data.get('link', '#')
                )
            )
    
    # Сохраняем сайт в базу данных
    try:
        user_site = UserSite(
            user_id=current_user.id,
            domain=f'site-{current_user.id}-{site.id}.prothemes.ru',
            is_active=True
        )
        from app import db
        db.session.add(user_site)
        db.session.commit()
        return jsonify({"success": True, "message": "Сайт успешно создан"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@constructor_bp.route('/templates')
@login_required
def templates():
    """Страница с доступными шаблонами."""
    templates = Template.query.filter_by(is_active=True).all()
    return render_template('templates.html', templates=templates)

@constructor_bp.route('/template/<int:template_id>')
@login_required
def template_detail(template_id):
    """Детальная страница шаблона."""
    template = Template.query.get_or_404(template_id)
    return render_template('template_detail.html', template=template)

@constructor_bp.route('/blocks')
@login_required
def blocks():
    """Страница с доступными блоками."""
    blocks = Block.query.filter_by(is_active=True).all()
    return render_template('blocks.html', blocks=blocks)

@constructor_bp.route('/save_site', methods=['POST'])
@login_required
def save_site():
    """Сохраняет структуру сайта пользователя."""
    data = request.json
    if not data or not data.get('name') or not data.get('structure'):
        return jsonify({'error': 'Missing data'}), 400
    
    site = UserSite(
        user_id=current_user.id,
        name=data['name'],
        structure_json=json.dumps(data['structure'])
    )
    
    from app import db
    db.session.add(site)
    db.session.commit()
    
    return jsonify({'success': True, 'site_id': site.id})

@constructor_bp.route('/my_sites')
@login_required
def my_sites():
    """Страница с сайтами пользователя."""
    sites = UserSite.query.filter_by(user_id=current_user.id).order_by(UserSite.last_updated.desc()).all()
    return render_template('my_sites.html', sites=sites)

@constructor_bp.route('/export_site/<int:site_id>')
@login_required
def export_site(site_id):
    """Экспортирует сайт пользователя в ZIP."""
    site = UserSite.query.filter_by(id=site_id, user_id=current_user.id).first_or_404()
    
    # Здесь должна быть логика генерации HTML из структуры
    # Пока возвращаем простой HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{site.name}</title>
    </head>
    <body>
        <h1>{site.name}</h1>
        <p>Сайт создан в ProThemesRU</p>
        <p>Структура: {site.structure_json}</p>
    </body>
    </html>
    """
    
    filename = f"{site.name.replace(' ', '_')}_{site.id}.zip"
    return export_site_as_zip(html_content, filename) 