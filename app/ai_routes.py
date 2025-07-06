from flask import Blueprint, request, jsonify
import random
import colorsys

ai_bp = Blueprint('ai', __name__)

# Простая система генерации цветовых палитр на основе ключевых слов
COLOR_PALETTES = {
    'nature': ['#2E8B57', '#90EE90', '#228B22', '#32CD32', '#006400'],
    'ocean': ['#1E90FF', '#87CEEB', '#4682B4', '#00CED1', '#008B8B'],
    'sunset': ['#FF6347', '#FF8C00', '#FFD700', '#FF69B4', '#DC143C'],
    'forest': ['#228B22', '#32CD32', '#006400', '#8FBC8F', '#556B2F'],
    'modern': ['#2C3E50', '#34495E', '#3498DB', '#E74C3C', '#ECF0F1'],
    'warm': ['#FF6B6B', '#FFE66D', '#FF8E53', '#FF6B9D', '#FFA07A'],
    'cool': ['#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD'],
    'minimal': ['#FFFFFF', '#F8F9FA', '#E9ECEF', '#6C757D', '#212529'],
    'vintage': ['#8B4513', '#D2691E', '#CD853F', '#DEB887', '#F5DEB3'],
    'neon': ['#FF1493', '#00FF00', '#00FFFF', '#FF00FF', '#FFFF00']
}

@ai_bp.route('/generate-palette', methods=['POST'])
def generate_palette():
    """Генерация цветовой палитры"""
    data = request.get_json()
    keyword = data.get('keyword', 'blue')
    
    # Простая логика генерации палитр
    palettes = {
        'blue': ['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe'],
        'green': ['#14532d', '#16a34a', '#22c55e', '#4ade80', '#bbf7d0'],
        'red': ['#7f1d1d', '#dc2626', '#ef4444', '#f87171', '#fecaca'],
        'purple': ['#581c87', '#9333ea', '#a855f7', '#c084fc', '#e9d5ff'],
        'orange': ['#7c2d12', '#ea580c', '#f97316', '#fb923c', '#fed7aa']
    }
    
    palette = palettes.get(keyword.lower(), palettes['blue'])
    
    return jsonify({
        'palette': palette,
        'keyword': keyword
    })

@ai_bp.route('/suggest_colors', methods=['POST'])
def suggest_colors():
    """Предлагает цвета на основе существующего цвета"""
    try:
        data = request.get_json()
        base_color = data.get('base_color', '#000000')
        
        # Парсим базовый цвет
        r, g, b = int(base_color[1:3], 16), int(base_color[3:5], 16), int(base_color[5:7], 16)
        
        # Генерируем комплементарные цвета
        suggestions = []
        
        # Комплементарный цвет
        comp_r, comp_g, comp_b = 255 - r, 255 - g, 255 - b
        suggestions.append(f'#{comp_r:02x}{comp_g:02x}{comp_b:02x}')
        
        # Аналогичные цвета
        for i in range(3):
            new_r = max(0, min(255, r + random.randint(-50, 50)))
            new_g = max(0, min(255, g + random.randint(-50, 50)))
            new_b = max(0, min(255, b + random.randint(-50, 50)))
            suggestions.append(f'#{new_r:02x}{new_g:02x}{new_b:02x}')
        
        # Монохромные варианты
        for i in range(2):
            factor = 0.3 + (i * 0.4)  # 30% и 70% от базового цвета
            mono_r = int(r * factor)
            mono_g = int(g * factor)
            mono_b = int(b * factor)
            suggestions.append(f'#{mono_r:02x}{mono_g:02x}{mono_b:02x}')
        
        return jsonify({
            'success': True,
            'suggestions': suggestions
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_bp.route('/analyze_design', methods=['POST'])
def analyze_design():
    """Анализирует дизайн и предлагает улучшения"""
    try:
        data = request.get_json()
        colors = data.get('colors', [])
        layout = data.get('layout', '')
        
        suggestions = []
        
        # Анализ цветовой схемы
        if len(colors) < 3:
            suggestions.append("Рекомендуется использовать 3-5 цветов для лучшего баланса")
        
        if len(colors) > 7:
            suggestions.append("Слишком много цветов может создать визуальный хаос")
        
        # Анализ контраста
        if colors:
            # Простая проверка на светлые/темные цвета
            light_colors = 0
            for color in colors:
                r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
                brightness = (r * 299 + g * 587 + b * 114) / 1000
                if brightness > 128:
                    light_colors += 1
            
            if light_colors == len(colors):
                suggestions.append("Рекомендуется добавить темные цвета для лучшего контраста")
            elif light_colors == 0:
                suggestions.append("Рекомендуется добавить светлые цвета для лучшей читаемости")
        
        return jsonify({
            'success': True,
            'suggestions': suggestions,
            'score': max(0, 100 - len(suggestions) * 20)  # Простая оценка
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@ai_bp.route('/health', methods=['GET'])
def health_check():
    """Проверка здоровья AI сервиса."""
    return jsonify({
        'status': 'ok',
        'service': 'ai_color_palette',
        'message': 'AI сервис работает'
    }) 