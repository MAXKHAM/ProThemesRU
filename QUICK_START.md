# 🚀 Быстрый старт ProThemesRU

## 📋 Что у нас есть

### 🌐 Основной сайт (ProThemesRU)
- **Репозиторий**: https://github.com/MAXKHAM/ProThemesRU
- **Frontend**: React + TypeScript
- **Backend**: Flask + SQLAlchemy
- **База данных**: SQLite/PostgreSQL

### 🤖 Telegram Bot (ProThemesRUBot)
- **Репозиторий**: https://github.com/MAXKHAM/ProThemesRUBot
- **Технологии**: python-telegram-bot
- **Функции**: Просмотр шаблонов, заказы, поддержка

## 🎯 Быстрый запуск

### 1. Запуск основного сайта

```bash
# Клонируйте репозиторий
git clone https://github.com/MAXKHAM/ProThemesRU.git
cd ProThemesRU

# Создайте виртуальное окружение
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Установите зависимости
pip install -r requirements.txt

# Настройте переменные окружения
copy env.example .env
# Отредактируйте .env файл

# Запустите backend
python app.py

# В новом терминале запустите frontend
cd frontend
npm install
npm start
```

**Сайт будет доступен**: http://localhost:3000

### 2. Запуск Telegram бота

```bash
# Клонируйте репозиторий бота
git clone https://github.com/MAXKHAM/ProThemesRUBot.git
cd ProThemesRUBot

# Установите зависимости
pip install -r requirements.txt

# Настройте переменные окружения
copy env.example .env
# Отредактируйте .env файл

# Запустите бота
python run_bot.py
```

## ⚙️ Настройка переменных окружения

### Для основного сайта (.env)

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///prothemesru.db
JWT_SECRET_KEY=your-jwt-secret-key
FLASK_ENV=development
```

### Для бота (.env в папке ProThemesRUBot)

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_ADMIN_CHAT_ID=your_admin_chat_id_here
API_BASE_URL=http://localhost:5000
```

## 🤖 Получение токена Telegram бота

1. Найдите @BotFather в Telegram
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте полученный токен в `.env`

## 🌐 Деплой на продакшен

### Render.com (рекомендуется)

#### Основной сайт:
1. Зайдите на [Render.com](https://render.com)
2. Подключите репозиторий `ProThemesRU`
3. Создайте **Web Service**
4. Настройте переменные окружения
5. Деплой произойдет автоматически

#### Telegram Bot:
1. В том же Render создайте **Worker Service**
2. Подключите репозиторий `ProThemesRUBot`
3. Настройте переменные окружения
4. Деплой произойдет автоматически

### GitHub Pages (только frontend)

Frontend автоматически деплоится на GitHub Pages при пуше в `master`.

## 📱 Команды бота

- `/start` - Главное меню
- `/templates` - Просмотр шаблонов
- `/blocks` - UI компоненты
- `/styles` - Стили и эффекты
- `/constructor` - Конструктор сайтов
- `/order` - Заказать сайт
- `/pricing` - Цены и тарифы
- `/help` - Помощь

## 🔧 Возможные проблемы

### Ошибка подключения к БД
```bash
# Создайте базу данных
python -c "from app import db; db.create_all()"
```

### Ошибки CORS
- Убедитесь, что backend запущен на порту 5000
- Проверьте настройки CORS в `app.py`

### Проблемы с ботом
- Проверьте токен в `.env`
- Убедитесь, что бот не заблокирован
- Проверьте логи в консоли

## 📞 Поддержка

- **GitHub Issues**: https://github.com/MAXKHAM/ProThemesRU/issues
- **Telegram**: @ProThemesSupport
- **Email**: support@prothemes.ru

## 🎉 Готово!

Теперь у вас есть:
- ✅ Работающий сайт на http://localhost:3000
- ✅ Telegram бот с полным функционалом
- ✅ Готовность к деплою на продакшен

**Удачного использования!** 🚀 