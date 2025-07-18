# React Canvas Editor

Профессиональный редактор канваса с поддержкой перетаскивания, изменения размера, выравнивания и распределения элементов.

## Новые возможности

### 🎯 Улучшенные взаимодействия с канвасом

#### Перетаскивание и изменение размера
- **Перетаскивание элементов**: Кликните и перетащите элемент для перемещения
- **Изменение размера**: 8 маркеров изменения размера вокруг выбранного элемента
- **Ограничения размера**: Минимальный размер 20x20px, максимальный 800x600px
- **Курсоры**: Динамическое изменение курсора в зависимости от действия

#### Множественное выделение
- **Ctrl/Cmd + клик**: Добавить/удалить элемент из выделения
- **Обычный клик**: Выделить только один элемент
- **Delete/Backspace**: Удалить выбранные элементы

### 🔧 Инструменты выравнивания и распределения

#### Выравнивание (требуется 2+ элемента)
- **По левому краю**: `fas fa-align-left`
- **По центру**: `fas fa-align-center`
- **По правому краю**: `fas fa-align-right`
- **По верхнему краю**: `fas fa-align-top`
- **По середине**: `fas fa-align-middle`
- **По нижнему краю**: `fas fa-align-bottom`

#### Распределение (требуется 3+ элемента)
- **По горизонтали**: `fas fa-arrows-alt-h`
- **По вертикали**: `fas fa-arrows-alt-v`

### 🎨 Улучшенный интерфейс

#### Панель свойств
- **Кнопки действий**: Отменить/Повторить, Сохранить, Очистить, Экспорт
- **Редактирование позиции**: Поля X, Y с валидацией
- **Редактирование размера**: Поля Ширина, Высота с валидацией
- **Специфичные свойства**: Для каждого типа элемента (текст, изображение, кнопка, фигура)

#### Стилизация
- **Ограничительная рамка**: Пунктирная рамка для выбранных элементов
- **Маркеры изменения размера**: 8 синих квадратиков с белой обводкой
- **Hover эффекты**: Подсветка при наведении
- **Адаптивный дизайн**: Поддержка мобильных устройств

## Технические детали

### Состояния Canvas
```javascript
const [isDragging, setIsDragging] = useState(false);
const [isResizing, setIsResizing] = useState(false);
const [dragStartCoords, setDragStartCoords] = useState({ x: 0, y: 0 });
const [initialElementState, setInitialElementState] = useState(null);
const [resizeHandle, setResizeHandle] = useState(null);
```

### Глобальные слушатели событий
- `mousemove` и `mouseup` прикреплены к `document`
- Корректная обработка перетаскивания даже при выходе курсора за пределы элемента
- Автоматическое снятие состояния при отпускании кнопки мыши

### Логика изменения размера
```javascript
const MIN_SIZE = 20;
const MAX_WIDTH = 800;
const MAX_HEIGHT = 600;
```

### Z-индекс
```javascript
const zIndex = elements.indexOf(el); // Соответствует порядку в панели слоев
```

## Использование

### Базовые операции
1. **Добавление элемента**: Перетащите из боковой панели на канвас
2. **Выделение**: Кликните по элементу
3. **Перетаскивание**: Кликните и перетащите выбранный элемент
4. **Изменение размера**: Перетащите любой из 8 маркеров
5. **Удаление**: Выделите элемент и нажмите Delete/Backspace

### Множественное выделение
1. **Добавить к выделению**: Ctrl/Cmd + клик по элементу
2. **Удалить из выделения**: Ctrl/Cmd + клик по выделенному элементу
3. **Выделить все**: Ctrl/Cmd + A (будущая функция)

### Выравнивание и распределение
1. **Выделите 2+ элемента** для выравнивания
2. **Выделите 3+ элемента** для распределения
3. **Используйте кнопки** в панели свойств

## Структура файлов

```
react-canvas-editor/
├── src/
│   ├── components/
│   │   ├── Canvas.js          # Основной компонент канваса
│   │   ├── PropertiesPanel.js # Панель свойств с инструментами
│   │   └── Editor.js          # Главный редактор
│   └── styles/
│       ├── Canvas.css         # Стили канваса и элементов
│       └── PropertiesPanel.css # Стили панели свойств
```

## Запуск

```bash
cd react-canvas-editor
npm install
npm start
```

Откройте http://localhost:3000 в браузере.

## Тестирование

### Проверьте следующие функции:
- [ ] Добавление элементов на канвас
- [ ] Выделение элементов (одиночное и множественное)
- [ ] Перетаскивание элементов
- [ ] Изменение размера через маркеры
- [ ] Выравнивание элементов (2+ элемента)
- [ ] Распределение элементов (3+ элемента)
- [ ] Удаление элементов (Delete/Backspace)
- [ ] Отмена/Повтор действий
- [ ] Сохранение и экспорт проекта

### Известные ограничения
- Максимальный размер элемента: 800x600px
- Минимальный размер элемента: 20x20px
- Распределение работает только с 3+ элементами
- Выравнивание работает только с 2+ элементами
