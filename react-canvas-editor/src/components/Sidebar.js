import React from 'react';
import '../styles/Sidebar.css';

function Sidebar({ 
  addElement,
  showGrid,
  setShowGrid,
  snapToGrid,
  setSnapToGrid,
  gridSize,
  setGridSize,
  snapToElements,
  setSnapToElements
}) {
  return (
    <div className="sidebar">
      <h3>Элементы</h3>
      
      <div className="element-buttons">
        <button onClick={() => addElement('text')}>
          <i className="fas fa-font"></i> Текст
        </button>
        <button onClick={() => addElement('image')}>
          <i className="fas fa-image"></i> Изображение
        </button>
        <button onClick={() => addElement('button')}>
          <i className="fas fa-square"></i> Кнопка
        </button>
        <button onClick={() => addElement('shape')}>
          <i className="fas fa-circle"></i> Фигура
        </button>
        <button onClick={() => addElement('group')}>
          <i className="fas fa-layer-group"></i> Группа
        </button>
      </div>

      <hr />

      <h3>Настройки сетки</h3>
      <div className="grid-controls">
        <label>
          <input
            type="checkbox"
            checked={showGrid}
            onChange={(e) => setShowGrid(e.target.checked)}
          />
          Показать сетку
        </label>
        
        <label>
          <input
            type="checkbox"
            checked={snapToGrid}
            onChange={(e) => setSnapToGrid(e.target.checked)}
            disabled={!showGrid}
          />
          Привязка к сетке
        </label>
        
        <div className="grid-size-control">
          <label>Размер сетки:</label>
          <input
            type="number"
            min="5"
            max="50"
            value={gridSize}
            onChange={(e) => setGridSize(parseInt(e.target.value))}
            disabled={!showGrid}
          />
        </div>
        
        <label>
          <input
            type="checkbox"
            checked={snapToElements}
            onChange={(e) => setSnapToElements(e.target.checked)}
          />
          Привязка к элементам
        </label>
      </div>
    </div>
  );
}

export default Sidebar; 