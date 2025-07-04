from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_cors import CORS
from metrics import init_metrics
import os
from io import BytesIO
from functools import wraps

# Создаем приложение
app = Flask(__name__)

# Настройка безопасности
Talisman(app)
CORS(app)

# Настройка лимитов
limiter = Limiter(
    app=app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)

# Инициализируем метрики
metrics, timeit = init_metrics(app)

# Настройка секретного ключа из переменных окружения
app.secret_key = os.environ.get('SECRET_KEY', 'supersecretkey')

DB_PATH = 'database.db'

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            email TEXT UNIQUE,
            password TEXT,
            telegram_id TEXT,
            ref TEXT
        )''')
        conn.commit()
        print("✅ База данных успешно инициализирована.")

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        ref = request.args.get('ref', None)
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                flash("Пользователь уже зарегистрирован!", "danger")
                return redirect(url_for('register'))
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO users (username, email, password, ref) VALUES (?, ?, ?, ?)",
                           (username, email, hashed_password, ref))
            conn.commit()
            flash("Регистрация успешна! Выполните вход.", "success")
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user[3], password):
                session['user_id'] = user[0]
                session['username'] = user[1]
                return redirect(url_for('dashboard'))
            else:
                flash("Неверные данные!", "danger")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/constructor', methods=['GET', 'POST'])
def constructor():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        selected_blocks = request.form.getlist('blocks')
        return generate_site(selected_blocks)
    return render_template('constructor.html', blocks=blocks)

def generate_site(selected_blocks):
    html = "<html><head><title>Сайт</title></head><body>"
    for block in selected_blocks:
        html += blocks.get(block, '')
    html += "</body></html>"
    zip_stream = BytesIO()
    with zipfile.ZipFile(zip_stream, 'w') as zipf:
        zipf.writestr("index.html", html)
    zip_stream.seek(0)
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
