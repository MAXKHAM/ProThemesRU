# 🚀 ProThemesRU - Платформа для создания профессиональных сайтов

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-orange.svg)](https://core.telegram.org/bots)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/your-username/ProThemesRU?style=social)](https://github.com/your-username/ProThemesRU)

🌟 **ProThemesRU** - это инновационная платформа для создания профессиональных веб-сайтов с помощью Telegram бота и веб-конструктора.

## 🚀 Возможности

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

# ProThemesRU - Конструктор Сайтов

Профессиональная платформа для создания сайтов с поддержкой Telegram бота и платежной системы.

## 🚀 Возможности

- **Конструктор сайтов** - Drag & Drop редактор с React
- **Готовые шаблоны** - Коллекция профессиональных шаблонов
- **Telegram бот** - Управление проектами через бота
- **Платежная система** - Интеграция с ЮKassa
- **AI генератор** - Автоматическая генерация цветовых палитр
- **PRO функции** - Расширенные возможности для премиум пользователей

## 📋 Требования

- Python 3.8+
- Node.js 16+
- SQLite (или PostgreSQL для продакшена)

## 🛠️ Установка

### 1. Клонирование и настройка

```bash
git clone <repository-url>
cd ProThemesRU1
```

### 2. Настройка Python окружения

```bash
# Создание виртуального окружения
python -m venv venv

# Активация (Windows)
venv\Scripts\activate

# Активация (Linux/Mac)
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### 3. Настройка React фронтенда

```bash
cd react-canvas-editor
npm install
```

### 4. Инициализация базы данных

```bash
python init_db.py
```

### 5. Настройка переменных окружения

Создайте файл `.env` в корневой директории:

```env
# Основные настройки
SECRET_KEY=your-very-secret-key-change-in-production
FLASK_ENV=development

# База данных
DATABASE_URL=sqlite:///prothemesru.db

# Telegram Bot
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
PUBLIC_APP_URL=https://your-domain.com

# ЮKassa (платежи)
YOOKASSA_SHOP_ID=your_shop_id
YOOKASSA_SECRET_KEY=your_secret_key

# Stripe (альтернативные платежи)
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_stripe_webhook_secret

# AI API (опционально)
AI_API_KEY=your_ai_api_key
```

## 🚀 Запуск

### Запуск Flask бэкенда

```bash
python run.py
```

Приложение будет доступно по адресу: http://127.0.0.1:5000

### Запуск React фронтенда

```bash
cd react-canvas-editor
npm start
```

Редактор будет доступен по адресу: http://localhost:3000

### Настройка Telegram бота

```bash
python setup_telegram.py
```

## 📱 Использование

### 1. Регистрация и вход

- Откройте http://127.0.0.1:5000
- Зарегистрируйтесь или войдите как admin/admin123

### 2. Конструктор сайтов

- Перейдите в раздел "Конструктор"
- Добавляйте блоки из панели слева
- Редактируйте содержимое блоков
- Настройте стили и цвета
- Экспортируйте готовый сайт

### 3. Готовые шаблоны

- Просмотрите портфолио шаблонов
- Выберите подходящий шаблон
- Настройте под свои нужды
- Закажите готовый сайт

### 4. Telegram бот

- Найдите вашего бота в Telegram
- Отправьте команду `/start`
- Используйте меню для навигации

## 🎨 Структура проекта

```
ProThemesRU1/
├── app/                    # Flask приложение
│   ├── auth/              # Аутентификация
│   ├── main/              # Основные страницы
│   ├── constructor/       # Конструктор сайтов
│   ├── payments/          # Платежная система
│   ├── telegram_bot/      # Telegram бот
│   ├── ai_routes.py       # AI функции
│   └── models.py          # Модели базы данных
├── react-canvas-editor/   # React редактор
│   ├── src/
│   │   ├── components/    # React компоненты
│   │   ├── styles/        # CSS стили
│   │   └── utils/         # Утилиты
│   └── package.json
├── templates/             # HTML шаблоны
├── static/               # Статические файлы
├── config.py             # Конфигурация
├── requirements.txt      # Python зависимости
└── README.md            # Документация
```

## 🔧 Настройка PRO функций

### Гейтинг функций

Система поддерживает ограничение функций для бесплатных пользователей:

- **Free аккаунт**: 3 сайта, с брендингом
- **PRO аккаунт**: Неограниченное количество сайтов, без брендинга

### Настройка платежей

1. Зарегистрируйтесь в [ЮKassa](https://yookassa.ru/)
2. Получите Shop ID и Secret Key
3. Добавьте в переменные окружения
4. Настройте вебхуки для обработки платежей

## 🤖 Telegram бот

### Команды бота

- `/start` - Главное меню
- `/portfolio` - Просмотр шаблонов
- `/constructor` - Ссылка на конструктор
- `/orders` - История заказов

### Настройка вебхука

```bash
# Установите ngrok для туннеля
ngrok http 5000

# Настройте PUBLIC_APP_URL в .env
PUBLIC_APP_URL=https://your-ngrok-url.ngrok.io

# Запустите настройку вебхука
python setup_telegram.py
```

## 🎯 AI функции

### Генерация цветовых палитр

- Автоматическая генерация на основе ключевых слов
- Предложение комплементарных цветов
- Анализ дизайна и рекомендации

### Использование

```javascript
// Пример запроса к AI API
fetch('/ai/generate_palette', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ keyword: 'nature' })
})
.then(response => response.json())
.then(data => console.log(data.palette));
```

## 🚀 Развертывание

### Heroku

```bash
# Создайте Procfile
echo "web: gunicorn run:app" > Procfile

# Добавьте переменные окружения в Heroku
heroku config:set SECRET_KEY=your-secret-key
heroku config:set TELEGRAM_BOT_TOKEN=your-bot-token
# ... другие переменные

# Разверните приложение
git push heroku main
```

### Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
```

## 📊 Мониторинг

### Логи

Логи приложения сохраняются в папке `logs/`:

```bash
tail -f logs/prothemesru.log
```

### Метрики

- Количество созданных сайтов
- Статистика платежей
- Активность пользователей

## 🔒 Безопасность

- Все пароли хешируются с помощью Werkzeug
- CSRF защита для форм
- Валидация входных данных
- Безопасные сессии

## 🤝 Поддержка

- **Email**: support@prothemesru.com
- **Telegram**: @ProThemesRU_Support
- **Документация**: [docs.prothemesru.com](https://docs.prothemesru.com)

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 🎉 Благодарности

- Flask и сообщество Python
- React и Facebook
- Telegram Bot API
- ЮKassa за платежную систему
- Все контрибьюторы проекта
