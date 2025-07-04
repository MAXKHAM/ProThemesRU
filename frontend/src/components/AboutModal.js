import React from 'react';
import '../styles/AboutModal.css';

function AboutModal({ open, onClose }) {
  if (!open) return null;
  return (
    <div className="about-modal-overlay" onClick={onClose}>
      <div className="about-modal" onClick={e => e.stopPropagation()}>
        <button className="about-modal-close" onClick={onClose}>&times;</button>
        <h2>О ProThemesRU</h2>
        <video src="/assets/car-road-snow-1751316071037.mp4" autoplay loop muted playsinline style={{height: '80px', width: '220px', maxWidth: '100%', display: 'block', margin: '0 auto 16px auto'}}></video>
        <p><b>ProThemesRU</b> — это инновационный онлайн-конструктор сайтов, созданный для дизайнеров, предпринимателей и всех, кто хочет быстро и красиво представить себя в интернете.</p>
        <ul>
          <li>Интуитивно понятный интерфейс (drag & drop, мультивыделение, слои)</li>
          <li>Мощные инструменты выравнивания и распределения элементов</li>
          <li>Экспорт готового сайта в HTML/CSS/ZIP одним кликом</li>
          <li>AI-генератор цветовых палитр и дизайн-подсказки</li>
          <li>Поддержка брендирования и кастомизации под ваши задачи</li>
          <li>Современный дизайн и адаптивность</li>
        </ul>
        <p>Мы верим, что создание сайта должно быть простым, быстрым и вдохновляющим. С ProThemesRU вы получаете полный контроль над своим проектом — от идеи до готового результата.</p>
        <div className="about-modal-footer">
          <span>© 2024 ProThemesRU</span> | <a href="https://prothemes.ru" target="_blank" rel="noopener noreferrer">prothemes.ru</a>
        </div>
      </div>
    </div>
  );
}

export default AboutModal; 