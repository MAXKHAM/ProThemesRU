import React, { useState, useRef, useEffect, forwardRef } from 'react';
import '../styles/Canvas.css';

const MIN_SIZE = 20;
const MAX_WIDTH = 800;
const MAX_HEIGHT = 600;

const Canvas = forwardRef(({ elements, updateElement, selectedElementIds, setSelectedElementIds, deleteElement }, ref) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isResizing, setIsResizing] = useState(false);
  const [dragStartCoords, setDragStartCoords] = useState({ x: 0, y: 0 });
  const [initialElementState, setInitialElementState] = useState(null);
  const [resizeHandle, setResizeHandle] = useState(null);

  const canvasRef = useRef(null);

  // Глобальные слушатели для перетаскивания и изменения размера
  useEffect(() => {
    const handleMouseMove = (e) => {
      if (isDragging && initialElementState) {
        const deltaX = e.clientX - dragStartCoords.x;
        const deltaY = e.clientY - dragStartCoords.y;
        
        const newX = Math.max(0, initialElementState.x + deltaX);
        const newY = Math.max(0, initialElementState.y + deltaY);
        
        updateElement(initialElementState.id, { x: newX, y: newY });
      } else if (isResizing && initialElementState && resizeHandle) {
        const deltaX = e.clientX - dragStartCoords.x;
        const deltaY = e.clientY - dragStartCoords.y;
        
        let newWidth = initialElementState.width;
        let newHeight = initialElementState.height;
        let newX = initialElementState.x;
        let newY = initialElementState.y;
        
        switch (resizeHandle) {
          case 'top-left':
            newWidth = Math.max(MIN_SIZE, Math.min(MAX_WIDTH, initialElementState.width - deltaX));
            newHeight = Math.max(MIN_SIZE, Math.min(MAX_HEIGHT, initialElementState.height - deltaY));
            newX = initialElementState.x + (initialElementState.width - newWidth);
            newY = initialElementState.y + (initialElementState.height - newHeight);
            break;
          case 'top-center':
            newHeight = Math.max(MIN_SIZE, Math.min(MAX_HEIGHT, initialElementState.height - deltaY));
            newY = initialElementState.y + (initialElementState.height - newHeight);
            break;
          case 'top-right':
            newWidth = Math.max(MIN_SIZE, Math.min(MAX_WIDTH, initialElementState.width + deltaX));
            newHeight = Math.max(MIN_SIZE, Math.min(MAX_HEIGHT, initialElementState.height - deltaY));
            newY = initialElementState.y + (initialElementState.height - newHeight);
            break;
          case 'mid-left':
            newWidth = Math.max(MIN_SIZE, Math.min(MAX_WIDTH, initialElementState.width - deltaX));
            newX = initialElementState.x + (initialElementState.width - newWidth);
            break;
          case 'mid-right':
            newWidth = Math.max(MIN_SIZE, Math.min(MAX_WIDTH, initialElementState.width + deltaX));
            break;
          case 'bottom-left':
            newWidth = Math.max(MIN_SIZE, Math.min(MAX_WIDTH, initialElementState.width - deltaX));
            newHeight = Math.max(MIN_SIZE, Math.min(MAX_HEIGHT, initialElementState.height + deltaY));
            newX = initialElementState.x + (initialElementState.width - newWidth);
            break;
          case 'bottom-center':
            newHeight = Math.max(MIN_SIZE, Math.min(MAX_HEIGHT, initialElementState.height + deltaY));
            break;
          case 'bottom-right':
            newWidth = Math.max(MIN_SIZE, Math.min(MAX_WIDTH, initialElementState.width + deltaX));
            newHeight = Math.max(MIN_SIZE, Math.min(MAX_HEIGHT, initialElementState.height + deltaY));
            break;
          default:
            break;
        }
        
        updateElement(initialElementState.id, { x: newX, y: newY, width: newWidth, height: newHeight });
      }
    };

    const handleMouseUp = () => {
      setIsDragging(false);
      setIsResizing(false);
      setInitialElementState(null);
      setResizeHandle(null);
    };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging, isResizing, dragStartCoords, initialElementState, resizeHandle, updateElement]);

  const handleMouseDownOnElement = (e, element) => {
    e.stopPropagation();
    
    // Если нажат Ctrl/Cmd, добавляем к выделению, иначе заменяем
    if (e.ctrlKey || e.metaKey) {
      setSelectedElementIds(prev => 
        prev.includes(element.id) 
          ? prev.filter(id => id !== element.id)
          : [...prev, element.id]
      );
    } else {
      setSelectedElementIds([element.id]);
    }
    
    setIsDragging(true);
    setDragStartCoords({ x: e.clientX, y: e.clientY });
    setInitialElementState(element);
  };

  const handleMouseDownOnHandle = (e, element, handle) => {
    e.stopPropagation();
    e.preventDefault();
    
    setSelectedElementIds([element.id]);
    setIsResizing(true);
    setResizeHandle(handle);
    setDragStartCoords({ x: e.clientX, y: e.clientY });
    setInitialElementState(element);
  };

  const handleMouseDownOnCanvas = (e) => {
    if (e.target === canvasRef.current) {
      setSelectedElementIds([]);
    }
  };

  const renderElement = (el) => {
    const isSelected = selectedElementIds.includes(el.id);
    const zIndex = elements.indexOf(el);

    let content;
    switch (el.type) {
      case 'text':
        content = <div className="text-element">{el.props.content}</div>;
        break;
      case 'image':
        content = <img src={el.props.src} alt={el.props.alt} className="image-element" />;
        break;
      case 'button':
        content = <button className="button-element">{el.props.label}</button>;
        break;
      case 'shape':
        content = <div className="shape-element" />;
        break;
      default:
        content = <div>Неизвестный элемент</div>;
    }

    return (
      <div
        key={el.id}
        className={`canvas-element ${isSelected ? 'selected' : ''}`}
        style={{
          left: el.x,
          top: el.y,
          width: el.width,
          height: el.height,
          zIndex,
          ...(el.type === 'text' && {
            fontSize: el.props.fontSize,
            color: el.props.color,
          }),
          ...(el.type === 'button' && {
            backgroundColor: el.props.bgColor,
            color: el.props.textColor,
          }),
          ...(el.type === 'shape' && {
            backgroundColor: el.props.bgColor,
            borderRadius: el.props.borderRadius,
          }),
        }}
        onMouseDown={(e) => handleMouseDownOnElement(e, el)}
      >
        {content}
        
        {/* Маркеры изменения размера для выбранного элемента */}
        {isSelected && (
          <>
            <div className="handle top-left" onMouseDown={(e) => handleMouseDownOnHandle(e, el, 'top-left')} />
            <div className="handle top-center" onMouseDown={(e) => handleMouseDownOnHandle(e, el, 'top-center')} />
            <div className="handle top-right" onMouseDown={(e) => handleMouseDownOnHandle(e, el, 'top-right')} />
            <div className="handle mid-left" onMouseDown={(e) => handleMouseDownOnHandle(e, el, 'mid-left')} />
            <div className="handle mid-right" onMouseDown={(e) => handleMouseDownOnHandle(e, el, 'mid-right')} />
            <div className="handle bottom-left" onMouseDown={(e) => handleMouseDownOnHandle(e, el, 'bottom-left')} />
            <div className="handle bottom-center" onMouseDown={(e) => handleMouseDownOnHandle(e, el, 'bottom-center')} />
            <div className="handle bottom-right" onMouseDown={(e) => handleMouseDownOnHandle(e, el, 'bottom-right')} />
          </>
        )}
      </div>
    );
  };

  return (
    <div
      ref={canvasRef}
      className="canvas"
      onMouseDown={handleMouseDownOnCanvas}
    >
      {elements.map(renderElement)}
    </div>
  );
});

Canvas.displayName = 'Canvas';

export default Canvas; 