@echo off
echo ========================================
echo ProThemesRU - Автоматический деплой
echo ========================================

echo.
echo 1. Добавляем все файлы в git...
git add .

echo.
echo 2. Создаем коммит...
git commit -m "Обновление ProThemesRU - полный функционал с ботом"

echo.
echo 3. Отправляем изменения на GitHub...
git push origin main

echo.
echo ========================================
echo Деплой завершен!
echo ========================================
echo.
echo Ваш сайт будет доступен на Vercel через несколько минут
echo Проверьте статус деплоя на: https://vercel.com/dashboard
echo.
echo Для деплоя бота на Railway:
echo 1. Перейдите в папку telegram_bot
echo 2. Запустите: railway login
echo 3. Запустите: railway up
echo.
pause 