import React, { useCallback, useRef, useState, useEffect } from 'react';
import '../styles/Canvas.css';

function Canvas({ elements, updateElement, updateMultipleElements, selectedElementIds, setSelectedElementIds, deleteElement }) {
  const canvasRef = useRef(null);

  // Состояния для взаимодействия
  const [isDragging, setIsDragging] = useState(false);
  const [isResizing, setIsResizing] = useState(false);
  const [dragStartCoords, setDragStartCoords] = useState({ x: 0, y: 0 });
  const [initialElementState, setInitialElementState] = useState(null);
  const [resizeHandle, setResizeHandle] = useState(null);
  const [draggedElementId, setDraggedElementId] = useState(null);

  // Минимальные и максимальные размеры элементов
  const MIN_SIZE = 20;
  const MAX_WIDTH = 1200;
  const MAX_HEIGHT = 800;

  // --- Мультивыделение ---
  const handleMouseDownOnElement = useCallback((e, id) => {
    e.stopPropagation();
    // Shift/Ctrl/Cmd для мультивыделения
    if (e.shiftKey || e.ctrlKey || e.metaKey) {
      setSelectedElementIds(prev => {
        if (prev.includes(id)) {
          return prev.filter(elId => elId !== id);
        } else {
          return [...prev, id];
        }
      });
    } else {
      setSelectedElementIds([id]);
    }
    setDraggedElementId(id);
    const element = elements.find(el => el.id === id);
    if (element) {
      setIsDragging(true);
      setDragStartCoords({ x: e.clientX, y: e.clientY });
      setInitialElementState({ x: element.x, y: element.y, width: element.width, height: element.height });
    }
  }, [elements, setSelectedElementIds]);

  // --- Drag & Resize ---
  useEffect(() => {
    const handleMouseMove = (e) => {
      if (isDragging && draggedElementId) {
        const dx = e.clientX - dragStartCoords.x;
        const dy = e.clientY - dragStartCoords.y;
        // Если выделено несколько элементов, двигаем все
        if (selectedElementIds.length > 1 && selectedElementIds.includes(draggedElementId)) {
          // Сохраняем начальные состояния всех выделенных
          if (!initialElementState.group) {
            setInitialElementState(state => ({ ...state, group: selectedElementIds.map(id => {
              const el = elements.find(e => e.id === id);
              return { id, x: el.x, y: el.y };
            }) }));
            return;
          }
          const updatesMap = {};
          initialElementState.group.forEach(({ id, x, y }) => {
            updatesMap[id] = { x: x + dx, y: y + dy };
          });
          updateMultipleElements(selectedElementIds, updatesMap);
        } else {
          updateElement(draggedElementId, {
            x: initialElementState.x + dx,
            y: initialElementState.y + dy,
          });
        }
      } else if (isResizing && initialElementState) {
        const dx = e.clientX - dragStartCoords.x;
        const dy = e.clientY - dragStartCoords.y;
        let newX = initialElementState.x;
        let newY = initialElementState.y;
        let newWidth = initialElementState.width;
        let newHeight = initialElementState.height;
        switch (resizeHandle) {
          case 'top-left':
            newX = Math.min(initialElementState.x + dx, initialElementState.x + initialElementState.width - MIN_SIZE);
            newY = Math.min(initialElementState.y + dy, initialElementState.y + initialElementState.height - MIN_SIZE);
            newWidth = Math.max(MIN_SIZE, initialElementState.width - dx);
            newHeight = Math.max(MIN_SIZE, initialElementState.height - dy);
            break;
          case 'top-center':
            newY = Math.min(initialElementState.y + dy, initialElementState.y + initialElementState.height - MIN_SIZE);
            newHeight = Math.max(MIN_SIZE, initialElementState.height - dy);
            break;
          case 'top-right':
            newY = Math.min(initialElementState.y + dy, initialElementState.y + initialElementState.height - MIN_SIZE);
            newWidth = Math.max(MIN_SIZE, initialElementState.width + dx);
            newHeight = Math.max(MIN_SIZE, initialElementState.height - dy);
            break;
          case 'mid-left':
            newX = Math.min(initialElementState.x + dx, initialElementState.x + initialElementState.width - MIN_SIZE);
            newWidth = Math.max(MIN_SIZE, initialElementState.width - dx);
            break;
          case 'mid-right':
            newWidth = Math.max(MIN_SIZE, initialElementState.width + dx);
            break;
          case 'bottom-left':
            newX = Math.min(initialElementState.x + dx, initialElementState.x + initialElementState.width - MIN_SIZE);
            newWidth = Math.max(MIN_SIZE, initialElementState.width - dx);
            newHeight = Math.max(MIN_SIZE, initialElementState.height + dy);
            break;
          case 'bottom-center':
            newHeight = Math.max(MIN_SIZE, initialElementState.height + dy);
            break;
          case 'bottom-right':
            newWidth = Math.max(MIN_SIZE, initialElementState.width + dx);
            newHeight = Math.max(MIN_SIZE, initialElementState.height + dy);
            break;
          default:
            break;
        }
        newWidth = Math.min(newWidth, MAX_WIDTH);
        newHeight = Math.min(newHeight, MAX_HEIGHT);
        updateElement(selectedElementIds[0], {
          x: newX,
          y: newY,
          width: newWidth,
          height: newHeight,
        });
      }
    };
    const handleMouseUp = () => {
      setIsDragging(false);
      setIsResizing(false);
      setResizeHandle(null);
      setInitialElementState(null);
      setDraggedElementId(null);
    };
    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, isResizing, dragStartCoords, initialElementState, resizeHandle, selectedElementIds, draggedElementId, elements, updateElement, updateMultipleElements]);

  // Bounding box для мультивыделения
  let boundingBox = null;
  if (selectedElementIds.length > 1) {
    const selected = elements.filter(el => selectedElementIds.includes(el.id));
    if (selected.length) {
      const minX = Math.min(...selected.map(el => el.x));
      const minY = Math.min(...selected.map(el => el.y));
      const maxX = Math.max(...selected.map(el => el.x + el.width));
      const maxY = Math.max(...selected.map(el => el.y + el.height));
      boundingBox = {
        x: minX,
        y: minY,
        width: maxX - minX,
        height: maxY - minY,
      };
    }
  }

  // Снятие выделения по клику на канвас
  const handleMouseDownOnCanvas = useCallback((e) => {
    if (e.target === canvasRef.current) {
      setSelectedElementIds([]);
    }
  }, [setSelectedElementIds]);

  return (
    <div
      ref={canvasRef}
      className="canvas"
      onMouseDown={handleMouseDownOnCanvas}
    >
      {/* Bounding box для мультивыделения */}
      {boundingBox && (
        <div
          className="bounding-box"
          style={{
            left: boundingBox.x,
            top: boundingBox.y,
            width: boundingBox.width,
            height: boundingBox.height,
          }}
        />
      )}
      {elements.map(el => (
        <div
          key={el.id}
          className={`canvas-element${selectedElementIds.includes(el.id) ? ' selected' : ''}`}
          style={{
            left: el.x,
            top: el.y,
            width: el.width,
            height: el.height,
            zIndex: elements.indexOf(el),
          }}
          onMouseDown={e => handleMouseDownOnElement(e, el.id)}
        >
          {el.type === 'text' && <div style={{ fontSize: el.props.fontSize, color: el.props.color }}>{el.props.content}</div>}
          {el.type === 'image' && <img src={el.props.src} alt={el.props.alt} style={{ width: '100%', height: '100%', objectFit: 'contain' }} />}
          {el.type === 'button' && <button style={{ backgroundColor: el.props.bgColor, color: el.props.textColor }}>{el.props.label}</button>}
          {el.type === 'shape' && <div style={{ backgroundColor: el.props.bgColor, borderRadius: el.props.borderRadius, width: '100%', height: '100%' }}></div>}
          {el.type === 'video' && (
            <video src={el.props.src} controls style={{ width: '100%', height: '100%' }} />
          )}
          {el.type === 'form' && (
            <form style={{ width: '100%', height: '100%' }}>
              <input type="text" placeholder="Ваше имя" style={{ width: '90%', margin: '5px' }} />
              <input type="email" placeholder="Email" style={{ width: '90%', margin: '5px' }} />
              <button type="submit">Отправить</button>
            </form>
          )}
          {el.type === 'slider' && (
            <div style={{ width: '100%', height: '100%', overflow: 'hidden', background: '#eee', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <img src={el.props.images && el.props.images[0]} alt="Слайдер" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            </div>
          )}
          {el.type === 'gallery' && (
            <div style={{ width: '100%', height: '100%', display: 'flex', flexWrap: 'wrap', gap: '4px', background: '#fafafa' }}>
              {el.props.images && el.props.images.map((src, idx) => (
                <img key={idx} src={src} alt={`Галерея ${idx}`} style={{ width: '48%', height: '48%', objectFit: 'cover' }} />
              ))}
            </div>
          )}

          {/* Маркеры изменения размера только для одного выбранного элемента */}
          {selectedElementIds.length === 1 && selectedElementIds[0] === el.id && (
            <>
              <div className="handle top-left" onMouseDown={e => { e.stopPropagation(); setIsResizing(true); setResizeHandle('top-left'); setDragStartCoords({ x: e.clientX, y: e.clientY }); setInitialElementState({ x: el.x, y: el.y, width: el.width, height: el.height }); }} />
              <div className="handle top-center" onMouseDown={e => { e.stopPropagation(); setIsResizing(true); setResizeHandle('top-center'); setDragStartCoords({ x: e.clientX, y: e.clientY }); setInitialElementState({ x: el.x, y: el.y, width: el.width, height: el.height }); }} />
              <div className="handle top-right" onMouseDown={e => { e.stopPropagation(); setIsResizing(true); setResizeHandle('top-right'); setDragStartCoords({ x: e.clientX, y: e.clientY }); setInitialElementState({ x: el.x, y: el.y, width: el.width, height: el.height }); }} />
              <div className="handle mid-left" onMouseDown={e => { e.stopPropagation(); setIsResizing(true); setResizeHandle('mid-left'); setDragStartCoords({ x: e.clientX, y: e.clientY }); setInitialElementState({ x: el.x, y: el.y, width: el.width, height: el.height }); }} />
              <div className="handle mid-right" onMouseDown={e => { e.stopPropagation(); setIsResizing(true); setResizeHandle('mid-right'); setDragStartCoords({ x: e.clientX, y: e.clientY }); setInitialElementState({ x: el.x, y: el.y, width: el.width, height: el.height }); }} />
              <div className="handle bottom-left" onMouseDown={e => { e.stopPropagation(); setIsResizing(true); setResizeHandle('bottom-left'); setDragStartCoords({ x: e.clientX, y: e.clientY }); setInitialElementState({ x: el.x, y: el.y, width: el.width, height: el.height }); }} />
              <div className="handle bottom-center" onMouseDown={e => { e.stopPropagation(); setIsResizing(true); setResizeHandle('bottom-center'); setDragStartCoords({ x: e.clientX, y: e.clientY }); setInitialElementState({ x: el.x, y: el.y, width: el.width, height: el.height }); }} />
              <div className="handle bottom-right" onMouseDown={e => { e.stopPropagation(); setIsResizing(true); setResizeHandle('bottom-right'); setDragStartCoords({ x: e.clientX, y: e.clientY }); setInitialElementState({ x: el.x, y: el.y, width: el.width, height: el.height }); }} />
            </>
          )}
        </div>
      ))}
    </div>
  );
}

export default Canvas; 