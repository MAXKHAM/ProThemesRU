import React from 'react';

export default function FloatingCart() {
  // TODO: реализовать drag&drop и содержимое корзины
  return (
    <div style={{ position: 'fixed', top: 20, right: 20, zIndex: 1000, background: '#fff', border: '1px solid #ddd', borderRadius: 8, padding: 16, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
      <b>Корзина</b>
      <div>Товары будут здесь</div>
    </div>
  );
} 