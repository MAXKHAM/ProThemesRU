Write-Host "========================================" -ForegroundColor Green
Write-Host "ProThemesRU - Автоматический деплой" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

Write-Host ""
Write-Host "1. Добавляем все файлы в git..." -ForegroundColor Yellow
git add .

Write-Host ""
Write-Host "2. Создаем коммит..." -ForegroundColor Yellow
git commit -m "Обновление ProThemesRU - полный функционал с ботом"

Write-Host ""
Write-Host "3. Отправляем изменения на GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Деплой завершен!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Ваш сайт будет доступен на Vercel через несколько минут" -ForegroundColor Cyan
Write-Host "Проверьте статус деплоя на: https://vercel.com/dashboard" -ForegroundColor Cyan
Write-Host ""
Write-Host "Для деплоя бота на Railway:" -ForegroundColor Cyan
Write-Host "1. Перейдите в папку telegram_bot" -ForegroundColor White
Write-Host "2. Запустите: railway login" -ForegroundColor White
Write-Host "3. Запустите: railway up" -ForegroundColor White
Write-Host ""
Read-Host "Нажмите Enter для завершения" 