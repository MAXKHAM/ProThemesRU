# 📚 API Документация ProThemesRU

## 🚀 Обзор

ProThemesRU - это полнофункциональная платформа для создания сайтов с визуальным конструктором, готовыми шаблонами, Telegram ботом и платежной системой.

**Версия:** 1.0.0  
**Статус:** Рабочая версия ✅

## 🔗 Базовый URL

```
https://your-vercel-url.vercel.app
```

## 📋 Доступные эндпоинты

### 🏠 Основные эндпоинты

#### `GET /`
Главная страница с информацией о платформе.

**Ответ:**
```json
{
  "message": "ProThemesRU - Полнофункциональная платформа",
  "status": "success",
  "version": "1.0.0",
  "features": [
    "Визуальный конструктор сайтов",
    "Готовые шаблоны",
    "Telegram бот",
    "Платежная система",
    "Админ панель"
  ]
}
```

#### `GET /api/health`
Проверка состояния API и базы данных.

**Ответ:**
```json
{
  "status": "healthy",
  "message": "API работает",
  "database": "connected",
  "templates_count": 5,
  "users_count": 0
}
```

### 🔐 Аутентификация

#### `POST /api/auth/register`
Регистрация нового пользователя.

**Тело запроса:**
```json
{
  "username": "user123",
  "email": "user@example.com",
  "password": "password123"
}
```

**Ответ:**
```json
{
  "message": "User registered successfully",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "role": "user"
  }
}
```

#### `POST /api/auth/login`
Вход в систему.

**Тело запроса:**
```json
{
  "username": "user123",
  "password": "password123"
}
```

**Ответ:**
```json
{
  "message": "Login successful",
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "role": "user"
  }
}
```

#### `GET /api/auth/me`
Получение данных текущего пользователя.

**Заголовки:**
```
Authorization: Bearer <access_token>
```

**Ответ:**
```json
{
  "user": {
    "id": 1,
    "username": "user123",
    "email": "user@example.com",
    "role": "user",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### 🏗️ Управление сайтами

#### `GET /api/sites`
Получение списка сайтов пользователя.

**Заголовки:**
```
Authorization: Bearer <access_token>
```

**Ответ:**
```json
{
  "sites": [
    {
      "id": 1,
      "name": "Мой сайт",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "is_published": false,
      "published_url": null
    }
  ]
}
```

#### `POST /api/sites`
Создание нового сайта.

**Заголовки:**
```
Authorization: Bearer <access_token>
```

**Тело запроса:**
```json
{
  "name": "Новый сайт",
  "elements": "[]",
  "canvas_settings": "{}"
}
```

#### `GET /api/sites/<id>`
Получение конкретного сайта.

#### `PUT /api/sites/<id>`
Обновление сайта.

### 🎨 Шаблоны

#### `GET /api/templates`
Получение всех доступных шаблонов.

**Ответ:**
```json
{
  "templates": [
    {
      "id": 1,
      "name": "Бизнес сайт",
      "category": "business",
      "price": 0.0,
      "downloads": 0,
      "rating": 0.0,
      "status": "active"
    }
  ]
}
```

#### `GET /api/templates/<id>`
Получение конкретного шаблона.

### 👨‍💼 Админ панель

#### `GET /api/admin/dashboard`
Админская панель (только для администраторов).

**Заголовки:**
```
Authorization: Bearer <access_token>
```

## 🔧 Тестирование API

### Локальное тестирование

1. Запустите сервер:
```bash
python app.py
```

2. Запустите тесты:
```bash
python test_api.py
```

### Продакшн тестирование

1. Обновите `BASE_URL` в `test_api.py`
2. Запустите тесты:
```bash
python test_api.py
```

## 🚀 Развертывание

### Vercel (рекомендуется)

1. Подключите репозиторий к Vercel
2. Настройте переменные окружения:
   - `SECRET_KEY`
   - `JWT_SECRET_KEY`
   - `DATABASE_URL` (если используете внешнюю БД)

3. Деплоймент произойдет автоматически

### Railway

1. Создайте проект в Railway
2. Подключите репозиторий
3. Настройте переменные окружения
4. Деплоймент произойдет автоматически

### Render

1. Создайте новый Web Service
2. Подключите репозиторий
3. Настройте:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
4. Настройте переменные окружения

## 📦 Зависимости

Основные зависимости:
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-CORS
- Werkzeug

Полный список в `requirements.txt`

## 🔒 Безопасность

- JWT токены для аутентификации
- Хеширование паролей
- CORS настройки
- Валидация входных данных

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи сервера
2. Убедитесь в правильности URL
3. Проверьте заголовки авторизации
4. Обратитесь к документации

---

**ProThemesRU API v1.0.0** - Полнофункциональная платформа для создания сайтов 🚀 