# Руководство по участию в проекте ProThemesRU

Спасибо за интерес к участию в проекте ProThemesRU! Мы приветствуем вклад от всех участников сообщества.

## 📋 Содержание

1. [Как начать](#как-начать)
2. [Структура проекта](#структура-проекта)
3. [Процесс разработки](#процесс-разработки)
4. [Стиль кода](#стиль-кода)
5. [Тестирование](#тестирование)
6. [Документация](#документация)
7. [Отправка изменений](#отправка-изменений)
8. [Сообщения о багах](#сообщения-о-багах)
9. [Предложения функций](#предложения-функций)
10. [Код поведения](#код-поведения)

## 🚀 Как начать

### Предварительные требования

- Python 3.8+
- Node.js 16+
- Git
- Знание React (для frontend)
- Знание Flask (для backend)

### Настройка окружения

1. **Форкните репозиторий**
   ```bash
   # Перейдите на GitHub и нажмите "Fork"
   # Затем клонируйте ваш форк
   git clone https://github.com/YOUR_USERNAME/prothemesru.git
   cd prothemesru
   ```

2. **Настройте upstream**
   ```bash
   git remote add upstream https://github.com/original-owner/prothemesru.git
   ```

3. **Установите зависимости**
   ```bash
   # Backend
   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или venv\Scripts\activate  # Windows
   pip install -r requirements.txt

   # Frontend
   cd react-canvas-editor
   npm install
   cd ..
   ```

4. **Настройте базу данных**
   ```bash
   python run.py --mode init
   ```

## 📁 Структура проекта

```
prothemesru/
├── app.py                 # Основной Flask файл
├── requirements.txt       # Python зависимости
├── react-canvas-editor/   # React frontend
│   ├── src/
│   │   ├── components/    # React компоненты
│   │   ├── pages/         # Страницы приложения
│   │   ├── utils/         # Утилиты
│   │   └── App.js         # Главный компонент
│   ├── public/            # Статические файлы
│   └── package.json       # Node.js зависимости
├── tests/                 # Тесты
├── docs/                  # Документация
├── uploads/               # Загруженные файлы
├── media/                 # Медиа-файлы
└── scraped_sites/         # Скрапленные сайты
```

## 🔄 Процесс разработки

### 1. Выбор задачи

- Просмотрите [Issues](https://github.com/your-username/prothemesru/issues)
- Выберите задачу с меткой "good first issue" для новичков
- Оставьте комментарий, что беретесь за задачу

### 2. Создание ветки

```bash
# Обновите main ветку
git checkout main
git pull upstream main

# Создайте новую ветку
git checkout -b feature/your-feature-name
# или
git checkout -b fix/your-bug-fix
```

### 3. Разработка

- Пишите код согласно [стилю кода](#стиль-кода)
- Добавляйте тесты для новых функций
- Обновляйте документацию при необходимости

### 4. Коммиты

```bash
# Добавьте изменения
git add .

# Создайте коммит с описательным сообщением
git commit -m "feat: add new feature for user management

- Add user roles and permissions
- Implement admin panel
- Add user activity tracking

Closes #123"
```

### 5. Push и Pull Request

```bash
# Отправьте ветку
git push origin feature/your-feature-name

# Создайте Pull Request на GitHub
```

## 📝 Стиль кода

### Python (Backend)

#### PEP 8
- Максимальная длина строки: 79 символов
- Отступы: 4 пробела
- Импорты: стандартная библиотека, сторонние, локальные

#### Пример кода
```python
def create_user(username: str, email: str, role: str = 'user') -> User:
    """
    Create a new user with the given credentials.
    
    Args:
        username: The username for the new user
        email: The email address for the new user
        role: The role for the new user (default: 'user')
    
    Returns:
        User: The created user object
    
    Raises:
        ValueError: If username or email already exists
    """
    if User.query.filter_by(username=username).first():
        raise ValueError(f"Username '{username}' already exists")
    
    if User.query.filter_by(email=email).first():
        raise ValueError(f"Email '{email}' already exists")
    
    user = User(
        username=username,
        email=email,
        role=role,
        password_hash=generate_password_hash(password)
    )
    
    db.session.add(user)
    db.session.commit()
    
    return user
```

### JavaScript/React (Frontend)

#### ESLint + Prettier
- Используйте функциональные компоненты с хуками
- Именуйте компоненты в PascalCase
- Используйте camelCase для переменных и функций

#### Пример кода
```javascript
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { Box, Typography, Button } from '@mui/material';

/**
 * UserProfile component displays user information and actions
 * @param {Object} props - Component props
 * @param {string} props.userId - User ID
 * @param {Function} props.onEdit - Edit callback function
 * @returns {JSX.Element} UserProfile component
 */
const UserProfile = ({ userId, onEdit }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await fetch(`/api/users/${userId}`);
        const userData = await response.json();
        setUser(userData);
      } catch (error) {
        console.error('Error fetching user:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [userId]);

  if (loading) {
    return <Typography>Loading...</Typography>;
  }

  if (!user) {
    return <Typography>User not found</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4">{user.name}</Typography>
      <Typography variant="body1">{user.email}</Typography>
      <Button onClick={() => onEdit(user)}>Edit Profile</Button>
    </Box>
  );
};

UserProfile.propTypes = {
  userId: PropTypes.string.isRequired,
  onEdit: PropTypes.func.isRequired,
};

export default UserProfile;
```

### Сообщения коммитов

Используйте [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Типы:
- `feat`: новая функция
- `fix`: исправление бага
- `docs`: изменения в документации
- `style`: форматирование, отсутствующие точки с запятой и т.д.
- `refactor`: рефакторинг кода
- `test`: добавление или исправление тестов
- `chore`: изменения в процессе сборки или вспомогательных инструментах

Примеры:
```
feat(auth): add JWT token refresh functionality

fix(editor): resolve canvas rendering issue on mobile devices

docs(api): update authentication endpoint documentation

test(media): add unit tests for file upload functionality
```

## 🧪 Тестирование

### Backend тесты

```bash
# Запуск всех тестов
python -m pytest tests/

# Запуск с покрытием
python -m pytest tests/ --cov=app --cov-report=html

# Запуск конкретного теста
python -m pytest tests/test_auth.py::test_login
```

### Frontend тесты

```bash
cd react-canvas-editor

# Запуск тестов
npm test

# Запуск с покрытием
npm test -- --coverage

# Запуск в watch режиме
npm test -- --watch
```

### E2E тесты

```bash
# Установка Playwright
npm install -D @playwright/test

# Запуск E2E тестов
npx playwright test
```

### Написание тестов

#### Backend (Python)
```python
import unittest
from app import app, db, User

class UserTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
    
    def test_create_user(self):
        response = self.app.post('/api/auth/register', 
                               json={'username': 'test', 'email': 'test@test.com'})
        self.assertEqual(response.status_code, 201)
    
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
```

#### Frontend (React)
```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import UserProfile from './UserProfile';

describe('UserProfile', () => {
  it('renders user information correctly', () => {
    const mockUser = {
      id: '1',
      name: 'John Doe',
      email: 'john@example.com'
    };
    
    render(<UserProfile user={mockUser} />);
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
  });
  
  it('calls onEdit when edit button is clicked', () => {
    const mockOnEdit = jest.fn();
    const mockUser = { id: '1', name: 'John Doe' };
    
    render(<UserProfile user={mockUser} onEdit={mockOnEdit} />);
    
    fireEvent.click(screen.getByText('Edit'));
    expect(mockOnEdit).toHaveBeenCalledWith(mockUser);
  });
});
```

## 📚 Документация

### Обновление документации

При добавлении новых функций обновляйте:

1. **README.md** - основные изменения
2. **API документация** - новые эндпоинты
3. **Комментарии в коде** - docstrings для функций
4. **Примеры использования** - демонстрация функций

### Стиль документации

- Используйте Markdown
- Добавляйте примеры кода
- Обновляйте скриншоты при изменении UI
- Проверяйте ссылки

## 🔄 Отправка изменений

### 1. Подготовка Pull Request

```bash
# Убедитесь, что все тесты проходят
python -m pytest tests/
cd react-canvas-editor && npm test && cd ..

# Проверьте стиль кода
python -m flake8 app/
cd react-canvas-editor && npm run lint && cd ..

# Обновите документацию
```

### 2. Создание Pull Request

1. Перейдите на GitHub
2. Нажмите "New Pull Request"
3. Выберите вашу ветку
4. Заполните шаблон PR:

```markdown
## Описание
Краткое описание изменений

## Тип изменений
- [ ] Bug fix (не ломает существующую функциональность)
- [ ] New feature (добавляет функциональность)
- [ ] Breaking change (ломает существующую функциональность)
- [ ] Documentation update

## Тестирование
- [ ] Добавлены/обновлены unit тесты
- [ ] Добавлены/обновлены integration тесты
- [ ] Протестировано вручную

## Чек-лист
- [ ] Код соответствует стилю проекта
- [ ] Добавлены комментарии к коду
- [ ] Обновлена документация
- [ ] Все тесты проходят
- [ ] Проверено на разных браузерах/устройствах

## Скриншоты (если применимо)
Добавьте скриншоты для UI изменений

## Дополнительная информация
Любая дополнительная информация
```

### 3. Code Review

- Отвечайте на комментарии ревьюера
- Вносите необходимые изменения
- Обновляйте PR при необходимости

## 🐛 Сообщения о багах

### Создание Issue

Используйте шаблон для багов:

```markdown
## Описание бага
Четкое и краткое описание бага

## Шаги для воспроизведения
1. Перейдите к '...'
2. Нажмите на '...'
3. Прокрутите вниз до '...'
4. Увидите ошибку

## Ожидаемое поведение
Что должно происходить

## Фактическое поведение
Что происходит на самом деле

## Скриншоты
Если применимо, добавьте скриншоты

## Окружение
- ОС: [например, Windows 10]
- Браузер: [например, Chrome 91]
- Версия: [например, 2.0.0]

## Дополнительная информация
Любая дополнительная информация
```

### Отладка

```bash
# Включение отладочного режима
export FLASK_DEBUG=1
python app.py

# Логирование
tail -f logs/app.log
```

## 💡 Предложения функций

### Создание Feature Request

```markdown
## Описание функции
Четкое и краткое описание желаемой функции

## Проблема
Описание проблемы, которую решает эта функция

## Предлагаемое решение
Описание предлагаемого решения

## Альтернативы
Рассмотренные альтернативные решения

## Дополнительная информация
Любая дополнительная информация
```

### Обсуждение

- Участвуйте в обсуждениях
- Предлагайте альтернативные решения
- Помогайте с реализацией

## 🤝 Код поведения

### Наши стандарты

Мы стремимся создать дружелюбную и инклюзивную среду:

- Используйте уважительный и инклюзивный язык
- Уважайте различные точки зрения и опыт
- Грациозно принимайте конструктивную критику
- Фокусируйтесь на том, что лучше для сообщества
- Проявляйте эмпатию к другим участникам

### Неприемлемое поведение

- Использование сексуализированного языка или образов
- Троллинг, оскорбительные/уничижительные комментарии
- Публичные или частные домогательства
- Публикация личной информации других участников
- Другое поведение, которое может быть сочтено неуместным

### Применение

Сообщения о неприемлемом поведении отправляйте на:
- Email: conduct@prothemesru.com
- GitHub: создайте private issue

## 🏆 Признание вклада

### Способы участия

- **Код**: исправления багов, новые функции
- **Документация**: улучшение README, API docs
- **Тестирование**: написание тестов, тестирование
- **Дизайн**: UI/UX улучшения, иконки
- **Переводы**: локализация интерфейса
- **Поддержка**: помощь другим участникам

### Признание

- Ваше имя будет добавлено в [CONTRIBUTORS.md](CONTRIBUTORS.md)
- Вы получите роль "Contributor" в GitHub
- Ваши PR будут отмечены в релизах

## 📞 Получение помощи

### Ресурсы

- [Документация](https://docs.prothemesru.com)
- [Issues](https://github.com/your-username/prothemesru/issues)
- [Discussions](https://github.com/your-username/prothemesru/discussions)
- [Wiki](https://github.com/your-username/prothemesru/wiki)

### Контакты

- **Email**: contributors@prothemesru.com
- **Telegram**: @prothemesru_contributors
- **Discord**: [Сервер сообщества](https://discord.gg/prothemesru)

## 🎯 Первые шаги

### Для новичков

1. **Познакомьтесь с проектом**
   - Прочитайте README.md
   - Изучите структуру кода
   - Запустите проект локально

2. **Выберите задачу**
   - Ищите метку "good first issue"
   - Начните с документации или тестов
   - Не стесняйтесь задавать вопросы

3. **Присоединяйтесь к сообществу**
   - Представьтесь в Discussions
   - Участвуйте в обсуждениях
   - Помогайте другим участникам

### Для опытных разработчиков

1. **Изучите архитектуру**
   - Поняйте структуру проекта
   - Изучите API дизайн
   - Познакомьтесь с процессами

2. **Выберите область**
   - Backend/Frontend/DevOps
   - Конкретные функции
   - Производительность/Безопасность

3. **Предложите улучшения**
   - Архитектурные изменения
   - Новые функции
   - Оптимизации

---

Спасибо за ваш вклад в ProThemesRU! 🚀

Вместе мы создаем лучшую платформу для создания сайтов. 