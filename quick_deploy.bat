@echo off
echo 🚀 ProThemesRU - Быстрый деплой на GitHub
echo.

echo 📁 Обновляем файлы...
copy app_final.py app.py >nul 2>&1
copy vercel_final.json vercel.json >nul 2>&1
copy requirements_final.txt requirements.txt >nul 2>&1
copy FINAL_README.md README.md >nul 2>&1

echo 🔧 Настраиваем git...
git config --global user.name "MAXKHAM"
git config --global user.email "maxkham@example.com"

echo 📤 Добавляем файлы...
git add .

echo 💾 Создаем коммит...
git commit -m "ProThemesRU: Финальный деплой - полный функционал"

echo 🚀 Отправляем на GitHub...
git push origin main

echo.
echo ✅ ДЕПЛОЙ ЗАВЕРШЕН!
echo.
echo 🌐 Сайт: https://github.com/MAXKHAM/ProThemesRU
echo 🤖 Бот: https://github.com/MAXKHAM/ProThemesRUBot
echo.
echo 📋 Следующие шаги:
echo 1. Проверьте Vercel dashboard
echo 2. Деплойте бота на Railway
echo.
pause 