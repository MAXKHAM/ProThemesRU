# Система блоков для конструктора сайтов ProThemesRU

# Базовые блоки
basic_blocks = {
    "header": {
        "name": "Заголовок",
        "category": "basic",
        "html": "<header class='site-header'><h1>Заголовок сайта</h1></header>",
        "css": ".site-header { padding: 20px; background: #f8f9fa; text-align: center; }",
        "properties": ["text", "background", "padding", "font-size"]
    },
    "footer": {
        "name": "Подвал",
        "category": "basic",
        "html": "<footer class='site-footer'><p>&copy; 2024 ProThemesRU. Все права защищены.</p></footer>",
        "css": ".site-footer { padding: 20px; background: #333; color: white; text-align: center; }",
        "properties": ["text", "background", "padding", "color"]
    },
    "navigation": {
        "name": "Навигация",
        "category": "basic",
        "html": "<nav class='main-nav'><ul><li><a href='#home'>Главная</a></li><li><a href='#about'>О нас</a></li><li><a href='#contact'>Контакты</a></li></ul></nav>",
        "css": ".main-nav ul { list-style: none; display: flex; gap: 20px; } .main-nav a { text-decoration: none; color: #333; }",
        "properties": ["menu-items", "background", "color", "font-size"]
    }
}

# Контентные блоки
content_blocks = {
    "hero_section": {
        "name": "Главный экран",
        "category": "content",
        "html": "<section class='hero'><div class='hero-content'><h1>Добро пожаловать</h1><p>Создавайте потрясающие сайты с ProThemesRU</p><button class='cta-button'>Начать</button></div></section>",
        "css": ".hero { min-height: 80vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(45deg, #667eea, #764ba2); color: white; } .hero-content { text-align: center; } .cta-button { padding: 15px 30px; background: #fff; color: #333; border: none; border-radius: 5px; font-size: 18px; cursor: pointer; }",
        "properties": ["title", "subtitle", "button-text", "background", "text-color"]
    },
    "about_section": {
        "name": "О нас",
        "category": "content",
        "html": "<section class='about'><div class='container'><h2>О нашей компании</h2><p>Мы создаем инновационные решения для вашего бизнеса. Наша команда экспертов поможет воплотить ваши идеи в жизнь.</p></div></section>",
        "css": ".about { padding: 80px 0; background: #f9f9f9; } .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }",
        "properties": ["title", "content", "background", "text-color"]
    },
    "contact_section": {
        "name": "Контакты",
        "category": "content",
        "html": "<section class='contact'><div class='container'><h2>Свяжитесь с нами</h2><div class='contact-info'><p>Email: info@prothemesru.com</p><p>Телефон: +7 (999) 123-45-67</p><p>Адрес: Москва, Россия</p></div></div></section>",
        "css": ".contact { padding: 80px 0; background: #333; color: white; } .contact-info { margin-top: 30px; }",
        "properties": ["title", "email", "phone", "address", "background"]
    }
}

# Интерактивные блоки
interactive_blocks = {
    "contact_form": {
        "name": "Форма обратной связи",
        "category": "interactive",
        "html": "<form class='contact-form'><input type='text' placeholder='Ваше имя' required><input type='email' placeholder='Email' required><textarea placeholder='Сообщение' rows='5'></textarea><button type='submit'>Отправить</button></form>",
        "css": ".contact-form { display: flex; flex-direction: column; gap: 15px; max-width: 500px; margin: 0 auto; } .contact-form input, .contact-form textarea { padding: 10px; border: 1px solid #ddd; border-radius: 5px; } .contact-form button { padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }",
        "properties": ["fields", "button-text", "background", "border-color"]
    },
    "gallery": {
        "name": "Галерея изображений",
        "category": "interactive",
        "html": "<div class='gallery'><div class='gallery-item'><img src='https://via.placeholder.com/300x200' alt='Изображение 1'></div><div class='gallery-item'><img src='https://via.placeholder.com/300x200' alt='Изображение 2'></div><div class='gallery-item'><img src='https://via.placeholder.com/300x200' alt='Изображение 3'></div></div>",
        "css": ".gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; padding: 20px; } .gallery-item img { width: 100%; height: auto; border-radius: 8px; }",
        "properties": ["images", "columns", "gap", "border-radius"]
    },
    "slider": {
        "name": "Слайдер",
        "category": "interactive",
        "html": "<div class='slider'><div class='slide active'><img src='https://via.placeholder.com/800x400' alt='Слайд 1'></div><div class='slide'><img src='https://via.placeholder.com/800x400' alt='Слайд 2'></div><div class='slide'><img src='https://via.placeholder.com/800x400' alt='Слайд 3'></div><button class='slider-btn prev'>&lt;</button><button class='slider-btn next'>&gt;</button></div>",
        "css": ".slider { position: relative; overflow: hidden; } .slide { display: none; } .slide.active { display: block; } .slider-btn { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.5); color: white; border: none; padding: 10px 15px; cursor: pointer; } .prev { left: 10px; } .next { right: 10px; }",
        "properties": ["slides", "autoplay", "interval", "show-arrows"]
    }
}

# Медиа блоки
media_blocks = {
    "video": {
        "name": "Видео",
        "category": "media",
        "html": "<div class='video-container'><video controls><source src='' type='video/mp4'>Ваш браузер не поддерживает видео.</video></div>",
        "css": ".video-container { max-width: 100%; margin: 20px 0; } .video-container video { width: 100%; height: auto; border-radius: 8px; }",
        "properties": ["video-url", "autoplay", "controls", "width", "height"]
    },
    "image": {
        "name": "Изображение",
        "category": "media",
        "html": "<div class='image-block'><img src='https://via.placeholder.com/600x400' alt='Описание изображения'></div>",
        "css": ".image-block { text-align: center; margin: 20px 0; } .image-block img { max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }",
        "properties": ["image-url", "alt-text", "width", "height", "border-radius"]
    },
    "audio": {
        "name": "Аудио",
        "category": "media",
        "html": "<div class='audio-container'><audio controls><source src='' type='audio/mpeg'>Ваш браузер не поддерживает аудио.</audio></div>",
        "css": ".audio-container { margin: 20px 0; } .audio-container audio { width: 100%; }",
        "properties": ["audio-url", "autoplay", "controls", "volume"]
    }
}

