# 🚀 Развертывание ProThemesRU - ПОШАГОВАЯ ИНСТРУКЦИЯ

## ✅ Ваш API уже работает!
**URL**: https://pro-themes-ru-maxkhams-projects.vercel.app/

## 🔄 Шаг 1: Обновление Backend на Vercel

### 1.1 Замените файл app.py
Замените содержимое `app.py` на `app_vercel.py`:

```bash
# Скопируйте содержимое app_vercel.py в app.py
cp app_vercel.py app.py
```

### 1.2 Обновите requirements.txt
Убедитесь, что в `requirements.txt` есть все зависимости:

```txt
Flask==2.3.3
Flask-SQLAlchemy==3.0.5
Flask-JWT-Extended==4.5.3
Flask-CORS==4.0.0
Werkzeug==2.3.7
python-dotenv==1.0.0
requests==2.31.0
```

### 1.3 Обновите vercel.json
Убедитесь, что `vercel.json` содержит:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ],
  "env": {
    "SECRET_KEY": "prothemesru-super-secret-key-2024",
    "JWT_SECRET_KEY": "prothemesru-jwt-secret-key-2024"
  }
}
```

### 1.4 Запустите деплой
```bash
vercel --prod
```

## 🤖 Шаг 2: Развертывание Telegram бота

### 2.1 Создайте бота в Telegram
1. Найдите [@BotFather](https://t.me/botfather)
2. Отправьте `/newbot`
3. Имя: `ProThemesRU Bot`
4. Username: `your_prothemesru_bot`
5. **Скопируйте токен!**

### 2.2 Разверните на Railway (Рекомендуется)

1. **Перейдите на**: https://railway.app
2. **Создайте аккаунт** (через GitHub)
3. **Создайте новый проект**
4. **Подключите GitHub репозиторий**
5. **Выберите папку** `telegram_bot`
6. **Установите переменные окружения**:

```
TELEGRAM_BOT_TOKEN=ваш_токен_бота
API_BASE_URL=https://pro-themes-ru-maxkhams-projects.vercel.app
```

7. **Деплой произойдет автоматически**

### 2.3 Альтернатива: Render

1. **Перейдите на**: https://render.com
2. **Создайте новый Web Service**
3. **Подключите GitHub**
4. **Настройки**:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python bot.py`
   - Environment Variables: как выше

## 🌐 Шаг 3: Развертывание Frontend

### 3.1 Перейдите в папку frontend
```bash
cd react-canvas-editor
```

### 3.2 Установите зависимости
```bash
npm install
```

### 3.3 Создайте .env.local
```env
REACT_APP_API_URL=https://pro-themes-ru-maxkhams-projects.vercel.app
REACT_APP_TELEGRAM_BOT_URL=https://t.me/your_bot_username
```

### 3.4 Разверните на Vercel
```bash
vercel --prod
```

## 🧪 Шаг 4: Тестирование

### 4.1 Тестируем API
```bash
python test_full_system.py --url "https://pro-themes-ru-maxkhams-projects.vercel.app"
```

### 4.2 Тестируем бота
1. Найдите вашего бота в Telegram
2. Отправьте `/start`
3. Проверьте все команды

### 4.3 Тестируем фронтенд
1. Откройте ваш веб-сайт
2. Проверьте подключение к API
3. Протестируйте конструктор

## 📊 Шаг 5: Мониторинг

### 5.1 Проверьте логи
- **Vercel**: Dashboard → Functions → Logs
- **Railway**: Project → Deployments → Logs
- **Render**: Service → Logs

### 5.2 Проверьте статус
- **API Health**: https://pro-themes-ru-maxkhams-projects.vercel.app/api/health
- **Main Page**: https://pro-themes-ru-maxkhams-projects.vercel.app/

## 🎯 Шаг 6: Финальная проверка

### ✅ Чек-лист:

- [ ] Backend API отвечает на `/api/health`
- [ ] Все API маршруты работают (templates, auth, sites)
- [ ] Telegram бот отвечает на `/start`
- [ ] Frontend загружается без ошибок
- [ ] Создание сайтов функционирует
- [ ] База данных подключена

## 🚀 Готово!

После выполнения всех шагов у вас будет:

1. **🖥️ Backend API** - https://pro-themes-ru-maxkhams-projects.vercel.app/
2. **🤖 Telegram Bot** - ваш бот в Telegram
3. **🌐 Frontend** - ваш веб-сайт
4. **📊 Мониторинг** - логи и статус

### 🎉 Поздравляем!

Ваша платформа ProThemesRU полностью развернута и готова к использованию!

**Теперь можете:**
- Привлекать пользователей
- Монетизировать платформу
- Развивать функциональность
- Масштабировать систему

## 📞 Поддержка

При возникновении проблем:
1. Проверьте логи деплоймента
2. Убедитесь в правильности переменных окружения
3. Проверьте подключение к API
4. Создайте issue в репозитории 