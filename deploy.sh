#!/bin/bash

# Скрипт для развертывания ProThemesRU
# Использование: ./deploy.sh [production|staging|development]

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Функции для логирования
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка аргументов
ENVIRONMENT=${1:-development}

if [[ ! "$ENVIRONMENT" =~ ^(production|staging|development)$ ]]; then
    log_error "Неверное окружение. Используйте: production, staging или development"
    exit 1
fi

log_info "Начинаем развертывание в окружении: $ENVIRONMENT"

# Создание необходимых директорий
log_info "Создание директорий..."
mkdir -p logs uploads static ssl

# Проверка наличия .env файла
if [ ! -f .env ]; then
    log_warning "Файл .env не найден. Создаем шаблон..."
    cp config/config_template.py config/config.py
    log_warning "Пожалуйста, настройте config/config.py перед продолжением"
    exit 1
fi

# Загрузка переменных окружения
log_info "Загрузка переменных окружения..."
source .env

# Проверка зависимостей
log_info "Проверка зависимостей..."

# Проверка Docker
if ! command -v docker &> /dev/null; then
    log_error "Docker не установлен"
    exit 1
fi

# Проверка Docker Compose
if ! command -v docker-compose &> /dev/null; then
    log_error "Docker Compose не установлен"
    exit 1
fi

# Остановка существующих контейнеров
log_info "Остановка существующих контейнеров..."
docker-compose down --remove-orphans

# Очистка неиспользуемых образов
log_info "Очистка неиспользуемых образов..."
docker image prune -f

# Сборка образов
log_info "Сборка Docker образов..."
docker-compose build --no-cache

# Создание SSL сертификатов для разработки
if [ "$ENVIRONMENT" = "development" ]; then
    log_info "Создание самоподписанных SSL сертификатов..."
    if [ ! -f ssl/cert.pem ] || [ ! -f ssl/key.pem ]; then
        openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
            -keyout ssl/key.pem \
            -out ssl/cert.pem \
            -subj "/C=RU/ST=Moscow/L=Moscow/O=ProThemesRU/CN=localhost"
    fi
fi

# Запуск сервисов
log_info "Запуск сервисов..."
docker-compose up -d

# Ожидание готовности базы данных
log_info "Ожидание готовности базы данных..."
sleep 10

# Проверка подключения к базе данных
log_info "Проверка подключения к базе данных..."
docker-compose exec -T backend python -c "
import psycopg2
import os
import sys

try:
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    conn.close()
    print('База данных готова')
except Exception as e:
    print(f'Ошибка подключения к БД: {e}')
    sys.exit(1)
"

# Применение миграций
log_info "Применение миграций базы данных..."
docker-compose exec -T backend flask db upgrade

# Создание администратора (если не существует)
log_info "Создание администратора..."
docker-compose exec -T backend python -c "
from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()
with app.app_context():
    admin = User.query.filter_by(email='admin@prothemes.ru').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@prothemes.ru',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print('Администратор создан: admin@prothemes.ru / admin123')
    else:
        print('Администратор уже существует')
"

# Проверка статуса сервисов
log_info "Проверка статуса сервисов..."
docker-compose ps

# Проверка доступности приложения
log_info "Проверка доступности приложения..."
sleep 5

if curl -f -s http://localhost/health > /dev/null; then
    log_success "Приложение доступно по адресу: http://localhost"
else
    log_warning "Приложение может быть недоступно. Проверьте логи:"
    docker-compose logs backend
fi

# Настройка мониторинга
if [ "$ENVIRONMENT" = "production" ]; then
    log_info "Настройка мониторинга..."
    
    # Проверка доступности Grafana
    if curl -f -s http://localhost:3000 > /dev/null; then
        log_success "Grafana доступна по адресу: http://localhost:3000"
        log_info "Логин: admin, Пароль: admin"
    fi
    
    # Проверка доступности Prometheus
    if curl -f -s http://localhost:9090 > /dev/null; then
        log_success "Prometheus доступен по адресу: http://localhost:9090"
    fi
fi

# Создание резервной копии
log_info "Создание резервной копии базы данных..."
BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
docker-compose exec -T db pg_dump -U prothemesru prothemesru > "backups/$BACKUP_FILE"
log_success "Резервная копия создана: backups/$BACKUP_FILE"

# Финальная информация
log_success "Развертывание завершено успешно!"
echo ""
echo "=== Информация о развертывании ==="
echo "Окружение: $ENVIRONMENT"
echo "Приложение: http://localhost"
echo "API: http://localhost/api"
echo "Документация API: http://localhost/api/docs"
echo ""

if [ "$ENVIRONMENT" = "production" ]; then
    echo "=== Мониторинг ==="
    echo "Grafana: http://localhost:3000"
    echo "Prometheus: http://localhost:9090"
    echo ""
fi

echo "=== Полезные команды ==="
echo "Просмотр логов: docker-compose logs -f"
echo "Остановка: docker-compose down"
echo "Перезапуск: docker-compose restart"
echo "Обновление: ./deploy.sh $ENVIRONMENT"
echo ""

# Проверка безопасности
log_info "Проверка безопасности..."
if [ "$ENVIRONMENT" = "production" ]; then
    # Проверка открытых портов
    log_info "Проверка открытых портов..."
    netstat -tlnp | grep -E ':(80|443|5000|5432|6379)' || true
    
    # Проверка SSL сертификатов
    if [ -f ssl/cert.pem ]; then
        log_info "Проверка SSL сертификата..."
        openssl x509 -in ssl/cert.pem -text -noout | grep -E "(Subject:|Not After:)"
    fi
fi

log_success "Развертывание ProThemesRU завершено!" 