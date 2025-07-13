# Инструкции по деплою ProThemesRU

## 🚀 Готовый полнофункциональный сайт

**Что включено:**
- ✅ Flask API с базой данных
- ✅ Авторизация пользователей (JWT)
- ✅ Управление сайтами пользователей
- ✅ Готовые шаблоны
- ✅ Админ панель
- ✅ Все необходимые зависимости

## 📋 Варианты деплоя

### 1. Railway (РЕКОМЕНДУЕТСЯ - самый простой)

**Шаги:**
1. Зайдите на [railway.app](https://railway.app)
2. Войдите через GitHub
3. Нажмите "New Project"
4. Выберите "Deploy from GitHub repo"
5. Выберите репозиторий `ProThemesRU`
6. Railway автоматически найдет `Procfile` и `requirements.txt`
7. Дождитесь деплоя (2-3 минуты)

**Преимущества:**
- Бесплатный тариф
- Автоматический деплой
- PostgreSQL база данных включена
- Простая настройка

### 2. Render (альтернатива)

**Шаги:**
1. Зайдите на [render.com](https://render.com)
2. Создайте аккаунт
3. Нажмите "New Web Service"
4. Подключите GitHub репозиторий
5. Настройки:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Добавьте переменные окружения:
   - `SECRET_KEY` (автогенерация)
   - `JWT_SECRET_KEY` (автогенерация)
7. Создайте PostgreSQL базу данных

### 3. Heroku (классика)

**Шаги:**
1. Установите Heroku CLI
2. Войдите: `heroku login`
3. Создайте приложение: `heroku create prothemesru-app`
4. Добавьте базу: `heroku addons:create heroku-postgresql:mini`
5. Деплой: `git push heroku master`
6. Откройте: `heroku open`

### 4. DigitalOcean App Platform

**Шаги:**
1. Зайдите на [digitalocean.com](https://digitalocean.com)
2. App Platform → Create App
3. Подключите GitHub
4. Выберите репозиторий
5. Настройте переменные окружения
6. Деплой

### 5. Fly.io (бесплатный)

**Шаги:**
1. Установите flyctl
2. `fly auth login`
3. `fly launch`
4. Выберите репозиторий
5. Настройте базу данных
6. `fly deploy`

## 🔧 Переменные окружения

Добавьте эти переменные в настройках платформы:

```env
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_ENV=production
```

## 📊 API Endpoints

После деплоя ваш API будет доступен по адресу:
- `https://your-app.railway.app/` - главная страница
- `https://your-app.railway.app/api/health` - проверка здоровья
- `https://your-app.railway.app/api/auth/register` - регистрация
- `https://your-app.railway.app/api/auth/login` - вход
- `https://your-app.railway.app/api/sites` - управление сайтами
- `https://your-app.railway.app/api/templates` - шаблоны

## 🧪 Тестирование

После деплоя проверьте:

1. **Главная страница:**
```bash
curl https://your-app.railway.app/
```

2. **API здоровье:**
```bash
curl https://your-app.railway.app/api/health
```

3. **Регистрация пользователя:**
```bash
curl -X POST https://your-app.railway.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@test.com","password":"password123"}'
```

## 🎯 Рекомендация

**Используйте Railway** - он самый простой и надежный для вашего проекта!

## 📞 Поддержка

Если возникнут проблемы:
1. Проверьте логи в панели управления
2. Убедитесь, что все переменные окружения установлены
3. Проверьте, что база данных подключена

**Удачи с деплоем! 🚀** 