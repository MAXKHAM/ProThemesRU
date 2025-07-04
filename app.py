from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Регистрируем все блюпринты
from app.constructor import constructor_bp
from app.main import main_bp
from app.auth import auth_bp
from app.api.blocks import blocks_bp
from app.api.projects import projects_bp
from app.api.templates import templates_bp
from app.api.users import users_bp

# Регистрируем блюпринты
app.register_blueprint(constructor_bp, url_prefix='/constructor')
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(blocks_bp, url_prefix='/api/blocks')
app.register_blueprint(projects_bp, url_prefix='/api/projects')
app.register_blueprint(templates_bp, url_prefix='/api/templates')
app.register_blueprint(users_bp, url_prefix='/api/users')

# Модели базы данных

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    projects = db.relationship('Project', backref='author', lazy=True)
    templates = db.relationship('Template', backref='creator', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='draft')
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'))
    blocks = db.relationship('ProjectBlock', backref='project', lazy=True)
    settings = db.Column(db.JSON)

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    preview_image = db.Column(db.String(200))
    category = db.Column(db.String(50))
    features = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    projects = db.relationship('Project', backref='template', lazy=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blocks = db.relationship('TemplateBlock', backref='template', lazy=True)

class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    html = db.Column(db.Text, nullable=False)
    styles = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связи с проектами и шаблонами
    project_blocks = db.relationship('ProjectBlock', backref='block', lazy=True)
    template_blocks = db.relationship('TemplateBlock', backref='block', lazy=True)

class ProjectBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    block_id = db.Column(db.Integer, db.ForeignKey('block.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    settings = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TemplateBlock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    template_id = db.Column(db.Integer, db.ForeignKey('template.id'), nullable=False)
    block_id = db.Column(db.Integer, db.ForeignKey('block.id'), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    settings = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Маршруты

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid email or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            username=request.form.get('username'),
            email=request.form.get('email')
        )
        user.set_password(request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        flash('Registration successful')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    templates = Template.query.filter_by(creator_id=current_user.id).all()
    return render_template('dashboard.html', projects=projects, templates=templates)

@app.route('/constructor')
@login_required
def constructor():
    return render_template('constructor.html')

@app.route('/templates')
@login_required
def templates():
    templates = Template.query.all()
    return render_template('templates.html', templates=templates)

@app.route('/projects')
@login_required
def projects():
    projects = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('projects.html', projects=projects)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
    return send_file(zip_stream, as_attachment=True, download_name="site.zip", mimetype='application/zip')

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/buy_pro', methods=['GET', 'POST'])
def buy_pro():
    if request.method == 'POST':
        # Здесь можно обработать оплату или заявку
        flash('Спасибо за интерес! Оплата пока не реализована.', 'info')
    return render_template('buy_pro.html')

@app.route('/about')
def about():
    return render_template('about.html')

def object_to_css_string(css_object):
    if not css_object:
        return ''
    return '; '.join(f'{k}: {v}' for k, v in css_object.items() if k and v) + (';' if css_object else '')

def _generate_html_css_from_elements(elements):
    """
    Генерирует HTML и CSS из массива элементов конструктора,
    используя адаптивный контейнер и вложенность для групп.
    """
    MAX_CONTAINER_WIDTH = 960

    element_map = {el['id']: el for el in elements}
    root_elements = [el for el in elements if not el.get('parentId')]

    minX = float('inf')
    minY = float('inf')
    maxX = float('-inf')
    maxY = float('-inf')

    if root_elements:
        for el in root_elements:
            minX = min(minX, el['x'])
            minY = min(minY, el['y'])
            maxX = max(maxX, el['x'] + el['width'])
            maxY = max(maxY, el['y'] + el['height'])
    else:
        minX = 0; minY = 0; maxX = MAX_CONTAINER_WIDTH; maxY = 300; # Default for empty canvas

    original_design_width = maxX - minX
    original_design_height = maxY - minY

    scale_factor = 1
    if original_design_width > MAX_CONTAINER_WIDTH and original_design_width > 0:
        scale_factor = MAX_CONTAINER_WIDTH / original_design_width

    scaled_container_height = original_design_height * scale_factor

    html_content_parts = []
    css_content_parts = []

    html_content_parts.append(f"""<!DOCTYPE html><html lang=\"ru\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Мой Сайт (ProThemesRU)</title>
    <link rel=\"stylesheet\" href=\"style.css\">
    <style>
        /* Базовые стили для элементов конструктора */
        .canvas-element {{
            box-sizing: border-box;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        /* Только для элементов, которые абсолютно позиционированы */
        .canvas-element[style*="position: absolute;"] {{
             position: absolute;
        }}

        .canvas-element > * {{            width: 100%;
            height: 100%;
            box-sizing: border-box;
        }}

        .text-element {{
            text-align: center;
            word-break: break-word;
            padding: 5px;
        }}
        .image-element {{
            display: block;
            object-fit: contain;
            max-width: 100%;
            height: auto;
        }}
        .button-element {{
            padding: 8px 15px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            white-space: nowrap;
        }}
        .shape-element {{
            /* background-color and border-radius are inline */
        }}
    </style>
</head>
<body>
    <div id=\"main-content-area\">""")

    css_content_parts.append(f"""
body {{
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    padding: 20px 0;
    box-sizing: border-box;
}}

#main-content-area {{
    position: relative;
    max-width: {MAX_CONTAINER_WIDTH}px;
    width: 100%;
    margin: 0 auto;
    min-height: {max(scaled_container_height, 200)}px;
    background-color: #ffffff;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow: hidden;
}}
""")

    # Рекурсивная функция для рендеринга элементов
    def render_element_html_and_css(element):
        children = [el for el in elements if el.get('parentId') == element['id']]

        inline_styles = ""
        element_classes = 'canvas-element'

        parent = element.get('parentId')
        is_child_of_flex_container = False
        if parent:
            parent_el = element_map.get(parent)
            if parent_el and parent_el.get('type') == 'group' and parent_el['props'].get('displayMode') == 'flex':
                is_child_of_flex_container = True

        if is_child_of_flex_container:
            inline_styles += f"width: {element['width']}px; height: {element['height']}px;"
        else:
            elX = element['x']
            elY = element['y']

            newX = (elX - minX) * scale_factor if element.get('parentId') is None else elX
            newY = (elY - minY) * scale_factor if element.get('parentId') is None else elY
            newWidth = element['width'] * scale_factor if element.get('parentId') is None else element['width']
            newHeight = element['height'] * scale_factor if element.get('parentId') is None else element['height']

            inline_styles += f"position: absolute; left: {newX}px; top: {newY}px; width: {newWidth}px; height: {newHeight}px;"

        # Добавляем пользовательские классы
        if element['props'].get('customClasses') and len(element['props']['customClasses']) > 0:
            element_classes += f" {' '.join(element['props']['customClasses'])}"
        
        inner_html = ""
        if element['type'] == 'text':
            inner_html = f'<div class="text-element">{element["props"].get("content", "")}</div>'
            inline_styles += f" font-size: {element['props'].get('fontSize', '16px')}; color: {element['props'].get('color', '#000000')};"
        elif element['type'] == 'image':
            inner_html = f'<img src="{element["props"].get("src", "")}" alt="{element["props"].get("alt", "")}" class="image-element">'
        elif element['type'] == 'button':
            inner_html = f'<button class="button-element">{element["props"].get("label", "")}</button>'
            inline_styles += f" background-color: {element['props'].get('bgColor', '#007bff')}; color: {element['props'].get('textColor', '#ffffff')};"
        elif element['type'] == 'shape':
            inner_html = f'<div class="shape-element"></div>'
            inline_styles += f" background-color: {element['props'].get('bgColor', '#ffc107')}; border-radius: {element['props'].get('borderRadius', '0')};"
        elif element['type'] == 'group':
            element_classes += ' group-element'
            if element['props'].get('displayMode') == 'flex':
                inline_styles += f" display: flex;"
                if element['props'].get('flexDirection'): inline_styles += f" flex-direction: {element['props']['flexDirection']};"
                if element['props'].get('justifyContent'): inline_styles += f" justify-content: {element['props']['justifyContent']};"
                if element['props'].get('alignItems'): inline_styles += f" align-items: {element['props']['alignItems']};"
                if element['props'].get('gap'): inline_styles += f" gap: {element['props']['gap']};"
            else: # absolute group
                inline_styles += f" position: absolute;"
                inline_styles += f" background-color: rgba(255, 255, 255, 0.05); border: 1px dashed rgba(0, 0, 0, 0.1);"

            for child in children:
                inner_html += render_element_html_and_css(child)
        else:
            inner_html = f'<div>Неизвестный элемент</div>'
        
        if element['props'].get('customStyles'):
            inline_styles += f" {object_to_css_string(element['props']['customStyles'])}"

        return f'        <div id="{element["id"]}" class="{element_classes}" style="{inline_styles}">{inner_html}</div>'    

    for el in root_elements:
        html_content_parts.append(render_element_html_and_css(el))

    html_content_parts.append(f"""    </div>
</body>
</html>""")

    return "".join(html_content_parts), "".join(css_content_parts)

if __name__ == '__main__':
    app.run(debug=True)
