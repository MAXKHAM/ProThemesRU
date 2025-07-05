# Система блоков ProThemesRU

Система блоков для конструктора сайтов ProThemesRU предоставляет готовые компоненты для быстрого создания веб-сайтов.

## Структура проекта

```
site_blocks/
├── __init__.py          # Главный файл системы блоков
├── basic/               # Базовые элементы
│   └── __init__.py
├── content/             # Контентные блоки
│   └── __init__.py
├── interactive/         # Интерактивные элементы
│   └── __init__.py
├── media/               # Медиа контент
│   └── __init__.py
├── business/            # Бизнес элементы
│   └── __init__.py
├── social/              # Социальные сети
│   └── __init__.py
├── templates/           # Шаблоны
│   └── __init__.py
├── export.py            # Экспорт блоков
├── import.py            # Импорт блоков
├── constructor.py       # Интеграция с конструктором
└── README.md            # Документация
```

## Категории блоков

### 1. Базовые элементы (basic)
- **Header** - Заголовок сайта
- **Footer** - Подвал сайта
- **Navigation** - Навигационное меню
- **Container** - Контейнер для контента
- **Divider** - Разделитель

### 2. Контентные блоки (content)
- **Hero Section** - Главный экран
- **About Section** - Секция "О нас"
- **Contact Section** - Контактная информация
- **Text Block** - Текстовый блок
- **Features Section** - Секция преимуществ

### 3. Интерактивные элементы (interactive)
- **Contact Form** - Форма обратной связи
- **Gallery** - Галерея изображений
- **Slider** - Слайдер
- **Accordion** - Аккордеон
- **Tabs** - Вкладки

### 4. Медиа контент (media)
- **Video** - Видео
- **Image** - Изображение
- **Audio** - Аудио
- **YouTube Video** - YouTube видео
- **Image Carousel** - Карусель изображений

### 5. Бизнес элементы (business)
- **Pricing Table** - Таблица цен
- **Testimonials** - Отзывы клиентов
- **CTA Section** - Призыв к действию
- **Product Card** - Карточка товара
- **Newsletter Signup** - Подписка на рассылку

### 6. Социальные сети (social)
- **Social Links** - Ссылки на социальные сети
- **Share Buttons** - Кнопки поделиться
- **Social Feed** - Лента социальных сетей
- **Comment System** - Система комментариев
- **Social Proof** - Социальные доказательства

## Использование

### Базовое использование

```python
from site_blocks import all_blocks, get_blocks_by_category, get_block_by_id

# Получение всех блоков
print(f"Всего блоков: {len(all_blocks)}")

# Получение блоков по категории
basic_blocks = get_blocks_by_category('basic')
print(f"Базовых блоков: {len(basic_blocks)}")

# Получение конкретного блока
header_block = get_block_by_id('header')
print(f"HTML заголовка: {header_block['html']}")
```

### Работа с конструктором

```python
from site_blocks.constructor import constructor

# Добавление блока на страницу
block = constructor.add_block_to_page('hero_section')

# Обновление свойства блока
constructor.update_block_property(block['id'], 'title', 'Новый заголовок')

# Генерация HTML страницы
html = constructor.get_page_html()

# Сохранение страницы
constructor.save_page('my_page.json')
```

### Экспорт блоков

```python
from site_blocks.export import export_all_formats

# Экспорт во всех форматах
files = export_all_formats('exports')
print(f"Экспортировано файлов: {len(files)}")
```

### Импорт блоков

```python
from site_blocks.import import import_from_file

# Импорт из JSON файла
blocks = import_from_file('external_blocks.json')
print(f"Импортировано блоков: {len(blocks)}")
```

## Структура блока

Каждый блок имеет следующую структуру:

```python
{
    "name": "Название блока",
    "category": "категория",
    "html": "<div>HTML код блока</div>",
    "css": ".block { стили }",
    "properties": ["свойство1", "свойство2"]
}
```

### Поля блока

- **name** (str) - Название блока для отображения
- **category** (str) - Категория блока
- **html** (str) - HTML код блока
- **css** (str) - CSS стили блока
- **properties** (list) - Список настраиваемых свойств

## Создание собственных блоков

### 1. Создание нового блока

```python
my_block = {
    "name": "Мой блок",
    "category": "content",
    "html": "<div class='my-block'><h2>Заголовок</h2><p>Текст</p></div>",
    "css": ".my-block { padding: 20px; background: #f0f0f0; }",
    "properties": ["title", "text", "background"]
}
```

### 2. Добавление в систему

```python
from site_blocks.content import content_blocks

content_blocks["my_block"] = my_block
```

## API Reference

### Основные функции

#### `get_blocks_by_category(category)`
Возвращает все блоки указанной категории.

**Параметры:**
- `category` (str) - Название категории

**Возвращает:**
- `dict` - Словарь блоков категории

#### `get_block_by_id(block_id)`
Возвращает блок по его ID.

**Параметры:**
- `block_id` (str) - ID блока

**Возвращает:**
- `dict` - Данные блока или None

#### `search_blocks(query)`
Поиск блоков по названию.

**Параметры:**
- `query` (str) - Поисковый запрос

**Возвращает:**
- `dict` - Словарь найденных блоков

### Класс BlockConstructor

#### `add_block_to_page(block_id, position=None)`
Добавляет блок на страницу.

#### `remove_block_from_page(block_id)`
Удаляет блок со страницы.

#### `move_block(block_id, new_position)`
Перемещает блок на новую позицию.

#### `update_block_property(block_id, property_name, property_value)`
Обновляет свойство блока.

#### `get_page_html()`
Генерирует HTML код страницы.

#### `save_page(file_path)`
Сохраняет страницу в файл.

#### `load_page(file_path)`
Загружает страницу из файла.

## Примеры использования

### Создание простой страницы

```python
from site_blocks.constructor import constructor

# Добавляем блоки
constructor.add_block_to_page('header')
constructor.add_block_to_page('hero_section')
constructor.add_block_to_page('about_section')
constructor.add_block_to_page('contact_form')
constructor.add_block_to_page('footer')

# Генерируем HTML
html = constructor.get_page_html()

# Сохраняем
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
```

### Настройка блока

```python
# Добавляем блок
block = constructor.add_block_to_page('hero_section')

# Настраиваем свойства
constructor.update_block_property(block['id'], 'title', 'Добро пожаловать!')
constructor.update_block_property(block['id'], 'subtitle', 'Создавайте потрясающие сайты')
constructor.update_block_property(block['id'], 'button-text', 'Начать сейчас')
```

### Работа с категориями

```python
# Получаем все категории
categories = constructor.get_blocks_by_category('business')

# Ищем блоки
found_blocks = constructor.search_blocks('форма')

# Получаем структуру страницы
structure = constructor.get_page_structure()
```

## Расширение системы

### Добавление новой категории

1. Создайте папку для категории
2. Создайте файл `__init__.py` с блоками
3. Добавьте категорию в `block_categories`
4. Импортируйте блоки в главный `__init__.py`

### Создание кастомных свойств

```python
# Определите свойства в блоке
"properties": ["custom_color", "custom_size", "custom_text"]

# Обработайте их в конструкторе
def apply_custom_properties(block, properties):
    html = block['html']
    for prop, value in properties.items():
        html = html.replace(f'{{{prop}}}', str(value))
    return html
```

## Поддержка

Для получения поддержки или предложения новых блоков, создайте issue в репозитории проекта.

## Лицензия

MIT License - см. файл LICENSE для подробностей. 