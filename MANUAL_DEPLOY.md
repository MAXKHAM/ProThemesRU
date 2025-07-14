# Ручной деплой ProThemesRU

## Вариант 1: GitHub Desktop (Рекомендуется)

1. **Скачайте GitHub Desktop**: https://desktop.github.com/
2. **Установите и войдите** в свой аккаунт GitHub
3. **Добавьте репозиторий**:
   - File → Add Local Repository
   - Выберите папку `C:\Users\user\Desktop\ProThemesRU1`
4. **Создайте коммит**:
   - Напишите сообщение: "Обновление ProThemesRU - полный функционал"
   - Нажмите "Commit to main"
5. **Отправьте изменения**:
   - Нажмите "Push origin"

## Вариант 2: Прямая загрузка на GitHub

1. **Перейдите на GitHub**: https://github.com
2. **Создайте новый репозиторий**: ProThemesRU
3. **Загрузите файлы**:
   - Нажмите "uploading an existing file"
   - Перетащите все файлы из папки проекта
   - Нажмите "Commit changes"

## Вариант 3: Vercel CLI

1. **Установите Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Войдите в Vercel**:
   ```bash
   vercel login
   ```

3. **Деплойте проект**:
   ```bash
   vercel
   ```

## Вариант 4: Прямой деплой на Vercel

1. **Перейдите на Vercel**: https://vercel.com
2. **Создайте новый проект**
3. **Подключите GitHub репозиторий**
4. **Настройте проект**:
   - Framework: Other
   - Root Directory: ./
   - Build Command: (оставьте пустым)
   - Output Directory: (оставьте пустым)

## Проверка деплоя

После деплоя проверьте:

1. **Сайт работает**: Ваш Vercel URL
2. **API отвечает**: `/api/health` endpoint
3. **Бот готов**: Деплойте на Railway

## Деплой бота на Railway

1. **Перейдите в папку** `telegram_bot`
2. **Установите Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```
3. **Войдите в Railway**:
   ```bash
   railway login
   ```
4. **Деплойте**:
   ```bash
   railway up
   ```

## Настройка переменных окружения

В Railway добавьте:
- `BOT_TOKEN` - токен вашего бота
- `WEBHOOK_URL` - URL вашего Vercel сайта + /webhook

## Установка вебхука

После деплоя выполните:
```
https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=https://your-vercel-domain.vercel.app/webhook
```

## Альтернативный способ - Git Bash

Если у вас установлен Git Bash:

1. **Откройте Git Bash** в папке проекта
2. **Выполните команды**:
   ```bash
   git add .
   git commit -m "Обновление ProThemesRU"
   git push origin main
   ```

## Проблемы и решения

### Git не установлен:
- Скачайте с: https://git-scm.com/
- Или используйте GitHub Desktop

### Проблемы с правами:
- Запустите от имени администратора
- Проверьте настройки git

### Vercel не видит изменения:
- Убедитесь, что файлы добавлены в git
- Проверьте, что коммит создан
- Подождите несколько минут

## Быстрый старт

1. **Скачайте GitHub Desktop**
2. **Добавьте папку проекта**
3. **Создайте коммит и отправьте**
4. **Настройте Vercel**
5. **Деплойте бота на Railway**

Готово! Ваш сайт будет работать на Vercel, а бот на Railway. 