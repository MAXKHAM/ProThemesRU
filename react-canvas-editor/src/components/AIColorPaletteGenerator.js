import React, { useState } from 'react';
import '../styles/AIColorPaletteGenerator.css';

const AIColorPaletteGenerator = ({ onColorSelect }) => {
  const [keyword, setKeyword] = useState('');
  const [palettes, setPalettes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const generatePalette = async () => {
    if (!keyword.trim()) {
      setError('Введите ключевое слово');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch('http://127.0.0.1:5000/ai/generate_palette', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ keyword: keyword.trim() }),
      });

      if (!response.ok) {
        throw new Error('Ошибка при генерации палитры');
      }

      const data = await response.json();
      setPalettes(data.palettes || []);
    } catch (err) {
      setError('Ошибка соединения с сервером');
      console.error('Error generating palette:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleColorClick = (color) => {
    if (onColorSelect) {
      onColorSelect(color);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      generatePalette();
    }
  };

  return (
    <div className="ai-palette-generator">
      <h3>
        <i className="fas fa-magic"></i>
        AI Генератор палитр
      </h3>
      
      <div className="input-group">
        <input
          type="text"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Введите ключевое слово..."
          disabled={loading}
        />
        <button 
          onClick={generatePalette}
          disabled={loading || !keyword.trim()}
        >
          {loading ? '...' : 'Генерировать'}
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      <div className="palettes-container">
        {palettes.map((palette, paletteIndex) => (
          <div key={paletteIndex} className="palette-item">
            {palette.map((color, colorIndex) => (
              <div
                key={colorIndex}
                className="color-box"
                style={{ backgroundColor: color }}
                onClick={() => handleColorClick(color)}
                title={color}
              />
            ))}
          </div>
        ))}
      </div>

      {palettes.length > 0 && (
        <div style={{ fontSize: '0.8em', color: '#666', marginTop: '10px' }}>
          Кликните на цвет, чтобы применить к выбранному элементу
        </div>
      )}
    </div>
  );
};

export default AIColorPaletteGenerator; 