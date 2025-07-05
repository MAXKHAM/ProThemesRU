# ProThemesRU - Платформа для создания профессиональных сайтов

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-orange.svg)](https://core.telegram.org/bots)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

🌟 **ProThemesRU** - это инновационная платформа для создания профессиональных веб-сайтов с помощью Telegram бота и веб-конструктора.

## 🚀 Возможности

### 📱 Telegram Bot
- 🤖 Интерактивный бот для создания сайтов
- 📚 Библиотека готовых шаблонов
- 🧱 UI компоненты и блоки
- 🎨 Стили и эффекты
- 💳 Система заказов и оплаты

### 🌐 Веб-платформа
- 🎨 Визуальный конструктор сайтов
- 📱 Адаптивный дизайн
- 🔧 Настройка и кастомизация
- 📊 Аналитика и статистика
- 👥 Система пользователей

### 📦 Шаблоны и блоки
- 💼 Бизнес-сайты
- 🎨 Портфолио
- 🛒 E-commerce
- 🏢 Корпоративные сайты
- 📝 Блоги
- 🍽️ Рестораны
- 🏠 Недвижимость
- 🏥 Медицина

## 📋 Требования

- Python 3.8+
- Flask 2.3+
- PostgreSQL (опционально)
- Telegram Bot Token
- SSL сертификат (для продакшена)

## 🛠️ Установка

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

Создайте файл `.env` в корневой папке:

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

# Платежи (опционально)
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
```

### 5. Инициализация базы данных

```bash
flask db init
flask db migrate
flask db upgrade
```

### 6. Загрузка дополнительных ресурсов

```bash
python download_templates.py
```

## 🚀 Запуск

### Веб-приложение

```bash
# Режим разработки
flask run

# Продакшен режим
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Telegram Bot

```bash
# Переходим в папку бота
cd telegram_bot

# Запускаем бота
python enhanced_bot.py

# Или используем скрипт
python run_bot.py
```

## 📱 Использование Telegram Bot

1. Найдите бота в Telegram: `@YourBotUsername`
2. Отправьте команду `/start`
3. Выберите нужную категорию:
   - 📚 Шаблоны
   - 🧱 Блоки
   - 🎨 Стили
   - 🎨 Конструктор
   - 📦 Заказать
   - 💰 Цены

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
├── app/                    # Основное Flask приложение
│   ├── api/               # API endpoints
│   ├── auth/              # Аутентификация
│   ├── constructor/       # Конструктор сайтов
│   ├── main/              # Основные страницы
│   ├── orders/            # Система заказов
│   ├── payment/           # Платежи
│   ├── services/          # Бизнес-логика
│   ├── static/            # Статические файлы
│   ├── templates/         # HTML шаблоны
│   └── utils/             # Утилиты
├── telegram_bot/          # Telegram бот
│   ├── enhanced_bot.py    # Основной бот
│   ├── config.py          # Конфигурация
│   ├── requirements.txt   # Зависимости
│   └── README.md          # Документация бота
├── templates/             # Библиотека шаблонов
│   ├── blocks/            # UI блоки
│   ├── enhanced_templates.json
│   ├── ui_components.json
│   └── styles_library.json
├── static/                # Статические ресурсы
├── migrations/            # Миграции БД
├── tests/                 # Тесты
├── app.py                 # Точка входа
├── requirements.txt       # Зависимости
└── README.md             # Документация
```

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

### Настройка платежей

```python
# app/payment/routes.py
import stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
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

## 📊 Мониторинг и аналитика

### Логирование

```python
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Метрики

- Количество пользователей
- Созданные сайты
- Доходы
- Популярные шаблоны

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
- [Unsplash](https://unsplash.com/) - Изображения

---

⭐ **Если проект вам понравился, поставьте звездочку!** 