import React, { useRef, useEffect, useCallback } from 'react';
import '../styles/Canvas.css';

function Canvas({
  elements,
  updateElement,
  selectedElementIds,
  setSelectedElementIds,
  deleteElement,
  // NEW: Canvas background props
  canvasBackgroundColor,
  canvasBackgroundImage,
  canvasBackgroundRepeat,
  canvasBackgroundSize,
  canvasBackgroundPosition,
  // NEW: Grid and snap props
  showGrid,
  snapToGrid,
  gridSize,
  snapToElements,
  // NEW: Context menu handler
  onContextMenu,
}) {
  const canvasRef = useRef(null);

  // Calculate canvas background styles
  const canvasBackgroundStyles = {
    backgroundColor: canvasBackgroundColor || '#ffffff',
    ...(canvasBackgroundImage && {
      backgroundImage: `url('${canvasBackgroundImage}')`,
      backgroundRepeat: canvasBackgroundRepeat || 'no-repeat',
      backgroundSize: canvasBackgroundSize || 'cover',
      backgroundPosition: canvasBackgroundPosition || 'center center',
    }),
  };

  const handleMouseDown = useCallback((e, elementId) => {
    if (e.button === 0) { // Left click only
      if (e.ctrlKey || e.metaKey) {
        // Multi-select
        setSelectedElementIds(prev => {
          if (prev.includes(elementId)) {
            return prev.filter(id => id !== elementId);
          } else {
            return [...prev, elementId];
          }
        });
      } else {
        // Single select
        setSelectedElementIds([elementId]);
      }
    }
  }, [setSelectedElementIds]);

  const handleCanvasClick = useCallback((e) => {
    if (e.target === canvasRef.current) {
      setSelectedElementIds([]);
    }
  }, [setSelectedElementIds]);

  const handleDragStart = useCallback((e, elementId) => {
    e.dataTransfer.setData('text/plain', elementId);
  }, []);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    const elementId = e.dataTransfer.getData('text/plain');
    const rect = canvasRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Apply snap to grid if enabled
    let snappedX = x;
    let snappedY = y;
    
    if (snapToGrid && showGrid) {
      snappedX = Math.round(x / gridSize) * gridSize;
      snappedY = Math.round(y / gridSize) * gridSize;
    }

    updateElement(elementId, { x: snappedX, y: snappedY });
  }, [updateElement, snapToGrid, showGrid, gridSize]);

  // Render grid
  const renderGrid = () => {
    if (!showGrid) return null;

    const gridLines = [];
    const canvasWidth = canvasRef.current?.offsetWidth || 800;
    const canvasHeight = canvasRef.current?.offsetHeight || 600;

    // Vertical lines
    for (let x = 0; x <= canvasWidth; x += gridSize) {
      gridLines.push(
        <line
          key={`v-${x}`}
          x1={x}
          y1={0}
          x2={x}
          y2={canvasHeight}
          stroke="#e0e0e0"
          strokeWidth="1"
          opacity="0.5"
        />
      );
    }

    // Horizontal lines
    for (let y = 0; y <= canvasHeight; y += gridSize) {
      gridLines.push(
        <line
          key={`h-${y}`}
          x1={0}
          y1={y}
          x2={canvasWidth}
          y2={y}
          stroke="#e0e0e0"
          strokeWidth="1"
          opacity="0.5"
        />
      );
    }

    return gridLines;
  };

  // Calculate selection box
  const getSelectionBox = () => {
    if (selectedElementIds.length === 0) return null;

    const selectedElements = elements.filter(el => selectedElementIds.includes(el.id));
    if (selectedElements.length === 0) return null;

    let minX = Infinity, minY = Infinity;
    let maxX = -Infinity, maxY = -Infinity;

    selectedElements.forEach(element => {
      minX = Math.min(minX, element.x);
      minY = Math.min(minY, element.y);
      maxX = Math.max(maxX, element.x + element.width);
      maxY = Math.max(maxY, element.y + element.height);
    });

    return {
      x: minX,
      y: minY,
      width: maxX - minX,
      height: maxY - minY,
    };
  };

  const selectionBox = getSelectionBox();

  return (
    <div className="canvas-container">
      <div
        ref={canvasRef}
        className="canvas"
        style={canvasBackgroundStyles}
        onClick={handleCanvasClick}
        onContextMenu={onContextMenu}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
      >
        {/* Grid overlay */}
        <svg
          className="grid-overlay"
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            pointerEvents: 'none',
            zIndex: 1,
          }}
        >
          {renderGrid()}
        </svg>

        {/* Elements */}
        {elements.map((element) => (
          <div
            key={element.id}
            className={`canvas-element ${element.type}-element ${
              selectedElementIds.includes(element.id) ? 'selected' : ''
            }`}
            style={{
              position: 'absolute',
              left: element.x,
              top: element.y,
              width: element.width,
              height: element.height,
              zIndex: element.props?.zIndex || 1,
              backgroundColor: element.props?.bgColor || 'transparent',
              color: element.props?.color || '#000000',
              fontSize: element.props?.fontSize || '16px',
              border: element.props?.borderWidth ? 
                `${element.props.borderWidth} ${element.props.borderStyle || 'solid'} ${element.props.borderColor || '#000000'}` : 
                'none',
              borderRadius: element.props?.borderRadius || '0',
              boxShadow: element.props?.boxShadowX ? 
                `${element.props.boxShadowX} ${element.props.boxShadowY || '0px'} ${element.props.boxShadowBlur || '0px'} ${element.props.boxShadowSpread || '0px'} ${element.props.boxShadowColor || 'rgba(0,0,0,0.2)'}` : 
                'none',
              ...(element.props?.backgroundColor && { backgroundColor: element.props.backgroundColor }),
              ...(element.props?.backgroundImage && {
                backgroundImage: `url('${element.props.backgroundImage}')`,
                backgroundRepeat: element.props.backgroundRepeat || 'no-repeat',
                backgroundSize: element.props.backgroundSize || 'cover',
                backgroundPosition: element.props.backgroundPosition || 'center center',
              }),
              ...(element.props?.displayMode === 'flex' && {
                display: 'flex',
                flexDirection: element.props.flexDirection || 'row',
                justifyContent: element.props.justifyContent || 'flex-start',
                alignItems: element.props.alignItems || 'stretch',
                gap: element.props.gap || '0px',
              }),
              ...(element.props?.displayMode === 'grid' && {
                display: 'grid',
                gridTemplateColumns: element.props.gridTemplateColumns || '1fr',
                gridTemplateRows: element.props.gridTemplateRows || 'auto',
                gap: element.props.gridGap || '0px',
              }),
            }}
            onMouseDown={(e) => handleMouseDown(e, element.id)}
            onContextMenu={(e) => onContextMenu(e, element.id)}
            draggable
            onDragStart={(e) => handleDragStart(e, element.id)}
          >
            {element.type === 'text' && (
              <div className="text-content">{element.props?.content || 'Текст'}</div>
            )}
            {element.type === 'image' && (
              <img
                src={element.props?.src || 'https://via.placeholder.com/150'}
                alt={element.props?.alt || 'Изображение'}
                style={{ width: '100%', height: '100%', objectFit: 'contain' }}
              />
            )}
            {element.type === 'button' && (
              <button
                style={{
                  backgroundColor: element.props?.bgColor || '#007bff',
                  color: element.props?.textColor || '#ffffff',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '14px',
                  padding: '8px 15px',
                }}
              >
                {element.props?.label || 'Кнопка'}
              </button>
            )}
            {element.type === 'shape' && (
              <div style={{ width: '100%', height: '100%' }}></div>
            )}
            {element.type === 'group' && (
              <div className="group-content">
                Группа элементов
              </div>
            )}
          </div>
        ))}

        {/* Selection box */}
        {selectionBox && (
          <div
            className="selection-box"
            style={{
              position: 'absolute',
              left: selectionBox.x - 2,
              top: selectionBox.y - 2,
              width: selectionBox.width + 4,
              height: selectionBox.height + 4,
              border: '2px dashed #007bff',
              backgroundColor: 'rgba(0, 123, 255, 0.1)',
              pointerEvents: 'none',
              zIndex: 1000,
            }}
          />
        )}
      </div>
    </div>
  );
}

export default Canvas; 