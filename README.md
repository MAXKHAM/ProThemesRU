# ProThemesRU - Платформа для создания сайтов

Современная платформа для создания профессиональных веб-сайтов с использованием готовых шаблонов и визуального редактора.

## 📚 Репозитории проекта

Проект разделен на несколько репозиториев для лучшей организации:

- **Основной репозиторий** - [ProThemesRU](https://github.com/MAXKHAM/ProThemesRU) (текущий)
  - Flask backend
  - React frontend
  - Шаблоны сайтов
  - Конструктор сайтов

- **Telegram Bot** - [ProThemesRUBot](https://github.com/MAXKHAM/ProThemesRUBot)
  - Уведомления пользователей
  - Поддержка клиентов
  - Интеграция с основной платформой

## 🚀 Возможности

### Для пользователей
- **Визуальный редактор сайтов** - создавайте сайты без знания программирования
- **Готовые шаблоны** - более 50 профессиональных шаблонов для разных ниш
- **Адаптивный дизайн** - все сайты автоматически адаптируются под мобильные устройства
- **SEO-оптимизация** - встроенные инструменты для продвижения
- **Хостинг и домены** - полный спектр услуг для запуска сайта
- **Техническая поддержка** - помощь на всех этапах создания

### Для администраторов
- **Панель управления** - полный контроль над платформой
- **Управление пользователями** - модерация и поддержка клиентов
- **Аналитика** - детальная статистика использования
- **Управление шаблонами** - добавление и редактирование шаблонов
- **Система заказов** - обработка платежей и заказов

## 🛠 Технологии

### Frontend
- **React 18** - современный UI фреймворк
- **TypeScript** - типизированный JavaScript
- **Tailwind CSS** - утилитарный CSS фреймворк
- **Framer Motion** - анимации и переходы
- **React Router** - навигация
- **React Icons** - иконки

### Backend
- **Flask** - веб-фреймворк Python
- **SQLAlchemy** - ORM для работы с базой данных
- **JWT** - аутентификация
- **Flask-CORS** - кросс-доменные запросы
- **BeautifulSoup** - парсинг веб-страниц

### База данных
- **SQLite** - для разработки
- **PostgreSQL** - для продакшена

### Дополнительные сервисы
- **Telegram Bot** - уведомления и поддержка ([отдельный репозиторий](https://github.com/MAXKHAM/ProThemesRUBot))
- **Payment Gateway** - обработка платежей
- **File Storage** - хранение файлов

## 📦 Установка и запуск

### Предварительные требования

- Python 3.11+
- Node.js 18+
- npm или yarn
- Git

### 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/ProThemesRU.git
cd ProThemesRU
```

### 2. Настройка бэкенда

```bash
# Создание виртуального окружения
python -m venv venv

# Активация виртуального окружения
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp config/config_template.py config/config.py
# Отредактируйте config.py с вашими настройками

# Инициализация базы данных
flask db init
flask db migrate
flask db upgrade

# Запуск бэкенда
python app.py
```

### 3. Настройка фронтенда

```bash
# Переход в папку фронтенда
cd frontend

# Установка зависимостей
npm install

# Запуск в режиме разработки
npm start
```

### 4. Настройка Telegram бота (опционально)

Telegram бот находится в отдельном репозитории: [ProThemesRUBot](https://github.com/MAXKHAM/ProThemesRUBot)

```bash
# Клонирование репозитория бота
git clone https://github.com/MAXKHAM/ProThemesRUBot.git
cd ProThemesRUBot

# Установка зависимостей
pip install -r requirements.txt

# Настройка переменных окружения
cp .env.example .env
# Отредактируйте .env с вашими настройками

# Запуск бота
python run_bot.py
```

## 🔧 Конфигурация

### Переменные окружения

Создайте файл `.env` в корневой папке:

```env
# Основные настройки
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///prothemesru.db
JWT_SECRET_KEY=your-jwt-secret-key

# Telegram Bot
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_ADMIN_ID=your-admin-id

# Платежи
PAYMENT_API_KEY=your-payment-api-key
PAYMENT_SECRET=your-payment-secret

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-email-password

# Файловое хранилище
UPLOAD_FOLDER=uploads
MAX_FILE_SIZE=16777216
```

### Настройка базы данных

Для продакшена рекомендуется использовать PostgreSQL:

```python
# config/config.py
DATABASE_URL = 'postgresql://username:password@localhost/prothemesru'
```

## 📁 Структура проекта

```
ProThemesRU/
├── app/                    # Основное Flask приложение
│   ├── api/               # API endpoints
│   ├── auth/              # Аутентификация
│   ├── constructor/       # Конструктор сайтов
│   ├── main/              # Основные маршруты
│   ├── orders/            # Управление заказами
│   ├── payment/           # Платежи
│   ├── services/          # Бизнес-логика
│   ├── static/            # Статические файлы
│   ├── templates/         # HTML шаблоны
│   └── utils/             # Утилиты
├── frontend/              # React приложение
│   ├── public/            # Публичные файлы
│   ├── src/               # Исходный код
│   │   ├── components/    # React компоненты
│   │   ├── contexts/      # React контексты
│   │   ├── hooks/         # Кастомные хуки
│   │   ├── pages/         # Страницы
│   │   ├── styles/        # Стили
│   │   ├── types/         # TypeScript типы
│   │   └── utils/         # Утилиты
│   └── package.json
├── templates/             # HTML шаблоны сайтов
├── site_blocks/           # Блоки для конструктора
├── static/                # Статические файлы
├── migrations/            # Миграции базы данных
├── tests/                 # Тесты
├── docs/                  # Документация
└── README.md
```

## 🚀 Развертывание

### Локальная разработка

1. Запустите бэкенд: `python app.py`
2. Запустите фронтенд: `cd frontend && npm start`
3. Откройте http://localhost:3000

### Продакшен

#### Docker (рекомендуется)

```bash
# Сборка образов
docker-compose build

# Запуск
docker-compose up -d
```

#### Ручное развертывание

1. **Настройка сервера**
   ```bash
   # Установка зависимостей
   sudo apt update
   sudo apt install python3 python3-pip nginx postgresql
   
   # Настройка PostgreSQL
   sudo -u postgres createdb prothemesru
   sudo -u postgres createuser prothemesru
   ```

2. **Настройка Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
       
       location /static {
           alias /path/to/ProThemesRU/static;
       }
   }
   ```

3. **Настройка systemd**
   ```ini
   [Unit]
   Description=ProThemesRU
   After=network.target
   
   [Service]
   User=www-data
   WorkingDirectory=/path/to/ProThemesRU
   Environment=PATH=/path/to/ProThemesRU/venv/bin
   ExecStart=/path/to/ProThemesRU/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
   
   [Install]
   WantedBy=multi-user.target
   ```

## 🧪 Тестирование

```bash
# Запуск тестов бэкенда
python -m pytest tests/

# Запуск тестов фронтенда
cd frontend
npm test

# Запуск линтера
npm run lint
```

## 📚 API Документация

### Аутентификация

```bash
# Регистрация
POST /api/auth/register
{
  "name": "Имя пользователя",
  "email": "user@example.com",
  "password": "password123"
}

# Вход
POST /api/auth/login
{
  "email": "user@example.com",
  "password": "password123"
}
```

### Проекты

```bash
# Получение проектов пользователя
GET /api/projects
Authorization: Bearer <token>

# Создание проекта
POST /api/projects
{
  "name": "Мой сайт",
  "description": "Описание проекта"
}

# Обновление проекта
PUT /api/projects/<id>
{
  "elements": [...],
  "settings": {...}
}
```

### Шаблоны

```bash
# Получение шаблонов
GET /api/templates?category=business

# Получение конкретного шаблона
GET /api/templates/<id>
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции: `git checkout -b feature/amazing-feature`
3. Зафиксируйте изменения: `git commit -m 'Add amazing feature'`
4. Отправьте в ветку: `git push origin feature/amazing-feature`
5. Откройте Pull Request

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

## 📞 Поддержка

- **Email**: support@prothemes.ru
- **Telegram**: @prothemesru_support
- **Документация**: [docs.prothemes.ru](https://docs.prothemes.ru)

## 🙏 Благодарности

- [React](https://reactjs.org/) - за отличный UI фреймворк
- [Flask](https://flask.palletsprojects.com/) - за простой и мощный веб-фреймворк
- [Tailwind CSS](https://tailwindcss.com/) - за утилитарный CSS фреймворк
- [Framer Motion](https://www.framer.com/motion/) - за потрясающие анимации

---

**ProThemesRU** - Создавайте профессиональные сайты легко и быстро! 🚀
