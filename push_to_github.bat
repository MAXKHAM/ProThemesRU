@echo off
title Отправка изменений на GitHub
color 0A

echo.
echo ========================================
echo    ОТПРАВКА ИЗМЕНЕНИЙ НА GITHUB
echo ========================================
echo.

echo [1/4] Настройка git...
git config --global user.name "MAXKHAM"
git config --global user.email "maxkham@example.com"

echo.
echo [2/4] Добавление всех файлов...
git add .

echo.
echo [3/4] Создание коммита...
git commit -m "ProThemesRU: Исправленный код - полный функционал"

echo.
echo [4/4] Отправка на GitHub...
git push origin main

echo.
echo ========================================
echo    ИЗМЕНЕНИЯ ОТПРАВЛЕНЫ!
echo ========================================
echo.
echo ✅ Основной репозиторий обновлен
echo ✅ Vercel автоматически обновит сайт
echo ✅ Бот готов к деплою на Railway
echo.
echo 🌐 Сайт: https://github.com/MAXKHAM/ProThemesRU
echo 🤖 Бот: https://github.com/MAXKHAM/ProThemesRUBot
echo.
pause 