# Бизнес блоки
business_blocks = {
    "pricing_table": {
        "name": "Таблица цен",
        "category": "business",
        "html": "<div class='pricing'><div class='pricing-card'><h3>Базовый</h3><div class='price'>₽999</div><ul><li>Функция 1</li><li>Функция 2</li><li>Функция 3</li></ul><button>Выбрать</button></div><div class='pricing-card featured'><h3>Про</h3><div class='price'>₽1999</div><ul><li>Все из Базового</li><li>Функция 4</li><li>Функция 5</li></ul><button>Выбрать</button></div><div class='pricing-card'><h3>Премиум</h3><div class='price'>₽2999</div><ul><li>Все из Про</li><li>Функция 6</li><li>Функция 7</li></ul><button>Выбрать</button></div></div>",
        "css": ".pricing { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; padding: 40px 0; } .pricing-card { border: 1px solid #ddd; border-radius: 10px; padding: 30px; text-align: center; } .pricing-card.featured { border-color: #007bff; transform: scale(1.05); } .price { font-size: 2em; font-weight: bold; color: #007bff; margin: 20px 0; } .pricing-card ul { list-style: none; padding: 0; } .pricing-card li { padding: 10px 0; border-bottom: 1px solid #eee; } .pricing-card button { padding: 12px 30px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; margin-top: 20px; }",
        "properties": ["plans", "prices", "features", "button-text", "highlighted-plan"]
    },
    "testimonials": {
        "name": "Отзывы клиентов",
        "category": "business",
        "html": "<section class='testimonials'><div class='container'><h2>Что говорят наши клиенты</h2><div class='testimonial-grid'><div class='testimonial'><p>'Отличный сервис! Создал сайт за несколько часов.'</p><div class='author'>- Иван Петров</div></div><div class='testimonial'><p>'Профессиональный подход и качественный результат.'</p><div class='author'>- Мария Сидорова</div></div></div></div></section>",
        "css": ".testimonials { padding: 80px 0; background: #f9f9f9; } .testimonial-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin-top: 40px; } .testimonial { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); } .author { font-weight: bold; margin-top: 15px; color: #007bff; }",
        "properties": ["title", "testimonials", "background", "text-color"]
    },
    "cta_section": {
        "name": "Призыв к действию",
        "category": "business",
        "html": "<section class='cta-section'><div class='container'><h2>Готовы начать?</h2><p>Присоединяйтесь к тысячам довольных клиентов</p><button class='cta-button'>Начать бесплатно</button></div></section>",
        "css": ".cta-section { padding: 80px 0; background: linear-gradient(45deg, #007bff, #0056b3); color: white; text-align: center; } .cta-button { padding: 15px 40px; background: white; color: #007bff; border: none; border-radius: 5px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 20px; }",
        "properties": ["title", "subtitle", "button-text", "background", "text-color"]
    }
}

# Социальные блоки
social_blocks = {
    "social_links": {
        "name": "Социальные сети",
        "category": "social",
        "html": "<div class='social-links'><a href='#' class='social-link'><i class='fab fa-facebook'></i></a><a href='#' class='social-link'><i class='fab fa-twitter'></i></a><a href='#' class='social-link'><i class='fab fa-instagram'></i></a><a href='#' class='social-link'><i class='fab fa-linkedin'></i></a></div>",
        "css": ".social-links { display: flex; gap: 15px; justify-content: center; margin: 20px 0; } .social-link { display: inline-block; width: 40px; height: 40px; background: #007bff; color: white; text-align: center; line-height: 40px; border-radius: 50%; text-decoration: none; transition: background 0.3s; } .social-link:hover { background: #0056b3; }",
        "properties": ["platforms", "colors", "size", "alignment"]
    },
    "share_buttons": {
        "name": "Кнопки поделиться",
        "category": "social",
        "html": "<div class='share-buttons'><button class='share-btn facebook'>Поделиться в Facebook</button><button class='share-btn twitter'>Поделиться в Twitter</button><button class='share-btn vk'>Поделиться в VK</button></div>",
        "css": ".share-buttons { display: flex; gap: 10px; margin: 20px 0; } .share-btn { padding: 10px 20px; border: none; border-radius: 5px; color: white; cursor: pointer; } .share-btn.facebook { background: #1877f2; } .share-btn.twitter { background: #1da1f2; } .share-btn.vk { background: #4c75a3; }",
        "properties": ["platforms", "button-text", "colors", "size"]
    }
}

# Все блоки объединены в один словарь
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

# Функция для получения блоков по категории
def get_blocks_by_category(category):
    """Возвращает все блоки указанной категории"""
    return {k: v for k, v in all_blocks.items() if v['category'] == category}

# Функция для получения всех категорий
def get_all_categories():
    """Возвращает список всех доступных категорий"""
    return list(block_categories.keys())

# Функция для получения блока по ID
def get_block_by_id(block_id):
    """Возвращает блок по его ID"""
    return all_blocks.get(block_id)

# Функция для поиска блоков
def search_blocks(query):
    """Поиск блоков по названию"""
    query = query.lower()
    return {k: v for k, v in all_blocks.items() if query in v['name'].lower()} 