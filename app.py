from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import json
import uuid
import requests
from datetime import datetime, timedelta
from urllib.parse import urljoin, urlparse
import re
import mimetypes
import shutil
from bs4 import BeautifulSoup

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///prothemesru.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MEDIA_FOLDER'] = 'media'
app.config['SCRAPED_FOLDER'] = 'scraped_sites'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MEDIA_FOLDER'], exist_ok=True)
os.makedirs(app.config['SCRAPED_FOLDER'], exist_ok=True)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user')  # user, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    name = db.Column(db.String(255))  # Full name
    phone = db.Column(db.String(20))
    company = db.Column(db.String(255))

class Site(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    elements = db.Column(db.Text)  # JSON string
    canvas_settings = db.Column(db.Text)  # JSON string for canvas background
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=False)
    published_url = db.Column(db.String(255))

class ScrapingProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    sections = db.Column(db.Text)  # JSON string
    fields = db.Column(db.Text)  # JSON string
    options = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MediaFile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, cancelled
    items = db.Column(db.Text)  # JSON string
    customer_info = db.Column(db.Text)  # JSON string
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Template(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    downloads = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')  # active, inactive
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Helper functions
def sanitize_filename(filename):
    """Sanitize filename for safe storage"""
    name, ext = os.path.splitext(filename)
    name = re.sub(r'[^\w\-_.]', '_', name)
    return f"{name}_{uuid.uuid4().hex[:8]}{ext}"

def download_asset(url, base_url, output_dir):
    """Download asset and return local path"""
    try:
        if not url.startswith(('http://', 'https://')):
            url = urljoin(base_url, url)
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Determine file extension
        content_type = response.headers.get('content-type', '')
        ext = mimetypes.guess_extension(content_type) or '.bin'
        
        # Create filename
        filename = f"asset_{uuid.uuid4().hex[:8]}{ext}"
        file_path = os.path.join(output_dir, filename)
        
        # Save file
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        return filename
    except Exception as e:
        print(f"Error downloading asset {url}: {e}")
        return None

def rewrite_html_urls(html_content, base_url, assets_dir):
    """Rewrite URLs in HTML content"""
    def replace_url(match):
        url = match.group(1)
        if url.startswith(('http://', 'https://', 'data:', '#')):
            return match.group(0)
        
        # Download asset and get local filename
        local_filename = download_asset(url, base_url, assets_dir)
        if local_filename:
            return f'src="{local_filename}"'
        return match.group(0)
    
    # Replace src attributes
    html_content = re.sub(r'src=["\']([^"\']+)["\']', replace_url, html_content)
    
    # Replace href attributes for CSS files
    html_content = re.sub(r'href=["\']([^"\']+\.css[^"\']*)["\']', replace_url, html_content)
    
    return html_content

def scrape_page(url, depth=1, follow_links=True, download_assets=True, asset_types=None):
    """Scrape single page with advanced options"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Create output directory
        domain = urlparse(url).netloc
        page_name = urlparse(url).path.strip('/') or 'index'
        output_dir = os.path.join(app.config['SCRAPED_FOLDER'], domain, page_name)
        assets_dir = os.path.join(output_dir, 'assets')
        os.makedirs(assets_dir, exist_ok=True)
        
        # Download and rewrite assets if enabled
        if download_assets:
            html_content = rewrite_html_urls(str(soup), url, assets_dir)
        else:
            html_content = str(soup)
        
        # Save HTML
        html_file = os.path.join(output_dir, 'index.html')
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Extract content based on scraping profile
        content = {
            'title': soup.title.string if soup.title else '',
            'text': soup.get_text(separator=' ', strip=True),
            'links': [a.get('href') for a in soup.find_all('a', href=True)],
            'images': [img.get('src') for img in soup.find_all('img', src=True)],
            'html_file': html_file,
            'assets_dir': assets_dir
        }
        
        return content
        
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# Authentication routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken'}), 400
    
    user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        name=data.get('name', ''),
        phone=data.get('phone', ''),
        company=data.get('company', ''),
        role='admin' if data.get('is_admin') else 'user'
    )
    
    db.session.add(user)
    db.session.commit()
    
    access_token = create_access_token(identity=user.id)
    return jsonify({
        'token': access_token,
        'user': {
            'id': user.id,
            'name': user.name or user.username,
            'email': user.email,
            'role': user.role
        }
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            'token': access_token,
            'user': {
                'id': user.id,
                'name': user.name or user.username,
                'email': user.email,
                'role': user.role
            }
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user': {
            'id': user.id,
            'name': user.name or user.username,
            'email': user.email,
            'role': user.role,
            'phone': user.phone,
            'company': user.company,
            'created_at': user.created_at.isoformat()
        }
    })

@app.route('/api/auth/update', methods=['PATCH'])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        user.name = data['name']
    if 'phone' in data:
        user.phone = data['phone']
    if 'company' in data:
        user.company = data['company']
    
    db.session.commit()
    
    return jsonify({
        'user': {
            'id': user.id,
            'name': user.name or user.username,
            'email': user.email,
            'role': user.role,
            'phone': user.phone,
            'company': user.company
        }
    })

# User management routes
@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    users = User.query.all()
    return jsonify({
        'users': [{
            'id': user.id,
            'name': user.name or user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.isoformat(),
            'is_active': user.is_active
        } for user in users]
    })

# Site management routes
@app.route('/api/sites', methods=['GET'])
@jwt_required()
def get_sites():
    user_id = get_jwt_identity()
    sites = Site.query.filter_by(user_id=user_id).all()
    
    return jsonify([{
        'id': site.id,
        'name': site.name,
        'created_at': site.created_at.isoformat(),
        'updated_at': site.updated_at.isoformat(),
        'is_published': site.is_published,
        'published_url': site.published_url
    } for site in sites])

@app.route('/api/sites', methods=['POST'])
@jwt_required()
def create_site():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    site = Site(
        user_id=user_id,
        name=data['name'],
        elements=json.dumps(data.get('elements', [])),
        canvas_settings=json.dumps(data.get('canvas_settings', {}))
    )
    
    db.session.add(site)
    db.session.commit()
    
    return jsonify({
        'id': site.id,
        'name': site.name,
        'message': 'Site created successfully'
    }), 201

@app.route('/api/sites/<int:site_id>', methods=['GET'])
@jwt_required()
def get_site(site_id):
    user_id = get_jwt_identity()
    site = Site.query.filter_by(id=site_id, user_id=user_id).first()
    
    if not site:
        return jsonify({'error': 'Site not found'}), 404
    
    return jsonify({
        'id': site.id,
        'name': site.name,
        'elements': json.loads(site.elements) if site.elements else [],
        'canvas_settings': json.loads(site.canvas_settings) if site.canvas_settings else {},
        'created_at': site.created_at.isoformat(),
        'updated_at': site.updated_at.isoformat(),
        'is_published': site.is_published,
        'published_url': site.published_url
    })

@app.route('/api/sites/<int:site_id>', methods=['PUT'])
@jwt_required()
def update_site(site_id):
    user_id = get_jwt_identity()
    site = Site.query.filter_by(id=site_id, user_id=user_id).first()
    
    if not site:
        return jsonify({'error': 'Site not found'}), 404
    
    data = request.get_json()
    
    site.name = data.get('name', site.name)
    site.elements = json.dumps(data.get('elements', []))
    site.canvas_settings = json.dumps(data.get('canvas_settings', {}))
    site.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'message': 'Site updated successfully'})

@app.route('/api/sites/<int:site_id>/publish', methods=['POST'])
@jwt_required()
def publish_site(site_id):
    user_id = get_jwt_identity()
    site = Site.query.filter_by(id=site_id, user_id=user_id).first()
    
    if not site:
        return jsonify({'error': 'Site not found'}), 404
    
    # Generate HTML and CSS
    elements = json.loads(site.elements) if site.elements else []
    canvas_settings = json.loads(site.canvas_settings) if site.canvas_settings else {}
    
    # Create HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{site.name}</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }}
            .canvas {{
                position: relative;
                width: 100%;
                min-height: 100vh;
                background-color: {canvas_settings.get('backgroundColor', '#ffffff')};
                background-image: {f"url('{canvas_settings.get('backgroundImage', '')}')" if canvas_settings.get('backgroundImage') else 'none'};
                background-repeat: {canvas_settings.get('backgroundRepeat', 'no-repeat')};
                background-size: {canvas_settings.get('backgroundSize', 'cover')};
                background-position: {canvas_settings.get('backgroundPosition', 'center')};
            }}
            {generate_css_for_elements(elements)}
        </style>
    </head>
    <body>
        <div class="canvas">
            {generate_html_for_elements(elements)}
        </div>
    </body>
    </html>
    """
    
    # Save published site
    published_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'published', str(site.id))
    os.makedirs(published_dir, exist_ok=True)
    
    html_file = os.path.join(published_dir, 'index.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    site.is_published = True
    site.published_url = f"/published/{site.id}/index.html"
    db.session.commit()
    
    return jsonify({
        'message': 'Site published successfully',
        'published_url': site.published_url
    })

# Media library routes
@app.route('/api/media', methods=['GET'])
@jwt_required()
def get_media():
    user_id = get_jwt_identity()
    media_files = MediaFile.query.filter_by(user_id=user_id).order_by(MediaFile.uploaded_at.desc()).all()
    
    return jsonify([{
        'id': file.id,
        'filename': file.filename,
        'original_filename': file.original_filename,
        'file_size': file.file_size,
        'mime_type': file.mime_type,
        'uploaded_at': file.uploaded_at.isoformat(),
        'url': f"/api/media/{file.id}"
    } for file in media_files])

@app.route('/api/media', methods=['POST'])
@jwt_required()
def upload_media():
    user_id = get_jwt_identity()
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Validate file type
    allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        return jsonify({'error': 'Invalid file type'}), 400
    
    # Save file
    filename = sanitize_filename(file.filename)
    file_path = os.path.join(app.config['MEDIA_FOLDER'], filename)
    file.save(file_path)
    
    # Create database record
    media_file = MediaFile(
        filename=filename,
        original_filename=file.filename,
        file_path=file_path,
        file_size=os.path.getsize(file_path),
        mime_type=file.content_type,
        user_id=user_id
    )
    
    db.session.add(media_file)
    db.session.commit()
    
    return jsonify({
        'id': media_file.id,
        'filename': filename,
        'original_filename': file.filename,
        'url': f"/api/media/{media_file.id}",
        'message': 'File uploaded successfully'
    }), 201

@app.route('/api/media/<int:file_id>', methods=['GET'])
@jwt_required()
def get_media_file(file_id):
    user_id = get_jwt_identity()
    media_file = MediaFile.query.filter_by(id=file_id, user_id=user_id).first()
    
    if not media_file:
        return jsonify({'error': 'File not found'}), 404
    
    return send_from_directory(app.config['MEDIA_FOLDER'], media_file.filename)

@app.route('/api/media/<int:file_id>', methods=['DELETE'])
@jwt_required()
def delete_media_file(file_id):
    user_id = get_jwt_identity()
    media_file = MediaFile.query.filter_by(id=file_id, user_id=user_id).first()
    
    if not media_file:
        return jsonify({'error': 'File not found'}), 404
    
    # Delete file from filesystem
    try:
        os.remove(media_file.file_path)
    except OSError:
        pass  # File might already be deleted
    
    # Delete from database
    db.session.delete(media_file)
    db.session.commit()
    
    return jsonify({'message': 'File deleted successfully'})

# Scraping routes
@app.route('/api/scraping/profiles', methods=['GET'])
@jwt_required()
def get_scraping_profiles():
    profiles = ScrapingProfile.query.all()
    
    return jsonify([{
        'id': profile.id,
        'name': profile.name,
        'url': profile.url,
        'sections': json.loads(profile.sections) if profile.sections else [],
        'fields': json.loads(profile.fields) if profile.fields else [],
        'options': json.loads(profile.options) if profile.options else {},
        'created_at': profile.created_at.isoformat(),
        'updated_at': profile.updated_at.isoformat()
    } for profile in profiles])

@app.route('/api/scraping/profiles', methods=['POST'])
@jwt_required()
def create_scraping_profile():
    data = request.get_json()
    
    profile = ScrapingProfile(
        name=data['name'],
        url=data['url'],
        sections=json.dumps(data.get('sections', [])),
        fields=json.dumps(data.get('fields', [])),
        options=json.dumps(data.get('options', {}))
    )
    
    db.session.add(profile)
    db.session.commit()
    
    return jsonify({
        'id': profile.id,
        'name': profile.name,
        'message': 'Profile created successfully'
    }), 201

@app.route('/api/scraping/profiles/<int:profile_id>', methods=['PUT'])
@jwt_required()
def update_scraping_profile(profile_id):
    profile = ScrapingProfile.query.get(profile_id)
    
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    data = request.get_json()
    
    profile.name = data.get('name', profile.name)
    profile.url = data.get('url', profile.url)
    profile.sections = json.dumps(data.get('sections', []))
    profile.fields = json.dumps(data.get('fields', []))
    profile.options = json.dumps(data.get('options', {}))
    profile.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({'message': 'Profile updated successfully'})

@app.route('/api/scraping/profiles/<int:profile_id>', methods=['DELETE'])
@jwt_required()
def delete_scraping_profile(profile_id):
    profile = ScrapingProfile.query.get(profile_id)
    
    if not profile:
        return jsonify({'error': 'Profile not found'}), 404
    
    db.session.delete(profile)
    db.session.commit()
    
    return jsonify({'message': 'Profile deleted successfully'})

@app.route('/api/scraping/scrape', methods=['POST'])
@jwt_required()
def scrape_site():
    data = request.get_json()
    url = data['url']
    options = data.get('options', {})
    
    # Scrape the site
    result = scrape_page(
        url=url,
        depth=options.get('maxDepth', 1),
        follow_links=options.get('followLinks', False),
        download_assets=options.get('downloadAssets', True),
        asset_types=options.get('assetTypes', ['images', 'css', 'js'])
    )
    
    if result:
        return jsonify({
            'message': 'Site scraped successfully',
            'result': result
        })
    else:
        return jsonify({'error': 'Failed to scrape site'}), 500

# Order routes
@app.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    if current_user.role == 'admin':
        orders = Order.query.all()
    else:
        orders = Order.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'orders': [{
            'id': order.id,
            'order_number': order.order_number,
            'amount': order.amount,
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'updated_at': order.updated_at.isoformat(),
            'items': json.loads(order.items) if order.items else [],
            'customer_info': json.loads(order.customer_info) if order.customer_info else {}
        } for order in orders]
    })

