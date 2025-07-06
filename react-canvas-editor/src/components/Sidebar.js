import React from 'react';
import '../styles/Sidebar.css';

function Sidebar({ addElement }) {
  const handleElementClick = (type) => {
    // Добавляем элемент в центр канваса
    addElement(type, 100, 100);
  };

  return (
    <div className="sidebar">
      <h3>Элементы</h3>
      <div className="element-buttons">
        <button 
          className="element-button" 
          onClick={() => handleElementClick('text')}
          title="Добавить текст"
        >
          <i className="fas fa-font"></i>
          <span>Текст</span>
        </button>
        
        <button 
          className="element-button" 
          onClick={() => handleElementClick('image')}
          title="Добавить изображение"
        >
          <i className="fas fa-image"></i>
          <span>Изображение</span>
        </button>
        
        <button 
          className="element-button" 
          onClick={() => handleElementClick('button')}
          title="Добавить кнопку"
        >
          <i className="fas fa-square"></i>
          <span>Кнопка</span>
        </button>
        
        <button 
          className="element-button" 
          onClick={() => handleElementClick('shape')}
          title="Добавить фигуру"
        >
          <i className="fas fa-circle"></i>
          <span>Фигура</span>
        </button>
      </div>
      
      <div className="sidebar-section">
        <h4>Инструкции</h4>
        <ul>
          <li>Нажмите на элемент для добавления</li>
          <li>Перетаскивайте элементы мышью</li>
          <li>Измените размер углами</li>
          <li>Выберите элемент для редактирования</li>
        </ul>
      </div>
    </div>
  );
}

export default Sidebar; 