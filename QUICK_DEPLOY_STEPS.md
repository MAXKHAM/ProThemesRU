# Быстрый деплой ProThemesRU

## 🚀 Шаг 1: Деплой основного сайта

### Вариант A: GitHub Desktop
1. Скачайте GitHub Desktop: https://desktop.github.com/
2. Откройте папку `C:\Users\user\Desktop\ProThemesRU1`
3. Создайте коммит: "ProThemesRU: Полный деплой"
4. Отправьте на GitHub

### Вариант B: Командная строка
```bash
git add .
git commit -m "ProThemesRU: Полный деплой - сайт + бот"
git push origin main
```

### Вариант C: Прямая загрузка
1. Перейдите на GitHub.com
2. Создайте репозиторий "ProThemesRU"
3. Загрузите все файлы из папки проекта

## 🤖 Шаг 2: Деплой Telegram бота

### На Railway:
1. Перейдите на https://railway.app
2. Создайте новый проект
3. Подключите GitHub репозиторий
4. Выберите папку `telegram_bot`
5. Настройте переменные окружения:
   - `BOT_TOKEN` = ваш_токен_бота
   - `WEBHOOK_URL` = https://ваш-сайт.vercel.app/webhook
6. Деплойте

### Через CLI:
```bash
cd telegram_bot
railway login
railway init
railway up
```

## 🔧 Шаг 3: Настройка вебхука

После деплоя выполните в браузере:
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://ваш-сайт.vercel.app/webhook
```

## ✅ Шаг 4: Проверка

1. **Сайт**: Откройте ваш Vercel URL
2. **API**: Проверьте `/api/health`
3. **Бот**: Отправьте `/start` в Telegram

## 📋 Что будет задеплоено:

### Основной сайт (Vercel):
- ✅ Полный функционал сайта
- ✅ API endpoints
- ✅ Админ панель
- ✅ Система заказов
- ✅ Платежи
- ✅ Реферальная программа
- ✅ Конструктор сайтов

### Telegram бот (Railway):
- ✅ Полный функционал бота
- ✅ Интеграция с сайтом
- ✅ Обработка заказов
- ✅ Уведомления
- ✅ Админ функции

## 🎯 Результат:

- **Сайт**: https://ваш-сайт.vercel.app
- **Бот**: Работает в Telegram
- **API**: Полностью функционален
- **Все функции**: Доступны

## 🆘 Если что-то не работает:

1. Проверьте логи в Vercel/Railway
2. Убедитесь, что переменные окружения настроены
3. Проверьте, что вебхук установлен
4. Убедитесь, что все файлы загружены

## 📞 Поддержка:

- Vercel dashboard: https://vercel.com/dashboard
- Railway dashboard: https://railway.app/dashboard
- GitHub: ваш репозиторий

**Готово! Ваш полный проект будет работать!** 