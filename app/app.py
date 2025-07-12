from flask import Flask, request, jsonify, send_from_directory, make_response
from flask_cors import CORS
import os
import json
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
import mimetypes
import hashlib
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt
from werkzeug.utils import secure_filename
from datetime import datetime

# --- КОНФИГУРАЦИЯ ---
app = Flask(__name__)
CORS(app)

# Конфигурация JWT
app.config["JWT_SECRET_KEY"] = "your-super-secret-jwt-key" # !!! Замените на реальный секретный ключ !!!
jwt = JWTManager(app)

SITE_DATA_FILE = 'site_data.json'
SITE_SETTINGS_FILE = 'site_settings.json'
PUBLIC_SITE_DIR = os.path.join(app.root_path, 'public_site')
SCRAPING_PROFILES_FILE = 'scraping_profiles.json'
PUBLIC_SCRAPED_SITES_DIR = os.path.join(app.root_path, 'public_scraped_sites')

# Media Upload Configuration
UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure directories exist
if not os.path.exists(PUBLIC_SITE_DIR):
    os.makedirs(PUBLIC_SITE_DIR)
if not os.path.exists(PUBLIC_SCRAPED_SITES_DIR):
    os.makedirs(PUBLIC_SCRAPED_SITES_DIR)
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# --- ВРЕМЕННЫЙ МЕХАНИЗМ АДМИНА (ДЛЯ ТЕСТОВ) ---
users = {
    "testuser": {"password": "password123", "is_admin": False},
    "admin": {"password": "adminpassword", "is_admin": True}
}

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return users.get(identity)

@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    user_data = users.get(identity)
    if user_data:
        return {"is_admin": user_data.get("is_admin", False)}
    return {"is_admin": False}

# --- МАРШРУТЫ АУТЕНТИФИКАЦИИ ---
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = users.get(username)
    if not user or user["password"] != password:
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token, is_admin=user["is_admin"])

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get("is_admin", False)
    return jsonify(logged_in_as=current_user, is_admin=is_admin), 200

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ CSS (Python-реализация) ---
def css_string_to_object(css_string):
    styles = {}
    if not css_string:
        return styles
    css_string = re.sub(r'\/\*[\s\S]*?\*\/|([^:]|^)\/\/.*$', r'\1', css_string)

    parts = css_string.split(';')
    for part in parts:
        trimmed_part = part.strip()
        if trimmed_part:
            if ':' in trimmed_part:
                key, value = trimmed_part.split(':', 1)
                styles[key.strip()] = value.strip()
    return styles

def object_to_css_string(css_object):
    if not css_object:
        return ""
    return "; ".join([f"{key}: {value}" for key, value in css_object.items()]) + (";" if css_object else "")

# --- НОВЫЕ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ УЛУЧШЕННОГО СКРАПИНГА ---
def get_file_extension_from_url(url):
    """Extract file extension from URL"""
    parsed = urlparse(url)
    path = parsed.path
    return os.path.splitext(path)[1]

def get_mime_type_from_url(url):
    """Guess MIME type from URL"""
    ext = get_file_extension_from_url(url)
    return mimetypes.guess_type(url)[0] or 'application/octet-stream'

def generate_unique_filename(original_url, content_hash=None):
    """Generate unique filename for downloaded resource"""
    parsed = urlparse(original_url)
    original_filename = os.path.basename(parsed.path)
    
    if not original_filename or '.' not in original_filename:
        # Generate filename based on content type
        mime_type = get_mime_type_from_url(original_url)
        if 'image' in mime_type:
            ext = '.jpg' if 'jpeg' in mime_type else '.png'
        elif 'css' in mime_type:
            ext = '.css'
        elif 'javascript' in mime_type:
            ext = '.js'
        else:
            ext = '.html'
        original_filename = f"resource{ext}"
    
    name, ext = os.path.splitext(original_filename)
    
    # Add hash if provided
    if content_hash:
        return f"{name}_{content_hash}{ext}"
    else:
        # Add timestamp as fallback
        import time
        return f"{name}_{int(time.time())}{ext}"

def download_resource(url, base_url, site_dir):
    """Download a resource and return local path"""
    try:
        absolute_url = urljoin(base_url, url)
        response = requests.get(absolute_url, timeout=10)
        response.raise_for_status()
        
        content = response.content
        content_hash = hashlib.md5(content).hexdigest()[:8]
        
        # Determine file type and directory
        mime_type = get_mime_type_from_url(absolute_url)
        if 'image' in mime_type:
            local_dir = os.path.join(site_dir, 'assets', 'images')
        elif 'css' in mime_type:
            local_dir = os.path.join(site_dir, 'assets', 'css')
        elif 'javascript' in mime_type:
            local_dir = os.path.join(site_dir, 'assets', 'js')
        else:
            local_dir = os.path.join(site_dir, 'assets', 'other')
        
        os.makedirs(local_dir, exist_ok=True)
        
        filename = generate_unique_filename(absolute_url, content_hash)
        local_path = os.path.join(local_dir, filename)
        
        # Save file
        with open(local_path, 'wb') as f:
            f.write(content)
        
        # Return relative path from site root
        return os.path.relpath(local_path, site_dir).replace('\\', '/')
        
    except Exception as e:
        app.logger.error(f"Failed to download {url}: {e}")
        return url  # Return original URL if download fails

