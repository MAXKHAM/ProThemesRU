Write-Host "========================================" -ForegroundColor Green
Write-Host "ProThemesRU - ПОЛНЫЙ ДЕПЛОЙ" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

Write-Host "[1/4] Подготовка к деплою..." -ForegroundColor Yellow
Write-Host ""

Write-Host "[2/4] Добавляем все файлы в git..." -ForegroundColor Yellow
git add .

Write-Host "[3/4] Создаем коммит со всеми изменениями..." -ForegroundColor Yellow
git commit -m "ProThemesRU: Полный деплой - сайт + бот + все функции"

Write-Host "[4/4] Отправляем на GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "ДЕПЛОЙ ЗАВЕРШЕН!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "✅ Основной сайт будет обновлен на Vercel" -ForegroundColor Cyan
Write-Host "✅ Telegram бот готов к деплою на Railway" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 Следующие шаги:" -ForegroundColor White
Write-Host "1. Проверьте Vercel dashboard для сайта" -ForegroundColor White
Write-Host "2. Деплойте бота на Railway:" -ForegroundColor White
Write-Host "   - Перейдите в папку telegram_bot" -ForegroundColor Gray
Write-Host "   - Выполните: railway login" -ForegroundColor Gray
Write-Host "   - Выполните: railway up" -ForegroundColor Gray
Write-Host ""
Write-Host "🔧 Настройка бота:" -ForegroundColor White
Write-Host "- Добавьте переменные окружения в Railway:" -ForegroundColor Gray
Write-Host "  BOT_TOKEN=ваш_токен_бота" -ForegroundColor Gray
Write-Host "  WEBHOOK_URL=https://ваш-сайт.vercel.app/webhook" -ForegroundColor Gray
Write-Host ""
Write-Host "🌐 Ваш сайт: https://ваш-сайт.vercel.app" -ForegroundColor Cyan
Write-Host "🤖 Бот будет работать после деплоя на Railway" -ForegroundColor Cyan
Write-Host ""
Read-Host "Нажмите Enter для завершения" 