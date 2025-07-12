# 🚀 Инструкции по деплою ProThemesRU

## Варианты деплоя

### 1. GitHub Pages (Frontend)

Проект автоматически деплоится на GitHub Pages при пуше в ветку `master`.

**URL**: https://maxkham.github.io/ProThemesRU/

### 2. Render.com (Full Stack)

#### Настройка на Render:

1. **Создайте аккаунт** на [Render.com](https://render.com)

2. **Подключите GitHub репозиторий**:
   - Нажмите "New +"
   - Выберите "Web Service"
   - Подключите репозиторий `ProThemesRU`

3. **Настройте переменные окружения**:
   ```
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://username:password@host:port/database
   JWT_SECRET_KEY=your-jwt-secret-key
   FLASK_ENV=production
   ```

4. **Настройки деплоя**:
   - **Build Command**: `pip install -r requirements.txt && cd frontend && npm install && npm run build`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

### 3. Railway.app

1. **Подключите репозиторий** на [Railway.app](https://railway.app)
2. **Добавьте PostgreSQL** базу данных
3. **Настройте переменные окружения**
4. **Деплой произойдет автоматически**

### 4. Heroku

1. **Установите Heroku CLI**
2. **Создайте приложение**:
   ```bash
   heroku create your-app-name
   ```

3. **Добавьте PostgreSQL**:
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Настройте переменные окружения**:
   ```bash
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set JWT_SECRET_KEY=your-jwt-secret
   ```

5. **Деплой**:
   ```bash
   git push heroku master
   ```

### 5. VPS/Сервер

#### Требования:
- Ubuntu 20.04+
- Python 3.11+
- Node.js 18+
- PostgreSQL 13+
- Nginx

#### Установка:

1. **Клонируйте репозиторий**:
   ```bash
   git clone https://github.com/MAXKHAM/ProThemesRU.git
   cd ProThemesRU
   ```

2. **Установите зависимости**:
   ```bash
   # Python
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Node.js
   cd frontend
   npm install
   npm run build
   cd ..
   ```

3. **Настройте базу данных**:
   ```bash
   sudo -u postgres createdb prothemesru
   sudo -u postgres createuser prothemesru
   sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE prothemesru TO prothemesru;"
   ```

4. **Настройте Nginx**:
   ```bash
   sudo cp nginx.conf /etc/nginx/sites-available/prothemesru
   sudo ln -s /etc/nginx/sites-available/prothemesru /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

5. **Настройте systemd**:
   ```bash
   sudo cp start.sh /etc/systemd/system/prothemesru.service
   sudo systemctl enable prothemesru
   sudo systemctl start prothemesru
   ```

## Переменные окружения

Создайте файл `.env` в корне проекта:

```env
# Основные настройки
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost/prothemesru
JWT_SECRET_KEY=your-jwt-secret-key
FLASK_ENV=production

# Платежи (опционально)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...

# Email (опционально)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-email-password

# Файловое хранилище
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=16777216
```

## Мониторинг

### Prometheus + Grafana

1. **Установите Prometheus**:
   ```bash
   docker run -d -p 9090:9090 -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
   ```

2. **Установите Grafana**:
   ```bash
   docker run -d -p 3000:3000 grafana/grafana
   ```

3. **Настройте дашборды** для мониторинга:
   - CPU и память
   - Запросы к API
   - Ошибки
   - Время ответа

## SSL/HTTPS

### Let's Encrypt (бесплатно):

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Автоматическое обновление:

```bash
sudo crontab -e
# Добавьте строку:
0 12 * * * /usr/bin/certbot renew --quiet
```

## Резервное копирование

### База данных:

```bash
# Создание бэкапа
pg_dump prothemesru > backup_$(date +%Y%m%d_%H%M%S).sql

# Восстановление
psql prothemesru < backup_file.sql
```

### Файлы:

```bash
# Создание архива
tar -czf uploads_backup_$(date +%Y%m%d_%H%M%S).tar.gz uploads/

# Восстановление
tar -xzf uploads_backup_file.tar.gz
```

## Troubleshooting

### Частые проблемы:

1. **Ошибка подключения к БД**:
   - Проверьте `DATABASE_URL`
   - Убедитесь, что PostgreSQL запущен

2. **Ошибки CORS**:
   - Проверьте настройки `CORS` в `app.py`
   - Убедитесь, что домены указаны правильно

3. **Проблемы с загрузкой файлов**:
   - Проверьте права доступа к папке `uploads`
   - Убедитесь, что `MAX_FILE_SIZE` достаточен

4. **Ошибки JWT**:
   - Проверьте `JWT_SECRET_KEY`
   - Убедитесь, что токены не истекли

### Логи:

```bash
# Просмотр логов приложения
sudo journalctl -u prothemesru -f

# Просмотр логов Nginx
sudo tail -f /var/log/nginx/error.log
```

## Поддержка

При возникновении проблем:

1. Проверьте логи приложения
2. Убедитесь, что все переменные окружения настроены
3. Проверьте подключение к базе данных
4. Обратитесь к документации Flask и React

**GitHub Issues**: https://github.com/MAXKHAM/ProThemesRU/issues 