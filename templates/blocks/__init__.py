# Главный файл системы блоков ProThemesRU

from .basic import basic_blocks
from .content import content_blocks
from .interactive import interactive_blocks
from .media import media_blocks
from .business import business_blocks
from .social import social_blocks

# Объединение всех блоков
all_blocks = {
    **basic_blocks,
    **content_blocks,
    **interactive_blocks,
    **media_blocks,
    **business_blocks,
    **social_blocks
}

# Категории блоков
block_categories = {
    "basic": "Базовые элементы",
    "content": "Контентные блоки",
    "interactive": "Интерактивные элементы",
    "media": "Медиа контент",
    "business": "Бизнес элементы",
    "social": "Социальные сети"
}

# Функции для работы с блоками
def get_blocks_by_category(category):
    """Возвращает все блоки указанной категории"""
    if category == "basic":
        return basic_blocks
    elif category == "content":
        return content_blocks
    elif category == "interactive":
        return interactive_blocks
    elif category == "media":
        return media_blocks
    elif category == "business":
        return business_blocks
    elif category == "social":
        return social_blocks
    else:
        return {}

def get_all_categories():
    """Возвращает список всех доступных категорий"""
    return list(block_categories.keys())

def get_block_by_id(block_id):
    """Возвращает блок по его ID"""
    return all_blocks.get(block_id)

def search_blocks(query):
    """Поиск блоков по названию"""
    query = query.lower()
    return {k: v for k, v in all_blocks.items() if query in v['name'].lower()}

def get_block_categories():
    """Возвращает словарь категорий с описаниями"""
    return block_categories

def get_blocks_count():
    """Возвращает количество блоков в каждой категории"""
    return {
        "basic": len(basic_blocks),
        "content": len(content_blocks),
        "interactive": len(interactive_blocks),
        "media": len(media_blocks),
        "business": len(business_blocks),
        "social": len(social_blocks),
        "total": len(all_blocks)
    } 