# Настройка переменных окружения для ProThemesRU Bot

## 📋 Обязательные переменные

### Для Railway деплоя:

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=ваш_токен_бота_от_BotFather
TELEGRAM_ADMIN_CHAT_ID=ваш_chat_id_администратора

# API Configuration
API_BASE_URL=https://pro-themes-ru.vercel.app
WEBHOOK_URL=https://pro-themes-ru.vercel.app/webhook

# Environment
ENVIRONMENT=production
PORT=8000
```

### Для локальной разработки:

```bash
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=ваш_токен_бота_от_BotFather
TELEGRAM_ADMIN_CHAT_ID=ваш_chat_id_администратора

# API Configuration
API_BASE_URL=http://localhost:5000
WEBHOOK_URL=http://localhost:5000/webhook

# Environment
ENVIRONMENT=development
PORT=8000

# Features
ENABLE_WEBHOOK=false
ENABLE_POLLING=true
```

## 🔧 Как получить токен бота:

1. **Найдите @BotFather в Telegram**
2. **Отправьте команду** `/newbot`
3. **Следуйте инструкциям** для создания бота
4. **Скопируйте токен** (выглядит как `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## 🔧 Как получить Chat ID:

1. **Найдите @userinfobot в Telegram**
2. **Отправьте любое сообщение**
3. **Скопируйте ваш Chat ID** (число, например `123456789`)

## 📋 Настройка в Railway:

### Через Railway Dashboard:
1. Перейдите в ваш проект на Railway
2. Откройте вкладку "Variables"
3. Добавьте каждую переменную:

```
TELEGRAM_BOT_TOKEN=ваш_токен
TELEGRAM_ADMIN_CHAT_ID=ваш_chat_id
API_BASE_URL=https://pro-themes-ru.vercel.app
WEBHOOK_URL=https://pro-themes-ru.vercel.app/webhook
ENVIRONMENT=production
PORT=8000
```

### Через Railway CLI:
```bash
railway variables set TELEGRAM_BOT_TOKEN=ваш_токен
railway variables set TELEGRAM_ADMIN_CHAT_ID=ваш_chat_id
railway variables set API_BASE_URL=https://pro-themes-ru.vercel.app
railway variables set WEBHOOK_URL=https://pro-themes-ru.vercel.app/webhook
railway variables set ENVIRONMENT=production
railway variables set PORT=8000
```

## 📋 Настройка локально:

### Создайте файл `.env` в папке `telegram_bot`:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=ваш_токен_бота
TELEGRAM_ADMIN_CHAT_ID=ваш_chat_id

# API Configuration
API_BASE_URL=http://localhost:5000
WEBHOOK_URL=http://localhost:5000/webhook

# Environment
ENVIRONMENT=development
PORT=8000

# Features
ENABLE_WEBHOOK=false
ENABLE_POLLING=true

# Logging
LOG_LEVEL=DEBUG
LOG_FILE=telegram_bot.log
```

## 🔍 Проверка настроек:

### Тест бота:
1. Запустите бота
2. Найдите его в Telegram
3. Отправьте `/start`
4. Проверьте ответ

### Тест API:
```bash
curl https://pro-themes-ru.vercel.app/api/health
```

### Тест webhook:
```bash
curl -X POST https://pro-themes-ru.vercel.app/webhook \
  -H "Content-Type: application/json" \
  -d '{"message":{"chat":{"id":123},"text":"/start"}}'
```

## 🚨 Важные замечания:

### Безопасность:
- ✅ **НЕ публикуйте** токен бота в открытом доступе
- ✅ **Используйте** переменные окружения
- ✅ **Регулярно обновляйте** токен при необходимости

### URL:
- ✅ **Используйте HTTPS** для продакшена
- ✅ **Проверьте** правильность URL
- ✅ **Убедитесь** что домен работает

### Окружение:
- ✅ **Development** - для локальной разработки
- ✅ **Production** - для продакшена
- ✅ **Проверьте** все переменные перед деплоем

## 📞 Поддержка:

Если возникли проблемы:
1. Проверьте правильность токена
2. Убедитесь, что все переменные установлены
3. Проверьте логи в Railway
4. Обратитесь в поддержку: @ProThemesRU_Support

## 🎯 Готово!

После настройки переменных окружения:
- ✅ Бот будет работать корректно
- ✅ Все функции будут доступны
- ✅ Интеграция с сайтом заработает
- ✅ Реферальная программа будет активна

**Удачи с настройкой! 🚀** 