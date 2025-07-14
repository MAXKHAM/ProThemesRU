# Деплой Telegram бота в отдельный репозиторий

## 📋 Шаг 1: Подготовка файлов бота

Создайте новую папку для бота и скопируйте туда файлы:

```bash
mkdir ProThemesRUBot
cd ProThemesRUBot
```

### Файлы для копирования:
- `telegram_bot/bot_final.py` → `bot.py`
- `telegram_bot/requirements.txt` → `requirements.txt`
- `telegram_bot/railway_final.json` → `railway.json`
- `telegram_bot/vercel.json` → `vercel.json` (если нужен)

## 📋 Шаг 2: Создание репозитория бота

### Вариант A: GitHub CLI
```bash
gh repo create MAXKHAM/ProThemesRUBot --public --clone
cd ProThemesRUBot
```

### Вариант B: Ручное создание
1. Перейдите на https://github.com/MAXKHAM/ProThemesRUBot
2. Создайте новый репозиторий
3. Клонируйте его локально

## 📋 Шаг 3: Загрузка файлов

```bash
# Копируем файлы
copy ..\telegram_bot\bot_final.py bot.py
copy ..\telegram_bot\requirements.txt requirements.txt
copy ..\telegram_bot\railway_final.json railway.json

# Добавляем в git
git add .
git commit -m "ProThemesRU Bot: Финальная версия"
git push origin main
```

## 📋 Шаг 4: Деплой на Railway

### Через Railway Dashboard:
1. Перейдите на https://railway.app
2. Создайте новый проект
3. Подключите репозиторий `MAXKHAM/ProThemesRUBot`
4. Настройте переменные окружения:
   ```
   BOT_TOKEN=ваш_токен_бота
   WEBHOOK_URL=https://ваш-сайт.vercel.app/webhook
   API_BASE_URL=https://ваш-сайт.vercel.app
   ```

### Через CLI:
```bash
railway login
railway init
railway up
```

## 📋 Шаг 5: Настройка вебхука

После деплоя выполните:
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://ваш-сайт.vercel.app/webhook
```

## 📋 Шаг 6: Проверка

1. Найдите бота в Telegram
2. Отправьте `/start`
3. Проверьте все команды

## 📁 Структура репозитория бота:

```
ProThemesRUBot/
├── bot.py              # Основной файл бота
├── requirements.txt    # Python зависимости
├── railway.json       # Конфигурация Railway
├── vercel.json        # Конфигурация Vercel (опционально)
├── README.md          # Документация
└── .gitignore         # Исключения git
```

## 🔧 Переменные окружения для Railway:

### Обязательные:
- `BOT_TOKEN` - токен вашего бота от BotFather
- `WEBHOOK_URL` - URL вашего основного сайта + /webhook
- `API_BASE_URL` - URL вашего основного сайта

### Дополнительные:
- `PORT` - порт (обычно 8000)
- `ENVIRONMENT` - окружение (production)

## ✅ Результат:

После выполнения всех шагов:
- ✅ Бот работает на Railway
- ✅ Интегрирован с основным сайтом
- ✅ Все команды работают
- ✅ Вебхук настроен

## 🆘 Если что-то не работает:

1. Проверьте переменные окружения в Railway
2. Убедитесь, что основной сайт работает
3. Проверьте логи в Railway dashboard
4. Убедитесь, что вебхук установлен правильно

## 📞 Поддержка:

- Railway: https://railway.app/dashboard
- GitHub: https://github.com/MAXKHAM/ProThemesRUBot
- Telegram: @ProThemesRU_Support

**Готово! Бот будет работать в отдельном репозитории! 🚀** 