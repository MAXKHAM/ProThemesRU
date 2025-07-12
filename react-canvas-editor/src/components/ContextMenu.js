import React from 'react';
import '../styles/ContextMenu.css';

function ContextMenu({ x, y, actions, onClose }) {
  return (
    <div 
      className="context-menu"
      style={{
        position: 'fixed',
        left: x,
        top: y,
        zIndex: 1000,
      }}
      onClick={(e) => e.stopPropagation()}
    >
      {actions.map((item, idx) =>
        item.type === 'separator' ? (
          <div key={idx} className="context-menu-separator" />
        ) : (
          <div
            key={idx}
            className={`context-menu-item${item.disabled ? ' disabled' : ''}`}
            onClick={() => !item.disabled && item.action()}
            style={{ 
              pointerEvents: item.disabled ? 'none' : 'auto', 
              opacity: item.disabled ? 0.5 : 1 
            }}
          >
            {item.label}
          </div>
        )
      )}
    </div>
  );
}

export default ContextMenu; 