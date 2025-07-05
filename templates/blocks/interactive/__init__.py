# Интерактивные блоки для конструктора сайтов

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
        "css": ".gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; padding: 20px; } .gallery-item img { width: 100%; height: auto; border-radius: 8px; cursor: pointer; transition: transform 0.3s; } .gallery-item img:hover { transform: scale(1.05); }",
        "properties": ["images", "columns", "gap", "border-radius", "lightbox"]
    },
    "slider": {
        "name": "Слайдер",
        "category": "interactive",
        "html": "<div class='slider'><div class='slide active'><img src='https://via.placeholder.com/800x400' alt='Слайд 1'></div><div class='slide'><img src='https://via.placeholder.com/800x400' alt='Слайд 2'></div><div class='slide'><img src='https://via.placeholder.com/800x400' alt='Слайд 3'></div><button class='slider-btn prev'>&lt;</button><button class='slider-btn next'>&gt;</button></div>",
        "css": ".slider { position: relative; overflow: hidden; } .slide { display: none; } .slide.active { display: block; } .slider-btn { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.5); color: white; border: none; padding: 10px 15px; cursor: pointer; } .prev { left: 10px; } .next { right: 10px; }",
        "properties": ["slides", "autoplay", "interval", "show-arrows", "show-dots"]
    },
    "accordion": {
        "name": "Аккордеон",
        "category": "interactive",
        "html": "<div class='accordion'><div class='accordion-item'><div class='accordion-header'>Заголовок 1</div><div class='accordion-content'><p>Содержимое первого элемента аккордеона.</p></div></div><div class='accordion-item'><div class='accordion-header'>Заголовок 2</div><div class='accordion-content'><p>Содержимое второго элемента аккордеона.</p></div></div></div>",
        "css": ".accordion { border: 1px solid #ddd; border-radius: 5px; } .accordion-item { border-bottom: 1px solid #ddd; } .accordion-header { padding: 15px; background: #f8f9fa; cursor: pointer; font-weight: bold; } .accordion-content { padding: 15px; display: none; } .accordion-content.active { display: block; }",
        "properties": ["items", "animation", "background", "border-color"]
    },
    "tabs": {
        "name": "Вкладки",
        "category": "interactive",
        "html": "<div class='tabs'><div class='tab-buttons'><button class='tab-btn active' data-tab='tab1'>Вкладка 1</button><button class='tab-btn' data-tab='tab2'>Вкладка 2</button><button class='tab-btn' data-tab='tab3'>Вкладка 3</button></div><div class='tab-content'><div class='tab-pane active' id='tab1'><p>Содержимое первой вкладки.</p></div><div class='tab-pane' id='tab2'><p>Содержимое второй вкладки.</p></div><div class='tab-pane' id='tab3'><p>Содержимое третьей вкладки.</p></div></div></div>",
        "css": ".tabs { margin: 20px 0; } .tab-buttons { display: flex; border-bottom: 1px solid #ddd; } .tab-btn { padding: 10px 20px; border: none; background: none; cursor: pointer; } .tab-btn.active { background: #007bff; color: white; } .tab-pane { display: none; padding: 20px; } .tab-pane.active { display: block; }",
        "properties": ["tabs", "animation", "background", "border-color"]
    }
} 