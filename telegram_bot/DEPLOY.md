# 🤖 Развертывание Telegram бота ProThemesRU

## 📋 Предварительные требования

1. **Telegram Bot Token** - получите у @BotFather
2. **API URL** - URL вашего развернутого API
3. **Платформа для развертывания** (Railway, Render, Heroku)

## 🔧 Настройка бота

### 1. Получение Telegram Bot Token

1. Откройте Telegram и найдите @BotFather
2. Отправьте команду `/newbot`
3. Следуйте инструкциям:
   - Введите имя бота (например: "ProThemesRU Bot")
   - Введите username бота (например: "prothemesru_bot")
4. Сохраните полученный токен

### 2. Настройка переменных окружения

Создайте файл `.env` в папке `telegram_bot/`:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
API_BASE_URL=https://your-vercel-url.vercel.app
LOG_LEVEL=INFO
```

## 🚀 Развертывание на Railway

### 1. Подготовка проекта

1. Создайте отдельный репозиторий для бота или используйте подпапку
2. Убедитесь, что в корне есть файлы:
   - `bot.py` - основной файл бота
   - `requirements.txt` - зависимости
   - `config.py` - конфигурация

### 2. Развертывание

1. Зайдите на [Railway.app](https://railway.app)
2. Создайте новый проект
3. Подключите ваш репозиторий
4. Настройте переменные окружения:
   - `TELEGRAM_BOT_TOKEN`
   - `API_BASE_URL`
   - `LOG_LEVEL`

### 3. Настройка запуска

В настройках проекта установите:
- **Start Command**: `python bot.py`
- **Health Check Path**: `/` (если есть)

## 🚀 Развертывание на Render

### 1. Подготовка

1. Создайте файл `render.yaml`:

```yaml
services:
  - type: web
    name: prothemesru-bot
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: python bot.py
    envVars:
      - key: TELEGRAM_BOT_TOKEN
        sync: false
      - key: API_BASE_URL
        value: https://your-vercel-url.vercel.app
      - key: LOG_LEVEL
        value: INFO
```

### 2. Развертывание

1. Зайдите на [Render.com](https://render.com)
2. Создайте новый Web Service
3. Подключите репозиторий
4. Настройте переменные окружения
5. Запустите деплоймент

## 🚀 Развертывание на Heroku

### 1. Подготовка

1. Создайте файл `Procfile`:

```
worker: python bot.py
```

2. Создайте файл `runtime.txt`:

```
python-3.11.7
```

### 2. Развертывание

1. Установите Heroku CLI
2. Выполните команды:

```bash
heroku create prothemesru-bot
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set API_BASE_URL=https://your-vercel-url.vercel.app
git push heroku main
heroku ps:scale worker=1
```

## 🔍 Тестирование бота

### 1. Проверка запуска

После развертывания проверьте логи:

```bash
# Railway
railway logs

# Render
# Логи доступны в веб-интерфейсе

# Heroku
heroku logs --tail
```

### 2. Тестирование команд

1. Найдите вашего бота в Telegram
2. Отправьте команду `/start`
3. Проверьте все кнопки и функции

## 📱 Использование бота

### Основные команды:

- `/start` - Главное меню
- `/templates` - Просмотр шаблонов
- `/my_sites` - Мои сайты
- `/help` - Помощь

### Функции:

1. **Просмотр шаблонов** - выбор готовых дизайнов
2. **Создание сайтов** - на основе шаблонов
3. **Управление сайтами** - просмотр и редактирование
4. **Интеграция с API** - связь с основным сервисом

## 🔧 Устранение неполадок

### Проблема: Бот не отвечает

**Решение:**
1. Проверьте логи на наличие ошибок
2. Убедитесь, что `TELEGRAM_BOT_TOKEN` правильный
3. Проверьте, что бот не заблокирован

### Проблема: Ошибки подключения к API

**Решение:**
1. Проверьте `API_BASE_URL`
2. Убедитесь, что API доступен
3. Проверьте CORS настройки

### Проблема: Бот падает при запуске

**Решение:**
1. Проверьте зависимости в `requirements.txt`
2. Убедитесь в правильности синтаксиса Python
3. Проверьте переменные окружения

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи развертывания
2. Убедитесь в корректности конфигурации
3. Проверьте доступность API
4. Обратитесь к документации Telegram Bot API

---

**ProThemesRU Telegram Bot** - Создавайте сайты прямо в Telegram! 🚀 