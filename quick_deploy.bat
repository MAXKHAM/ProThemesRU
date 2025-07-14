@echo off
echo ProThemesRU - Быстрый деплой
echo.

echo Добавляем файлы в git...
git add .

echo Создаем коммит...
git commit -m "Обновление ProThemesRU"

echo Отправляем на GitHub...
git push

echo.
echo Деплой завершен! Проверьте Vercel dashboard.
pause 