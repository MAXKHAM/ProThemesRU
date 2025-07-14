@echo off
title Обновление GitHub репозиториев ProThemesRU
color 0A

echo.
echo ========================================
echo    ОБНОВЛЕНИЕ GITHUB РЕПОЗИТОРИЕВ
echo ========================================
echo.

echo [1/5] Проверка git...
git --version
if %errorlevel% neq 0 (
    echo ❌ Git не установлен!
    echo Скачайте Git с: https://git-scm.com/
    pause
    exit /b 1
)

echo.
echo [2/5] Настройка git...
git config --global user.name "MAXKHAM"
git config --global user.email "maxkham@example.com"

echo.
echo [3/5] Добавление всех файлов...
git add .

echo.
echo [4/5] Создание коммита...
git commit -m "ProThemesRU: Исправленный код - полный функционал с env поддержкой"

echo.
echo [5/5] Отправка на GitHub...
git push origin main

echo.
echo ========================================
echo    GITHUB ОБНОВЛЕН!
echo ========================================
echo.
echo ✅ Основной репозиторий: https://github.com/MAXKHAM/ProThemesRU
echo ✅ Репозиторий бота: https://github.com/MAXKHAM/ProThemesRUBot
echo.
echo 🌐 Vercel автоматически обновит сайт
echo 🤖 Бот готов к деплою на Railway
echo.
echo 📋 Следующие шаги:
echo 1. Проверьте Vercel dashboard
echo 2. Деплойте бота на Railway
echo 3. Настройте переменные окружения
echo.
pause 