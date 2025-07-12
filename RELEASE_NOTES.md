# 🚀 Подробная инструкция по деплою на Render.com

##  Подготовка к деплою

### 1. Создание аккаунта на Render
1. Перейдите на [Render.com](https://render.com)
2. Нажмите "Get Started for Free"
3. Зарегистрируйтесь через GitHub (рекомендуется)

### 2. Подготовка репозиториев
Убедитесь, что у вас есть доступ к репозиториям:
- **Основной сайт**: https://github.com/MAXKHAM/ProThemesRU
- **Telegram Bot**: https://github.com/MAXKHAM/ProThemesRUBot

## 🌐 Деплой основного сайта (ProThemesRU)

### Шаг 1: Создание Web Service

1. **Войдите в Render Dashboard**
2. **Нажмите "New +"** → **"Web Service"**
3. **Подключите GitHub репозиторий**:
   - Выберите `ProThemesRU`
   - Нажмите "Connect"

### Шаг 2: Настройка Web Service

**Основные настройки:**
```
Name: prothemesru-main
Environment: Python 3
Region: Frankfurt (EU Central) - Frankfurt
Branch: master
Root Directory: (оставьте пустым)
```

**Build Command:**
```bash
pip install -r requirements.txt && cd frontend && npm install && npm run build
```

**Start Command:**
```bash
gunicorn --bind 0.0.0.0:$PORT app:app
```

### Шаг 3: Переменные окружения

Нажмите "Environment" и добавьте:

```env
SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
DATABASE_URL=postgresql://username:password@host:port/database
JWT_SECRET_KEY=your-jwt-secret-key-here-make-it-different
FLASK_ENV=production
PYTHONPATH=/opt/render/project/src
```

### Шаг 4: Создание PostgreSQL базы данных

1. **В Dashboard нажмите "New +"** → **"PostgreSQL"**
2. **Настройте базу данных**:
   ```
   Name: prothemesru-db
   Database: prothemesru
   User: prothemesru_user
   Region: Frankfurt (EU Central) - Frankfurt
   ```
3. **Скопируйте Internal Database URL**
4. **Вставьте в переменную `DATABASE_URL`** в Web Service

### Шаг 5: Запуск деплоя

1. **Нажмите "Create Web Service"**
2. **Дождитесь завершения деплоя** (5-10 минут)
3. **Получите URL**: `https://your-app-name.onrender.com`

## 🤖 Деплой Telegram Bot (ProThemesRUBot)

### Шаг 1: Создание Worker Service

1. **В Dashboard нажмите "New +"** → **"Worker Service"**
2. **Подключите GitHub репозиторий**:
   - Выберите `ProThemesRUBot`
   - Нажмите "Connect"

### Шаг 2: Настройка Worker Service

**Основные настройки:**
```
Name: prothemesru-bot
Environment: Python 3
Region: Frankfurt (EU Central) - Frankfurt
Branch: main
Root Directory: (оставьте пустым)
```

**Build Command:**
```bash
<code_block_to_apply_changes_from>
```

**Start Command:**
```bash
python run_bot.py
```

### Шаг 3: Переменные окружения для бота

```env
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
TELEGRAM_ADMIN_CHAT_ID=your_telegram_chat_id
API_BASE_URL=https://your-main-app-name.onrender.com
LOG_LEVEL=INFO
```

### Шаг 4: Получение токена бота

1. **Найдите @BotFather в Telegram**
2. **Отправьте `/newbot`**
3. **Следуйте инструкциям**:
   ```
   /newbot
   ProThemesRU Bot
   prothemesru_bot
   ```
4. **Скопируйте токен** (например: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)
5. **Вставьте в переменную `TELEGRAM_BOT_TOKEN`**

### Шаг 5: Получение Chat ID администратора

1. **Найдите @userinfobot в Telegram**
2. **Отправьте любое сообщение**
3. **Скопируйте ваш Chat ID** (например: `123456789`)
4. **Вставьте в переменную `TELEGRAM_ADMIN_CHAT_ID`**

### Шаг 6: Запуск бота

1. **Нажмите "Create Worker Service"**
2. **Дождитесь завершения деплоя**
3. **Проверьте логи** - бот должен запуститься без ошибок

##  Настройка домена (опционально)

### Шаг 1: Покупка домена
1. Купите домен (например, на Namecheap или GoDaddy)
2. Получите доступ к DNS настройкам

### Шаг 2: Настройка в Render
1. **В Web Service перейдите в "Settings"**
2. **Найдите "Custom Domains"**
3. **Добавьте ваш домен**:
   ```
   Domain: your-domain.com
   Force HTTPS: Yes
   ```

### Шаг 3: Настройка DNS
Добавьте CNAME запись:
```
Type: CNAME
Name: @
Value: your-app-name.onrender.com
TTL: 3600
```

## 📊 Мониторинг и логи

### Просмотр логов
1. **В Dashboard выберите ваш сервис**
2. **Перейдите во вкладку "Logs"**
3. **Следите за ошибками и предупреждениями**

### Мониторинг производительности
1. **Перейдите во вкладку "Metrics"**
2. **Следите за**:
   - Response Time
   - Request Count
   - Error Rate
   - Memory Usage

## 🚨 Решение проблем

### Ошибка "Build failed"
```bash
# Проверьте логи сборки
# Убедитесь, что все зависимости в requirements.txt
# Проверьте версию Python (должна быть 3.11+)
```

### Ошибка "Database connection failed"
```bash
# Проверьте DATABASE_URL
# Убедитесь, что PostgreSQL создан
# Проверьте права доступа к базе данных
```

### Бот не отвечает
```bash
# Проверьте TELEGRAM_BOT_TOKEN
# Убедитесь, что бот не заблокирован
# Проверьте логи Worker Service
```

### Ошибки CORS
```bash
# В app.py проверьте настройки CORS
# Добавьте ваш домен в ALLOWED_ORIGINS
```

## 💰 Стоимость

### Бесплатный план:
- **Web Service**: 750 часов/месяц
- **Worker Service**: 750 часов/месяц
- **PostgreSQL**: 90 дней бесплатно

### Платный план (если нужно):
- **Web Service**: $7/месяц
- **Worker Service**: $7/месяц
- **PostgreSQL**: $7/месяц

## ✅ Проверка работоспособности

### 1. Проверка сайта:
- Откройте URL вашего Web Service
- Убедитесь, что сайт загружается
- Проверьте все функции

### 2. Проверка бота:
- Найдите вашего бота в Telegram
- Отправьте `/start`
- Проверьте все команды

### 3. Проверка API:
- Откройте `https://your-app.onrender.com/api/templates`
- Убедитесь, что API отвечает

## 🎉 Готово!

После выполнения всех шагов у вас будет:
- ✅ Работающий сайт на Render
- ✅ Работающий Telegram бот
- ✅ База данных PostgreSQL
- ✅ Автоматические деплои при пуше в GitHub

**URL вашего сайта**: `https://your-app-name.onrender.com`
**Бот в Telegram**: `@your_bot_username`

Удачного использования! 🚀 