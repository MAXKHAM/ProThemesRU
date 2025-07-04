import React from 'react';

export default function FloatingCalculator() {
  // TODO: реализовать drag&drop и калькулятор
  return (
    <div style={{ position: 'fixed', bottom: 20, right: 20, zIndex: 1000, background: '#fff', border: '1px solid #ddd', borderRadius: 8, padding: 16, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
      <b>Калькулятор</b>
      <div>Здесь будет калькулятор</div>
    </div>
  );
} 