def rewrite_urls_in_html(html_content, base_url, site_dir):
    """Rewrite URLs in HTML content to local paths"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Rewrite src attributes
    for tag in soup.find_all(['img', 'script', 'link']):
        if tag.has_attr('src'):
            local_path = download_resource(tag['src'], base_url, site_dir)
            tag['src'] = local_path
        if tag.has_attr('href') and tag.name == 'link':
            local_path = download_resource(tag['href'], base_url, site_dir)
            tag['href'] = local_path
    
    # Rewrite inline styles with url()
    for tag in soup.find_all(style=True):
        style_content = tag['style']
        # Simple regex to find url() patterns
        url_pattern = r'url\(["\']?([^"\')\s]+)["\']?\)'
        
        def replace_url(match):
            url = match.group(1)
            local_path = download_resource(url, base_url, site_dir)
            return f'url("{local_path}")'
        
        tag['style'] = re.sub(url_pattern, replace_url, style_content)
    
    return str(soup)

def scrape_site_recursive(start_url, max_depth=2, visited=None):
    """Recursively scrape site pages"""
    if visited is None:
        visited = set()
    
    if start_url in visited or len(visited) >= 50:  # Limit to prevent infinite loops
        return []
    
    visited.add(start_url)
    pages = []
    
    try:
        response = requests.get(start_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract page content
        page_data = {
            'url': start_url,
            'title': soup.find('title').text if soup.find('title') else 'Untitled',
            'content': str(soup),
            'depth': len(visited) - 1
        }
        pages.append(page_data)
        
        # Find links to other pages on same domain
        if len(visited) < max_depth:
            domain = urlparse(start_url).netloc
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(start_url, href)
                link_domain = urlparse(absolute_url).netloc
                
                # Only follow links to same domain
                if link_domain == domain and absolute_url not in visited:
                    sub_pages = scrape_site_recursive(absolute_url, max_depth, visited)
                    pages.extend(sub_pages)
        
        return pages
        
    except Exception as e:
        app.logger.error(f"Failed to scrape {start_url}: {e}")
        return []

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ ГЕНЕРАЦИИ HTML/CSS ---
def _generate_html_css_from_elements(elements, canvas_settings=None):
    """
    Генерирует HTML и CSS из массива элементов конструктора,
    используя адаптивный контейнер и вложенность для групп.
    """
    if canvas_settings is None:
        canvas_settings = {
            "backgroundColor": "#ffffff",
            "backgroundImage": "",
            "backgroundRepeat": "no-repeat",
            "backgroundSize": "cover",
            "backgroundPosition": "center center"
        }

    MAX_CONTAINER_WIDTH = 960

    element_map = {el['id']: el for el in elements}
    # Ensure all elements have a zIndex for sorting
    for el in elements:
        if 'props' not in el: el['props'] = {}
        if 'zIndex' not in el['props']: el['props']['zIndex'] = 1

    sorted_elements = sorted(elements, key=lambda x: x['props'].get('zIndex', 1))

    minX = float('inf')
    minY = float('inf')
    maxX = float('-inf')
    maxY = float('-inf')

    if elements: # Use all elements for bounding box calculation
        for el in elements:
            # Need absolute positions for bounding box if elements are nested
            abs_x = el['x']
            abs_y = el['y']
            current_parent = element_map.get(el.get('parentId'))
            while current_parent:
                abs_x += current_parent['x']
                abs_y += current_parent['y']
                current_parent = element_map.get(current_parent.get('parentId'))

            minX = min(minX, abs_x)
            minY = min(minY, abs_y)
            maxX = max(maxX, abs_x + el['width'])
            maxY = max(maxY, abs_y + el['height'])
    else:
        minX = 0; minY = 0; maxX = MAX_CONTAINER_WIDTH; maxY = 300;

    original_design_width = maxX - minX
    original_design_height = maxY - minY

    scale_factor = MAX_CONTAINER_WIDTH / original_design_width if original_design_width > MAX_CONTAINER_WIDTH and original_design_width > 0 else 1

    scaled_container_height = original_design_height * scale_factor

    html_content = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Мой Сайт (ProThemesRU)</title>
    <link rel="stylesheet" href="style.css">
    <style>
        /* Базовые стили для элементов конструктора */
        .canvas-element {{
            box-sizing: border-box;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        /* Only for elements that are absolutely positioned */
        .canvas-element[style*="position: absolute;"] {{
             position: absolute;
        }}

        .canvas-element > * {{
            width: 100%;
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
    <div id="main-content-area">
"""
    css_content = f"""
body {{
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background-color: #f0f0f0; /* Default body background */
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
    background-color: #ffffff; /* Default, overridden by canvas settings */
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
    border-radius: 8px;
    overflow: hidden;
"""
    # Apply canvas background settings to #main-content-area
    if canvas_settings.get('backgroundColor'):
        css_content += f"    background-color: {canvas_settings['backgroundColor']};\n"
    if canvas_settings.get('backgroundImage'):
        bg_img_src = canvas_settings['backgroundImage']
        # If image is from uploads, ensure it's served correctly
        if bg_img_src.startswith('/uploads/'):
            bg_img_src = f'{bg_img_src}' # Assuming Flask serves /uploads/
        css_content += f"    background-image: url('{bg_img_src}');\n"
        css_content += f"    background-repeat: {canvas_settings.get('backgroundRepeat', 'no-repeat')};\n"
        css_content += f"    background-size: {canvas_settings.get('backgroundSize', 'cover')};\n"
        css_content += f"    background-position: {canvas_settings.get('backgroundPosition', 'center center')};\n"
    css_content += "}\n" # Close #main-content-area style block

    # Recursive function to render elements
    def render_element_html_and_css(element):
        # Children should also be sorted by z-index if they are rendered within a group
        children = sorted([el for el in sorted_elements if el.get('parentId') == element['id']], key=lambda x: x['props'].get('zIndex', 1))

        inline_styles = ''
        element_classes = 'canvas-element'

        parent = element.get('parentId')
        is_child_of_flex_container = False
        is_child_of_grid_container = False
        if parent:
            parent_el = element_map.get(parent)
            if parent_el and parent_el.get('type') == 'group':
                if parent_el['props'].get('displayMode') == 'flex':
                    is_child_of_flex_container = True
                elif parent_el['props'].get('displayMode') == 'grid':
                    is_child_of_grid_container = True

        if is_child_of_flex_container or is_child_of_grid_container:
            inline_styles += f"width: {element['width']}px; height: {element['height']}px;"
        else:
            elX = element['x']
            elY = element['y']
            # For root elements, scale their positions relative to the overall design bounding box
            newX = (elX - minX) * scale_factor if element.get('parentId') is None else elX
            newY = (elY - minY) * scale_factor if element.get('parentId') is None else elY
            newWidth = element['width'] * scale_factor if element.get('parentId') is None else element['width']
            newHeight = element['height'] * scale_factor if element.get('parentId') is None else element['height']

            inline_styles += f"position: absolute; left: {newX}px; top: {newY}px; width: {newWidth}px; height: {newHeight}px;"

        # Apply z-index
        if element['props'].get('zIndex') is not None:
            inline_styles += f" z-index: {element['props']['zIndex']};"

        if element['props'].get('customClasses') and len(element['props']['customClasses']) > 0:
            element_classes += f" {' '.join(element['props']['customClasses'])}"
        inner_html = ""
        if element['type'] == 'text':
            inner_html = f'<div class="text-element">{element["props"].get("content", "")}</div>'
            inline_styles += f" font-size: {element['props'].get('fontSize', '16px')}; color: {element['props'].get('color', '#000000')};"
        elif element['type'] == 'image':
            src = element["props"].get("src", "")
            # If image is from uploads, use the public path
            if src.startswith('/uploads/'):
                src = f'{src}' # Assuming Flask serves /uploads/
            inner_html = f'<img src="{src}" alt="{element["props"].get("alt", "")}" class="image-element">'
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
            elif element['props'].get('displayMode') == 'grid':
                inline_styles += f" display: grid;"
                if element['props'].get('gridTemplateColumns'): inline_styles += f" grid-template-columns: {element['props']['gridTemplateColumns']};"
                if element['props'].get('gridTemplateRows'): inline_styles += f" grid-template-rows: {element['props']['gridTemplateRows']};"
                if element['props'].get('gridGap'): inline_styles += f" gap: {element['props']['gridGap']};"
            else: # absolute group
                inline_styles += f" position: absolute;"
            for child in children:
                inner_html += render_element_html_and_css(child)
        else:
            inner_html = f'<div>Неизвестный элемент</div>'

        # Apply Border properties
        if element['props'].get('borderWidth') and element['props']['borderWidth'] != '0px' and \
           element['props'].get('borderStyle') and element['props'].get('borderColor'):
            inline_styles += f" border: {element['props']['borderWidth']} {element['props']['borderStyle']} {element['props']['borderColor']};"

        # Apply Box Shadow properties
        if any(element['props'].get(prop) for prop in ['boxShadowX', 'boxShadowY', 'boxShadowBlur', 'boxShadowSpread']):
            inline_styles += f" box-shadow: {element['props'].get('boxShadowX', '0px')} {element['props'].get('boxShadowY', '0px')} {element['props'].get('boxShadowBlur', '0px')} {element['props'].get('boxShadowSpread', '0px')} {element['props'].get('boxShadowColor', 'rgba(0,0,0,0.2)')};"

        # Apply Background properties
        if element['props'].get('backgroundColor'):
            inline_styles += f" background-color: {element['props']['backgroundColor']};"
        if element['props'].get('backgroundImage'):
            # If background image is from uploads, use the public path
            bg_img_src = element['props']['backgroundImage']
            if bg_img_src.startswith('/uploads/'):
                bg_img_src = f'{bg_img_src}' # Assuming Flask serves /uploads/
            inline_styles += f" background-image: url('{bg_img_src}');"
            inline_styles += f" background-repeat: {element['props'].get('backgroundRepeat', 'no-repeat')};"
            inline_styles += f" background-size: {element['props'].get('backgroundSize', 'cover')};"
            inline_styles += f" background-position: {element['props'].get('backgroundPosition', 'center center')};"

        if element['props'].get('customStyles'):
            inline_styles += f" {object_to_css_string(element['props']['customStyles'])};"

        return f'        <div id="{element["id"]}" class="{element_classes}" style="{inline_styles}">{inner_html}</div>'

    # Filter out only root elements to start rendering tree
    root_elements_for_html = [el for el in sorted_elements if not el.get('parentId')]
    html_content += "".join([render_element_html_and_css(el) for el in root_elements_for_html])

    html_content += f"""    </div>
</body>
</html>"""

    return {"htmlContent": html_content, "cssContent": css_content}

