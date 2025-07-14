@echo off
title Исправление отправки на GitHub
color 0A

echo.
echo ========================================
echo    ИСПРАВЛЕНИЕ ОТПРАВКИ НА GITHUB
echo ========================================
echo.

echo [1/6] Проверка текущей ветки...
git branch

echo.
echo [2/6] Проверка удаленных репозиториев...
git remote -v

echo.
echo [3/6] Добавление файлов...
git add .

echo.
echo [4/6] Создание коммита...
git commit -m "ProThemesRU: Исправленный код - полный функционал с env поддержкой"

echo.
echo [5/6] Попытка отправки на master...
git push origin master

echo.
echo [6/6] Если master не работает, попробуем main...
git push origin main

echo.
echo ========================================
echo    ПРОВЕРЬТЕ РЕЗУЛЬТАТ ВЫШЕ
echo ========================================
echo.
echo Если есть ошибки, попробуйте:
echo 1. git branch -a (показать все ветки)
echo 2. git checkout master (переключиться на master)
echo 3. git push origin master (отправить на master)
echo.
pause 