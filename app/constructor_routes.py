from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

constructor_bp = Blueprint('constructor', __name__)

@constructor_bp.route('/')
@login_required
def constructor():
    """Страница конструктора"""
    return render_template('constructor.html')

@constructor_bp.route('/save', methods=['POST'])
@login_required
def save_project():
    """Сохранение проекта"""
    data = request.get_json()
    # Здесь будет логика сохранения проекта
    return jsonify({'status': 'success', 'message': 'Проект сохранен'})

@constructor_bp.route('/export', methods=['POST'])
@login_required
def export_project():
    """Экспорт проекта"""
    data = request.get_json()
    # Здесь будет логика экспорта проекта
    return jsonify({'status': 'success', 'message': 'Проект экспортирован'}) 