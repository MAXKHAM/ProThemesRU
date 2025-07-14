Write-Host "Обновление файлов ProThemesRU..." -ForegroundColor Green

# Переименование финальных файлов
Write-Host "Переименование файлов..." -ForegroundColor Yellow

# Основные файлы
if (Test-Path "app_final.py") {
    Copy-Item "app_final.py" "app.py" -Force
    Write-Host "✅ app_final.py → app.py" -ForegroundColor Green
}

if (Test-Path "vercel_final.json") {
    Copy-Item "vercel_final.json" "vercel.json" -Force
    Write-Host "✅ vercel_final.json → vercel.json" -ForegroundColor Green
}

if (Test-Path "requirements_final.txt") {
    Copy-Item "requirements_final.txt" "requirements.txt" -Force
    Write-Host "✅ requirements_final.txt → requirements.txt" -ForegroundColor Green
}

if (Test-Path "FINAL_README.md") {
    Copy-Item "FINAL_README.md" "README.md" -Force
    Write-Host "✅ FINAL_README.md → README.md" -ForegroundColor Green
}

# Файлы бота
if (Test-Path "telegram_bot/bot_final.py") {
    Copy-Item "telegram_bot/bot_final.py" "telegram_bot/bot.py" -Force
    Write-Host "✅ telegram_bot/bot_final.py → telegram_bot/bot.py" -ForegroundColor Green
}

if (Test-Path "telegram_bot/railway_final.json") {
    Copy-Item "telegram_bot/railway_final.json" "telegram_bot/railway.json" -Force
    Write-Host "✅ telegram_bot/railway_final.json → telegram_bot/railway.json" -ForegroundColor Green
}

Write-Host ""
Write-Host "Все файлы обновлены!" -ForegroundColor Green
Write-Host "Теперь можно выполнить деплой." -ForegroundColor Cyan 