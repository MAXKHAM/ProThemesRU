# 🚀 ProThemesRU - Платформа для создания профессиональных сайтов

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-orange.svg)](https://core.telegram.org/bots)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/your-username/ProThemesRU?style=social)](https://github.com/your-username/ProThemesRU)

🌟 **ProThemesRU** - это инновационная платформа для создания профессиональных веб-сайтов с помощью Telegram бота и веб-конструктора.

## ✨ Возможности

### 🤖 Telegram Bot
- 📱 Интерактивный бот для создания сайтов
- 📚 Библиотека готовых шаблонов (45+ шаблонов)
- 🧱 UI компоненты и блоки (50+ компонентов)
- 🎨 Стили и эффекты (30+ стилей)
- 💳 Система заказов и оплаты
- 👥 Управление пользователями

### 🌐 Веб-платформа
- 🎨 Визуальный конструктор сайтов
- 📱 Адаптивный дизайн
- 🔧 Настройка и кастомизация
- 📊 Аналитика и статистика
- 👥 Система пользователей
- 🔐 Аутентификация

### 📦 Шаблоны и блоки
- 💼 **Бизнес-сайты**: Лендинги, корпоративные сайты
- 🎨 **Портфолио**: Креативные галереи, портфолио
- 🛒 **E-commerce**: Интернет-магазины
- 🏢 **Корпоративные**: Компании, организации
- 📝 **Блоги**: Платформы для ведения блогов
- 🍽️ **Рестораны**: Сайты ресторанов и кафе
- 🏠 **Недвижимость**: Агентства недвижимости
- 🏥 **Медицина**: Медицинские учреждения
- 💻 **SaaS**: Программное обеспечение как услуга
- 🎓 **Образование**: Образовательные платформы
- 💪 **Фитнес**: Фитнес клубы и спортзалы
- ⚖️ **Юридические**: Юридические фирмы
- 🎨 **Дизайн**: Дизайн-студии
- 🏗️ **Строительство**: Строительные компании

## 🛠️ Технологии

### Backend
- **Python 3.8+**
- **Flask 2.3+** - Веб-фреймворк
- **SQLAlchemy** - ORM
- **PostgreSQL/SQLite** - База данных
- **python-telegram-bot** - Telegram Bot API

### Frontend
- **HTML5/CSS3**
- **JavaScript (ES6+)**
- **Bootstrap 5** - CSS фреймворк
- **Tailwind CSS** - Utility-first CSS
- **React/Vue.js** - JavaScript фреймворки

### Дополнительные технологии
- **Font Awesome** - Иконки
- **Google Fonts** - Шрифты
- **GSAP** - Анимации
- **Framer Motion** - React анимации

## 📋 Требования

- Python 3.8+
- Flask 2.3+
- PostgreSQL (опционально)
- Telegram Bot Token
- SSL сертификат (для продакшена)

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/ProThemesRU.git
cd ProThemesRU
```

### 2. Настройка виртуального окружения

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
# Основные зависимости
pip install -r requirements.txt

# Зависимости для Telegram бота
pip install -r telegram_bot/requirements.txt
```

### 4. Настройка переменных окружения

Создайте файл `.env`:

```env
# Основные настройки
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# База данных
DATABASE_URL=sqlite:///prothemesru.db

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_ADMIN_CHAT_ID=your-admin-chat-id

# API настройки
API_BASE_URL=http://localhost:5000
```

### 5. Запуск

```bash
# Веб-приложение
flask run

# Telegram Bot (в отдельном терминале)
cd telegram_bot
python enhanced_bot.py
```

## 📱 Использование Telegram Bot

1. Найдите бота в Telegram: `@YourBotUsername`
2. Отправьте команду `/start`
3. Выберите нужную категорию:
   - 📚 **Шаблоны** - Просмотр готовых шаблонов
   - 🧱 **Блоки** - UI компоненты
   - 🎨 **Стили** - Стили и эффекты
   - 🎨 **Конструктор** - Создание сайта
   - 📦 **Заказать** - Оформление заказа
   - 💰 **Цены** - Тарифы и цены

## 🌐 Веб-интерфейс

Откройте браузер и перейдите по адресу: `http://localhost:5000`

### Основные страницы:
- `/` - Главная страница
- `/constructor` - Конструктор сайтов
- `/templates` - Библиотека шаблонов
- `/portfolio` - Портфолио работ
- `/pricing` - Тарифы и цены
- `/admin` - Панель администратора

## 📁 Структура проекта

```
ProThemesRU/
├── 📱 telegram_bot/          # Telegram бот
│   ├── enhanced_bot.py       # Основной бот
│   ├── config.py             # Конфигурация
│   ├── requirements.txt      # Зависимости
│   └── README.md             # Документация бота
├── 🎨 templates/             # Библиотека шаблонов
│   ├── blocks/               # 45+ шаблонов
│   ├── premium_templates.json
│   └── enhanced_templates.json
├── 🧱 static/                # Статические ресурсы
│   ├── css/                  # Стили
│   │   ├── premium_styles.css
│   │   ├── modern_fonts.css
│   │   └── icon_library.css
│   ├── js/                   # JavaScript
│   ├── images/               # Изображения
│   └── fonts/                # Шрифты
├── 🌐 app/                   # Flask приложение
├── 📚 README.md             # Документация
└── 📋 PUBLISH_INSTRUCTIONS.md # Инструкции по публикации
```

## 🎨 Шаблоны и стили

### 📊 Статистика
- **Шаблонов**: 45+
- **UI компонентов**: 50+
- **Стилей**: 30+
- **Категорий**: 14
- **Шрифтов**: 15+
- **Иконок**: 100+

### 🎯 Возможности
- ✅ Создание сайтов через Telegram
- ✅ Визуальный конструктор
- ✅ Готовые шаблоны
- ✅ UI библиотека
- ✅ Система заказов
- ✅ Адаптивный дизайн
- ✅ SEO-оптимизация
- ✅ Система платежей
- ✅ Анимации и эффекты
- ✅ Современные шрифты

## 🔧 Конфигурация

### Настройка Telegram Bot

1. Создайте бота через [@BotFather](https://t.me/botfather)
2. Получите токен и добавьте в `.env`
3. Настройте webhook (для продакшена):

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://your-domain.com/webhook"}'
```

### Настройка базы данных

```python
# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///prothemesru.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## 🚀 Деплой

### Heroku

```bash
# Создайте приложение на Heroku
heroku create your-app-name

# Добавьте переменные окружения
heroku config:set TELEGRAM_BOT_TOKEN=your-token
heroku config:set SECRET_KEY=your-secret-key

# Деплой
git push heroku main
```

### Railway

```bash
# Установите Railway CLI
npm install -g @railway/cli

# Логин и деплой
railway login
railway init
railway up
```

### Docker

```bash
# Сборка образа
docker build -t prothemesru .

# Запуск контейнера
docker run -p 5000:5000 --env-file .env prothemesru
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

## 📝 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 📞 Поддержка

- 📧 Email: support@prothemes.ru
- 💬 Telegram: @ProThemesSupport
- 🌐 Сайт: https://prothemes.ru
- 📖 Документация: https://docs.prothemes.ru

## 🙏 Благодарности

- [Flask](https://flask.palletsprojects.com/) - Веб-фреймворк
- [python-telegram-bot](https://python-telegram-bot.org/) - Telegram Bot API
- [Bootstrap](https://getbootstrap.com/) - CSS фреймворк
- [Font Awesome](https://fontawesome.com/) - Иконки
- [Google Fonts](https://fonts.google.com/) - Шрифты
- [Unsplash](https://unsplash.com/) - Изображения

## 📈 Статистика проекта

- ⭐ **Звезды**: 0
- 🔄 **Форки**: 0
- 👀 **Просмотры**: 0
- 📥 **Загрузки**: 0

---

⭐ **Если проект вам понравился, поставьте звездочку!**

🚀 **Готовы создать профессиональный сайт? Начните прямо сейчас!**