# NEW: Helper function for allowed extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# NEW: Media Library Endpoints
@app.route("/api/admin/media/upload", methods=["POST"])
@jwt_required()
def upload_media():
    claims = get_jwt()
    if not claims.get("is_admin"):
        return jsonify({"msg": "Admin access required"}), 403

    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Ensure unique filename to prevent overwrites
        base, ext = os.path.splitext(filename)
        counter = 1
        new_filename = filename
        while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], new_filename)):
            new_filename = f"{base}_{counter}{ext}"
            counter += 1
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
        file.save(file_path)
        # Return URL relative to public access
        file_url = f"/uploads/{new_filename}"
        return jsonify({"msg": "File uploaded successfully", "url": file_url}), 200
    return jsonify({"msg": "File type not allowed"}), 400

@app.route("/api/admin/media/list", methods=["GET"])
@jwt_required()
def list_media():
    claims = get_jwt()
    if not claims.get("is_admin"):
        return jsonify({"msg": "Admin access required"}), 403

    media_files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(filename):
            file_url = f"/uploads/{filename}"
            media_files.append({"name": filename, "url": file_url})
    return jsonify(media_files), 200

@app.route("/api/admin/media/delete", methods=["POST"])
@jwt_required()
def delete_media():
    claims = get_jwt()
    if not claims.get("is_admin"):
        return jsonify({"msg": "Admin access required"}), 403

    data = request.json
    file_url = data.get('url')
    if not file_url:
        return jsonify({"msg": "URL not provided"}), 400

    # Extract filename from URL
    filename = os.path.basename(file_url)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.exists(file_path) and allowed_file(filename):
        try:
            os.remove(file_path)
            return jsonify({"msg": f"File '{filename}' deleted successfully"}), 200
        except Exception as e:
            return jsonify({"msg": f"Error deleting file: {str(e)}"}), 500
    return jsonify({"msg": "File not found or not allowed type"}), 404

