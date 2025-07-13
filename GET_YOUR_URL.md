# 🔗 Получение вашего реального URL

## 📍 Текущий статус

Ваш API работает и возвращает:
```json
{
  "message": "ProThemesRU - Рабочая версия",
  "status": "success", 
  "version": "1.0.0"
}
```

## 🎯 Что нужно сделать

### 1. Получите ваш реальный URL

**Если вы развернули на Vercel:**
1. Перейдите на [vercel.com/dashboard](https://vercel.com/dashboard)
2. Найдите ваш проект ProThemesRU
3. Скопируйте URL (например: `https://prothemesru-abc123.vercel.app`)

**Если вы развернули на Railway:**
1. Перейдите на [railway.app/dashboard](https://railway.app/dashboard)
2. Найдите ваш проект
3. Скопируйте URL из вкладки "Deployments"

**Если вы развернули на Render:**
1. Перейдите на [render.com/dashboard](https://render.com/dashboard)
2. Найдите ваш сервис
3. Скопируйте URL

### 2. Обновите все файлы

Замените `https://your-vercel-url.vercel.app` на ваш реальный URL во всех файлах:

#### В `telegram_bot/config.py`:
```python
API_BASE_URL = "https://your-real-url.com"
```

#### В `telegram_bot/bot.py`:
```python
API_BASE_URL = os.environ.get('API_BASE_URL', 'https://your-real-url.com')
```

#### В `test_api.py`:
```python
BASE_URL = "https://your-real-url.com"
```

#### В `test_full_system.py`:
```bash
python test_full_system.py --url "https://your-real-url.com"
```

### 3. Протестируйте систему

После обновления URL запустите тест:

```bash
python test_full_system.py --url "https://your-real-url.com"
```

### 4. Разверните Telegram бота

1. Перейдите в папку `telegram_bot`
2. Обновите `API_BASE_URL` в переменных окружения
3. Разверните на Railway/Render

## 🚀 Быстрый старт

1. **Скопируйте ваш URL**
2. **Выполните команду:**
```bash
python update_urls.py "https://your-real-url.com"
```
3. **Протестируйте:**
```bash
python test_full_system.py --url "https://your-real-url.com"
```

## 📞 Поддержка

Если у вас возникли проблемы:
1. Проверьте, что сервер запущен
2. Убедитесь в правильности URL
3. Проверьте логи деплоймента
4. Создайте issue с описанием проблемы

## 🎉 Готово!

После обновления URL ваша система будет полностью функциональной! 