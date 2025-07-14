@echo off
echo ========================================
echo ProThemesRU - ПОЛНЫЙ ДЕПЛОЙ
echo ========================================
echo.

echo [1/4] Подготовка к деплою...
echo.

echo [2/4] Добавляем все файлы в git...
git add .

echo [3/4] Создаем коммит со всеми изменениями...
git commit -m "ProThemesRU: Полный деплой - сайт + бот + все функции"

echo [4/4] Отправляем на GitHub...
git push origin main

echo.
echo ========================================
echo ДЕПЛОЙ ЗАВЕРШЕН!
echo ========================================
echo.
echo ✅ Основной сайт будет обновлен на Vercel
echo ✅ Telegram бот готов к деплою на Railway
echo.
echo 📋 Следующие шаги:
echo 1. Проверьте Vercel dashboard для сайта
echo 2. Деплойте бота на Railway:
echo    - Перейдите в папку telegram_bot
echo    - Выполните: railway login
echo    - Выполните: railway up
echo.
echo 🔧 Настройка бота:
echo - Добавьте переменные окружения в Railway:
echo   BOT_TOKEN=ваш_токен_бота
echo   WEBHOOK_URL=https://ваш-сайт.vercel.app/webhook
echo.
echo 🌐 Ваш сайт: https://ваш-сайт.vercel.app
echo 🤖 Бот будет работать после деплоя на Railway
echo.
pause 