@app.route('/api/orders', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Generate order number
    order_number = f"ORD-{datetime.now().strftime('%Y-%m')}-{uuid.uuid4().hex[:6].upper()}"
    
    order = Order(
        order_number=order_number,
        user_id=user_id,
        amount=data['amount'],
        items=json.dumps(data['items']),
        customer_info=json.dumps(data['customer_info']),
        status='pending'
    )
    
    db.session.add(order)
    db.session.commit()
    
    return jsonify({
        'order': {
            'id': order.id,
            'order_number': order.order_number,
            'amount': order.amount,
            'status': order.status,
            'created_at': order.created_at.isoformat()
        }
    }), 201

# Template routes
@app.route('/api/templates', methods=['GET'])
def get_templates():
    templates = Template.query.filter_by(status='active').all()
    return jsonify({
        'templates': [{
            'id': template.id,
            'name': template.name,
            'category': template.category,
            'price': template.price,
            'downloads': template.downloads,
            'rating': template.rating,
            'status': template.status
        } for template in templates]
    })

@app.route('/api/admin/templates', methods=['GET'])
@jwt_required()
def admin_get_templates():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    templates = Template.query.all()
    return jsonify({
        'templates': [{
            'id': template.id,
            'name': template.name,
            'category': template.category,
            'price': template.price,
            'downloads': template.downloads,
            'rating': template.rating,
            'status': template.status,
            'created_at': template.created_at.isoformat()
        } for template in templates]
    })

# Admin routes
@app.route('/api/admin/dashboard', methods=['GET'])
@jwt_required()
def admin_dashboard():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get statistics
    total_users = User.query.count()
    total_projects = Site.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.amount)).filter_by(status='completed').scalar() or 0
    active_templates = Template.query.filter_by(status='active').count()
    
    # Get recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    return jsonify({
        'stats': {
            'total_users': total_users,
            'total_projects': total_projects,
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'active_templates': active_templates
        },
        'recent_orders': [{
            'id': order.id,
            'order_number': order.order_number,
            'amount': order.amount,
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'customer_info': json.loads(order.customer_info) if order.customer_info else {}
        } for order in recent_orders]
    })

