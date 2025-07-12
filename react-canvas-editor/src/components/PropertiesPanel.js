import React, { useState, useEffect, useCallback } from 'react';
import '../styles/PropertiesPanel.css';
import { cssStringToObject, objectToCssString } from '../utils/exportUtils';

function PropertiesPanel({
  selectedElement,
  selectedElementIds,
  activeSelection,
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
  distributeElements,
  isAdmin,
  loadMySite,
  publishMySite,
  groupSelectedElements,
  ungroupElements,
  // NEW: Canvas background props
  canvasBackgroundColor,
  canvasBackgroundImage,
  canvasBackgroundRepeat,
  canvasBackgroundSize,
  canvasBackgroundPosition,
  updateCanvasBackground, // NEW: Setter for canvas background
}) {
  const [localContent, setLocalContent] = useState('');
  const [localFontSize, setLocalFontSize] = useState('');
  const [localColor, setLocalColor] = useState('');
  const [localSrc, setLocalSrc] = useState('');
  const [localAlt, setLocalAlt] = useState('');
  const [localLabel, setLocalLabel] = useState('');
  const [localBgColor, setLocalBgColor] = useState('');
  const [localTextColor, setLocalTextColor] = useState('');
  const [localBorderRadius, setLocalBorderRadius] = useState('');
  const [localCustomClasses, setLocalCustomClasses] = useState('');
  const [localCustomStyles, setLocalCustomStyles] = useState('');

  // States for general styling properties
  const [localBorderWidth, setLocalBorderWidth] = useState('');
  const [localBorderStyle, setLocalBorderStyle] = useState('');
  const [localBorderColor, setLocalBorderColor] = useState('');
  const [localBoxShadowX, setLocalBoxShadowX] = useState('');
  const [localBoxShadowY, setLocalBoxShadowY] = useState('');
  const [localBoxShadowBlur, setLocalBoxShadowBlur] = useState('');
  const [localBoxShadowSpread, setLocalBoxShadowSpread] = useState('');
  const [localBoxShadowColor, setLocalBoxShadowColor] = useState('');
  const [localBackgroundColor, setLocalBackgroundColor] = useState(''); // Element's background color
  const [localBackgroundImage, setLocalBackgroundImage] = useState(''); // Element's background image
  const [localBackgroundRepeat, setLocalBackgroundRepeat] = useState('');
  const [localBackgroundSize, setLocalBackgroundSize] = useState('');
  const [localBackgroundPosition, setLocalBackgroundPosition] = useState('');
  const [localZIndex, setLocalZIndex] = useState('');

  // Group properties
  const [localDisplayMode, setLocalDisplayMode] = useState('absolute');
  const [localFlexDirection, setLocalFlexDirection] = useState('row');
  const [localJustifyContent, setLocalJustifyContent] = useState('flex-start');
  const [localAlignItems, setLocalAlignItems] = useState('stretch');
  const [localGap, setLocalGap] = useState('0px');
  const [localGridTemplateColumns, setLocalGridTemplateColumns] = useState('1fr');
  const [localGridTemplateRows, setLocalGridTemplateRows] = useState('auto');
  const [localGridGap, setLocalGridGap] = useState('0px');

  useEffect(() => {
    if (selectedElement) {
      setLocalContent(selectedElement.props.content || '');
      setLocalFontSize(selectedElement.props.fontSize || '');
      setLocalColor(selectedElement.props.color || '');
      setLocalSrc(selectedElement.props.src || '');
      setLocalAlt(selectedElement.props.alt || '');
      setLocalLabel(selectedElement.props.label || '');
      setLocalBgColor(selectedElement.props.bgColor || '');
      setLocalTextColor(selectedElement.props.textColor || '');
      setLocalBorderRadius(selectedElement.props.borderRadius || '');
      setLocalCustomClasses((selectedElement.props.customClasses || []).join(' '));
      setLocalCustomStyles(objectToCssString(selectedElement.props.customStyles || {}));

      // Set local states for general styling
      setLocalBorderWidth(selectedElement.props.borderWidth || '0px');
      setLocalBorderStyle(selectedElement.props.borderStyle || 'solid');
      setLocalBorderColor(selectedElement.props.borderColor || '#000000');
      setLocalBoxShadowX(selectedElement.props.boxShadowX || '0px');
      setLocalBoxShadowY(selectedElement.props.boxShadowY || '0px');
      setLocalBoxShadowBlur(selectedElement.props.boxShadowBlur || '0px');
      setLocalBoxShadowSpread(selectedElement.props.boxShadowSpread || '0px');
      setLocalBoxShadowColor(selectedElement.props.boxShadowColor || 'rgba(0,0,0,0.2)');
      setLocalBackgroundColor(selectedElement.props.backgroundColor || '');
      setLocalBackgroundImage(selectedElement.props.backgroundImage || '');
      setLocalBackgroundRepeat(selectedElement.props.backgroundRepeat || 'no-repeat');
      setLocalBackgroundSize(selectedElement.props.backgroundSize || 'cover');
      setLocalBackgroundPosition(selectedElement.props.backgroundPosition || 'center center');
      setLocalZIndex(selectedElement.props.zIndex || 1);

      // Group properties
      setLocalDisplayMode(selectedElement.props.displayMode || 'absolute');
      setLocalFlexDirection(selectedElement.props.flexDirection || 'row');
      setLocalJustifyContent(selectedElement.props.justifyContent || 'flex-start');
      setLocalAlignItems(selectedElement.props.alignItems || 'stretch');
      setLocalGap(selectedElement.props.gap || '0px');
      setLocalGridTemplateColumns(selectedElement.props.gridTemplateColumns || '1fr');
      setLocalGridTemplateRows(selectedElement.props.gridTemplateRows || 'auto');
      setLocalGridGap(selectedElement.props.gridGap || '0px');

    } else {
      // Reset all local states when no element is selected
      setLocalContent('');
      setLocalFontSize('');
      setLocalColor('');
      setLocalSrc('');
      setLocalAlt('');
      setLocalLabel('');
      setLocalBgColor('');
      setLocalTextColor('');
      setLocalBorderRadius('');
      setLocalCustomClasses('');
      setLocalCustomStyles('');
      setLocalBorderWidth('');
      setLocalBorderStyle('');
      setLocalBorderColor('');
      setLocalBoxShadowX('');
      setLocalBoxShadowY('');
      setLocalBoxShadowBlur('');
      setLocalBoxShadowSpread('');
      setLocalBoxShadowColor('');
      setLocalBackgroundColor('');
      setLocalBackgroundImage('');
      setLocalBackgroundRepeat('');
      setLocalBackgroundSize('');
      setLocalBackgroundPosition('');
      setLocalZIndex('');
      setLocalDisplayMode('absolute');
      setLocalFlexDirection('row');
      setLocalJustifyContent('flex-start');
      setLocalAlignItems('stretch');
      setLocalGap('0px');
      setLocalGridTemplateColumns('1fr');
      setLocalGridTemplateRows('auto');
      setLocalGridGap('0px');
    }
  }, [selectedElement]);

  const handlePropChange = useCallback((propName, value) => {
    if (!selectedElement) return; // This function is only for element properties
    let parsedValue = value;

    // Special handling for number-like CSS properties
    if (['fontSize', 'gap', 'gridGap', 'borderWidth', 'boxShadowX', 'boxShadowY', 'boxShadowBlur', 'boxShadowSpread'].includes(propName)) {
        if (!isNaN(parseFloat(value)) && value.trim() !== '') {
            parsedValue = parseFloat(value) + (value.includes('px') || value.includes('%') || value.includes('em') || value.includes('rem') ? '' : 'px');
        } else if (value.trim() === '') {
            parsedValue = ''; // Allow empty string to clear the value
        } else {
            parsedValue = value; // Keep non-numeric values as is (e.g. "auto", "initial")
        }
    }
    if (propName === 'customClasses') {
        parsedValue = value.split(' ').filter(cls => cls.trim() !== '');
    } else if (propName === 'customStyles') {
        parsedValue = cssStringToObject(value);
    } else if (propName === 'zIndex') {
        parsedValue = parseInt(value, 10);
        if (isNaN(parsedValue)) parsedValue = 1; // Default to 1 if not a valid number
    }

    updateElementProps(selectedElement.id, { [propName]: parsedValue });
  }, [selectedElement, updateElementProps]);

  // NEW: handleCanvasBackgroundChange for canvas properties
  const handleCanvasBackgroundChange = useCallback((propName, value) => {
    updateCanvasBackground(propName, value);
  }, [updateCanvasBackground]);

  if (!selectedElement) {
    return (
      <div className="properties-panel">
        <h3>Свойства (ничего не выбрано)</h3>

        {/* NEW: Canvas/Page Settings */}
        <div className="property-section">
          <h4>Настройки страницы</h4>
          <div className="property-group">
            <label>Цвет фона канваса:</label>
            <input
                type="color"
                value={canvasBackgroundColor}
                onChange={(e) => handleCanvasBackgroundChange('backgroundColor', e.target.value)}
            />
          </div>
          <div className="property-group">
            <label>Фоновое изображение канваса (URL):</label>
            <input
                type="text"
                value={canvasBackgroundImage}
                onChange={(e) => handleCanvasBackgroundChange('backgroundImage', e.target.value)}
                placeholder="https://example.com/bg.jpg or /uploads/my_image.png"
            />
          </div>
          {canvasBackgroundImage && (
            <>
                <div className="property-group">
                    <label>Повтор фона:</label>
                    <select
                        value={canvasBackgroundRepeat}
                        onChange={(e) => handleCanvasBackgroundChange('backgroundRepeat', e.target.value)}
                    >
                        <option value="no-repeat">Нет повтора</option>
                        <option value="repeat">Повторять</option>
                        <option value="repeat-x">Повторять по X</option>
                        <option value="repeat-y">Повторять по Y</option>
                    </select>
                </div>
                <div className="property-group">
                    <label>Размер фона:</label>
                    <select
                        value={canvasBackgroundSize}
                        onChange={(e) => handleCanvasBackgroundChange('backgroundSize', e.target.value)}
                    >
                        <option value="auto">Авто</option>
                        <option value="cover">Покрыть</option>
                        <option value="contain">Вписать</option>
                    </select>
                </div>
                <div className="property-group">
                    <label>Позиция фона:</label>
                    <input
                        type="text"
                        value={canvasBackgroundPosition}
                        onChange={(e) => handleCanvasBackgroundChange('backgroundPosition', e.target.value)}
                        placeholder="center center"
                    />
                </div>
            </>
          )}
        </div>

        <hr /> {/* Separator for global actions */}

        <div className="button-group">
            <button onClick={saveCanvas}><i className="fas fa-save"></i> Сохранить Проект</button>
            <button onClick={clearCanvas}><i className="fas fa-eraser"></i> Очистить Канвас</button>
            <button onClick={exportToHtmlCss}><i className="fas fa-code"></i> Экспорт HTML/CSS</button>
        </div>
        <div className="button-group">
            <button onClick={undo} disabled={!canUndo}><i className="fas fa-undo"></i> Отменить</button>
            <button onClick={redo} disabled={!canRedo}><i className="fas fa-redo"></i> Повторить</button>
        </div>

        {isAdmin && (
            <div className="admin-actions">
                <h4>Админ действия</h4>
                <button onClick={loadMySite}><i className="fas fa-cloud-download-alt"></i> Загрузить мой сайт</button>
                <button onClick={publishMySite}><i className="fas fa-cloud-upload-alt"></i> Опубликовать мой сайт</button>
            </div>
        )}
      </div>
    );
  }

  const isGroup = selectedElement.type === 'group';
  const isImage = selectedElement.type === 'image';

  return (
    <div className="properties-panel">
      <h3>Свойства элемента: {selectedElement.props.name || selectedElement.type}</h3>

      {/* General Properties */}
      <div className="property-section">
        <h4>Общие</h4>
        <div className="property-group">
          <label>ID:</label>
          <input type="text" value={selectedElement.id} readOnly />
        </div>
        <div className="property-group">
          <label>Имя:</label>
          <input
            type="text"
            value={selectedElement.props.name || ''}
            onChange={(e) => handlePropChange('name', e.target.value)}
          />
        </div>
        <div className="property-group">
          <label>X:</label>
          <input
            type="number"
            value={selectedElement.x}
            onChange={(e) => updateElement(selectedElement.id, { x: parseFloat(e.target.value) })}
          />
        </div>
        <div className="property-group">
          <label>Y:</label>
          <input
            type="number"
            value={selectedElement.y}
            onChange={(e) => updateElement(selectedElement.id, { y: parseFloat(e.target.value) })}
          />
        </div>
        <div className="property-group">
          <label>Ширина:</label>
          <input
            type="number"
            value={selectedElement.width}
            onChange={(e) => updateElement(selectedElement.id, { width: parseFloat(e.target.value) })}
          />
        </div>
        <div className="property-group">
          <label>Высота:</label>
          <input
            type="number"
            value={selectedElement.height}
            onChange={(e) => updateElement(selectedElement.id, { height: parseFloat(e.target.value) })}
          />
        </div>
        <div className="property-group">
          <label>Z-Index:</label>
          <input
            type="number"
            value={localZIndex}
            onChange={(e) => {
                setLocalZIndex(e.target.value);
                handlePropChange('zIndex', e.target.value);
            }}
          />
        </div>
      </div>

      {/* Type-Specific Properties */}
      {selectedElement.type === 'text' && (
        <div className="property-section">
          <h4>Текст</h4>
          <div className="property-group">
            <label>Содержимое:</label>
            <textarea
              value={localContent}
              onChange={(e) => { setLocalContent(e.target.value); handlePropChange('content', e.target.value); }}
            />
          </div>
          <div className="property-group">
            <label>Размер шрифта:</label>
            <input
              type="text"
              value={localFontSize}
              onChange={(e) => { setLocalFontSize(e.target.value); handlePropChange('fontSize', e.target.value); }}
              placeholder="16px"
            />
          </div>
          <div className="property-group">
            <label>Цвет:</label>
            <input
              type="color"
              value={localColor}
              onChange={(e) => { setLocalColor(e.target.value); handlePropChange('color', e.target.value); }}
            />
          </div>
        </div>
      )}

      {isImage && (
        <div className="property-section">
          <h4>Изображение</h4>
          <div className="property-group">
            <label>URL Источника (src):</label>
            <input
              type="text"
              value={localSrc}
              onChange={(e) => { setLocalSrc(e.target.value); handlePropChange('src', e.target.value); }}
              placeholder="https://via.placeholder.com/150"
            />
          </div>
          <div className="property-group">
            <label>Alt-текст:</label>
            <input
              type="text"
              value={localAlt}
              onChange={(e) => { setLocalAlt(e.target.value); handlePropChange('alt', e.target.value); }}
              placeholder="Описание изображения"
            />
          </div>
        </div>
      )}

      {selectedElement.type === 'button' && (
        <div className="property-section">
          <h4>Кнопка</h4>
          <div className="property-group">
            <label>Текст кнопки:</label>
            <input
              type="text"
              value={localLabel}
              onChange={(e) => { setLocalLabel(e.target.value); handlePropChange('label', e.target.value); }}
            />
          </div>
          <div className="property-group">
            <label>Цвет фона:</label>
            <input
              type="color"
              value={localBgColor}
              onChange={(e) => { setLocalBgColor(e.target.value); handlePropChange('bgColor', e.target.value); }}
            />
          </div>
          <div className="property-group">
            <label>Цвет текста:</label>
            <input
              type="color"
              value={localTextColor}
              onChange={(e) => { setLocalTextColor(e.target.value); handlePropChange('textColor', e.target.value); }}
            />
          </div>
        </div>
      )}

      {selectedElement.type === 'shape' && (
        <div className="property-section">
          <h4>Фигура</h4>
          <div className="property-group">
            <label>Цвет фона:</label>
            <input
              type="color"
              value={localBgColor}
              onChange={(e) => { setLocalBgColor(e.target.value); handlePropChange('bgColor', e.target.value); }}
            />
          </div>
          <div className="property-group">
            <label>Радиус скругления:</label>
            <input
              type="text"
              value={localBorderRadius}
              onChange={(e) => { setLocalBorderRadius(e.target.value); handlePropChange('borderRadius', e.target.value); }}
              placeholder="0px or 50%"
            />
          </div>
        </div>
      )}

      {isGroup && (
        <div className="property-section">
            <h4>Группа (Контейнер)</h4>
            <div className="property-group">
                <label>Режим отображения:</label>
                <select value={localDisplayMode} onChange={(e) => { setLocalDisplayMode(e.target.value); handlePropChange('displayMode', e.target.value); }}>
                    <option value="absolute">Абсолютный</option>
                    <option value="flex">Flexbox</option>
                    <option value="grid">Grid</option>
                </select>
            </div>
            {localDisplayMode === 'flex' && (
                <>
                    <div className="property-group">
                        <label>Направление Flex:</label>
                        <select value={localFlexDirection} onChange={(e) => { setLocalFlexDirection(e.target.value); handlePropChange('flexDirection', e.target.value); }}>
                            <option value="row">Ряд</option>
                            <option value="column">Колонка</option>
                        </select>
                    </div>
                    <div className="property-group">
                        <label>Выравнивание по главной оси:</label>
                        <select value={localJustifyContent} onChange={(e) => { setLocalJustifyContent(e.target.value); handlePropChange('justifyContent', e.target.value); }}>
                            <option value="flex-start">Начало</option>
                            <option value="flex-end">Конец</option>
                            <option value="center">Центр</option>
                            <option value="space-between">По краям</option>
                            <option value="space-around">Вокруг</option>
                            <option value="space-evenly">Равномерно</option>
                        </select>
                    </div>
                    <div className="property-group">
                        <label>Выравнивание по поперечной оси:</label>
                        <select value={localAlignItems} onChange={(e) => { setLocalAlignItems(e.target.value); handlePropChange('alignItems', e.target.value); }}>
                            <option value="stretch">Растянуть</option>
                            <option value="flex-start">Начало</option>
                            <option value="flex-end">Конец</option>
                            <option value="center">Центр</option>
                            <option value="baseline">Базовая линия</option>
                        </select>
                    </div>
                    <div className="property-group">
                        <label>Зазор (gap):</label>
                        <input
                            type="text"
                            value={localGap}
                            onChange={(e) => { setLocalGap(e.target.value); handlePropChange('gap', e.target.value); }}
                            placeholder="10px"
                        />
                    </div>
                </>
            )}
            {localDisplayMode === 'grid' && (
                <>
                    <div className="property-group">
                        <label>Шаблон колонок (grid-template-columns):</label>
                        <input
                            type="text"
                            value={localGridTemplateColumns}
                            onChange={(e) => { setLocalGridTemplateColumns(e.target.value); handlePropChange('gridTemplateColumns', e.target.value); }}
                            placeholder="1fr 1fr"
                        />
                    </div>
                    <div className="property-group">
                        <label>Шаблон строк (grid-template-rows):</label>
                        <input
                            type="text"
                            value={localGridTemplateRows}
                            onChange={(e) => { setLocalGridTemplateRows(e.target.value); handlePropChange('gridTemplateRows', e.target.value); }}
                            placeholder="auto auto"
                        />
                    </div>
                    <div className="property-group">
                        <label>Зазор сетки (grid-gap):</label>
                        <input
                            type="text"
                            value={localGridGap}
                            onChange={(e) => { setLocalGridGap(e.target.value); handlePropChange('gridGap', e.target.value); }}
                            placeholder="10px"
                        />
                    </div>
                </>
            )}
        </div>
      )}

      {/* Styling Properties (for selected element) */}
      <div className="property-section">
        <h4>Стилизация элемента</h4>
        {/* Background */}
        <div className="property-group">
            <label>Цвет фона:</label>
            <input
                type="color"
                value={localBackgroundColor}
                onChange={(e) => { setLocalBackgroundColor(e.target.value); handlePropChange('backgroundColor', e.target.value); }}
            />
        </div>
        <div className="property-group">
            <label>Фоновое изображение (URL):</label>
            <input
                type="text"
                value={localBackgroundImage}
                onChange={(e) => { setLocalBackgroundImage(e.target.value); handlePropChange('backgroundImage', e.target.value); }}
                placeholder="https://example.com/bg.jpg or /uploads/my_image.png"
            />
        </div>
        {localBackgroundImage && (
            <>
                <div className="property-group">
                    <label>Повтор фона:</label>
                    <select
                        value={localBackgroundRepeat}
                        onChange={(e) => { setLocalBackgroundRepeat(e.target.value); handlePropChange('backgroundRepeat', e.target.value); }}
                    >
                        <option value="no-repeat">Нет повтора</option>
                        <option value="repeat">Повторять</option>
                        <option value="repeat-x">Повторять по X</option>
                        <option value="repeat-y">Повторять по Y</option>
                    </select>
                </div>
                <div className="property-group">
                    <label>Размер фона:</label>
                    <select
                        value={localBackgroundSize}
                        onChange={(e) => { setLocalBackgroundSize(e.target.value); handlePropChange('backgroundSize', e.target.value); }}
                    >
                        <option value="auto">Авто</option>
                        <option value="cover">Покрыть</option>
                        <option value="contain">Вписать</option>
                    </select>
                </div>
                <div className="property-group">
                    <label>Позиция фона:</label>
                    <input
                        type="text"
                        value={localBackgroundPosition}
                        onChange={(e) => { setLocalBackgroundPosition(e.target.value); handlePropChange('backgroundPosition', e.target.value); }}
                        placeholder="center center"
                    />
                </div>
            </>
        )}

        {/* Border */}
        <div className="property-group">
            <label>Толщина границы:</label>
            <input
                type="text"
                value={localBorderWidth}
                onChange={(e) => { setLocalBorderWidth(e.target.value); handlePropChange('borderWidth', e.target.value); }}
                placeholder="1px"
            />
        </div>
        <div className="property-group">
            <label>Стиль границы:</label>
            <select
                value={localBorderStyle}
                onChange={(e) => { setLocalBorderStyle(e.target.value); handlePropChange('borderStyle', e.target.value); }}
            >
                <option value="none">Нет</option>
                <option value="solid">Сплошная</option>
                <option value="dashed">Пунктирная</option>
                <option value="dotted">Точечная</option>
                <option value="double">Двойная</option>
            </select>
        </div>
        <div className="property-group">
            <label>Цвет границы:</label>
            <input
                type="color"
                value={localBorderColor}
                onChange={(e) => { setLocalBorderColor(e.target.value); handlePropChange('borderColor', e.target.value); }}
            />
        </div>

        {/* Box Shadow */}
        <div className="property-group">
            <label>Тень (X Y Blur Spread Color):</label>
            <div style={{ display: 'flex', gap: '5px' }}>
                <input
                    type="text"
                    value={localBoxShadowX}
                    onChange={(e) => { setLocalBoxShadowX(e.target.value); handlePropChange('boxShadowX', e.target.value); }}
                    placeholder="X (px)" style={{ width: '20%' }}
                />
                <input
                    type="text"
                    value={localBoxShadowY}
                    onChange={(e) => { setLocalBoxShadowY(e.target.value); handlePropChange('boxShadowY', e.target.value); }}
                    placeholder="Y (px)" style={{ width: '20%' }}
                />
                <input
                    type="text"
                    value={localBoxShadowBlur}
                    onChange={(e) => { setLocalBoxShadowBlur(e.target.value); handlePropChange('boxShadowBlur', e.target.value); }}
                    placeholder="Blur (px)" style={{ width: '20%' }}
                />
                <input
                    type="text"
                    value={localBoxShadowSpread}
                    onChange={(e) => { setLocalBoxShadowSpread(e.target.value); handlePropChange('boxShadowSpread', e.target.value); }}
                    placeholder="Spread (px)" style={{ width: '20%' }}
                />
                <input
                    type="color"
                    value={localBoxShadowColor}
                    onChange={(e) => { setLocalBoxShadowColor(e.target.value); handlePropChange('boxShadowColor', e.target.value); }}
                    style={{ width: '15%' }}
                />
            </div>
        </div>
      </div>

      {/* Advanced Properties */}
      <div className="property-section">
        <h4>Дополнительно</h4>
        <div className="property-group">
          <label>Пользовательские классы (через пробел):</label>
          <input
            type="text"
            value={localCustomClasses}
            onChange={(e) => { setLocalCustomClasses(e.target.value); handlePropChange('customClasses', e.target.value); }}
            placeholder="my-class another-class"
          />
        </div>
        <div className="property-group">
          <label>Пользовательские стили (CSS):</label>
          <textarea
            value={localCustomStyles}
            onChange={(e) => { setLocalCustomStyles(e.target.value); handlePropChange('customStyles', e.target.value); }}
            rows="5"
            placeholder="font-weight: bold; margin-top: 10px;"
          />
        </div>
      </div>

      {/* Actions for Selected Element */}
      <div className="property-section">
        <h4>Действия</h4>
        <div className="button-group">
            <button onClick={deleteSelectedElements}><i className="fas fa-trash"></i> Удалить Выбранные</button>
            <button onClick={groupSelectedElements} disabled={activeSelection.ids.length < 2 || activeSelection.elements.some(el => el.type === 'group' || (el.parentId && selectedElementIds.includes(el.parentId)))}>
                <i className="fas fa-layer-group"></i> Группировать
            </button>
            <button onClick={() => ungroupElements(selectedElement.type === 'group' ? selectedElement.id : selectedElement.parentId)} disabled={!isGroup && !selectedElement.parentId}>
                <i className="fas fa-object-ungroup"></i> Разгруппировать
            </button>
        </div>
        <div className="button-group">
            <button onClick={() => alignElements('left')} disabled={activeSelection.elements.length < 2}><i className="fas fa-align-left"></i> Выровнять по левому</button>
            <button onClick={() => alignElements('center-h')} disabled={activeSelection.elements.length < 2}><i className="fas fa-align-center"></i> Выровнять по центру (Г)</button>
            <button onClick={() => alignElements('right')} disabled={activeSelection.elements.length < 2}><i className="fas fa-align-right"></i> Выровнять по правому</button>
            <button onClick={() => alignElements('top')} disabled={activeSelection.elements.length < 2}><i className="fas fa-align-top"></i> Выровнять по верхнему</button>
            <button onClick={() => alignElements('center-v')} disabled={activeSelection.elements.length < 2}><i className="fas fa-align-center"></i> Выровнять по центру (В)</button>
            <button onClick={() => alignElements('bottom')} disabled={activeSelection.elements.length < 2}><i className="fas fa-align-bottom"></i> Выровнять по нижнему</button>
        </div>
        <div className="button-group">
            <button onClick={() => distributeElements('horizontal')} disabled={activeSelection.elements.length < 3}><i className="fas fa-arrows-alt-h"></i> Распределить (Г)</button>
            <button onClick={() => distributeElements('vertical')} disabled={activeSelection.elements.length < 3}><i className="fas fa-arrows-alt-v"></i> Распределить (В)</button>
        </div>
      </div>

      <hr />

      {/* Global Actions (always visible) */}
      <div className="button-group">
          <button onClick={saveCanvas}><i className="fas fa-save"></i> Сохранить Проект</button>
          <button onClick={clearCanvas}><i className="fas fa-eraser"></i> Очистить Канвас</button>
          <button onClick={exportToHtmlCss}><i className="fas fa-code"></i> Экспорт HTML/CSS</button>
      </div>
      <div className="button-group">
          <button onClick={undo} disabled={!canUndo}><i className="fas fa-undo"></i> Отменить</button>
          <button onClick={redo} disabled={!canRedo}><i className="fas fa-redo"></i> Повторить</button>
      </div>

      {isAdmin && (
          <div className="admin-actions">
              <h4>Админ действия</h4>
              <button onClick={loadMySite}><i className="fas fa-cloud-download-alt"></i> Загрузить мой сайт</button>
              <button onClick={publishMySite}><i className="fas fa-cloud-upload-alt"></i> Опубликовать мой сайт</button>
          </div>
      )}
    </div>
  );
}

export default PropertiesPanel; 