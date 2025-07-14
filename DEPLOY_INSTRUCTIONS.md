# Инструкция по деплою ProThemesRU

## Шаг 1: Инициализация Git репозитория

Откройте командную строку или PowerShell в папке проекта и выполните:

```bash
# Инициализация git
git init

# Добавление всех файлов
git add .

# Первый коммит
git commit -m "Инициализация ProThemesRU"

# Добавление удаленного репозитория (замените YOUR_USERNAME на ваше имя пользователя GitHub)
git remote add origin https://github.com/YOUR_USERNAME/ProThemesRU.git

# Переименование ветки в main
git branch -M main

# Отправка на GitHub
git push -u origin main
```

## Шаг 2: Настройка Vercel

1. Перейдите на https://vercel.com
2. Войдите в аккаунт
3. Нажмите "New Project"
4. Выберите ваш репозиторий ProThemesRU
5. Настройте проект:
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: оставьте пустым
   - Output Directory: оставьте пустым
6. Нажмите "Deploy"

## Шаг 3: Деплой Telegram бота на Railway

1. Перейдите в папку `telegram_bot`
2. Выполните команды:

```bash
# Установка Railway CLI
npm install -g @railway/cli

# Вход в Railway
railway login

# Инициализация проекта
railway init

# Деплой
railway up
```

3. Настройте переменные окружения в Railway:
   - `BOT_TOKEN` - токен вашего бота
   - `WEBHOOK_URL` - URL вашего Vercel сайта + /webhook

## Шаг 4: Настройка вебхука для бота

После деплоя на Vercel, установите вебхук:

```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-vercel-domain.vercel.app/webhook
```

## Автоматические скрипты

### Для Windows (PowerShell):
```powershell
# Запустите deploy_script.ps1
powershell -ExecutionPolicy Bypass -File deploy_script.ps1
```

### Для Windows (CMD):
```cmd
# Запустите deploy_script.bat
deploy_script.bat
```

## Проверка деплоя

1. **Сайт**: Проверьте ваш Vercel URL
2. **API**: Проверьте `/api/health` endpoint
3. **Бот**: Отправьте `/start` в Telegram

## Возможные проблемы

### Git не инициализирован:
```bash
git init
git add .
git commit -m "Initial commit"
```

### Проблемы с правами доступа:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Проблемы с Vercel:
- Убедитесь, что в корне проекта есть `vercel.json`
- Проверьте, что все зависимости указаны в `requirements.txt`

### Проблемы с ботом:
- Проверьте переменные окружения в Railway
- Убедитесь, что вебхук установлен правильно
- Проверьте логи в Railway dashboard

## Структура проекта после деплоя

```
ProThemesRU/
├── app/                    # Flask приложение
├── telegram_bot/          # Telegram бот
├── frontend/              # React приложение
├── public/                # Статические файлы
├── templates/             # HTML шаблоны
├── requirements.txt       # Python зависимости
├── vercel.json           # Конфигурация Vercel
└── README.md             # Документация
```

## Поддержка

Если возникли проблемы:
1. Проверьте логи в Vercel и Railway
2. Убедитесь, что все переменные окружения настроены
3. Проверьте, что все файлы добавлены в git
4. Убедитесь, что вебхук установлен правильно 