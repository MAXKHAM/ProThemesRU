import React, { useCallback, useState, useEffect } from 'react';
import '../styles/PropertiesPanel.css';

function PropertiesPanel({
  selectedElement,
  selectedElementIds,
  elements,
  updateElementProps,
  updateElement,
  updateMultipleElements,
  saveCanvas,
  clearCanvas,
  exportToHtmlCss,
  undo,
  redo,
  canUndo,
  canRedo,
  deleteSelectedElements,
  alignElements,
  distributeElements
}) {
  const [localX, setLocalX] = useState('');
  const [localY, setLocalY] = useState('');
  const [localWidth, setLocalWidth] = useState('');
  const [localHeight, setLocalHeight] = useState('');

  useEffect(() => {
    if (selectedElement) {
      setLocalX(Math.round(selectedElement.x).toString());
      setLocalY(Math.round(selectedElement.y).toString());
      setLocalWidth(Math.round(selectedElement.width).toString());
      setLocalHeight(Math.round(selectedElement.height).toString());
    } else {
      setLocalX('');
      setLocalY('');
      setLocalWidth('');
      setLocalHeight('');
    }
  }, [selectedElement]);

  const handleChange = useCallback((e) => {
    const { name, value, type, checked } = e.target;
    if (selectedElement) {
        updateElementProps(selectedElement.id, { [name]: type === 'checkbox' ? checked : value });
    }
  }, [selectedElement, updateElementProps]);

  const handleDimensionChange = useCallback((e) => {
    const { name, value } = e.target;
    const numValue = parseFloat(value);

    switch (name) {
      case 'x': setLocalX(value); break;
      case 'y': setLocalY(value); break;
      case 'width': setLocalWidth(value); break;
      case 'height': setLocalHeight(value); break;
      default: break;
    }

    if (!isNaN(numValue) && selectedElement) {
      updateElement(selectedElement.id, { [name]: numValue });
    }
  }, [selectedElement, updateElement]);

  const renderPanelContent = () => {
    if (selectedElementIds.length === 0) {
      return (
        <>
          <h3>Свойства</h3>
          <p>Выберите элемент на канвасе для редактирования его свойств.</p>
        </>
      );
    } else if (selectedElementIds.length === 1) {
      const renderProperties = () => {
        switch (selectedElement.type) {
          case 'text':
            return (
              <>
                <div className="property-group">
                  <label>Содержимое:</label>
                  <textarea
                    name="content"
                    value={selectedElement.props.content || ''}
                    onChange={handleChange}
                  />
                </div>
                <div className="property-group">
                  <label>Размер шрифта:</label>
                  <input
                    type="text"
                    name="fontSize"
                    value={selectedElement.props.fontSize || ''}
                    onChange={handleChange}
                  />
                </div>
                <div className="property-group">
                  <label>Цвет текста:</label>
                  <input
                    type="color"
                    name="color"
                    value={selectedElement.props.color || '#000000'}
                    onChange={handleChange}
                  />
                </div>
              </>
            );
          case 'image':
            return (
              <>
                <div className="property-group">
                  <label>URL изображения:</label>
                  <input
                    type="text"
                    name="src"
                    value={selectedElement.props.src || ''}
                    onChange={handleChange}
                  />
                </div>
                <div className="property-group">
                  <label>Alt текст:</label>
                  <input
                    type="text"
                    name="alt"
                    value={selectedElement.props.alt || ''}
                    onChange={handleChange}
                  />
                </div>
              </>
            );
          case 'button':
            return (
              <>
                <div className="property-group">
                  <label>Текст кнопки:</label>
                  <input
                    type="text"
                    name="label"
                    value={selectedElement.props.label || ''}
                    onChange={handleChange}
                  />
                </div>
                <div className="property-group">
                  <label>Цвет фона:</label>
                  <input
                    type="color"
                    name="bgColor"
                    value={selectedElement.props.bgColor || '#007bff'}
                    onChange={handleChange}
                  />
                </div>
                <div className="property-group">
                  <label>Цвет текста:</label>
                  <input
                    type="color"
                    name="textColor"
                    value={selectedElement.props.textColor || '#ffffff'}
                    onChange={handleChange}
                  />
                </div>
              </>
            );
          case 'shape':
            return (
              <>
                <div className="property-group">
                  <label>Цвет фона:</label>
                  <input
                    type="color"
                    name="bgColor"
                    value={selectedElement.props.bgColor || '#ffc107'}
                    onChange={handleChange}
                  />
                </div>
                <div className="property-group">
                  <label>Скругление углов (px или %):</label>
                  <input
                    type="text"
                    name="borderRadius"
                    value={selectedElement.props.borderRadius || '0'}
                    onChange={handleChange}
                  />
                </div>
              </>
            );
          default:
            return null;
        }
      };

      return (
        <>
          <h3>Свойства элемента ({selectedElement.type})</h3>
          <div className="property-group">
            <label>X:</label>
            <input
              type="number"
              name="x"
              value={localX}
              onChange={handleDimensionChange}
            />
          </div>
          <div className="property-group">
            <label>Y:</label>
            <input
              type="number"
              name="y"
              value={localY}
              onChange={handleDimensionChange}
            />
          </div>
          <div className="property-group">
            <label>Ширина:</label>
            <input
              type="number"
              name="width"
              value={localWidth}
              onChange={handleDimensionChange}
            />
          </div>
          <div className="property-group">
            <label>Высота:</label>
            <input
              type="number"
              name="height"
              value={localHeight}
              onChange={handleDimensionChange}
            />
          </div>
          <hr />
          {renderProperties()}
        </>
      );
    } else {
      // Выбрано несколько элементов - показываем инструменты выравнивания/распределения
      return (
        <>
          <h3>Групповые операции ({selectedElementIds.length})</h3>
          <div className="group-actions">
            <h4>Выравнивание</h4>
            <div className="alignment-buttons">
              <button title="Выровнять по левому краю" onClick={() => alignElements('left')} disabled={selectedElementIds.length < 2}>
                <i className="fas fa-align-left"></i>
              </button>
              <button title="Выровнять по центру (горизонтально)" onClick={() => alignElements('center-h')} disabled={selectedElementIds.length < 2}>
                <i className="fas fa-align-center"></i>
              </button>
              <button title="Выровнять по правому краю" onClick={() => alignElements('right')} disabled={selectedElementIds.length < 2}>
                <i className="fas fa-align-right"></i>
              </button>
              <button title="Выровнять по верхнему краю" onClick={() => alignElements('top')} disabled={selectedElementIds.length < 2}>
                <i className="fas fa-align-top"></i>
              </button>
              <button title="Выровнять по середине (вертикально)" onClick={() => alignElements('center-v')} disabled={selectedElementIds.length < 2}>
                <i className="fas fa-align-middle"></i>
              </button>
              <button title="Выровнять по нижнему краю" onClick={() => alignElements('bottom')} disabled={selectedElementIds.length < 2}>
                <i className="fas fa-align-bottom"></i>
              </button>
            </div>
            <h4>Распределение</h4>
            <div className="distribution-buttons">
              <button title="Распределить горизонтально" onClick={() => distributeElements('horizontal')} disabled={selectedElementIds.length < 3}>
                <i className="fas fa-arrows-alt-h"></i>
              </button>
              <button title="Распределить вертикально" onClick={() => distributeElements('vertical')} disabled={selectedElementIds.length < 3}>
                <i className="fas fa-arrows-alt-v"></i>
              </button>
            </div>
          </div>
        </>
      );
    }
  };

  return (
    <div className="properties-panel">
      {renderPanelContent()}

      <div className="editor-actions">
        {selectedElementIds.length > 0 && (
          <button onClick={deleteSelectedElements} className="action-button delete-button">
            <i className="fas fa-trash-alt"></i> Удалить Выбранные ({selectedElementIds.length})
          </button>
        )}
        <button onClick={saveCanvas} className="action-button save-button">
          <i className="fas fa-save"></i> Сохранить Проект
        </button>
        <button onClick={clearCanvas} className="action-button clear-button">
          <i className="fas fa-trash-alt"></i> Очистить Канвас
        </button>
        <button onClick={exportToHtmlCss} className="action-button export-button">
          <i className="fas fa-file-export"></i> Экспорт в HTML/CSS
        </button>
        <hr />
        <button onClick={undo} disabled={!canUndo} className="action-button undo-button">
          <i className="fas fa-undo"></i> Отменить
        </button>
        <button onClick={redo} disabled={!canRedo} className="action-button redo-button">
          <i className="fas fa-redo"></i> Повторить
        </button>
      </div>
    </div>
  );
}

export default PropertiesPanel; 