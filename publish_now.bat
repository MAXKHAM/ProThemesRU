@echo off
echo 🚀 ProThemesRU - Быстрая публикация на GitHub
echo =============================================

echo.
echo 📋 Проверка статуса...
git status

echo.
echo 📦 Добавление файлов...
git add .

echo.
echo 💾 Создание коммита...
git commit -m "Final: Complete ProThemesRU with Render deployment and enhanced templates"

echo.
echo 🌐 Проверка remote...
git remote -v

echo.
echo ⚠️  ВАЖНО: Убедитесь что remote origin настроен правильно!
echo.
echo Если remote не настроен, выполните:
echo git remote add origin https://github.com/YOUR_USERNAME/ProThemesRU.git
echo.
echo Затем нажмите любую клавишу для публикации...
pause

echo.
echo 🚀 Публикация на GitHub...
git push origin master

echo.
echo ✅ Готово! Проверьте ваш репозиторий на GitHub
echo.
pause 