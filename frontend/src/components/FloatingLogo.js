import React from 'react';
import logo from '../assets/logo.png';

export default function FloatingLogo() {
  // TODO: реализовать drag&drop и стилизацию
  return (
    <div style={{ position: 'fixed', top: 20, left: 20, zIndex: 1000, background: 'rgba(255,255,255,0.8)', borderRadius: '50%', padding: 8, boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
      <img src={logo} alt="Лого" style={{ width: 48, height: 48 }} />
    </div>
  );
} 