@echo off
title Обновление GitHub репозиториев ProThemesRU
color 0A

echo.
echo ========================================
echo    ОБНОВЛЕНИЕ GITHUB РЕПОЗИТОРИЕВ
echo ========================================
echo.

echo [1/5] Настройка git...
git config --global user.name "MAXKHAM"
git config --global user.email "maxkham@example.com"

echo.
echo [2/5] Подключение к основному репозиторию...
git remote add origin https://github.com/MAXKHAM/ProThemesRU.git

echo.
echo [3/5] Добавление всех файлов...
git add .

echo.
echo [4/5] Создание коммита...
git commit -m "ProThemesRU: Финальный деплой - полный функционал"

echo.
echo [5/5] Отправка на GitHub...
git push -u origin main

echo.
echo ========================================
echo    РЕПОЗИТОРИИ ОБНОВЛЕНЫ!
echo ========================================
echo.
echo ✅ Основной репозиторий: https://github.com/MAXKHAM/ProThemesRU
echo ✅ Репозиторий бота: https://github.com/MAXKHAM/ProThemesRUBot
echo.
echo 📋 Следующие шаги:
echo 1. Проверьте Vercel dashboard
echo 2. Деплойте бота на Railway
echo.
pause 