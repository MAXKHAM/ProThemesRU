import React, { useCallback, useState } from 'react';
import '../styles/LayersPanel.css';

function LayersPanel({ elements, selectedElementIds, setSelectedElementIds, updateElement, updateElementProps, onMoveLayer, getAbsolutePosition }) {
  const [editingId, setEditingId] = useState(null);
  const [draggedItem, setDraggedItem] = useState(null);

  const handleSelect = useCallback((id) => {
    setSelectedElementIds([id]);
  }, [setSelectedElementIds]);

  const handleNameChange = useCallback((e, id) => {
    updateElementProps(id, { name: e.target.value });
  }, [updateElementProps]);

  const handleDoubleClick = useCallback((id) => {
    setEditingId(id);
  }, []);

  const handleBlur = useCallback(() => {
    setEditingId(null);
  }, []);

  const getElementTypeIcon = (type) => {
    switch (type) {
      case 'text': return <i className="fas fa-font"></i>;
      case 'image': return <i className="fas fa-image"></i>;
      case 'button': return <i className="fas fa-square-full"></i>;
      case 'shape': return <i className="fas fa-shapes"></i>;
      case 'group': return <i className="fas fa-layer-group"></i>;
      default: return <i className="fas fa-cube"></i>;
    }
  };

  const handleDragStart = useCallback((e, id) => {
    const element = elements.find(el => el.id === id);
    if (!element || element.parentId) {
        e.preventDefault();
        return;
    }
    setDraggedItem(element);
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', id);
  }, [elements]);

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  }, []);

  const handleDrop = useCallback((e, dropId) => {
    e.preventDefault();
    const draggedId = e.dataTransfer.getData('text/plain');
    if (!draggedId || draggedId === dropId) return;

    const fromIndex = elements.findIndex(el => el.id === draggedId);
    const toIndex = elements.findIndex(el => el.id === dropId);

    if (fromIndex !== -1 && toIndex !== -1) {
      const draggedEl = elements[fromIndex];
      const dropEl = elements[toIndex];

      if (draggedEl.parentId || dropEl.parentId) {
          alert('Перемещение элементов внутри или из групп через панель слоев пока не поддерживается.');
          setDraggedItem(null);
          return;
      }

      onMoveLayer(fromIndex, toIndex);
    }
    setDraggedItem(null);
  }, [elements, onMoveLayer]);

  const handleDragEnd = useCallback(() => {
    setDraggedItem(null);
  }, []);

  const sortedElements = [...elements].sort((a, b) => {
      if (a.type === 'group' && b.type !== 'group') return -1;
      if (a.type !== 'group' && b.type === 'group') return 1;

      return elements.indexOf(a) - elements.indexOf(b);
  }).reverse();

  return (
    <div className="layers-panel">
      <h3><i className="fas fa-layer-group"></i> Слои ({elements.length})</h3>
      <div className="layers-list">
        {sortedElements.length === 0 && <p className="no-layers">Нет элементов на канвасе.</p>}
        {sortedElements.map((el) => {
          const isSelected = selectedElementIds.includes(el.id) || (el.parentId && selectedElementIds.includes(el.parentId));
          const isChildOfSelectedGroup = el.parentId && selectedElementIds.includes(el.parentId);

          return (
            <div
              key={el.id}
              className={`layer-item ${isSelected ? 'selected' : ''} ${draggedItem && draggedItem.id === el.id ? 'dragging' : ''} ${el.parentId ? 'is-child-layer' : ''}`}
              onClick={() => handleSelect(el.id)}
              onDoubleClick={() => handleDoubleClick(el.id)}
              draggable={!el.parentId}
              onDragStart={(e) => handleDragStart(e, el.id)}
              onDragOver={handleDragOver}
              onDrop={(e) => handleDrop(e, el.id)}
              onDragEnd={handleDragEnd}
            >
              <div className="layer-handle"><i className="fas fa-grip-lines"></i></div>
              <div className="layer-type-icon">{getElementTypeIcon(el.type)}</div>
              {editingId === el.id ? (
                <input
                  type="text"
                  value={el.props.name || `${el.type} ${el.id.substring(0, 4)}`}
                  onChange={(e) => handleNameChange(e, el.id)}
                  onBlur={handleBlur}
                  autoFocus
                  onFocus={(e) => e.target.select()}
                />
              ) : (
                <span className="layer-name">
                  {el.props.name || `${el.type} ${el.id.substring(0, 4)}`}
                  {el.parentId && <span className="parent-indicator"> (в группе)</span>}
                </span>
              )}
              <div className="layer-actions">
                <button className="layer-action-btn" title="Скрыть/Показать (пока не работает)">
                  <i className="fas fa-eye"></i>
                </button>
                <button className="layer-action-btn" title="Блокировать/Разблокировать (пока не работает)">
                  <i className="fas fa-lock"></i>
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default LayersPanel; 