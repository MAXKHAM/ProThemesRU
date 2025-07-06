from flask import Blueprint, request, jsonify
import random

ai_tools_bp = Blueprint('ai_tools', __name__)

# Имитация "AI" для генерации цветовых палитр
# В реальном проекте здесь будет логика взаимодействия с ML-моделями
def generate_mock_palette(keyword):
    keyword = keyword.lower()
    
    # Очень простая логика на основе ключевых слов
    if "природа" in keyword or "лес" in keyword or "зеленый" in keyword:
        return [
            ["#4CAF50", "#8BC34A", "#CDDC39", "#FFEB3B", "#FFC107"], # Зеленый, желтый
            ["#1B5E20", "#388E3C", "#66BB6A", "#A5D6A7", "#C8E6C9"]  # Оттенки зеленого
        ]
    elif "техно" in keyword or "синий" in keyword or "футуризм" in keyword:
        return [
            ["#2196F3", "#03A9F4", "#00BCD4", "#00BCD4", "#26C6DA"], # Синий, голубой
            ["#3F51B5", "#303F9F", "#1A237E", "#5C6BC0", "#9FA8DA"]  # Темно-синий
        ]
    elif "тепло" in keyword or "красный" in keyword or "оранжевый" in keyword:
        return [
            ["#FF5722", "#FF9800", "#FFC107", "#FFEB3B", "#FFECB3"], # Оранжевый, красный, желтый
            ["#D32F2F", "#F44336", "#EF5350", "#E57373", "#EF9A9A"]  # Оттенки красного
        ]
    elif "холод" in keyword or "фиолетовый" in keyword or "синий" in keyword:
        return [
            ["#9C27B0", "#673AB7", "#3F51B5", "#2196F3", "#03A9F4"], # Фиолетовый, синий
            ["#4A148C", "#6A1B9A", "#8E24AA", "#AB47BC", "#CE93D8"]  # Оттенки фиолетового
        ]
    else:
        # Случайные палитры, если ключевое слово не распознано
        palettes = [
            ["#F44336", "#E91E63", "#9C27B0", "#673AB7", "#3F51B5"],
            ["#2196F3", "#03A9F4", "#00BCD4", "#009688", "#4CAF50"],
            ["#8BC34A", "#CDDC39", "#FFEB3B", "#FFC107", "#FF9800"],
            ["#FF5722", "#795548", "#607D8B", "#9E9E9E", "#BDBDBD"],
            ["#FFEB3B", "#FFC107", "#FF9800", "#FF5722", "#F44336"]
        ]
        return random.sample(palettes, 2) # Выбираем 2 случайные палитры

@ai_tools_bp.route('/generate_palette', methods=['POST'])
def generate_palette():
    data = request.get_json()
    keyword = data.get('keyword', 'default')

    if not keyword:
        return jsonify({"error": "Keyword is required"}), 400

    palettes = generate_mock_palette(keyword)
    return jsonify({"palettes": palettes}) 