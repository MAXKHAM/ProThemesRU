import React from 'react';
import '../styles/Footer.css';
import logo from '../assets/logo.png';

function Footer() {
  return (
    <footer className="brand-footer">
      <div className="footer-content">
        <div className="footer-logo-block">
          <img src={logo} alt="ProThemesRU" className="footer-logo" />
          <span className="footer-brand">ProThemesRU</span>
        </div>
        <div className="footer-links">
          <a href="https://prothemes.ru" target="_blank" rel="noopener noreferrer">prothemes.ru</a>
          <span> | </span>
          <a href="#about" onClick={e => {e.preventDefault(); window.scrollTo({top: 0, behavior: 'smooth'});}}>О нас</a>
        </div>
        <div className="footer-copyright">
          © 2024 ProThemesRU. Все права защищены.
        </div>
      </div>
      <video className="footer-bg-video" src="/assets/car-road-snow-1751316071037.mp4" autoPlay loop muted playsInline></video>
    </footer>
  );
}

export default Footer; 