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
    # ... существующий код получения данных ...
    page = WebsitePage(
        title=site_title,
        background_color=site_background_color,
        background_image=site_background_image,
        font_family=site_font_family
    )
    page.add_block(
        HeaderBlock(
            block_id="main-header",
            logo_text=site_title,
            nav_items={"Главная": "#", "О нас": "#about", "Контакты": "#contact"}
        )
    )
    page.add_block(
        HeroSectionBlock(
            block_id="hero-section",
            title=hero_title,
            subtitle=hero_subtitle,
            button_text=hero_button_text,
            button_url=hero_button_url
        )
    )
    for i, content in enumerate(text_blocks_content):
        if content:
            page.add_block(
                TextBlock(
                    block_id=f"text-block-{i+1}",
                    content=content
                )
            )
    if image_src:
        page.add_block(
            ImageBlock(
                block_id="main-image",
                src=image_src,
                alt=image_alt
            )
        )
    # Добавляем калькулятор, если выбран чекбокс
    if request.form.get('add_calculator'):
        page.add_block(
            CalculatorBlock(
                block_id="calculator-block",
                title="Калькулятор"
            )
        )
    page.add_block(
        FooterBlock(
            block_id="main-footer",
            copyright_text=footer_text
        )
    )
    html_content = page.render()
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr('index.html', html_content)
        zip_file.writestr('style.css', page._generate_dynamic_styles().replace('<style>', '').replace('</style>', ''))
        zip_file.writestr('script.js', '// Custom scripts for your generated site\nconsole.log("Hello from your generated site!");')
    zip_buffer.seek(0)
    flash('Ваш сайт успешно сгенерирован и скачан!', 'success')
    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name='my_generated_site.zip',
        mimetype='application/zip'
    )

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