import React, { useCallback, useState, useEffect } from 'react';
import '../styles/PropertiesPanel.css';
import { cssStringToObject, objectToCssString } from '../utils/exportUtils';

function PropertiesPanel({ selectedElement, selectedElementIds, activeSelection, updateElementProps, updateElement, saveCanvas, clearCanvas, exportToHtmlCss, undo, redo, canUndo, canRedo, deleteSelectedElements, alignElements, distributeElements, isAdmin, loadMySite, publishMySite, groupSelectedElements, ungroupElements }) {
  const [localX, setLocalX] = useState('');
  const [localY, setLocalY] = useState('');
  const [localWidth, setLocalWidth] = useState('');
  const [localHeight, setLocalHeight] = useState('');
  const [localCustomClasses, setLocalCustomClasses] = useState('');
  const [localCustomStyles, setLocalCustomStyles] = useState('');
  const [localDisplayMode, setLocalDisplayMode] = useState('absolute');
  const [localFlexDirection, setLocalFlexDirection] = useState('row');
  const [localJustifyContent, setLocalJustifyContent] = useState('flex-start');
  const [localAlignItems, setLocalAlignItems] = useState('stretch');
  const [localGap, setLocalGap] = useState('0px');

  const elementForSingleProperties = selectedElementIds.length === 1 && selectedElement && selectedElement.type !== 'group'
    ? selectedElement
    : null;
  const groupForProperties = selectedElementIds.length === 1 && selectedElement && selectedElement.type === 'group'
    ? selectedElement
    : null;

  useEffect(() => {
    const elementToDisplay = groupForProperties || elementForSingleProperties;
    if (elementToDisplay) {
      setLocalX(Math.round(elementToDisplay.x).toString());
      setLocalY(Math.round(elementToDisplay.y).toString());
      setLocalWidth(Math.round(elementToDisplay.width).toString());
      setLocalHeight(Math.round(elementToDisplay.height).toString());
      setLocalCustomClasses(elementToDisplay.props.customClasses ? elementToDisplay.props.customClasses.join(' ') : '');
      setLocalCustomStyles(elementToDisplay.props.customStyles ? objectToCssString(elementToDisplay.props.customStyles) : '');
      if (elementToDisplay.type === 'group') {
        setLocalDisplayMode(elementToDisplay.props.displayMode || 'absolute');
        setLocalFlexDirection(elementToDisplay.props.flexDirection || 'row');
        setLocalJustifyContent(elementToDisplay.props.justifyContent || 'flex-start');
        setLocalAlignItems(elementToDisplay.props.alignItems || 'stretch');
        setLocalGap(elementToDisplay.props.gap || '0px');
      } else {
        setLocalDisplayMode('absolute');
        setLocalFlexDirection('row');
        setLocalJustifyContent('flex-start');
        setLocalAlignItems('stretch');
        setLocalGap('0px');
      }
    } else {
      setLocalX('');
      setLocalY('');
      setLocalWidth('');
      setLocalHeight('');
      setLocalCustomClasses('');
      setLocalCustomStyles('');
      setLocalDisplayMode('absolute');
      setLocalFlexDirection('row');
      setLocalJustifyContent('flex-start');
      setLocalAlignItems('stretch');
      setLocalGap('0px');
    }
  }, [elementForSingleProperties, groupForProperties]);

  const handleChange = useCallback((e) => {
    const { name, value, type, checked } = e.target;
    const targetElement = groupForProperties || elementForSingleProperties;
    if (!targetElement) return;
    if (name === 'customClasses') {
        setLocalCustomClasses(value);
        updateElementProps(targetElement.id, { [name]: value.split(' ').filter(cls => cls.trim() !== '') });
    } else if (name === 'customStyles') {
        setLocalCustomStyles(value);
        updateElementProps(targetElement.id, { [name]: cssStringToObject(value) });
    } else if (name === 'displayMode') {
        setLocalDisplayMode(value);
        updateElementProps(targetElement.id, { [name]: value });
    } else if (name === 'flexDirection') {
        setLocalFlexDirection(value);
        updateElementProps(targetElement.id, { [name]: value });
    } else if (name === 'justifyContent') {
        setLocalJustifyContent(value);
        updateElementProps(targetElement.id, { [name]: value });
    } else if (name === 'alignItems') {
        setLocalAlignItems(value);
        updateElementProps(targetElement.id, { [name]: value });
    } else if (name === 'gap') {
        setLocalGap(value);
        updateElementProps(targetElement.id, { [name]: value });
    } else {
        updateElementProps(targetElement.id, { [name]: type === 'checkbox' ? checked : value });
    }
  }, [elementForSingleProperties, groupForProperties, updateElementProps]);

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
    const targetElement = groupForProperties || elementForSingleProperties;
    if (!isNaN(numValue) && targetElement) {
      updateElement(targetElement.id, { [name]: numValue });
    }
  }, [elementForSingleProperties, groupForProperties, updateElement]);

  const renderSingleElementProperties = () => {
    if (!elementForSingleProperties) return null;
    switch (elementForSingleProperties.type) {
      case 'text':
        return (
          <>
            <div className="property-group">
              <label>Содержимое:</label>
              <textarea
                name="content"
                value={elementForSingleProperties.props.content || ''}
                onChange={handleChange}
              />
            </div>
            <div className="property-group">
              <label>Размер шрифта:</label>
              <input
                type="text"
                name="fontSize"
                value={elementForSingleProperties.props.fontSize || ''}
                onChange={handleChange}
              />
            </div>
            <div className="property-group">
              <label>Цвет текста:</label>
              <input
                type="color"
                name="color"
                value={elementForSingleProperties.props.color || '#000000'}
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
                value={elementForSingleProperties.props.src || ''}
                onChange={handleChange}
              />
            </div>
            <div className="property-group">
              <label>Alt текст:</label>
              <input
                type="text"
                name="alt"
                value={elementForSingleProperties.props.alt || ''}
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
                value={elementForSingleProperties.props.label || ''}
                onChange={handleChange}
              />
            </div>
            <div className="property-group">
              <label>Цвет фона:</label>
              <input
                type="color"
                name="bgColor"
                value={elementForSingleProperties.props.bgColor || '#007bff'}
                onChange={handleChange}
              />
            </div>
            <div className="property-group">
              <label>Цвет текста:</label>
              <input
                type="color"
                name="textColor"
                value={elementForSingleProperties.props.textColor || '#ffffff'}
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
                value={elementForSingleProperties.props.bgColor || '#ffc107'}
                onChange={handleChange}
              />
            </div>
            <div className="property-group">
              <label>Скругление углов (px или %):</label>
              <input
                type="text"
                name="borderRadius"
                value={elementForSingleProperties.props.borderRadius || '0'}
                onChange={handleChange}
              />
            </div>
          </>
        );
      default:
        return null;
    }
  };

  const renderPanelContent = () => {
    const targetElement = groupForProperties || elementForSingleProperties;
    if (!targetElement) {
        if (selectedElementIds.length > 1) {
            const hasGroupSelected = activeSelection.elements.some(el => el.type === 'group');
            const canUngroup = activeSelection.elements.some(el => el.type === 'group' || el.parentId);
            return (
                <>
                    <h3>Групповые операции ({activeSelection.elements.length})</h3>
                    <div className="group-actions">
                        <h4>Группировка</h4>
                        <div className="grouping-buttons">
                            <button
                                title="Группировать выбранные элементы (Ctrl/Cmd + G)"
                                onClick={groupSelectedElements}
                                disabled={activeSelection.elements.length < 2 || hasGroupSelected}
                            >
                                <i className="fas fa-object-group"></i> Группировать
                            </button>
                            <button
                                title="Разгруппировать выбранную группу (Ctrl/Cmd + Shift + G)"
                                onClick={() => ungroupElements(activeSelection.elements.find(el => el.type === 'group' || el.parentId)?.type === 'group' ? activeSelection.elements.find(el => el.type === 'group' || el.parentId).id : activeSelection.elements.find(el => el.parentId)?.parentId)}
                                disabled={!canUngroup}
                            >
                                <i className="fas fa-object-ungroup"></i> Разгруппировать
                            </button>
                        </div>
                        <hr/>
                        <h4>Выравнивание</h4>
                        <div className="alignment-buttons">
                            <button title="Выровнять по левому краю" onClick={() => alignElements('left')} disabled={activeSelection.elements.filter(el => el.type !== 'group').length < 2}><i className="fas fa-align-left"></i></button>
                            <button title="Выровнять по центру (горизонтально)" onClick={() => alignElements('center-h')} disabled={activeSelection.elements.filter(el => el.type !== 'group').length < 2}><i className="fas fa-align-center"></i></button>
                            <button title="Выровнять по правому краю" onClick={() => alignElements('right')} disabled={activeSelection.elements.filter(el => el.type !== 'group').length < 2}><i className="fas fa-align-right"></i></button>
                            <button title="Выровнять по верхнему краю" onClick={() => alignElements('top')} disabled={activeSelection.elements.filter(el => el.type !== 'group').length < 2}><i className="fas fa-align-top"></i></button>
                            <button title="Выровнять по середине (вертикально)" onClick={() => alignElements('center-v')} disabled={activeSelection.elements.filter(el => el.type !== 'group').length < 2}><i className="fas fa-align-middle"></i></button>
                            <button title="Выровнять по нижнему краю" onClick={() => alignElements('bottom')} disabled={activeSelection.elements.filter(el => el.type !== 'group').length < 2}><i className="fas fa-align-bottom"></i></button>
                        </div>
                        <h4>Распределение</h4>
                        <div className="distribution-buttons">
                            <button title="Распределить горизонтально" onClick={() => distributeElements('horizontal')} disabled={activeSelection.elements.filter(el => el.type !== 'group').length < 3}><i className="fas fa-arrows-alt-h"></i></button>
                            <button title="Распределить вертикально" onClick={() => distributeElements('vertical')} disabled={activeSelection.elements.filter(el => el.type !== 'group').length < 3}><i className="fas fa-arrows-alt-v"></i></button>
                        </div>
                    </div>
                </>
            );
        }
        return (
            <>
                <h3>Свойства</h3>
                <p>Выберите элемент на канвасе для редактирования его свойств.</p>
            </>
        );
    } else {
        return (
            <>
                <h3>Свойства {targetElement.type === 'group' ? `Группы (${targetElement.props.name || targetElement.id.substring(0,4)})` : `элемента (${targetElement.type})`}</h3>
                <div className="property-group">
                    <label>Имя:</label>
                    <input
                        type="text"
                        name="name"
                        value={targetElement.props.name || ''}
                        onChange={handleChange}
                    />
                </div>
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
                <div className="property-group">
                    <label>Пользовательские классы (через пробел):</label>
                    <input
                        type="text"
                        name="customClasses"
                        value={localCustomClasses}
                        onChange={handleChange}
                        placeholder="my-class another-class"
                    />
                </div>
                <div className="property-group">
                    <label>Пользовательские инлайн-стили (CSS):</label>
                    <textarea
                        name="customStyles"
                        value={localCustomStyles}
                        onChange={handleChange}
                        placeholder="color: red; font-size: 16px;"
                        rows="4"
                    />
                </div>
                <hr />
                {targetElement.type !== 'group' && renderSingleElementProperties()}
                {targetElement.type === 'group' && (
                    <>
                        <h4>Настройки макета группы</h4>
                        <div className="property-group">
                            <label>Режим отображения:</label>
                            <select name="displayMode" value={localDisplayMode} onChange={handleChange}>
                                <option value="absolute">Абсолютный</option>
                                <option value="flex">Flexbox</option>
                            </select>
                        </div>
                        {localDisplayMode === 'flex' && (
                            <>
                                <div className="property-group">
                                    <label>Направление Flex:</label>
                                    <select name="flexDirection" value={localFlexDirection} onChange={handleChange}>
                                        <option value="row">Ряд (row)</option>
                                        <option value="column">Колонка (column)</option>
                                        <option value="row-reverse">Ряд обратный (row-reverse)</option>
                                        <option value="column-reverse">Колонка обратная (column-reverse)</option>
                                    </select>
                                </div>
                                <div className="property-group">
                                    <label>Выравнивание по главной оси (justify-content):</label>
                                    <select name="justifyContent" value={localJustifyContent} onChange={handleChange}>
                                        <option value="flex-start">Начало (flex-start)</option>
                                        <option value="flex-end">Конец (flex-end)</option>
                                        <option value="center">Центр (center)</option>
                                        <option value="space-between">Между (space-between)</option>
                                        <option value="space-around">Вокруг (space-around)</option>
                                        <option value="space-evenly">Равномерно (space-evenly)</option>
                                    </select>
                                </div>
                                <div className="property-group">
                                    <label>Выравнивание по поперечной оси (align-items):</label>
                                    <select name="alignItems" value={localAlignItems} onChange={handleChange}>
                                        <option value="stretch">Растянуть (stretch)</option>
                                        <option value="flex-start">Начало (flex-start)</option>
                                        <option value="flex-end">Конец (flex-end)</option>
                                        <option value="center">Центр (center)</option>
                                        <option value="baseline">Базовая линия (baseline)</option>
                                    </select>
                                </div>
                                <div className="property-group">
                                    <label>Отступ между элементами (gap):</label>
                                    <input
                                        type="text"
                                        name="gap"
                                        value={localGap}
                                        onChange={handleChange}
                                        placeholder="10px or 1em"
                                    />
                                </div>
                            </>
                        )}
                        <hr />
                    </>
                )}
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
        {isAdmin && (
            <>
                <hr />
                <button onClick={loadMySite} className="action-button admin-load-button">
                    <i className="fas fa-download"></i> Загрузить Мой Сайт
                </button>
                <button onClick={publishMySite} className="action-button admin-publish-button">
                    <i className="fas fa-upload"></i> Опубликовать Мой Сайт
                </button>
            </>
        )}
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