# NEW: Route to serve uploaded files publicly
@app.route("/uploads/<filename>")
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# --- NEW: ADVANCED SCRAPING FUNCTIONS ---
ASSET_SUBDIRS = {
    'image': 'images',
    'css': 'css',
    'script': 'js'
}

def _sanitize_filename(url, asset_type):
    """Generates a safe filename from a URL, adding a hash to prevent collisions."""
    parsed_url = urlparse(url)
    path = parsed_url.path
    if not path or path == '/':
        path = 'index' # For root CSS/JS
    
    # Remove leading slash for path components
    path_components = [p for p in path.split('/') if p]
    
    # Extract original extension or guess it
    original_filename = path_components[-1] if path_components else 'asset'
    name, ext = os.path.splitext(original_filename)
    
    # If no obvious extension, try to guess from MIME type
    if not ext:
        mime_type, _ = mimetypes.guess_type(url)
        if mime_type:
            if 'image' in mime_type: ext = '.png' # Default image
            elif 'css' in mime_type: ext = '.css'
            elif 'javascript' in mime_type: ext = '.js'
        else: # Fallback to generic based on asset_type
            if asset_type == 'image': ext = '.png'
            elif asset_type == 'css': ext = '.css'
            elif asset_type == 'script': ext = '.js'
            else: ext = '.bin' # Unknown binary

    # Use a hash of the full URL to ensure uniqueness and avoid long names
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()[:8]
    
    # Combine original name part (sanitized) with hash and extension
    sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '', name)
    if not sanitized_name: sanitized_name = 'asset'
    
    return f"{sanitized_name}_{url_hash}{ext}"

def _download_asset(asset_url, base_url, site_output_dir, asset_type, downloaded_assets):
    """
    Downloads an asset (image, css, js) and returns its new local path.
    `downloaded_assets` is a dict to store original_url -> local_path mapping.
    """
    if not asset_url:
        return ""

    absolute_asset_url = urljoin(base_url, unquote(asset_url)) # Decode URL
    if absolute_asset_url in downloaded_assets:
        return downloaded_assets[absolute_asset_url] # Already downloaded

    parsed_url = urlparse(absolute_asset_url)
    # Skip if not http/https or not a valid domain
    if parsed_url.scheme not in ['http', 'https'] or not parsed_url.netloc:
        return "" # Not a web asset, or invalid URL

    # Determine subdirectory based on asset type
    subdir = ASSET_SUBDIRS.get(asset_type, 'misc')
    asset_dir = os.path.join(site_output_dir, 'assets', subdir)
    os.makedirs(asset_dir, exist_ok=True)

    local_filename = _sanitize_filename(absolute_asset_url, asset_type)
    local_path = os.path.join(asset_dir, local_filename)
    relative_local_path = os.path.join('assets', subdir, local_filename)

    try:
        app.logger.info(f"Downloading {asset_type}: {absolute_asset_url} to {local_path}")
        response = requests.get(absolute_asset_url, stream=True, timeout=10)
        response.raise_for_status()

        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        downloaded_assets[absolute_asset_url] = relative_local_path
        return relative_local_path
    except requests.exceptions.RequestException as e:
        app.logger.warning(f"Failed to download {asset_type} {absolute_asset_url}: {e}")
        return "" # Return empty string or original URL to indicate failure
    except Exception as e:
        app.logger.error(f"Error saving asset {absolute_asset_url}: {e}")
        return ""

