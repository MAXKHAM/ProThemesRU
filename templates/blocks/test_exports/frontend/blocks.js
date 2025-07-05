// Блоки для фронтенда

export const blocks = {
  'header': {
    name: 'Заголовок',
    category: 'basic',
    html: `<header class='site-header'><h1>Заголовок сайта</h1></header>`,
    css: `.site-header { padding: 20px; background: #f8f9fa; text-align: center; }`,
    properties: ["text", "background", "padding", "font-size"]
  },
  'footer': {
    name: 'Подвал',
    category: 'basic',
    html: `<footer class='site-footer'><p>&copy; 2024 ProThemesRU. Все права защищены.</p></footer>`,
    css: `.site-footer { padding: 20px; background: #333; color: white; text-align: center; }`,
    properties: ["text", "background", "padding", "color"]
  },
  'navigation': {
    name: 'Навигация',
    category: 'basic',
    html: `<nav class='main-nav'><ul><li><a href='#home'>Главная</a></li><li><a href='#about'>О нас</a></li><li><a href='#contact'>Контакты</a></li></ul></nav>`,
    css: `.main-nav ul { list-style: none; display: flex; gap: 20px; } .main-nav a { text-decoration: none; color: #333; }`,
    properties: ["menu-items", "background", "color", "font-size"]
  },
  'container': {
    name: 'Контейнер',
    category: 'basic',
    html: `<div class='container'><p>Содержимое контейнера</p></div>`,
    css: `.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }`,
    properties: ["max-width", "padding", "background", "border"]
  },
  'divider': {
    name: 'Разделитель',
    category: 'basic',
    html: `<hr class='divider'>`,
    css: `.divider { border: none; height: 2px; background: linear-gradient(90deg, transparent, #007bff, transparent); margin: 40px 0; }`,
    properties: ["color", "height", "style", "margin"]
  },
  'hero_section': {
    name: 'Главный экран',
    category: 'content',
    html: `<section class='hero'><div class='hero-content'><h1>Добро пожаловать</h1><p>Создавайте потрясающие сайты с ProThemesRU</p><button class='cta-button'>Начать</button></div></section>`,
    css: `.hero { min-height: 80vh; display: flex; align-items: center; justify-content: center; background: linear-gradient(45deg, #667eea, #764ba2); color: white; } .hero-content { text-align: center; } .cta-button { padding: 15px 30px; background: #fff; color: #333; border: none; border-radius: 5px; font-size: 18px; cursor: pointer; }`,
    properties: ["title", "subtitle", "button-text", "background", "text-color"]
  },
  'about_section': {
    name: 'О нас',
    category: 'content',
    html: `<section class='about'><div class='container'><h2>О нашей компании</h2><p>Мы создаем инновационные решения для вашего бизнеса. Наша команда экспертов поможет воплотить ваши идеи в жизнь.</p></div></section>`,
    css: `.about { padding: 80px 0; background: #f9f9f9; } .container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }`,
    properties: ["title", "content", "background", "text-color"]
  },
  'contact_section': {
    name: 'Контакты',
    category: 'content',
    html: `<section class='contact'><div class='container'><h2>Свяжитесь с нами</h2><div class='contact-info'><p>Email: info@prothemesru.com</p><p>Телефон: +7 (999) 123-45-67</p><p>Адрес: Москва, Россия</p></div></div></section>`,
    css: `.contact { padding: 80px 0; background: #333; color: white; } .contact-info { margin-top: 30px; }`,
    properties: ["title", "email", "phone", "address", "background"]
  },
  'text_block': {
    name: 'Текстовый блок',
    category: 'content',
    html: `<div class='text-block'><h2>Заголовок</h2><p>Это пример текстового блока. Здесь можно разместить любой контент: параграфы, списки, цитаты и многое другое.</p></div>`,
    css: `.text-block { padding: 40px 0; } .text-block h2 { margin-bottom: 20px; color: #333; } .text-block p { line-height: 1.6; color: #666; }`,
    properties: ["title", "content", "font-size", "line-height", "color"]
  },
  'features_section': {
    name: 'Преимущества',
    category: 'content',
    html: `<section class='features'><div class='container'><h2>Наши преимущества</h2><div class='features-grid'><div class='feature'><h3>Качество</h3><p>Высокое качество всех решений</p></div><div class='feature'><h3>Скорость</h3><p>Быстрая разработка и внедрение</p></div><div class='feature'><h3>Поддержка</h3><p>24/7 техническая поддержка</p></div></div></div></section>`,
    css: `.features { padding: 80px 0; background: #fff; } .features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; margin-top: 40px; } .feature { text-align: center; padding: 30px; } .feature h3 { color: #007bff; margin-bottom: 15px; }`,
    properties: ["title", "features", "columns", "background", "text-color"]
  },
  'contact_form': {
    name: 'Форма обратной связи',
    category: 'interactive',
    html: `<form class='contact-form'><input type='text' placeholder='Ваше имя' required><input type='email' placeholder='Email' required><textarea placeholder='Сообщение' rows='5'></textarea><button type='submit'>Отправить</button></form>`,
    css: `.contact-form { display: flex; flex-direction: column; gap: 15px; max-width: 500px; margin: 0 auto; } .contact-form input, .contact-form textarea { padding: 10px; border: 1px solid #ddd; border-radius: 5px; } .contact-form button { padding: 12px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }`,
    properties: ["fields", "button-text", "background", "border-color"]
  },
  'gallery': {
    name: 'Галерея изображений',
    category: 'interactive',
    html: `<div class='gallery'><div class='gallery-item'><img src='https://via.placeholder.com/300x200' alt='Изображение 1'></div><div class='gallery-item'><img src='https://via.placeholder.com/300x200' alt='Изображение 2'></div><div class='gallery-item'><img src='https://via.placeholder.com/300x200' alt='Изображение 3'></div></div>`,
    css: `.gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; padding: 20px; } .gallery-item img { width: 100%; height: auto; border-radius: 8px; cursor: pointer; transition: transform 0.3s; } .gallery-item img:hover { transform: scale(1.05); }`,
    properties: ["images", "columns", "gap", "border-radius", "lightbox"]
  },
  'slider': {
    name: 'Слайдер',
    category: 'interactive',
    html: `<div class='slider'><div class='slide active'><img src='https://via.placeholder.com/800x400' alt='Слайд 1'></div><div class='slide'><img src='https://via.placeholder.com/800x400' alt='Слайд 2'></div><div class='slide'><img src='https://via.placeholder.com/800x400' alt='Слайд 3'></div><button class='slider-btn prev'>&lt;</button><button class='slider-btn next'>&gt;</button></div>`,
    css: `.slider { position: relative; overflow: hidden; } .slide { display: none; } .slide.active { display: block; } .slider-btn { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.5); color: white; border: none; padding: 10px 15px; cursor: pointer; } .prev { left: 10px; } .next { right: 10px; }`,
    properties: ["slides", "autoplay", "interval", "show-arrows", "show-dots"]
  },
  'accordion': {
    name: 'Аккордеон',
    category: 'interactive',
    html: `<div class='accordion'><div class='accordion-item'><div class='accordion-header'>Заголовок 1</div><div class='accordion-content'><p>Содержимое первого элемента аккордеона.</p></div></div><div class='accordion-item'><div class='accordion-header'>Заголовок 2</div><div class='accordion-content'><p>Содержимое второго элемента аккордеона.</p></div></div></div>`,
    css: `.accordion { border: 1px solid #ddd; border-radius: 5px; } .accordion-item { border-bottom: 1px solid #ddd; } .accordion-header { padding: 15px; background: #f8f9fa; cursor: pointer; font-weight: bold; } .accordion-content { padding: 15px; display: none; } .accordion-content.active { display: block; }`,
    properties: ["items", "animation", "background", "border-color"]
  },
  'tabs': {
    name: 'Вкладки',
    category: 'interactive',
    html: `<div class='tabs'><div class='tab-buttons'><button class='tab-btn active' data-tab='tab1'>Вкладка 1</button><button class='tab-btn' data-tab='tab2'>Вкладка 2</button><button class='tab-btn' data-tab='tab3'>Вкладка 3</button></div><div class='tab-content'><div class='tab-pane active' id='tab1'><p>Содержимое первой вкладки.</p></div><div class='tab-pane' id='tab2'><p>Содержимое второй вкладки.</p></div><div class='tab-pane' id='tab3'><p>Содержимое третьей вкладки.</p></div></div></div>`,
    css: `.tabs { margin: 20px 0; } .tab-buttons { display: flex; border-bottom: 1px solid #ddd; } .tab-btn { padding: 10px 20px; border: none; background: none; cursor: pointer; } .tab-btn.active { background: #007bff; color: white; } .tab-pane { display: none; padding: 20px; } .tab-pane.active { display: block; }`,
    properties: ["tabs", "animation", "background", "border-color"]
  },
  'video': {
    name: 'Видео',
    category: 'media',
    html: `<div class='video-container'><video controls><source src='' type='video/mp4'>Ваш браузер не поддерживает видео.</video></div>`,
    css: `.video-container { max-width: 100%; margin: 20px 0; } .video-container video { width: 100%; height: auto; border-radius: 8px; }`,
    properties: ["video-url", "autoplay", "controls", "width", "height", "poster"]
  },
  'image': {
    name: 'Изображение',
    category: 'media',
    html: `<div class='image-block'><img src='https://via.placeholder.com/600x400' alt='Описание изображения'></div>`,
    css: `.image-block { text-align: center; margin: 20px 0; } .image-block img { max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }`,
    properties: ["image-url", "alt-text", "width", "height", "border-radius", "shadow"]
  },
  'audio': {
    name: 'Аудио',
    category: 'media',
    html: `<div class='audio-container'><audio controls><source src='' type='audio/mpeg'>Ваш браузер не поддерживает аудио.</audio></div>`,
    css: `.audio-container { margin: 20px 0; } .audio-container audio { width: 100%; }`,
    properties: ["audio-url", "autoplay", "controls", "volume", "loop"]
  },
  'youtube_video': {
    name: 'YouTube видео',
    category: 'media',
    html: `<div class='youtube-container'><iframe width='560' height='315' src='' frameborder='0' allowfullscreen></iframe></div>`,
    css: `.youtube-container { position: relative; width: 100%; max-width: 560px; margin: 20px auto; } .youtube-container iframe { width: 100%; height: 315px; border-radius: 8px; }`,
    properties: ["video-id", "width", "height", "autoplay", "controls"]
  },
  'image_carousel': {
    name: 'Карусель изображений',
    category: 'media',
    html: `<div class='image-carousel'><div class='carousel-container'><img src='https://via.placeholder.com/800x400' alt='Изображение 1' class='carousel-image active'><img src='https://via.placeholder.com/800x400' alt='Изображение 2' class='carousel-image'><img src='https://via.placeholder.com/800x400' alt='Изображение 3' class='carousel-image'></div><div class='carousel-dots'><span class='dot active'></span><span class='dot'></span><span class='dot'></span></div></div>`,
    css: `.image-carousel { position: relative; max-width: 800px; margin: 0 auto; } .carousel-container { position: relative; overflow: hidden; } .carousel-image { width: 100%; height: auto; display: none; } .carousel-image.active { display: block; } .carousel-dots { text-align: center; margin-top: 10px; } .dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; background: #ccc; margin: 0 5px; cursor: pointer; } .dot.active { background: #007bff; }`,
    properties: ["images", "autoplay", "interval", "show-dots", "show-arrows"]
  },
  'pricing_table': {
    name: 'Таблица цен',
    category: 'business',
    html: `<div class='pricing'><div class='pricing-card'><h3>Базовый</h3><div class='price'>₽999</div><ul><li>Функция 1</li><li>Функция 2</li><li>Функция 3</li></ul><button>Выбрать</button></div><div class='pricing-card featured'><h3>Про</h3><div class='price'>₽1999</div><ul><li>Все из Базового</li><li>Функция 4</li><li>Функция 5</li></ul><button>Выбрать</button></div><div class='pricing-card'><h3>Премиум</h3><div class='price'>₽2999</div><ul><li>Все из Про</li><li>Функция 6</li><li>Функция 7</li></ul><button>Выбрать</button></div></div>`,
    css: `.pricing { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; padding: 40px 0; } .pricing-card { border: 1px solid #ddd; border-radius: 10px; padding: 30px; text-align: center; } .pricing-card.featured { border-color: #007bff; transform: scale(1.05); } .price { font-size: 2em; font-weight: bold; color: #007bff; margin: 20px 0; } .pricing-card ul { list-style: none; padding: 0; } .pricing-card li { padding: 10px 0; border-bottom: 1px solid #eee; } .pricing-card button { padding: 12px 30px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; margin-top: 20px; }`,
    properties: ["plans", "prices", "features", "button-text", "highlighted-plan"]
  },
  'testimonials': {
    name: 'Отзывы клиентов',
    category: 'business',
    html: `<section class='testimonials'><div class='container'><h2>Что говорят наши клиенты</h2><div class='testimonial-grid'><div class='testimonial'><p>'Отличный сервис! Создал сайт за несколько часов.'</p><div class='author'>- Иван Петров</div></div><div class='testimonial'><p>'Профессиональный подход и качественный результат.'</p><div class='author'>- Мария Сидорова</div></div></div></div></section>`,
    css: `.testimonials { padding: 80px 0; background: #f9f9f9; } .testimonial-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 30px; margin-top: 40px; } .testimonial { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); } .author { font-weight: bold; margin-top: 15px; color: #007bff; }`,
    properties: ["title", "testimonials", "background", "text-color", "show-avatar"]
  },
  'cta_section': {
    name: 'Призыв к действию',
    category: 'business',
    html: `<section class='cta-section'><div class='container'><h2>Готовы начать?</h2><p>Присоединяйтесь к тысячам довольных клиентов</p><button class='cta-button'>Начать бесплатно</button></div></section>`,
    css: `.cta-section { padding: 80px 0; background: linear-gradient(45deg, #007bff, #0056b3); color: white; text-align: center; } .cta-button { padding: 15px 40px; background: white; color: #007bff; border: none; border-radius: 5px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 20px; }`,
    properties: ["title", "subtitle", "button-text", "background", "text-color"]
  },
  'product_card': {
    name: 'Карточка товара',
    category: 'business',
    html: `<div class='product-card'><img src='https://via.placeholder.com/300x200' alt='Товар' class='product-image'><div class='product-info'><h3>Название товара</h3><p class='product-description'>Описание товара</p><div class='product-price'>₽1999</div><button class='buy-button'>Купить</button></div></div>`,
    css: `.product-card { border: 1px solid #ddd; border-radius: 10px; overflow: hidden; transition: transform 0.3s; } .product-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0,0,0,0.1); } .product-image { width: 100%; height: 200px; object-fit: cover; } .product-info { padding: 20px; } .product-price { font-size: 1.5em; font-weight: bold; color: #007bff; margin: 10px 0; } .buy-button { width: 100%; padding: 10px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }`,
    properties: ["title", "description", "price", "image", "button-text"]
  },
  'newsletter_signup': {
    name: 'Подписка на рассылку',
    category: 'business',
    html: `<div class='newsletter'><h3>Подпишитесь на новости</h3><p>Получайте последние обновления и специальные предложения</p><form class='newsletter-form'><input type='email' placeholder='Ваш email' required><button type='submit'>Подписаться</button></form></div>`,
    css: `.newsletter { text-align: center; padding: 40px; background: #f8f9fa; border-radius: 10px; } .newsletter-form { display: flex; gap: 10px; max-width: 400px; margin: 20px auto 0; } .newsletter-form input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; } .newsletter-form button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }`,
    properties: ["title", "description", "button-text", "background", "border-radius"]
  },
  'social_links': {
    name: 'Социальные сети',
    category: 'social',
    html: `<div class='social-links'><a href='#' class='social-link'><i class='fab fa-facebook'></i></a><a href='#' class='social-link'><i class='fab fa-twitter'></i></a><a href='#' class='social-link'><i class='fab fa-instagram'></i></a><a href='#' class='social-link'><i class='fab fa-linkedin'></i></a></div>`,
    css: `.social-links { display: flex; gap: 15px; justify-content: center; margin: 20px 0; } .social-link { display: inline-block; width: 40px; height: 40px; background: #007bff; color: white; text-align: center; line-height: 40px; border-radius: 50%; text-decoration: none; transition: background 0.3s; } .social-link:hover { background: #0056b3; }`,
    properties: ["platforms", "colors", "size", "alignment", "show-text"]
  },
  'share_buttons': {
    name: 'Кнопки поделиться',
    category: 'social',
    html: `<div class='share-buttons'><button class='share-btn facebook'>Поделиться в Facebook</button><button class='share-btn twitter'>Поделиться в Twitter</button><button class='share-btn vk'>Поделиться в VK</button></div>`,
    css: `.share-buttons { display: flex; gap: 10px; margin: 20px 0; } .share-btn { padding: 10px 20px; border: none; border-radius: 5px; color: white; cursor: pointer; } .share-btn.facebook { background: #1877f2; } .share-btn.twitter { background: #1da1f2; } .share-btn.vk { background: #4c75a3; }`,
    properties: ["platforms", "button-text", "colors", "size", "show-icons"]
  },
  'social_feed': {
    name: 'Лента социальных сетей',
    category: 'social',
    html: `<div class='social-feed'><h3>Мы в социальных сетях</h3><div class='feed-container'><div class='feed-item'><div class='feed-header'><img src='https://via.placeholder.com/40x40' alt='Avatar' class='feed-avatar'><span class='feed-author'>@username</span></div><p class='feed-text'>Отличный сервис! Рекомендую всем!</p><div class='feed-meta'><span class='feed-date'>2 часа назад</span><span class='feed-likes'>❤️ 15</span></div></div></div></div>`,
    css: `.social-feed { max-width: 400px; margin: 0 auto; } .feed-container { border: 1px solid #ddd; border-radius: 10px; padding: 20px; } .feed-item { margin-bottom: 20px; } .feed-header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; } .feed-avatar { width: 40px; height: 40px; border-radius: 50%; } .feed-author { font-weight: bold; } .feed-text { margin: 10px 0; } .feed-meta { display: flex; justify-content: space-between; color: #666; font-size: 0.9em; }`,
    properties: ["platform", "posts-count", "show-avatars", "show-likes", "auto-refresh"]
  },
  'comment_system': {
    name: 'Система комментариев',
    category: 'social',
    html: `<div class='comments-section'><h3>Комментарии (3)</h3><div class='comment-form'><textarea placeholder='Написать комментарий...' rows='3'></textarea><button class='comment-submit'>Отправить</button></div><div class='comments-list'><div class='comment'><div class='comment-header'><img src='https://via.placeholder.com/32x32' alt='User' class='comment-avatar'><span class='comment-author'>Пользователь</span><span class='comment-date'>2 часа назад</span></div><p class='comment-text'>Отличная статья!</p></div></div></div>`,
    css: `.comments-section { margin: 40px 0; } .comment-form { margin-bottom: 20px; } .comment-form textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; resize: vertical; } .comment-submit { padding: 8px 16px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px; } .comment { border-bottom: 1px solid #eee; padding: 15px 0; } .comment-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; } .comment-avatar { width: 32px; height: 32px; border-radius: 50%; } .comment-date { color: #666; font-size: 0.9em; }`,
    properties: ["moderation", "show-avatars", "allow-replies", "sort-by", "page-size"]
  },
  'social_proof': {
    name: 'Социальные доказательства',
    category: 'social',
    html: `<div class='social-proof'><div class='proof-item'><div class='proof-number'>10,000+</div><div class='proof-label'>Довольных клиентов</div></div><div class='proof-item'><div class='proof-number'>4.9</div><div class='proof-label'>Рейтинг на Trustpilot</div></div><div class='proof-item'><div class='proof-number'>99%</div><div class='proof-label'>Время безотказной работы</div></div></div>`,
    css: `.social-proof { display: flex; justify-content: space-around; padding: 40px 0; background: #f8f9fa; border-radius: 10px; } .proof-item { text-align: center; } .proof-number { font-size: 2.5em; font-weight: bold; color: #007bff; } .proof-label { color: #666; margin-top: 5px; }`,
    properties: ["metrics", "background", "text-color", "animation", "show-icons"]
  },
};

export const categories = {"basic": "Базовые элементы", "content": "Контентные блоки", "interactive": "Интерактивные элементы", "media": "Медиа контент", "business": "Бизнес элементы", "social": "Социальные сети"};
