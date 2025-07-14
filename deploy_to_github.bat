@echo off
title Деплой ProThemesRU на GitHub
color 0A

echo.
echo ========================================
echo    ДЕПЛОЙ PROTHEMESRU НА GITHUB
echo ========================================
echo.

echo [1/6] Обновление файлов...
powershell -ExecutionPolicy Bypass -File update_files.ps1

echo.
echo [2/6] Настройка git...
git config --global user.name "MAXKHAM"
git config --global user.email "maxkham@example.com"

echo.
echo [3/6] Подключение к репозиторию...
git remote add origin https://github.com/MAXKHAM/ProThemesRU.git

echo.
echo [4/6] Добавление файлов...
git add .

echo.
echo [5/6] Создание коммита...
git commit -m "ProThemesRU: Финальный деплой - полный функционал с ботом"

echo.
echo [6/6] Отправка на GitHub...
git push -u origin main

echo.
echo ========================================
echo    ДЕПЛОЙ ЗАВЕРШЕН!
echo ========================================
echo.
echo ✅ Основной репозиторий: https://github.com/MAXKHAM/ProThemesRU
echo ✅ Репозиторий бота: https://github.com/MAXKHAM/ProThemesRUBot
echo.
echo 🌐 Сайт будет обновлен на Vercel автоматически
echo 🤖 Бот готов к деплою на Railway
echo.
echo 📋 Следующие шаги:
echo 1. Проверьте Vercel dashboard
echo 2. Деплойте бота на Railway
echo 3. Настройте переменные окружения
echo.
pause 