def _rewrite_html_urls(html_content, base_url, site_output_dir, download_assets, asset_types_to_download, downloaded_assets):
    """
    Rewrites URLs in HTML content to point to locally downloaded assets.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Rewrite <img> tags
    if 'images' in asset_types_to_download:
        for img in soup.find_all('img', src=True):
            original_src = img['src']
            local_src = _download_asset(original_src, base_url, site_output_dir, 'image', downloaded_assets)
            if local_src:
                img['src'] = local_src

    # Rewrite <link> tags for stylesheets
    if 'css' in asset_types_to_download:
        for link in soup.find_all('link', rel='stylesheet', href=True):
            original_href = link['href']
            local_href = _download_asset(original_href, base_url, site_output_dir, 'css', downloaded_assets)
            if local_href:
                link['href'] = local_href

    # Rewrite <script> tags
    if 'js' in asset_types_to_download:
        for script in soup.find_all('script', src=True):
            original_src = script['src']
            local_src = _download_asset(original_src, base_url, site_output_dir, 'script', downloaded_assets)
            if local_src:
                script['src'] = local_src

    # Rewrite URLs in inline style attributes (background-image: url(...))
    for tag in soup.find_all(style=True):
        style_attr = tag['style']
        # Regex to find url(...) patterns
        def replace_url_in_style(match):
            original_url = match.group(1)
            # Check if it's a data URI or already local
            if original_url.startswith('data:') or original_url.startswith('assets/'):
                return match.group(0) # Don't process
            
            # Try to guess asset type for style background images
            asset_type = 'image' # Assume images for now in style URLs
            local_path = _download_asset(original_url, base_url, site_output_dir, asset_type, downloaded_assets)
            if local_path:
                return f"url('{local_path}')"
            return match.group(0) # Keep original if download fails

        tag['style'] = re.sub(r"url\(['\"]?(.*?)['\"]?\)", replace_url_in_style, style_attr)

    return str(soup)

def _scrape_page(url, profile, site_output_dir, visited_urls, downloaded_assets, current_depth, max_depth, follow_links, download_assets, asset_types):
    """
    Recursively scrapes a single page, downloads assets, rewrites URLs, and follows links.
    """
    if url in visited_urls:
        return [] # Already visited
    
    parsed_url = urlparse(url)
    # Ensure we stay within the same domain
    if parsed_url.netloc != urlparse(profile['targetUrl']).netloc:
        app.logger.info(f"Skipping external URL: {url}")
        return []

    visited_urls.add(url)
    app.logger.info(f"Scraping: {url} (Depth: {current_depth})")

    try:
        response = requests.get(url, timeout=15) # Increased timeout
        response.raise_for_status()
        html_content = response.text

        # 1. Download assets and rewrite URLs in HTML
        if download_assets:
            html_content = _rewrite_html_urls(html_content, url, site_output_dir, download_assets, asset_types, downloaded_assets)
        
        soup = BeautifulSoup(html_content, 'html.parser')

        # 2. Apply scraping profile for content extraction (existing logic)
        page_extracted_data = []
        for section in profile.get('sections', []):
            output_file_name = section.get('outputFileName', 'index.html')
            root_selector = section.get('rootSelector')
            fields_to_extract = section.get('fields', {})
            output_template = section.get('outputTemplate', '<div>No template provided</div>')

            if not root_selector:
                app.logger.warning(f"Skipping section in profile {profile['id']} due to missing rootSelector.")
                continue

            extracted_data_list = []
            for item_tag in soup.select(root_selector):
                extracted_item_data = {}
                for field_name, field_config in fields_to_extract.items():
                    selector = field_config.get('selector')
                    attribute = field_config.get('attribute')
                    
                    if not selector: continue

                    sub_tag = item_tag.select_one(selector)
                    if sub_tag:
                        if attribute == 'text':
                            extracted_item_data[field_name] = sub_tag.get_text(strip=True)
                        elif attribute: # Any other attribute like 'href', 'src'
                            extracted_item_data[field_name] = sub_tag.get(attribute, '')
                        else: # Default to text if attribute is not specified
                            extracted_item_data[field_name] = sub_tag.get_text(strip=True)
                    else:
                        extracted_item_data[field_name] = '' # Ensure field exists even if not found
                extracted_data_list.append(extracted_item_data)
            
            # Generate HTML for this section
            section_html_content = ""
            for data_item in extracted_data_list:
                temp_html = output_template
                for key, value in data_item.items():
                    temp_html = temp_html.replace(f"{{{{{key}}}}}", value)
                section_html_content += temp_html + "\n"
            
            page_extracted_data.append({
                "output_file_name": output_file_name,
                "content": section_html_content
            })

        # 3. Save the processed page
        # Determine a unique filename for the page based on its URL path
        page_path = parsed_url.path.strip('/')
        if not page_path or page_path.endswith('/'):
            page_path += 'index.html'
        
        # Ensure path is valid for filesystem
        safe_page_path = re.sub(r'[^\w\-_.]', '_', page_path) # Replace invalid chars with underscore

        page_output_dir = os.path.join(site_output_dir, 'pages')
        os.makedirs(page_output_dir, exist_ok=True)
        
        output_html_filename = safe_page_path
        if not output_html_filename.endswith('.html'): # Ensure .html extension
            output_html_filename = f"{output_html_filename.split('.')[0] or 'page'}.html"
            
        page_file_path = os.path.join(page_output_dir, output_html_filename)
        
        # If multiple sections, save each to its own file. If only one, save to its name.
        if len(page_extracted_data) > 0:
            for data in page_extracted_data:
                final_output_path = os.path.join(page_output_dir, data['output_file_name'])
                final_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Скрапленный сайт - {profile['name']} - {data['output_file_name']}</title>
    <link rel="stylesheet" href="../assets/css/scraped_style.css"> <!-- Example for a base scraped style -->
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; }}
        .scraped-item {{ background-color: #fff; border: 1px solid #ddd; padding: 15px; margin-bottom: 10px; border-radius: 5px; }}
        .scraped-item img {{ max-width: 100%; height: auto; display: block; margin-bottom: 10px; }}
        .scraped-item h2 {{ color: #333; font-size: 20px; }}
        .scraped-item p {{ color: #666; font-size: 14px; }}
        .scraped-item a {{ color: #007bff; text-decoration: none; }}
        .scraped-item a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>Результаты скрапинга: {profile['name']}</h1>
    <p>URL: <a href="{url}" target="_blank">{url}</a></p>
    <div class="scraped-content">
        {data['content']}
    </div>
</body>
</html>"""
                with open(final_output_path, 'w', encoding='utf-8') as f:
                    f.write(final_html)
        else: # If no specific sections, just save the raw (rewritten) HTML
            final_html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Скрапленный сайт - {profile['name']}</title>
    <link rel="stylesheet" href="../assets/css/scraped_style.css">
</head>
<body>
    {html_content}
