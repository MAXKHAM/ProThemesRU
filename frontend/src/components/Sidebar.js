import React from 'react';

export default function Sidebar({ onAddElement }) {
  return (
    <aside className="sidebar">
      <button onClick={() => onAddElement('text')}>Текст</button>
      <button onClick={() => onAddElement('image')}>Изображение</button>
      <button onClick={() => onAddElement('button')}>Кнопка</button>
      <button onClick={() => onAddElement('shape')}>Фигура</button>
      {/* Новые типы блоков */}
      <button onClick={() => onAddElement('video')}>Видео</button>
      <button onClick={() => onAddElement('form')}>Форма</button>
      <button onClick={() => onAddElement('slider')}>Слайдер</button>
      <button onClick={() => onAddElement('gallery')}>Галерея</button>
      {/* Можно добавить стили и иконки */}
    </aside>
  );
} 