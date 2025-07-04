from flask import Blueprint, jsonify, request
from app.models import Block
from app import db

blocks_bp = Blueprint('blocks', __name__)

# Базовые блоки
BASE_BLOCKS = {
    'header': {
        'type': 'header',
        'name': 'Заголовок',
        'html': '''
            <header class="block-header">
                <nav class="navbar navbar-expand-lg">
                    <div class="container">
                        <a class="navbar-brand" href="#">{logo}</a>
                        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                            <span class="navbar-toggler-icon"></span>
                        </button>
                        <div class="collapse navbar-collapse" id="navbarNav">
                            <ul class="navbar-nav">
                                <li class="nav-item">
                                    <a class="nav-link" href="#">Главная</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="#">О нас</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="#">Услуги</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="#">Контакты</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </nav>
            </header>
        ''',
        'styles': {
            'backgroundColor': '#ffffff',
            'padding': '20px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
        }
    },
    'hero': {
        'type': 'hero',
        'name': 'Герой',
        'html': '''
            <section class="block-hero">
                <div class="container">
                    <div class="row align-items-center">
                        <div class="col-md-6">
                            <h1 class="editable">{title}</h1>
                            <p class="editable">{description}</p>
                            <a href="#" class="btn btn-primary">{buttonText}</a>
                        </div>
                        <div class="col-md-6">
                            <img src="{imageUrl}" alt="{altText}" class="img-fluid">
                        </div>
                    </div>
                </div>
            </section>
        ''',
        'styles': {
            'backgroundColor': '#f8fafc',
            'minHeight': '400px',
            'padding': '40px'
        }
    },
    'features': {
        'type': 'features',
        'name': 'Функции',
        'html': '''
            <section class="block-features">
                <div class="container">
                    <div class="row">
                        <div class="col-md-4">
                            <div class="feature-item">
                                <i class="fas fa-check-circle"></i>
                                <h3>{feature1Title}</h3>
                                <p>{feature1Description}</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="feature-item">
                                <i class="fas fa-check-circle"></i>
                                <h3>{feature2Title}</h3>
                                <p>{feature2Description}</p>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="feature-item">
                                <i class="fas fa-check-circle"></i>
                                <h3>{feature3Title}</h3>
                                <p>{feature3Description}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        ''',
        'styles': {
            'backgroundColor': '#ffffff',
            'padding': '60px'
        }
    },
    'portfolio': {
        'type': 'portfolio',
        'name': 'Портфолио',
        'html': '''
            <section class="block-portfolio">
                <div class="container">
                    <h2 class="section-title">{title}</h2>
                    <div class="row portfolio-grid">
                        <!-- Добавляется через JavaScript -->
                    </div>
                </div>
            </section>
        ''',
        'styles': {
            'backgroundColor': '#f8fafc',
            'padding': '80px'
        }
    },
    'contact': {
        'type': 'contact',
        'name': 'Контакты',
        'html': '''
            <section class="block-contact">
                <div class="container">
                    <h2 class="section-title">{title}</h2>
                    <div class="row">
                        <div class="col-md-6">
                            <form class="contact-form">
                                <div class="mb-3">
                                    <input type="text" class="form-control" placeholder="Имя">
                                </div>
                                <div class="mb-3">
                                    <input type="email" class="form-control" placeholder="Email">
                                </div>
                                <div class="mb-3">
                                    <textarea class="form-control" placeholder="Сообщение"></textarea>
                                </div>
                                <button type="submit" class="btn btn-primary">Отправить</button>
                            </form>
                        </div>
                        <div class="col-md-6">
                            <div class="contact-info">
                                <h3>Контактная информация</h3>
                                <p><i class="fas fa-map-marker-alt"></i> {address}</p>
                                <p><i class="fas fa-phone"></i> {phone}</p>
                                <p><i class="fas fa-envelope"></i> {email}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
        ''',
        'styles': {
            'backgroundColor': '#ffffff',
            'padding': '80px'
        }
    }
}

@blocks_bp.route('/api/blocks', methods=['GET'])
def get_blocks():
    return jsonify(list(BASE_BLOCKS.values()))

@blocks_bp.route('/api/block/<block_type>', methods=['GET'])
def get_block(block_type):
    block = BASE_BLOCKS.get(block_type)
    if not block:
        return jsonify({'error': 'Block not found'}), 404
    return jsonify(block)

@blocks_bp.route('/api/block/<block_type>/preview', methods=['POST'])
def preview_block(block_type):
    data = request.json
    block = BASE_BLOCKS.get(block_type)
    if not block:
        return jsonify({'error': 'Block not found'}), 404
    
    # Заменяем плейсхолдеры данными
    html = block['html']
    for key, value in data.items():
        html = html.replace(f'{{{key}}}', str(value))
    
    return jsonify({
        'html': html,
        'styles': block['styles']
    })
