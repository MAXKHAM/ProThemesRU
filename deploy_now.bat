@echo off
title ProThemesRU - Деплой
color 0A

echo.
echo ========================================
echo    ProThemesRU - ПОЛНЫЙ ДЕПЛОЙ
echo ========================================
echo.

echo [1/4] Проверяем git...
git --version
if %errorlevel% neq 0 (
    echo ОШИБКА: Git не установлен!
    echo Скачайте Git с: https://git-scm.com/
    pause
    exit /b 1
)

echo.
echo [2/4] Добавляем все файлы...
git add .
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось добавить файлы!
    pause
    exit /b 1
)

echo.
echo [3/4] Создаем коммит...
git commit -m "ProThemesRU: Полный деплой - сайт + бот + все функции"
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось создать коммит!
    pause
    exit /b 1
)

echo.
echo [4/4] Отправляем на GitHub...
git push origin main
if %errorlevel% neq 0 (
    echo ОШИБКА: Не удалось отправить на GitHub!
    pause
    exit /b 1
)

echo.
echo ========================================
echo    ДЕПЛОЙ УСПЕШНО ЗАВЕРШЕН!
echo ========================================
echo.
echo ✅ Основной сайт обновлен на Vercel
echo ✅ Telegram бот готов к деплою на Railway
echo.
echo 📋 Следующие шаги:
echo 1. Проверьте Vercel dashboard
echo 2. Деплойте бота на Railway
echo.
echo Нажмите любую клавишу для завершения...
pause > nul 