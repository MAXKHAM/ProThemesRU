import React, { useCallback, useState } from 'react';
import '../styles/LayersPanel.css'; // Создадим этот CSS файл

function LayersPanel({ elements, selectedElementId, setSelectedElementId, updateElement, updateElementProps, onMoveLayer }) {
  const [editingId, setEditingId] = useState(null); // Состояние для отслеживания редактируемого имени
  const [draggedItem, setDraggedItem] = useState(null); // Отслеживание перетаскиваемого элемента

  const handleSelect = useCallback((id) => {
    setSelectedElementId(id);
  }, [setSelectedElementId]);

  const handleNameChange = useCallback((e, id) => {
    // Обновляем свойство 'name' элемента, если оно есть.
    // Если нет, создаем его.
    updateElementProps(id, { name: e.target.value });
  }, [updateElementProps]);

  const handleDoubleClick = useCallback((id) => {
    setEditingId(id);
  }, []);

  const handleBlur = useCallback(() => {
    setEditingId(null);
  }, []);

  // Определяем иконку для типа элемента
  const getElementTypeIcon = (type) => {
    switch (type) {
      case 'text': return <i className="fas fa-font"></i>;
      case 'image': return <i className="fas fa-image"></i>;
      case 'button': return <i className="fas fa-square-full"></i>;
      case 'shape': return <i className="fas fa-shapes"></i>;
      default: return <i className="fas fa-cube"></i>;
    }
  };

  // --- Drag & Drop для изменения порядка слоев ---
  const handleDragStart = useCallback((e, index) => {
    setDraggedItem(elements[index]); // Запоминаем элемент, который начали перетаскивать
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', index.toString()); // Передаем индекс элемента
  }, [elements]);

  const handleDragOver = useCallback((e) => {
    e.preventDefault(); // Разрешаем drop
    e.dataTransfer.dropEffect = 'move';
  }, []);

  const handleDrop = useCallback((e, dropIndex) => {
    e.preventDefault();
    const draggedIndex = parseInt(e.dataTransfer.getData('text/plain'));
    
    if (draggedItem && draggedIndex !== dropIndex) {
      onMoveLayer(draggedIndex, dropIndex); // Вызываем функцию из Editor.js
    }
    setDraggedItem(null); // Сбрасываем перетаскиваемый элемент
  }, [draggedItem, onMoveLayer]);

  const handleDragEnd = useCallback(() => {
    setDraggedItem(null);
  }, []);

  // Сортируем элементы, чтобы более высокие Z-index были сверху в списке
  // (На канвасе они уже рендерятся в правильном порядке, здесь только для UI)
  const sortedElements = [...elements].reverse(); // Чтобы верхние элементы на канвасе были сверху в панели

  return (
    <div className="layers-panel">
      <h3><i className="fas fa-layer-group"></i> Слои ({elements.length})</h3>
      <div className="layers-list">
        {sortedElements.length === 0 && <p className="no-layers">Нет элементов на канвасе.</p>}
        {sortedElements.map((el, index) => {
          // Индекс в исходном массиве (для onMoveLayer)
          const originalIndex = elements.findIndex(item => item.id === el.id); 

          return (
            <div
              key={el.id}
              className={`layer-item ${el.id === selectedElementId ? 'selected' : ''} ${draggedItem && draggedItem.id === el.id ? 'dragging' : ''}`}
              onClick={() => handleSelect(el.id)}
              onDoubleClick={() => handleDoubleClick(el.id)}
              draggable="true"
              onDragStart={(e) => handleDragStart(e, originalIndex)}
              onDragOver={handleDragOver}
              onDrop={(e) => handleDrop(e, originalIndex)}
              onDragEnd={handleDragEnd}
            >
              <div className="layer-handle"><i className="fas fa-grip-lines"></i></div>
              <div className="layer-type-icon">{getElementTypeIcon(el.type)}</div>
              {editingId === el.id ? (
                <input
                  type="text"
                  value={el.props.name || `${el.type} ${el.id.substring(0, 4)}`}
                  onChange={(e) => handleNameChange(e, el.id)}
                  onBlur={handleBlur}
                  autoFocus
                  onFocus={(e) => e.target.select()} // Выделяем весь текст при фокусе
                />
              ) : (
                <span className="layer-name">
                  {el.props.name || `${el.type} ${el.id.substring(0, 4)}`}
                </span>
              )}
              {/* Опциональные иконки для будущих функций */}
              <div className="layer-actions">
                <button className="layer-action-btn" title="Скрыть/Показать (пока не работает)">
                  <i className="fas fa-eye"></i>
                </button>
                <button className="layer-action-btn" title="Блокировать/Разблокировать (пока не работает)">
                  <i className="fas fa-lock"></i>
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default LayersPanel; 