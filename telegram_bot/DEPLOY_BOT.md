# 🚀 Деплой Telegram бота ProThemesRU на Vercel

## ✅ Что исправлено в боте:

### 🔧 **Основные исправления:**
- ✅ Обновлен API URL на реальный: `https://prothemesru.vercel.app`
- ✅ Добавлена обработка ошибок и таймаутов
- ✅ Fallback шаблоны если API недоступен
- ✅ Webhook поддержка для Vercel
- ✅ Улучшенное логирование
- ✅ Стабильная работа без перебоев

### 🎯 **Функции бота:**
- ✅ `/start` - Главное меню
- ✅ `/templates` - Просмотр шаблонов
- ✅ `/my_sites` - Мои сайты
- ✅ `/help` - Помощь
- ✅ Интерактивные кнопки
- ✅ Ссылки на веб-интерфейс

## 🚀 Как задеплоить бота:

### Шаг 1: Подготовка файлов
Убедитесь, что в папке `telegram_bot/` есть:
- ✅ `webhook_bot.py` - основной файл бота
- ✅ `requirements.txt` - зависимости
- ✅ `vercel.json` - конфигурация Vercel

### Шаг 2: Создание vercel.json для бота
Создайте файл `telegram_bot/vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "webhook_bot.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/webhook_bot.py"
    }
  ],
  "env": {
    "TELEGRAM_BOT_TOKEN": "@telegram_bot_token",
    "API_BASE_URL": "https://prothemesru.vercel.app",
    "WEBHOOK_URL": "https://your-bot-domain.vercel.app/webhook"
  }
}
```

### Шаг 3: Настройка переменных окружения в Vercel
1. Зайдите в Vercel Dashboard
2. Выберите проект бота
3. Перейдите в Settings → Environment Variables
4. Добавьте переменные:
   ```
   TELEGRAM_BOT_TOKEN=ваш_токен_бота
   API_BASE_URL=https://prothemesru.vercel.app
   WEBHOOK_URL=https://your-bot-domain.vercel.app/webhook
   ```

### Шаг 4: Деплой на Vercel
```bash
# Перейдите в папку бота
cd telegram_bot

# Добавьте файлы в Git
git add .

# Закоммитьте изменения
git commit -m "Обновленный бот с webhook поддержкой"

# Отправьте на GitHub
git push origin master
```

### Шаг 5: Настройка webhook
После деплоя:
1. Откройте: `https://your-bot-domain.vercel.app/set-webhook`
2. Убедитесь, что webhook установлен
3. Проверьте статус: `https://your-bot-domain.vercel.app/health`

## 🔧 Проверка работы бота:

### Тест команд:
1. Найдите бота в Telegram: `@ProThemesRU_Bot`
2. Отправьте `/start`
3. Проверьте все кнопки
4. Попробуйте `/templates`
5. Проверьте `/help`

### Проверка API:
- Health check: `https://your-bot-domain.vercel.app/health`
- Webhook status: `https://your-bot-domain.vercel.app/set-webhook`

## 🚨 Возможные проблемы и решения:

### Проблема 1: Бот не отвечает
**Решение:**
- Проверьте TELEGRAM_BOT_TOKEN
- Убедитесь, что webhook установлен
- Проверьте логи в Vercel Dashboard

### Проблема 2: API недоступен
**Решение:**
- Бот использует fallback шаблоны
- Проверьте API_BASE_URL
- Убедитесь, что основной сайт работает

### Проблема 3: Webhook не работает
**Решение:**
- Проверьте WEBHOOK_URL
- Убедитесь, что домен правильный
- Переустановите webhook через /set-webhook

## 📱 Команды бота:

### Основные команды:
- `/start` - Главное меню
- `/help` - Справка
- `/templates` - Шаблоны
- `/my_sites` - Мои сайты

### Интерактивные кнопки:
- 🏗️ Создать сайт
- 📋 Шаблоны
- 👤 Мои сайты
- ❓ Помощь

## 🎯 Результат:

После успешного деплоя у вас будет:
- ✅ Работающий Telegram бот
- ✅ Интеграция с основным API
- ✅ Стабильная работа 24/7
- ✅ Поддержка webhook
- ✅ Обработка ошибок

## 📞 Поддержка:

Если бот не работает:
1. Проверьте логи в Vercel Dashboard
2. Убедитесь, что все переменные окружения установлены
3. Проверьте webhook статус
4. Обратитесь в поддержку: @ProThemesRU_Bot

**УДАЧИ С ДЕПЛОЕМ БОТА!** 🚀 