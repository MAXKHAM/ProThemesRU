from typing import Dict, List, Optional
from transformers import AutoModel, AutoTokenizer
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os
from dotenv import load_dotenv

load_dotenv()

class DesignService:
    def __init__(self):
        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self.embeddings = None
        self.design_templates = []
        self.index = None
        self._load_design_templates()
        self._build_index()

    def _load_design_templates(self):
        """Загружает шаблоны дизайна из файла"""
        with open('design_templates.json', 'r', encoding='utf-8') as f:
            self.design_templates = json.load(f)

    def _build_index(self):
        """Строит индекс для быстрого поиска похожих дизайнов"""
        texts = [template['description'] for template in self.design_templates]
        embeddings = self.model.encode(texts)
        self.embeddings = embeddings
        
        # Создаем индекс FAISS
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings))

    def suggest_design(self, description: str) -> List[Dict]:
        """
        Предлагает дизайн на основе описания
        
        Args:
            description: Описание желаемого дизайна
            
        Returns:
            Список предложенных дизайнов
        """
        # Получаем эмбеддинг описания
        query_embedding = self.model.encode([description])
        
        # Находим похожие дизайны
        D, I = self.index.search(query_embedding, 5)
        
        # Формируем результат
        suggestions = []
        for idx in I[0]:
            template = self.design_templates[idx]
            suggestions.append({
                'name': template['name'],
                'description': template['description'],
                'elements': template['elements'],
                'confidence': 1 - D[0][list(I[0]).index(idx)] / 100
            })
        
        return suggestions

    def generate_color_scheme(self, mood: str) -> Dict:
        """
        Генерирует цветовую схему на основе настроения
        
        Args:
            mood: Описание настроения (например, "корпоративный", "творческий", "минималистичный")
            
        Returns:
            Словарь с цветами в формате HEX
        """
        # Простой пример генерации цветовой схемы
        color_schemes = {
            'корпоративный': {
                'primary': '#007bff',
                'secondary': '#6c757d',
                'accent': '#28a745',
                'background': '#f8f9fa'
            },
            'творческий': {
                'primary': '#ff6b6b',
                'secondary': '#4ecdc4',
                'accent': '#45b7d1',
                'background': '#f5f7fa'
            },
            'минималистичный': {
                'primary': '#2d3436',
                'secondary': '#7f8c8d',
                'accent': '#3498db',
                'background': '#ffffff'
            }
        }
        
        # Выбираем схему на основе настроения
        mood = mood.lower()
        if 'корпоратив' in mood:
            return color_schemes['корпоративный']
        elif 'творческ' in mood:
            return color_schemes['творческий']
        else:
            return color_schemes['минималистичный']

    def analyze_design(self, design: Dict) -> Dict:
        """
        Анализирует дизайн и предлагает улучшения
        
        Args:
            design: Словарь с описанием дизайна
            
        Returns:
            Словарь с результатами анализа
        """
        analysis = {
            'readability': self._analyze_readability(design),
            'contrast': self._analyze_contrast(design),
            'balance': self._analyze_balance(design),
            'suggestions': self._get_improvement_suggestions(design)
        }
        return analysis

    def _analyze_readability(self, design: Dict) -> float:
        """Анализирует читаемость дизайна"""
        # Простой пример анализа
        font_size = design.get('font_size', 16)
        line_height = design.get('line_height', 1.5)
        return min(1.0, (font_size / 16) * (line_height / 1.5))

    def _analyze_contrast(self, design: Dict) -> float:
        """Анализирует контрастность"""
        # Простой пример анализа контраста
        from wcag_contrast_ratio import contrast_ratio
        bg_color = design.get('background_color', '#ffffff')
        text_color = design.get('text_color', '#000000')
        
        try:
            ratio = contrast_ratio(text_color, bg_color)
            return min(1.0, (ratio - 3.0) / 7.0)  # WCAG AAA requires at least 7:1
        except:
            return 0.5

    def _analyze_balance(self, design: Dict) -> float:
        """Анализирует баланс композиции"""
        # Простой пример анализа
        elements = design.get('elements', [])
        if not elements:
            return 0.5
            
        total_weight = sum(element.get('weight', 1) for element in elements)
        left_weight = sum(
            element.get('weight', 1) 
            for element in elements 
            if element.get('position', {}).get('x') < 0.5
        )
        
        return min(1.0, abs(0.5 - (left_weight / total_weight)))

    def _get_improvement_suggestions(self, design: Dict) -> List[str]:
        """Получает предложения по улучшению дизайна"""
        suggestions = []
        
        if self._analyze_readability(design) < 0.7:
            suggestions.append("Увеличьте размер шрифта и/или межстрочный интервал для лучшей читаемости")
            
        if self._analyze_contrast(design) < 0.7:
            suggestions.append("Улучшите контрастность текста и фона для лучшей видимости")
            
        if self._analyze_balance(design) > 0.3:
            suggestions.append("Рассмотрите возможность перераспределения элементов для лучшего баланса")
            
        return suggestions

# Создаем экземпляр сервиса
ai_design_service = DesignService()
