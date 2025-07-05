@echo off
echo 🚀 ProThemesRU - Quick Publish to GitHub
echo ========================================

echo.
echo 📋 Проверка статуса Git...
git status

echo.
echo 📦 Добавление всех файлов...
git add .

echo.
echo 💾 Создание коммита...
git commit -m "Update: Final version with all templates and styles"

echo.
echo ⚠️  ВАЖНО: Перед публикацией выполните следующие шаги:
echo.
echo 1. Создайте репозиторий на GitHub:
echo    - Перейдите на https://github.com
echo    - Нажмите "New repository"
echo    - Название: ProThemesRU
echo    - Описание: 🚀 Платформа для создания профессиональных сайтов
echo    - Public repository
echo.
echo 2. Настройте remote origin:
echo    git remote add origin https://github.com/YOUR_USERNAME/ProThemesRU.git
echo.
echo 3. Опубликуйте код:
echo    git push -u origin master
echo.
echo 📚 Подробные инструкции в файле: PUBLISH_TO_GITHUB.md
echo.

pause 