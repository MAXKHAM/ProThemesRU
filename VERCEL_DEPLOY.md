# Деплой на Vercel (БЕСПЛАТНО!)

## 🚀 Пошаговая инструкция

### 1. Подготовка
- У вас есть `app_simple.py` - рабочее Flask приложение
- `vercel.json` - конфигурация для Vercel
- `requirements.txt` - зависимости
- Всё залито на GitHub

### 2. Деплой на Vercel

1. **Зайдите на [vercel.com](https://vercel.com)**
2. **Нажмите "Sign Up" и войдите через GitHub**
3. **Нажмите "New Project"**
4. **Выберите ваш репозиторий `ProThemesRU`**
5. **Vercel автоматически:**
   - Найдет `vercel.json`
   - Установит зависимости из `requirements.txt`
   - Запустит `app_simple.py`
6. **Нажмите "Deploy"**
7. **Дождитесь деплоя (1-2 минуты)**

### 3. Результат
- Ваш сайт будет доступен по адресу: `https://prothemesru.vercel.app`
- API будет работать: `https://prothemesru.vercel.app/api/health`

### 4. Преимущества Vercel
- ✅ Полностью бесплатный
- ✅ Автоматический деплой
- ✅ Быстрая работа
- ✅ SSL сертификат включен
- ✅ CDN по всему миру

### 5. Тестирование
После деплоя проверьте:
- `https://your-app.vercel.app/` - главная страница
- `https://your-app.vercel.app/api/health` - API здоровье
- `https://your-app.vercel.app/api/test` - тестовая страница

## 🎯 Готово!
Vercel должен деплоить без проблем! 