</body></html>"""
            with open(page_file_path, 'w', encoding='utf-8') as f:
                f.write(final_html)

        # 4. Find and queue new links to follow
        new_links_to_follow = []
        if follow_links and current_depth < max_depth:
            for a_tag in soup.find_all('a', href=True):
                link_href = a_tag['href']
                absolute_link = urljoin(url, link_href)
                
                # Check if it's an internal link and not already visited
                if urlparse(absolute_link).netloc == parsed_url.netloc and absolute_link not in visited_urls:
                    # Basic check to avoid non-HTML links (e.g., mailto, tel, #anchors, .pdf)
                    if not absolute_link.startswith(('mailto:', 'tel:', '#')) and not absolute_link.lower().endswith(('.pdf', '.zip', '.doc', '.docx')):
                        new_links_to_follow.append(absolute_link)
        
        return new_links_to_follow

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching URL {url}: {e}")
    except Exception as e:
        app.logger.error(f"Error processing page {url}: {e}")
    return []

# --- ЭНДПОИНТЫ ДЛЯ АДМИНА ---

@app.route("/api/admin/load_my_site_data", methods=["GET"])
@jwt_required()
def load_my_site_data():
    claims = get_jwt()
    if not claims.get("is_admin"):
        return jsonify({"msg": "Admin access required"}), 403

    elements_data = []
    if os.path.exists(SITE_DATA_FILE):
        with open(SITE_DATA_FILE, 'r', encoding='utf-8') as f:
            elements_data = json.load(f)
        for el in elements_data:
            if 'parentId' not in el:
                el['parentId'] = None
            if 'props' not in el:
                el['props'] = {}
            if 'customClasses' not in el['props']:
                el['props']['customClasses'] = []
            if 'customStyles' not in el['props']:
                el['props']['customStyles'] = {}
            if 'zIndex' not in el['props']:
                el['props']['zIndex'] = 1
            # Ensure group properties exist
            if el.get('type') == 'group':
                if 'displayMode' not in el['props']: el['props']['displayMode'] = 'absolute'
                if 'flexDirection' not in el['props']: el['props']['flexDirection'] = 'row'
                if 'justifyContent' not in el['props']: el['props']['justifyContent'] = 'flex-start'
                if 'alignItems' not in el['props']: el['props']['alignItems'] = 'stretch'
                if 'gap' not in el['props']: el['props']['gap'] = '0px'
                if 'gridTemplateColumns' not in el['props']: el['props']['gridTemplateColumns'] = '1fr'
                if 'gridTemplateRows' not in el['props']: el['props']['gridTemplateRows'] = 'auto'
                if 'gridGap' not in el['props']: el['props']['gridGap'] = '0px'

            # Ensure general styling properties exist for all elements
            if 'borderWidth' not in el['props']: el['props']['borderWidth'] = '0px'
            if 'borderStyle' not in el['props']: el['props']['borderStyle'] = 'solid'
            if 'borderColor' not in el['props']: el['props']['borderColor'] = '#000000'
            if 'boxShadowX' not in el['props']: el['props']['boxShadowX'] = '0px'
            if 'boxShadowY' not in el['props']: el['props']['boxShadowY'] = '0px'
            if 'boxShadowBlur' not in el['props']: el['props']['boxShadowBlur'] = '0px'
            if 'boxShadowSpread' not in el['props']: el['props']['boxShadowSpread'] = '0px'
            if 'boxShadowColor' not in el['props']: el['props']['boxShadowColor'] = 'rgba(0,0,0,0.2)'
            if 'backgroundColor' not in el['props']: el['props']['backgroundColor'] = '' # Empty string for no default override
            if 'backgroundImage' not in el['props']: el['props']['backgroundImage'] = ''
            if 'backgroundRepeat' not in el['props']: el['props']['backgroundRepeat'] = 'no-repeat'
            if 'backgroundSize' not in el['props']: el['props']['backgroundSize'] = 'cover'
            if 'backgroundPosition' not in el['props']: el['props']['backgroundPosition'] = 'center center'

            # Special default for groups' background in editor if not set
            if el.get('type') == 'group' and not el['props'].get('backgroundColor'):
                el['props']['backgroundColor'] = 'rgba(255, 255, 255, 0.05)'
            if el.get('type') == 'group' and not el['props'].get('borderWidth') and not el['props'].get('borderStyle') and not el['props'].get('borderColor'):
                el['props']['borderWidth'] = '1px'
                el['props']['borderStyle'] = 'dashed'
                el['props']['borderColor'] = 'rgba(0, 0, 0, 0.1)'

    canvas_settings = {}
    if os.path.exists(SITE_SETTINGS_FILE):
        with open(SITE_SETTINGS_FILE, 'r', encoding='utf-8') as f:
            canvas_settings = json.load(f)

    response = make_response(jsonify(elements_data), 200)
    response.headers['X-Canvas-Settings'] = json.dumps(canvas_settings)
    return response

@app.route("/api/admin/publish_my_site", methods=["POST"])
@jwt_required()
def publish_my_site():
    claims = get_jwt()
    if not claims.get("is_admin"):
        return jsonify({"msg": "Admin access required"}), 403

    elements = request.json
    canvas_settings_json = request.headers.get('X-Canvas-Settings')
    canvas_settings = {}
    if canvas_settings_json:
        try:
            canvas_settings = json.loads(canvas_settings_json)
        except json.JSONDecodeError:
            app.logger.warning("Invalid X-Canvas-Settings header received.")

    if not isinstance(elements, list):
        return jsonify({"msg": "Invalid data format, expected a list of elements"}), 400
    try:
        # Ensure elements have zIndex property before passing to generation
        for el in elements:
            if 'props' not in el: el['props'] = {}
            if 'zIndex' not in el['props']: el['props']['zIndex'] = 1

        # Pass canvas_settings to the generation function
        result = _generate_html_css_from_elements(elements, canvas_settings)
        html_content = result['htmlContent']
        css_content = result['cssContent']

        with open(os.path.join(PUBLIC_SITE_DIR, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_content)
        with open(os.path.join(PUBLIC_SITE_DIR, 'style.css'), 'w', encoding='utf-8') as f:
            f.write(css_content)

        # Save canvas settings separately
        with open(SITE_SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(canvas_settings, f, ensure_ascii=False, indent=4)
        return jsonify({"msg": "Site published successfully!"}), 200
    except Exception as e:
        app.logger.error(f"Error publishing site: {e}")
        return jsonify({"msg": f"Failed to publish site: {str(e)}"}), 500

# NEW: Route to serve scraped pages and assets
@app.route("/public/scraped/<site_dir>/pages/<path:filename>")
def serve_public_scraped_page(site_dir, filename):
    return send_from_directory(os.path.join(PUBLIC_SCRAPED_SITES_DIR, site_dir, 'pages'), filename)

@app.route("/public/scraped/<site_dir>/assets/<subdir>/<path:filename>")
def serve_public_scraped_asset(site_dir, subdir, filename):
    return send_from_directory(os.path.join(PUBLIC_SCRAPED_SITES_DIR, site_dir, 'assets', subdir), filename)

# NEW: Admin endpoints for scraping profiles
@app.route("/api/admin/scraping_profiles", methods=["GET"])
@jwt_required()
def get_scraping_profiles():
    claims = get_jwt()
    if not claims.get("is_admin"):
        return jsonify({"msg": "Admin access required"}), 403

    profiles = []
    if os.path.exists(SCRAPING_PROFILES_FILE):
        with open(SCRAPING_PROFILES_FILE, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
        return jsonify(profiles), 200
    return jsonify([]), 200

@app.route("/api/admin/scraping_profiles", methods=["POST"])
@jwt_required()
def save_scraping_profile():
    claims = get_jwt()
    if not claims.get("is_admin"):
        return jsonify({"msg": "Admin access required"}), 403

    profile = request.json
    if not profile or not profile.get('id') or not profile.get('name') or not profile.get('sections'):
        return jsonify({"msg": "Invalid profile data"}), 400

    profiles = []
    if os.path.exists(SCRAPING_PROFILES_FILE):
        with open(SCRAPING_PROFILES_FILE, 'r', encoding='utf-8') as f:
            profiles = json.load(f)

    # Update existing or add new
    updated = False
    for i, p in enumerate(profiles):
        if p['id'] == profile['id']:
            profiles[i] = profile
            updated = True
            break
    if not updated:
        profiles.append(profile)

    with open(SCRAPING_PROFILES_FILE, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)

    return jsonify({"msg": "Scraping profile saved successfully!", "profile": profile}), 200

@app.route("/api/admin/scraping_profiles/<profile_id>", methods=["DELETE"])
@jwt_required()
def delete_scraping_profile(profile_id):
    claims = get_jwt()
    if not claims.get("is_admin"):
        return jsonify({"msg": "Admin access required"}), 403

    profiles = []
    if os.path.exists(SCRAPING_PROFILES_FILE):
        with open(SCRAPING_PROFILES_FILE, 'r', encoding='utf-8') as f:
            profiles = json.load(f)

    initial_len = len(profiles)
    profiles = [p for p in profiles if p['id'] != profile_id]

    if len(profiles) == initial_len:
        return jsonify({"msg": "Profile not found"}), 404

    with open(SCRAPING_PROFILES_FILE, 'w', encoding='utf-8') as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)

    return jsonify({"msg": "Scraping profile deleted successfully!"}), 200

# NEW: Main scraping endpoint
@app.route("/api/admin/scrape_site", methods=["POST"])
@jwt_required()
def scrape_site():
    claims = get_jwt()
    if not claims.get("is_admin"):
        return jsonify({"msg": "Admin access required"}), 403    
    data = request.json
    target_url = data.get('url')
    profile_id = data.get('profileId')
    
    # NEW: Advanced scraping options
    follow_links = data.get('followLinks', False)
    max_depth = int(data.get('maxDepth', 1)) # Default to 1 (only initial page)
    download_assets = data.get('downloadAssets', False)
    asset_types_to_download = []
    if data.get('downloadImages'): asset_types_to_download.append('images')
    if data.get('downloadCss'): asset_types_to_download.append('css')
    if data.get('downloadJs'): asset_types_to_download.append('js')

    if not target_url or not profile_id:
        return jsonify({"msg": "URL and Profile ID are required"}), 400

    profiles = []
    if os.path.exists(SCRAPING_PROFILES_FILE):
        with open(SCRAPING_PROFILES_FILE, 'r', encoding='utf-8') as f:
            profiles = json.load(f)
    
    profile = next((p for p in profiles if p['id'] == profile_id), None)
    if not profile:
        return jsonify({"msg": "Scraping profile not found"}), 404

    site_name = re.sub(r'[^a-zA-Z0-9_-]', '', urlparse(target_url).netloc.replace('.', '_')).strip('_')
    site_output_root_dir = os.path.join(PUBLIC_SCRAPED_SITES_DIR, site_name)
    
    # Clear previous scraped data for this site name
    if os.path.exists(site_output_root_dir):
        import shutil
        shutil.rmtree(site_output_root_dir)
    os.makedirs(site_output_root_dir, exist_ok=True)
    os.makedirs(os.path.join(site_output_root_dir, 'pages'), exist_ok=True)
    os.makedirs(os.path.join(site_output_root_dir, 'assets', 'images'), exist_ok=True)
    os.makedirs(os.path.join(site_output_root_dir, 'assets', 'css'), exist_ok=True)
    os.makedirs(os.path.join(site_output_root_dir, 'assets', 'js'), exist_ok=True)

    # Add targetUrl to profile for domain checking
    profile['targetUrl'] = target_url

    visited_urls = set()
    urls_to_visit = [(target_url, 0)] # (url, depth)
    downloaded_assets = {} # Map original_url -> local_path
    scraped_pages_count = 0
    downloaded_assets_count = 0

    while urls_to_visit:
        current_url, current_depth = urls_to_visit.pop(0) # Use pop(0) for BFS-like behavior

        if current_depth > max_depth:
            continue

        new_links = _scrape_page(
            current_url,
            profile,
            site_output_root_dir,
            visited_urls,
            downloaded_assets,
            current_depth,
            max_depth,
            follow_links,
            download_assets,
            asset_types_to_download
        )
        
        if current_url not in visited_urls: # Only count if successfully scraped
             scraped_pages_count += 1

        for link in new_links:
            if link not in visited_urls:
                urls_to_visit.append((link, current_depth + 1))
    
    downloaded_assets_count = len(downloaded_assets)

    return jsonify({
        "msg": "Site scraped successfully!",
        "site_dir": site_name,
        "scraped_pages_count": scraped_pages_count,
        "downloaded_assets_count": downloaded_assets_count,
        "base_url": f"/public/scraped/{site_name}/pages/index.html" # Provide a direct link to the main scraped page
    }), 200

@app.route("/public/scraped/<path:filename>")
def serve_public_scraped_site(filename):
    return send_from_directory(PUBLIC_SCRAPED_SITES_DIR, filename)

# --- МАРШРУТЫ ДЛЯ РАБОТЫ С САЙТОМ ---
@app.route("/api/save_site", methods=["POST"])
@jwt_required()
def save_site():
    try:
        data = request.get_json()
        elements = data.get('elements', [])
        canvas_settings = data.get('canvasSettings', {})  # NEW: Get canvas settings
        
        # Save elements
        with open(SITE_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(elements, f, ensure_ascii=False, indent=2)
        
        # NEW: Save canvas settings separately
        with open(SITE_SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(canvas_settings, f, ensure_ascii=False, indent=2)
        
        return jsonify({"message": "Сайт успешно сохранен"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/load_site", methods=["GET"])
@jwt_required()
def load_site():
    try:
        elements = []
        canvas_settings = {}  # NEW: Load canvas settings
        
        if os.path.exists(SITE_DATA_FILE):
            with open(SITE_DATA_FILE, 'r', encoding='utf-8') as f:
                elements = json.load(f)
        
        # NEW: Load canvas settings if file exists
        if os.path.exists(SITE_SETTINGS_FILE):
            with open(SITE_SETTINGS_FILE, 'r', encoding='utf-8') as f:
                canvas_settings = json.load(f)
        
        return jsonify({
            "elements": elements,
            "canvasSettings": canvas_settings  # NEW: Return canvas settings
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/publish_site", methods=["POST"])
@jwt_required()
def publish_site():
    try:
        data = request.get_json()
        elements = data.get('elements', [])
        canvas_settings = data.get('canvasSettings', {})  # NEW: Get canvas settings
        
        # Generate HTML and CSS with canvas settings
        result = _generate_html_css_from_elements(elements, canvas_settings)
        
        # Save to public directory
        with open(os.path.join(PUBLIC_SITE_DIR, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(result['htmlContent'])
        
        with open(os.path.join(PUBLIC_SITE_DIR, 'style.css'), 'w', encoding='utf-8') as f:
            f.write(result['cssContent'])
        
        return jsonify({"message": "Сайт успешно опубликован", "url": "/public_site/index.html"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- МАРШРУТЫ ДЛЯ МЕДИА ---
@app.route("/api/upload_media", methods=["POST"])
@jwt_required()
def upload_media():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Add timestamp to prevent conflicts
            import time
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{int(time.time())}{ext}"
            
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            return jsonify({
                "message": "File uploaded successfully",
                "filename": filename,
                "url": f"/uploads/{filename}"
            }), 200
        else:
            return jsonify({"error": "File type not allowed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/media_files", methods=["GET"])
@jwt_required()
def get_media_files():
    try:
        files = []
        if os.path.exists(UPLOAD_FOLDER):
            for filename in os.listdir(UPLOAD_FOLDER):
                if allowed_file(filename):
                    files.append({
                        "filename": filename,
                        "url": f"/uploads/{filename}",
                        "size": os.path.getsize(os.path.join(UPLOAD_FOLDER, filename))
                    })
        return jsonify({"files": files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# --- МАРШРУТЫ ДЛЯ СКРАПИНГА ---
@app.route("/api/scrape_profile", methods=["POST"])
@jwt_required()
def scrape_profile():
    try:
        data = request.get_json()
        profile_url = data.get('profile_url')
        
        if not profile_url:
            return jsonify({"error": "URL профиля не указан"}), 400
        
        # Load existing profiles
        profiles = []
        if os.path.exists(SCRAPING_PROFILES_FILE):
            with open(SCRAPING_PROFILES_FILE, 'r', encoding='utf-8') as f:
                profiles = json.load(f)
        
        # Scrape profile data
        response = requests.get(profile_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract basic info (customize based on target site)
        profile_data = {
            'url': profile_url,
            'title': soup.find('title').text if soup.find('title') else 'Unknown',
            'description': soup.find('meta', {'name': 'description'})['content'] if soup.find('meta', {'name': 'description'}) else '',
            'scraped_at': str(datetime.now())
        }
        
        profiles.append(profile_data)
        
        # Save updated profiles
        with open(SCRAPING_PROFILES_FILE, 'w', encoding='utf-8') as f:
            json.dump(profiles, f, ensure_ascii=False, indent=2)
        
        return jsonify({"message": "Профиль успешно обработан", "data": profile_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/scraped_profiles", methods=["GET"])
@jwt_required()
def get_scraped_profiles():
    try:
        profiles = []
        if os.path.exists(SCRAPING_PROFILES_FILE):
            with open(SCRAPING_PROFILES_FILE, 'r', encoding='utf-8') as f:
                profiles = json.load(f)
        return jsonify({"profiles": profiles}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- СТАТИЧЕСКИЕ МАРШРУТЫ ---
@app.route("/public_site/<path:filename>")
def public_site(filename):
    return send_from_directory(PUBLIC_SITE_DIR, filename)

@app.route("/public_site/")
def public_site_index():
    return send_from_directory(PUBLIC_SITE_DIR, 'index.html')

@app.route("/")
def index():
    return "ProThemesRU Backend is running. Access React frontend on port 3000."

if __name__ == '__main__':
    app.run(debug=True, port=5000) 