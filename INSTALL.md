# ProThemesRU - Инструкции по установке

## 📋 Содержание

1. [Системные требования](#системные-требования)
2. [Быстрая установка](#быстрая-установка)
3. [Установка вручную](#установка-вручную)
4. [Установка с Docker](#установка-с-docker)
5. [Установка на сервер](#установка-на-сервер)
6. [Настройка для продакшена](#настройка-для-продакшена)
7. [Устранение неполадок](#устранение-неполадок)

## 🖥 Системные требования

### Минимальные требования
- **ОС**: Linux, macOS, Windows 10+
- **Python**: 3.8 или выше
- **Node.js**: 16 или выше
- **RAM**: 4 GB
- **Диск**: 10 GB свободного места

### Рекомендуемые требования
- **ОС**: Ubuntu 20.04+, CentOS 8+, macOS 11+
- **Python**: 3.9 или выше
- **Node.js**: 18 или выше
- **RAM**: 8 GB
- **Диск**: 50 GB свободного места
- **Процессор**: 4 ядра

## ⚡ Быстрая установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/your-username/prothemesru.git
cd prothemesru
```

### 2. Автоматическая установка
```bash
chmod +x start.sh
./start.sh install
```

### 3. Настройка базы данных
```bash
./start.sh setup
```

### 4. Запуск приложения
```bash
./start.sh start
```

Приложение будет доступно по адресам:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## 🔧 Установка вручную

### Шаг 1: Подготовка системы

#### Ubuntu/Debian
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nodejs npm git
```

#### CentOS/RHEL
```bash
sudo yum update
sudo yum install python3 python3-pip nodejs npm git
```

#### macOS
```bash
# Установка Homebrew (если не установлен)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Установка зависимостей
brew install python3 node git
```

#### Windows
1. Скачайте и установите [Python 3.9+](https://www.python.org/downloads/)
2. Скачайте и установите [Node.js 16+](https://nodejs.org/)
3. Скачайте и установите [Git](https://git-scm.com/)

### Шаг 2: Клонирование и настройка

```bash
# Клонирование репозитория
git clone https://github.com/your-username/prothemesru.git
cd prothemesru

# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Установка Python зависимостей
pip install -r requirements.txt
```

### Шаг 3: Настройка переменных окружения

```bash
# Копирование примера конфигурации
cp env.example .env

# Редактирование конфигурации
nano .env
```

Основные настройки в `.env`:
```env
# Безопасность
SECRET_KEY=your-super-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this

# База данных
DATABASE_URL=sqlite:///prothemesru.db

# Пути к файлам
UPLOAD_FOLDER=uploads
MEDIA_FOLDER=media
SCRAPED_FOLDER=scraped_sites
```

### Шаг 4: Настройка базы данных

```bash
# Инициализация базы данных
python run.py --mode init
```

### Шаг 5: Настройка Frontend

```bash
# Переход в директорию frontend
cd react-canvas-editor

# Установка зависимостей
npm install

# Создание конфигурации
cp .env.example .env

# Редактирование конфигурации
nano .env
```

Настройки frontend в `.env`:
```env
REACT_APP_API_URL=http://localhost:5000/api
REACT_APP_BASE_URL=http://localhost:3000
```

### Шаг 6: Запуск приложения

```bash
# Запуск backend (в первом терминале)
cd /path/to/prothemesru
source venv/bin/activate
python run.py --mode dev

# Запуск frontend (во втором терминале)
cd /path/to/prothemesru/react-canvas-editor
npm start
```

## 🐳 Установка с Docker

### Предварительные требования
- Docker 20.10+
- Docker Compose 2.0+

### Быстрая установка с Docker

```bash
# Клонирование репозитория
git clone https://github.com/your-username/prothemesru.git
cd prothemesru

# Создание конфигурации
cp env.example .env
nano .env

# Запуск с Docker Compose
docker-compose up -d

# Проверка статуса
docker-compose ps
```

### Настройка для продакшена с Docker

```bash
# Создание продакшн конфигурации
cp docker-compose.yml docker-compose.prod.yml

# Редактирование конфигурации
nano docker-compose.prod.yml

# Запуск в продакшн режиме
docker-compose -f docker-compose.prod.yml up -d
```

## 🖥 Установка на сервер

### Подготовка сервера

#### Ubuntu 20.04 Server

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка необходимых пакетов
sudo apt install -y python3 python3-pip python3-venv nodejs npm git nginx postgresql postgresql-contrib redis-server

# Установка дополнительных инструментов
sudo apt install -y curl wget unzip software-properties-common apt-transport-https ca-certificates gnupg lsb-release
```

#### Настройка PostgreSQL

```bash
# Создание пользователя и базы данных
sudo -u postgres psql

CREATE USER prothemesru WITH PASSWORD 'your_password';
CREATE DATABASE prothemesru OWNER prothemesru;
GRANT ALL PRIVILEGES ON DATABASE prothemesru TO prothemesru;
\q
```

#### Настройка Redis

```bash
# Проверка статуса Redis
sudo systemctl status redis

# Включение автозапуска
sudo systemctl enable redis
```

### Установка приложения

```bash
# Создание пользователя для приложения
sudo useradd -m -s /bin/bash prothemesru
sudo usermod -aG sudo prothemesru

# Переключение на пользователя приложения
sudo su - prothemesru

# Клонирование репозитория
git clone https://github.com/your-username/prothemesru.git
cd prothemesru

# Настройка виртуального окружения
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настройка конфигурации
cp env.example .env
nano .env
```

### Настройка Nginx

```bash
# Создание конфигурации Nginx
sudo nano /etc/nginx/sites-available/prothemesru
```

Содержимое конфигурации:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Static files
    location /uploads {
        alias /home/prothemesru/prothemesru/uploads;
    }

    location /media {
        alias /home/prothemesru/prothemesru/media;
    }
}
```

```bash
# Активация конфигурации
sudo ln -s /etc/nginx/sites-available/prothemesru /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Настройка systemd сервисов

#### Backend сервис
```bash
sudo nano /etc/systemd/system/prothemesru-backend.service
```

Содержимое:
```ini
[Unit]
Description=ProThemesRU Backend
After=network.target

[Service]
Type=simple
User=prothemesru
WorkingDirectory=/home/prothemesru/prothemesru
Environment=PATH=/home/prothemesru/prothemesru/venv/bin
ExecStart=/home/prothemesru/prothemesru/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Frontend сервис
```bash
sudo nano /etc/systemd/system/prothemesru-frontend.service
```

Содержимое:
```ini
[Unit]
Description=ProThemesRU Frontend
After=network.target

[Service]
Type=simple
User=prothemesru
WorkingDirectory=/home/prothemesru/prothemesru/react-canvas-editor
ExecStart=/usr/bin/npm start
Restart=always
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

```bash
# Активация сервисов
sudo systemctl daemon-reload
sudo systemctl enable prothemesru-backend
sudo systemctl enable prothemesru-frontend
sudo systemctl start prothemesru-backend
sudo systemctl start prothemesru-frontend
```

## 🚀 Настройка для продакшена

### Безопасность

#### SSL сертификат с Let's Encrypt
```bash
# Установка Certbot
sudo apt install certbot python3-certbot-nginx

# Получение SSL сертификата
sudo certbot --nginx -d your-domain.com

# Автоматическое обновление
sudo crontab -e
# Добавить строку:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

#### Настройка файрвола
```bash
# Установка UFW
sudo apt install ufw

# Настройка правил
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### Мониторинг и логирование

#### Установка мониторинга
```bash
# Установка Prometheus и Grafana
sudo apt install prometheus grafana

# Настройка автозапуска
sudo systemctl enable prometheus
sudo systemctl enable grafana-server
```

#### Настройка логирования
```bash
# Создание директории для логов
sudo mkdir -p /var/log/prothemesru
sudo chown prothemesru:prothemesru /var/log/prothemesru

# Настройка logrotate
sudo nano /etc/logrotate.d/prothemesru
```

Содержимое:
```
/var/log/prothemesru/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 prothemesru prothemesru
}
```

### Резервное копирование

#### Автоматическое резервное копирование
```bash
# Создание скрипта резервного копирования
sudo nano /usr/local/bin/backup-prothemesru.sh
```

Содержимое:
```bash
#!/bin/bash
BACKUP_DIR="/backup/prothemesru"
DATE=$(date +%Y%m%d_%H%M%S)

# Создание директории для резервных копий
mkdir -p $BACKUP_DIR

# Резервное копирование базы данных
pg_dump prothemesru > $BACKUP_DIR/db_$DATE.sql

# Резервное копирование файлов
tar -czf $BACKUP_DIR/files_$DATE.tar.gz /home/prothemesru/prothemesru/uploads /home/prothemesru/prothemesru/media

# Удаление старых резервных копий (старше 30 дней)
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

```bash
# Сделать скрипт исполняемым
sudo chmod +x /usr/local/bin/backup-prothemesru.sh

# Добавить в cron (ежедневно в 2:00)
sudo crontab -e
# Добавить строку:
# 0 2 * * * /usr/local/bin/backup-prothemesru.sh
```

## 🔧 Устранение неполадок

### Частые проблемы

#### 1. Ошибка "Module not found"
```bash
# Активируйте виртуальное окружение
source venv/bin/activate

# Переустановите зависимости
pip install -r requirements.txt
```

#### 2. Ошибка "Port already in use"
```bash
# Найдите процесс, использующий порт
sudo lsof -i :5000
sudo lsof -i :3000

# Остановите процесс
sudo kill -9 <PID>
```

#### 3. Ошибка "Permission denied"
```bash
# Измените права доступа
sudo chown -R $USER:$USER /path/to/prothemesru
chmod +x start.sh
```

#### 4. Проблемы с базой данных
```bash
# Пересоздайте базу данных
rm -f prothemesru.db
python run.py --mode init
```

#### 5. Проблемы с Node.js зависимостями
```bash
# Очистите кэш npm
npm cache clean --force

# Удалите node_modules и переустановите
rm -rf node_modules package-lock.json
npm install
```

### Логи и отладка

#### Просмотр логов
```bash
# Backend логи
tail -f /var/log/prothemesru/backend.log

# Frontend логи
tail -f /var/log/prothemesru/frontend.log

# Nginx логи
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

#### Включение отладочного режима
```bash
# В файле .env
DEBUG=True
FLASK_DEBUG=True
```

### Получение помощи

Если у вас возникли проблемы:

1. Проверьте [FAQ](FAQ.md)
2. Просмотрите [документацию](docs/)
3. Создайте [issue](https://github.com/your-username/prothemesru/issues)
4. Обратитесь в [поддержку](mailto:support@prothemesru.com)

## 📞 Поддержка

- **Email**: support@prothemesru.com
- **Telegram**: @prothemesru_support
- **Документация**: [docs.prothemesru.com](https://docs.prothemesru.com)
- **GitHub Issues**: [github.com/your-username/prothemesru/issues](https://github.com/your-username/prothemesru/issues) 