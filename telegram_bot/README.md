# 🤖 Telegram Bot для ProThemesRU

Telegram бот для создания и управления сайтами через мессенджер.

## 🚀 Возможности

- ✅ Создание сайтов из шаблонов
- ✅ Управление личными сайтами
- ✅ Просмотр доступных шаблонов
- ✅ Интеграция с API ProThemesRU
- ✅ Удобный интерфейс с кнопками

## 📋 Требования

- Python 3.8+
- Telegram Bot Token
- API URL ProThemesRU

## 🔧 Установка

1. **Клонируйте репозиторий:**
```bash
git clone <your-repo>
cd telegram_bot
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Настройте переменные окружения:**
```bash
export TELEGRAM_BOT_TOKEN="your-bot-token"
export API_BASE_URL="https://your-api-url.vercel.app"
```

4. **Запустите бота:**
```bash
python run_bot.py
```

## 🌐 Развертывание

### Railway (Рекомендуется)

1. Создайте аккаунт на [Railway](https://railway.app)
2. Подключите GitHub репозиторий
3. Установите переменные окружения:
   - `TELEGRAM_BOT_TOKEN`
   - `API_BASE_URL`
4. Деплой произойдет автоматически

### Render

1. Создайте аккаунт на [Render](https://render.com)
2. Создайте новый Web Service
3. Подключите GitHub репозиторий
4. Установите переменные окружения
5. Start Command: `python bot.py`

### Heroku

1. Создайте аккаунт на [Heroku](https://heroku.com)
2. Установите Heroku CLI
3. Выполните команды:
```bash
heroku create your-bot-name
heroku config:set TELEGRAM_BOT_TOKEN="your-token"
heroku config:set API_BASE_URL="your-api-url"
git push heroku main
```

## 🔑 Получение Telegram Bot Token

1. Найдите [@BotFather](https://t.me/botfather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям
4. Скопируйте полученный токен

## 📱 Использование

1. Найдите вашего бота в Telegram
2. Отправьте `/start`
3. Используйте кнопки для навигации
4. Создавайте сайты прямо в чате!

## 🛠️ Разработка

### Структура проекта:
```
telegram_bot/
├── bot.py              # Основной файл бота
├── config.py           # Конфигурация
├── requirements.txt    # Зависимости
├── run_bot.py         # Скрипт запуска
├── Procfile           # Для Heroku
├── railway.json       # Для Railway
└── README.md          # Документация
```

### Добавление новых команд:

1. Создайте новый метод в классе `ProThemesRUBot`
2. Добавьте обработчик в `main()`
3. Обновите меню при необходимости

## 🔍 Отладка

Включите логирование:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи
2. Убедитесь в правильности токена
3. Проверьте доступность API
4. Создайте issue в репозитории

## 📄 Лицензия

MIT License - используйте свободно! 