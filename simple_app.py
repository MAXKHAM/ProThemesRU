from flask import Flask, render_template_string, request, redirect, url_for, flash, send_from_directory
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Простая HTML страница с логотипом и калькулятором
MAIN_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ProThemesRU - Создание профессиональных сайтов</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* Калькулятор цен */
        .price-calculator {
            position: fixed;
            left: 20px;
            right: auto;
            top: 20px;
            cursor: move;
            user-select: none;
            z-index: 2000;
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            min-width: 220px;
            max-width: 300px;
            font-size: 0.95rem;
        }
        
        .calculator-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            color: #667eea;
            font-weight: bold;
        }
        
        .calculator-header .emoji {
            font-size: 1.5rem;
            margin-right: 10px;
        }
        
        .calculator-options {
            margin-bottom: 15px;
        }
        
        .calculator-option {
            display: flex;
            align-items: center;
            margin-bottom: 8px;
        }
        
        .calculator-option input[type="checkbox"] {
            margin-right: 8px;
            transform: scale(1.2);
        }
        
        .calculator-option label {
            font-size: 0.9rem;
            color: #666;
            cursor: pointer;
        }
        
        .calculator-item {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            padding: 5px 0;
            border-bottom: 1px solid #eee;
            font-size: 0.9rem;
        }
        
        .calculator-total {
            font-weight: bold;
            font-size: 1.2rem;
            color: #667eea;
            border-top: 2px solid #667eea;
            padding-top: 10px;
            margin-top: 10px;
        }
        
        .calculator-button {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.8rem;
            cursor: pointer;
            margin-top: 10px;
            width: 100%;
        }
        
        .calculator-button:hover {
            transform: translateY(-1px);
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 50px;
        }
        
        .logo {
            font-size: 4rem;
            margin-bottom: 20px;
            display: block;
        }
        
        .header h1 {
            font-size: 3rem;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
        }
        
        .feature-card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s ease;
            cursor: pointer;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
        }
        
        .feature-card h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.5rem;
        }
        
        .feature-card p {
            color: #666;
            line-height: 1.6;
        }
        
        .cta-section {
            text-align: center;
            color: white;
            margin-bottom: 50px;
        }
        
        .cta-button {
            display: inline-block;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 15px 40px;
            text-decoration: none;
            border-radius: 50px;
            font-size: 1.2rem;
            font-weight: bold;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .cta-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
        }
        
        .footer {
            text-align: center;
            color: white;
            opacity: 0.8;
            margin-top: 50px;
        }
        
        .emoji {
            font-size: 3rem;
            margin-bottom: 20px;
        }
        
        /* Навигация */
        .nav {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .nav a {
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 25px;
            background: rgba(255,255,255,0.1);
            transition: background 0.3s ease;
        }
        
        .nav a:hover {
            background: rgba(255,255,255,0.2);
        }
        
        .logo img { width: 90px; height: 90px; object-fit: contain; box-shadow: 0 4px 24px rgba(0,0,0,0.18); border-radius: 50%; background: #fff; padding: 8px; }
    </style>
</head>
<body>
    <div class="cart-widget" onclick="toggleCart()">🛒 <span id="cart-total">0 ₽</span></div>

    <div class="cart-modal">
        <div class="cart-content">
            <h2>🛒 Корзина</h2>
            <div id="cart-items"></div>
            <div class="total-price">
                <span>Итого к оплате: </span>
                <span id="final-price">0 ₽</span>
            </div>
            <button onclick="clearCart()">Очистить корзину</button>
            <button onclick="orderNow()">Оформить заказ</button>
        </div>
    </div>

    <div class="container">
        <!-- Навигация -->
        <div class="nav">
            <a href="/">Главная</a>
            <a href="/portfolio">Портфолио</a>
            <a href="/pricing">Цены</a>
            <a href="/contact">Контакты</a>
        </div>
        
        <div class="header">
            <div class="logo"><img src="/static/images/logo.png" alt="ProThemesRU Logo"></div>
            <h1>ProThemesRU</h1>
            <p>Создавайте профессиональные сайты за считанные минуты</p>
        </div>
        
        <div class="features">
            <div class="feature-card" onclick="window.location.href='/portfolio'">
                <div class="emoji">📚</div>
                <h3>Готовые шаблоны</h3>
                <p>Более 50 профессиональных шаблонов для различных ниш бизнеса. От лендингов до интернет-магазинов.</p>
            </div>
            
            <div class="feature-card" onclick="window.location.href='/constructor'">
                <div class="emoji">🎨</div>
                <h3>Визуальный конструктор</h3>
                <p>Drag & Drop редактор для создания уникальных сайтов. Никаких знаний программирования не требуется.</p>
            </div>
            
            <div class="feature-card" onclick="window.location.href='/pricing'">
                <div class="emoji">⚡</div>
                <h3>Быстрая разработка</h3>
                <p>Создайте полноценный сайт за 10 минут. Готовые блоки и компоненты ускорят процесс разработки.</p>
            </div>
            
            <div class="feature-card" onclick="window.location.href='/features'">
                <div class="emoji">📱</div>
                <h3>Адаптивный дизайн</h3>
                <p>Все сайты автоматически адаптируются под мобильные устройства, планшеты и десктопы.</p>
            </div>
            
            <div class="feature-card" onclick="window.location.href='/support'">
                <div class="emoji">🔧</div>
                <h3>Техническая поддержка</h3>
                <p>Наша команда экспертов готова помочь с настройкой и доработкой вашего сайта 24/7.</p>
            </div>
            
            <div class="feature-card" onclick="window.location.href='/pricing'">
                <div class="emoji">💰</div>
                <h3>Доступные цены</h3>
                <p>Старт от 5,000 ₽. Гибкие тарифы для бизнеса любого размера. Без скрытых платежей.</p>
            </div>
        </div>
        
        <div class="cta-section">
            <h2>Готовы создать свой сайт?</h2>
            <p style="margin-bottom: 30px; font-size: 1.1rem;">Присоединяйтесь к тысячам довольных клиентов</p>
            <a href="/contact" class="cta-button">Начать создание сайта</a>
        </div>
        
        <div class="footer">
            <p>&copy; 2024 ProThemesRU. Все права защищены.</p>
            <p>Создание профессиональных сайтов | Поддержка 24/7 | Гарантия качества</p>
        </div>
    </div>

    <script>
        const prices = {
            landing: 5000,
            corporate: 15000,
            ecommerce: 25000,
            portfolio: 8000,
            seo: 3000,
            support: 5000,
            analytics: 2000
        };

        function calculatePrice() {
            let basePrice = 0;
            let extraPrice = 0;
            
            // Основные услуги (можно выбрать только одну)
            const mainServices = ['landing', 'corporate', 'ecommerce', 'portfolio'];
            let mainSelected = false;
            
            mainServices.forEach(service => {
                if (document.getElementById(service).checked) {
                    if (!mainSelected) {
                        basePrice = prices[service];
                        mainSelected = true;
                    } else {
                        // Если выбрано несколько основных услуг, берем самую дорогую
                        if (prices[service] > basePrice) {
                            basePrice = prices[service];
                        }
                    }
                }
            });
            
            // Дополнительные услуги
            const extraServices = ['seo', 'support', 'analytics'];
            extraServices.forEach(service => {
                if (document.getElementById(service).checked) {
                    extraPrice += prices[service];
                }
            });
            
            const total = basePrice + extraPrice;
            
            document.getElementById('base-price').textContent = basePrice.toLocaleString() + ' ₽';
            document.getElementById('extra-price').textContent = extraPrice.toLocaleString() + ' ₽';
            document.getElementById('total-price').textContent = total.toLocaleString() + ' ₽';
        }

        function orderNow() {
            const total = document.getElementById('total-price').textContent;
            if (total === '0 ₽') {
                alert('Пожалуйста, выберите хотя бы одну услугу!');
                return;
            }
            
            // Сохраняем выбранные опции в localStorage для передачи на страницу заказа
            const selectedOptions = {};
            Object.keys(prices).forEach(service => {
                selectedOptions[service] = document.getElementById(service).checked;
            });
            localStorage.setItem('selectedOptions', JSON.stringify(selectedOptions));
            localStorage.setItem('totalPrice', total);
            
            window.location.href = '/contact';
        }

        // Инициализация калькулятора
        calculatePrice();

        function toggleCart() {
            const cartModal = document.querySelector('.cart-modal');
            cartModal.style.display = cartModal.style.display === 'none' ? 'block' : 'none';
        }

        function addToCart(template) {
            const cartItems = document.getElementById('cart-items');
            const cartTotal = document.getElementById('final-price');
            
            const templateName = template.getAttribute('data-name');
            const templatePrice = template.getAttribute('data-price');
            
            const itemHTML = `
                <div class="cart-item">
                    <span>${templateName}</span>
                    <span>${templatePrice} ₽</span>
                </div>
            `;
            
            cartItems.innerHTML += itemHTML;
            cartTotal.textContent = (parseFloat(cartTotal.textContent) + parseFloat(templatePrice)).toLocaleString() + ' ₽';
        }

        function updateCart() {
            const cartItems = document.getElementById('cart-items');
            const cartTotal = document.getElementById('final-price');
            
            let total = 0;
            const items = cartItems.querySelectorAll('.cart-item');
            items.forEach(item => {
                const price = item.querySelector('span:last-child').textContent.split(' ')[0];
                total += parseFloat(price);
            });
            
            cartTotal.textContent = total.toLocaleString() + ' ₽';
        }

        function clearCart() {
            const cartItems = document.getElementById('cart-items');
            const cartTotal = document.getElementById('final-price');
            
            cartItems.innerHTML = '';
            cartTotal.textContent = '0 ₽';
        }

        // Drag&Drop для калькулятора
        const calc = document.querySelector('.price-calculator');
        let isDragging = false, offsetX = 0, offsetY = 0;
        if (calc) {
            calc.addEventListener('mousedown', function(e) {
                isDragging = true;
                offsetX = e.clientX - calc.getBoundingClientRect().left;
                offsetY = e.clientY - calc.getBoundingClientRect().top;
                calc.style.transition = 'none';
            });
            document.addEventListener('mousemove', function(e) {
                if (isDragging) {
                    calc.style.left = (e.clientX - offsetX) + 'px';
                    calc.style.top = (e.clientY - offsetY) + 'px';
                }
            });
            document.addEventListener('mouseup', function() {
                isDragging = false;
                calc.style.transition = '';
            });
        }
    </script>
</body>
</html>
"""

# --- Динамическое портфолио ---
TEMPLATE_ROOT = os.path.join(os.path.dirname(__file__), 'templates', 'blocks')

# Автоматический сбор шаблонов
def get_templates_list():
    template_dirs = []
    for entry in os.listdir(TEMPLATE_ROOT):
        full_path = os.path.join(TEMPLATE_ROOT, entry)
        if os.path.isdir(full_path) and (entry.endswith('_Template') or entry in ['ecommerce', 'landing', 'business', 'agency', 'portfolio']):
            for sub in os.listdir(full_path):
                sub_path = os.path.join(full_path, sub)
                if os.path.isdir(sub_path):
                    template_dirs.append((entry, sub, sub_path))
    # Добавим простые шаблоны (без вложенных папок)
    for entry in os.listdir(TEMPLATE_ROOT):
        full_path = os.path.join(TEMPLATE_ROOT, entry)
        if os.path.isdir(full_path) and entry not in ['__pycache__', 'test_exports', 'html5up_downloads'] and not entry.endswith('_Template'):
            template_dirs.append((entry, entry, full_path))
    templates = []
    for cat, name, path in template_dirs:
        # Миниатюра
        preview = None
        for root, dirs, files in os.walk(path):
            for f in files:
                if f.lower().startswith('preview') and (f.endswith('.jpg') or f.endswith('.png')):
                    preview = os.path.relpath(os.path.join(root, f), TEMPLATE_ROOT)
                    break
            if preview: break
        # Если нет preview, ищем первое jpg/png
        if not preview:
            for root, dirs, files in os.walk(path):
                for f in files:
                    if f.endswith('.jpg') or f.endswith('.png'):
                        preview = os.path.relpath(os.path.join(root, f), TEMPLATE_ROOT)
                        break
                if preview: break
        # Описание и тип
        desc = f'Готовый шаблон "{name}" из категории {cat}'
        ttype = 'e-commerce' if 'ecom' in name.lower() or 'shop' in name.lower() else ('лендинг' if 'landing' in name.lower() else 'бизнес')
        # Путь к index.html
        index_path = None
        for root, dirs, files in os.walk(path):
            for f in files:
                if f == 'index.html':
                    index_path = os.path.relpath(os.path.join(root, f), TEMPLATE_ROOT)
                    break
            if index_path: break
        templates.append({
            'name': name,
            'category': cat,
            'desc': desc,
            'type': ttype,
            'preview': preview,
            'index': index_path
        })
    return templates

@app.route('/portfolio')
def portfolio():
    templates = get_templates_list()
    # Фильтрация по типу
    filter_type = request.args.get('type')
    if filter_type:
        templates = [t for t in templates if t['type'] == filter_type]
    # HTML шаблон
    html = '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Портфолио шаблонов - ProThemesRU</title>
        <style>
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #222; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            .container { max-width: 1200px; margin: 0 auto; padding: 30px 10px; }
            .nav { display: flex; justify-content: center; gap: 20px; margin-bottom: 30px; }
            .nav a { color: white; text-decoration: none; padding: 10px 20px; border-radius: 25px; background: rgba(255,255,255,0.1); transition: background 0.3s; }
            .nav a:hover { background: rgba(255,255,255,0.2); }
            h1 { text-align: center; color: #fff; margin-bottom: 30px; }
            .filters { text-align: center; margin-bottom: 30px; }
            .filters button { margin: 0 8px; padding: 8px 20px; border-radius: 20px; border: none; background: #fff; color: #667eea; font-weight: bold; cursor: pointer; transition: background 0.2s; }
            .filters button.active, .filters button:hover { background: #667eea; color: #fff; }
            .templates-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(270px, 1fr)); gap: 30px; }
            .template-card { background: #fff; border-radius: 15px; box-shadow: 0 6px 24px rgba(0,0,0,0.08); overflow: hidden; display: flex; flex-direction: column; }
            .template-card img { width: 100%; height: 180px; object-fit: cover; background: #f3f3f3; }
            .template-card .info { padding: 18px; flex: 1; display: flex; flex-direction: column; }
            .template-card h3 { color: #667eea; margin-bottom: 10px; font-size: 1.1rem; }
            .template-card p { color: #444; font-size: 0.97rem; margin-bottom: 10px; }
            .template-card .type { font-size: 0.85rem; color: #fff; background: #667eea; border-radius: 12px; padding: 2px 12px; display: inline-block; margin-bottom: 10px; }
            .template-card .actions { margin-top: auto; }
            .template-card .actions a { display: inline-block; margin-right: 10px; background: #ff6b6b; color: #fff; padding: 8px 18px; border-radius: 20px; text-decoration: none; font-weight: bold; transition: background 0.2s; }
            .template-card .actions a:hover { background: #ee5a24; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="nav">
                <a href="/">Главная</a>
                <a href="/portfolio">Портфолио</a>
                <a href="/pricing">Цены</a>
                <a href="/contact">Контакты</a>
            </div>
            <h1>Портфолио шаблонов</h1>
            <div class="filters">
                <form method="get" style="display:inline;">
                    <button type="submit" name="type" value="" class="{{'' if filter_type else 'active'}}">Все</button>
                    <button type="submit" name="type" value="лендинг" class="{{'active' if filter_type=='лендинг' else ''}}">Лендинги</button>
                    <button type="submit" name="type" value="e-commerce" class="{{'active' if filter_type=='e-commerce' else ''}}">Магазины</button>
                    <button type="submit" name="type" value="бизнес" class="{{'active' if filter_type=='бизнес' else ''}}">Бизнес</button>
                </form>
            </div>
            <div class="templates-grid">
                {% for t in templates %}
                <div class="template-card">
                    {% if t.preview %}<img src="/portfolio_preview/{{t.preview}}" alt="{{t.name}} preview">{% endif %}
                    <div class="info">
                        <span class="type">{{t.type}}</span>
                        <h3>{{t.name}}</h3>
                        <p>{{t.desc}}</p>
                        <div class="actions">
                            {% if t.index %}<a href="/portfolio_demo/{{t.index}}" target="_blank">Демо</a>{% endif %}
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html, templates=templates, filter_type=filter_type)

# Для отдачи миниатюр и демо
@app.route('/portfolio_preview/<path:filename>')
def portfolio_preview(filename):
    return send_from_directory(os.path.join(TEMPLATE_ROOT), filename)

@app.route('/portfolio_demo/<path:filename>')
def portfolio_demo(filename):
    # Открываем index.html шаблона как демо
    dir_path = os.path.dirname(os.path.join(TEMPLATE_ROOT, filename))
    fname = os.path.basename(filename)
    return send_from_directory(dir_path, fname)

@app.route('/pricing')
def pricing():
    return render_template_string(PRICING_PAGE)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        service = request.form.get('service')
        message = request.form.get('message')
        selected_options = request.form.get('selected_options')
        calculated_price = request.form.get('calculated_price')
        
        # Здесь можно добавить логику отправки email или сохранения в базу данных
        print(f"Новая заявка от {name} ({email})")
        if calculated_price:
            print(f"Выбранные услуги: {selected_options}")
            print(f"Рассчитанная стоимость: {calculated_price}")
        
        flash(f'Спасибо, {name}! Ваша заявка отправлена. Мы свяжемся с вами в ближайшее время.')
        return redirect(url_for('index'))
    
    return render_template_string(CONTACT_PAGE)

@app.route('/constructor')
def constructor():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Конструктор сайтов - ProThemesRU</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 50px 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            h1 { font-size: 3rem; margin-bottom: 30px; }
            p { font-size: 1.2rem; margin-bottom: 30px; }
            a { color: white; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎨 Конструктор сайтов</h1>
            <p>Визуальный редактор для создания уникальных сайтов</p>
            <p>Страница в разработке...</p>
            <a href="/">← Вернуться на главную</a>
        </div>
    </body>
    </html>
    """)

@app.route('/features')
def features():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Возможности - ProThemesRU</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 50px 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            h1 { font-size: 3rem; margin-bottom: 30px; }
            p { font-size: 1.2rem; margin-bottom: 30px; }
            a { color: white; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📱 Адаптивный дизайн</h1>
            <p>Все сайты автоматически адаптируются под любые устройства</p>
            <a href="/">← Вернуться на главную</a>
        </div>
    </body>
    </html>
    """)

@app.route('/support')
def support():
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Поддержка - ProThemesRU</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 50px 20px;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            h1 { font-size: 3rem; margin-bottom: 30px; }
            p { font-size: 1.2rem; margin-bottom: 30px; }
            a { color: white; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔧 Техническая поддержка</h1>
            <p>Наша команда экспертов готова помочь 24/7</p>
            <a href="/">← Вернуться на главную</a>
        </div>
    </body>
    </html>
    """)

if __name__ == '__main__':
    print("🚀 Запуск ProThemesRU...")
    print("📱 Сайт доступен по адресу: http://localhost:5000")
    print("📧 Контакты: http://localhost:5000/contact")
    print("🎨 Портфолио: http://localhost:5000/portfolio")
    print("💰 Цены: http://localhost:5000/pricing")
    print("⏹️  Для остановки нажмите Ctrl+C")
    app.run(debug=True, host='0.0.0.0', port=5000) 