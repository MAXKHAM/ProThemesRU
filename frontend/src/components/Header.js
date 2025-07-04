import React, { useState } from 'react';
import '../styles/Header.css';
import AboutModal from './AboutModal';

function Header() {
  const [aboutOpen, setAboutOpen] = useState(false);
  return (
    <header className="brand-header" style={{
      background: `url('/assets/logo-main.jpg') center left/cover no-repeat`,
      minHeight: '320px',
      display: 'flex',
      alignItems: 'center',
      padding: '0 48px',
      color: '#fff',
      borderRadius: '0 0 32px 0',
      boxShadow: '0 4px 32px rgba(0,0,0,0.08)'
    }}>
      <div style={{flex: '0 0 320px', display: 'flex', alignItems: 'center', justifyContent: 'center'}}>
        <img src="/assets/logo-main.jpg" alt="ProThemesRU" style={{width: '260px', height: '260px', objectFit: 'contain', borderRadius: '24px', boxShadow: '0 2px 16px rgba(0,0,0,0.15)'}} />
      </div>
      <div style={{flex: 1, marginLeft: '48px', display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>
        <h1 style={{fontSize: '3rem', fontWeight: 800, marginBottom: '16px', color: '#fff', textShadow: '0 2px 8px rgba(0,0,0,0.15)'}}>ProThemesRU</h1>
        <div style={{fontSize: '1.5rem', marginBottom: '32px', color: '#fff', textShadow: '0 2px 8px rgba(0,0,0,0.10)'}}>Ваша платформа для быстрого создания сайтов</div>
        <div style={{display: 'flex', gap: '20px'}}>
          <a href="#canvas" style={{padding: '16px 32px', background: '#ffb300', color: '#222', borderRadius: '8px', fontWeight: 700, fontSize: '1.1rem', textDecoration: 'none', boxShadow: '0 2px 8px rgba(0,0,0,0.10)'}}>Начать бесплатно</a>
          <button style={{padding: '16px 32px', background: '#fff', color: '#ffb300', border: 'none', borderRadius: '8px', fontWeight: 700, fontSize: '1.1rem', cursor: 'pointer', boxShadow: '0 2px 8px rgba(0,0,0,0.10)'}} onClick={() => setAboutOpen(true)}>О нас</button>
        </div>
      </div>
      <AboutModal open={aboutOpen} onClose={() => setAboutOpen(false)} />
    </header>
  );
}

export default Header; 