@app.route('/api/admin/users', methods=['GET'])
@jwt_required()
def admin_get_users():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    users = User.query.all()
    return jsonify({
        'users': [{
            'id': user.id,
            'name': user.name or user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.isoformat(),
            'is_active': user.is_active
        } for user in users]
    })

@app.route('/api/admin/orders', methods=['GET'])
@jwt_required()
def admin_get_orders():
    user_id = get_jwt_identity()
    current_user = User.query.get(user_id)
    
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    orders = Order.query.all()
    return jsonify({
        'orders': [{
            'id': order.id,
            'order_number': order.order_number,
            'amount': order.amount,
            'status': order.status,
            'created_at': order.created_at.isoformat(),
            'customer_info': json.loads(order.customer_info) if order.customer_info else {}
        } for order in orders]
    })

# Public routes for serving published sites
@app.route('/published/<int:site_id>/<path:filename>')
def serve_published_site(site_id, filename):
    published_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'published', str(site_id))
    return send_from_directory(published_dir, filename)

@app.route('/scraped/<path:filename>')
def serve_scraped_content(filename):
    return send_from_directory(app.config['SCRAPED_FOLDER'], filename)

# Helper functions for HTML/CSS generation
def generate_css_for_elements(elements):
    """Generate CSS for elements"""
    css = ""
    for element in elements:
        element_id = element.get('id', '')
        styles = element.get('styles', {})
        
        if styles:
            css += f"\n#{element_id} {{\n"
            for property, value in styles.items():
                css += f"    {property}: {value};\n"
            css += "}\n"
    
    return css

def generate_html_for_elements(elements):
    """Generate HTML for elements"""
    html = ""
    for element in elements:
        element_type = element.get('type', 'div')
        element_id = element.get('id', '')
        content = element.get('content', '')
        styles = element.get('styles', {})
        
        # Create element
        if element_type == 'text':
            html += f'<div id="{element_id}" class="text-element">{content}</div>\n'
        elif element_type == 'image':
            src = content if content else 'placeholder.jpg'
            html += f'<img id="{element_id}" src="{src}" alt="Image" class="image-element">\n'
        elif element_type == 'button':
            html += f'<button id="{element_id}" class="button-element">{content}</button>\n'
        elif element_type == 'shape':
            html += f'<div id="{element_id}" class="shape-element"></div>\n'
        elif element_type == 'group':
            children = element.get('children', [])
            html += f'<div id="{element_id}" class="group-element">\n'
            html += generate_html_for_elements(children)
            html += '</div>\n'
        else:
            html += f'<div id="{element_id}" class="element">{content}</div>\n'
    
    return html

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
