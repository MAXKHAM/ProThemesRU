# 🚀 ProThemesRU - Полнофункциональная платформа для создания сайтов

## 📋 Описание

ProThemesRU - это современная платформа для создания профессиональных сайтов с визуальным конструктором, готовыми шаблонами, Telegram ботом и интегрированной платежной системой.

## ✨ Основные возможности

- 🎨 **Визуальный конструктор сайтов** - создавайте сайты без знания кода
- 📋 **Готовые шаблоны** - более 25 профессиональных шаблонов
- 🤖 **Telegram бот** - управление сайтами прямо в мессенджере
- 💳 **Платежная система** - безопасные онлайн платежи
- 👨‍💼 **Админ панель** - полное управление платформой
- 📱 **Адаптивный дизайн** - сайты работают на всех устройствах
- 🔍 **SEO оптимизация** - встроенные инструменты для продвижения

## 🏗️ Архитектура

```
ProThemesRU/
├── app.py                 # Основной Flask сервер
├── api/                   # API эндпоинты
├── frontend/              # React приложение
├── telegram_bot/          # Telegram бот
├── templates/             # HTML шаблоны
├── static/               # Статические файлы
└── database/             # База данных
```

## 🚀 Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/ProThemesRU.git
cd ProThemesRU
```

### 2. Установка зависимостей

```bash
# Backend зависимости
pip install -r requirements.txt

# Frontend зависимости
cd frontend
npm install
cd ..
```

### 3. Настройка переменных окружения

Создайте файл `.env`:

```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URL=sqlite:///prothemesru.db
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
API_BASE_URL=https://your-api-url.com
```

### 4. Запуск приложения

```bash
# Запуск backend
python app.py

# Запуск frontend (в отдельном терминале)
cd frontend
npm start
```

## 🌐 API Документация

### Основные эндпоинты

- `GET /` - Главная страница
- `GET /api/health` - Проверка состояния API
- `POST /api/auth/register` - Регистрация
- `POST /api/auth/login` - Вход в систему
- `GET /api/templates` - Получение шаблонов
- `GET /api/sites` - Управление сайтами

Подробная документация: [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

## 🤖 Telegram бот

### Настройка бота

1. Получите токен у @BotFather
2. Настройте переменные окружения
3. Разверните бота на платформе

### Команды бота

- `/start` - Главное меню
- `/templates` - Просмотр шаблонов
- `/my_sites` - Мои сайты
- `/help` - Помощь

Подробная инструкция: [telegram_bot/DEPLOY.md](telegram_bot/DEPLOY.md)

## 🚀 Развертывание

### Vercel (рекомендуется)

1. Подключите репозиторий к Vercel
2. Настройте переменные окружения
3. Деплоймент произойдет автоматически

### Railway

1. Создайте проект в Railway
2. Подключите репозиторий
3. Настройте переменные окружения

### Render

1. Создайте Web Service
2. Подключите репозиторий
3. Настройте build и start команды

## 📱 Frontend

React приложение с современным UI:

- 🎨 Современный дизайн
- 📱 Адаптивная верстка
- ⚡ Быстрая загрузка
- 🔧 Легкая кастомизация

### Запуск frontend

```bash
cd frontend
npm install
npm start
```

## 🗄️ База данных

Поддерживаемые СУБД:
- SQLite (по умолчанию)
- PostgreSQL
- MySQL

### Миграции

```bash
flask db init
flask db migrate
flask db upgrade
```

## 🔧 Разработка

### Структура проекта

```
├── app/
│   ├── api/              # API эндпоинты
│   ├── auth/             # Аутентификация
│   ├── main/             # Основные маршруты
│   ├── models/           # Модели данных
│   └── services/         # Бизнес-логика
├── frontend/
│   ├── src/
│   │   ├── components/   # React компоненты
│   │   ├── pages/        # Страницы
│   │   └── utils/        # Утилиты
│   └── public/           # Статические файлы
└── telegram_bot/         # Telegram бот
```

### Добавление новых функций

1. Создайте API эндпоинт в `app/api/`
2. Добавьте модель в `app/models/`
3. Создайте React компонент в `frontend/src/components/`
4. Обновите документацию

## 🧪 Тестирование

### Запуск тестов

```bash
# Backend тесты
python -m pytest tests/

# Frontend тесты
cd frontend
npm test
```

### API тестирование

```bash
python test_api.py
```

## 📊 Мониторинг

- Логирование всех операций
- Мониторинг производительности
- Отслеживание ошибок
- Аналитика использования

## 🔒 Безопасность

- JWT аутентификация
- Хеширование паролей
- CORS защита
- Валидация входных данных
- HTTPS шифрование

## 📈 Производительность

- Кэширование запросов
- Оптимизация изображений
- Минификация CSS/JS
- CDN для статических файлов

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License - см. файл [LICENSE](LICENSE)

## 📞 Поддержка

- 📧 Email: support@prothemesru.com
- 💬 Telegram: @prothemesru_support
- 🌐 Сайт: https://prothemesru.com

## 🙏 Благодарности

- Flask Framework
- React.js
- Telegram Bot API
- Все участники проекта

---

**ProThemesRU v1.0.0** - Создавайте профессиональные сайты легко! 🚀
