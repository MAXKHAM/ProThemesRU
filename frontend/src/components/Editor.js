import React, { useState, useRef, useEffect, useCallback } from 'react';
import Header from './Header';
import Sidebar from './Sidebar';
import Canvas from './Canvas';
import PropertiesPanel from './PropertiesPanel';
import AIColorPaletteGenerator from './AIColorPaletteGenerator';
import LayersPanel from './LayersPanel';
import { generateUniqueId } from '../utils/idGenerator';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import logo from '../assets/logo.png';
import { generateHtmlCss } from '../utils/exportUtils';
import Footer from './Footer';
import FloatingCart from './FloatingCart';
import FloatingCalculator from './FloatingCalculator';
import FloatingLogo from './FloatingLogo';

const MAX_HISTORY_SIZE = 50;

function Editor() {
  const [elements, setElements] = useState([]);
  const [selectedElementIds, setSelectedElementIds] = useState([]);
  const canvasRef = useRef(null);

  const [history, setHistory] = useState([[]]);
  const [historyIndex, setHistoryIndex] = useState(0);

  useEffect(() => {
    if (history[historyIndex] === elements) {
        return;
    }

    const newHistory = history.slice(0, historyIndex + 1);
    newHistory.push(elements);

    if (newHistory.length > MAX_HISTORY_SIZE) {
        newHistory.shift();
    }

    setHistory(newHistory);
    setHistoryIndex(newHistory.length - 1);
  }, [elements, history, historyIndex]);

  useEffect(() => {
    try {
      const savedElements = localStorage.getItem('canvasElements');
      if (savedElements) {
        let loadedElements = JSON.parse(savedElements);
        // Ensure loaded elements have parentId, customClasses, customStyles, and new flex properties
        loadedElements = loadedElements.map(el => ({
            ...el,
            parentId: el.parentId === undefined ? null : el.parentId,
            props: {
                ...(el.props || {}),
                customClasses: el.props && el.props.customClasses === undefined ? [] : el.props.customClasses,
                customStyles: el.props && el.props.customStyles === undefined ? {} : el.props.customStyles,
                // NEW: Default for flex properties for groups
                displayMode: el.type === 'group' && el.props && el.props.displayMode === undefined ? 'absolute' : (el.props ? el.props.displayMode : undefined),
                flexDirection: el.type === 'group' && el.props && el.props.flexDirection === undefined ? 'row' : (el.props ? el.props.flexDirection : undefined),
                justifyContent: el.type === 'group' && el.props && el.props.justifyContent === undefined ? 'flex-start' : (el.props ? el.props.justifyContent : undefined),
                alignItems: el.type === 'group' && el.props && el.props.alignItems === undefined ? 'stretch' : (el.props ? el.props.alignItems : undefined),
                gap: el.type === 'group' && el.props && el.props.gap === undefined ? '0px' : (el.props ? el.props.gap : undefined),
            }
        }));
        setElements(loadedElements);
        setHistory([loadedElements]);
        setHistoryIndex(0);
      }
    } catch (e) {
      console.error("Failed to load elements from localStorage", e);
    }
  }, []);

  const selectedElement = selectedElementIds.length > 0
    ? elements.find(el => el.id === selectedElementIds[0])
    : null;

  const addElement = useCallback((type, x = 100, y = 100) => {
    const newElement = {
      id: generateUniqueId(),
      type,
      x,
      y,
      width: 150,
      height: 50,
      parentId: null,
      props: {
        name: `${type.charAt(0).toUpperCase() + type.slice(1)} ${elements.filter(el => el.type !== 'group').length + 1}`,
        customClasses: [],
        customStyles: {},
      },
    };
    switch (type) {
      case 'text':
        newElement.props = { ...newElement.props, content: 'Новый текст', fontSize: '16px', color: '#000000' };
        newElement.width = 200;
        newElement.height = 40;
        break;
      case 'image':
        newElement.props = { ...newElement.props, src: 'https://via.placeholder.com/150', alt: 'Изображение' };
        newElement.width = 150;
        newElement.height = 150;
        break;
      case 'button':
        newElement.props = { ...newElement.props, label: 'Кнопка', bgColor: '#007bff', textColor: '#ffffff' };
        newElement.width = 120;
        newElement.height = 40;
        break;
      case 'shape':
        newElement.props = { ...newElement.props, bgColor: '#ffc107', borderRadius: '0' };
        newElement.width = 100;
        newElement.height = 100;
        break;
      case 'video':
        newElement.props = { ...newElement.props, src: 'https://www.w3schools.com/html/mov_bbb.mp4' };
        newElement.width = 320;
        newElement.height = 180;
        break;
      case 'form':
        newElement.props = { ...newElement.props, fields: [{ type: 'text', placeholder: 'Ваше имя' }, { type: 'email', placeholder: 'Email' }], submitLabel: 'Отправить' };
        newElement.width = 250;
        newElement.height = 120;
        break;
      case 'slider':
        newElement.props = { ...newElement.props, images: ['https://via.placeholder.com/300x150', 'https://via.placeholder.com/300x151'] };
        newElement.width = 300;
        newElement.height = 150;
        break;
      case 'gallery':
        newElement.props = { ...newElement.props, images: ['https://via.placeholder.com/100', 'https://via.placeholder.com/101', 'https://via.placeholder.com/102', 'https://via.placeholder.com/103'] };
        newElement.width = 220;
        newElement.height = 120;
        break;
      case 'group':
        newElement.props = {
            ...newElement.props,
            name: `Группа ${elements.filter(el => el.type === 'group').length + 1}`,
            displayMode: 'absolute',
            flexDirection: 'row',
            justifyContent: 'flex-start',
            alignItems: 'stretch',
            gap: '0px',
        };
        newElement.width = 250;
        newElement.height = 150;
        break;
      default:
        break;
    }
    setElements(prevElements => [...prevElements, newElement]);
    setSelectedElementIds([newElement.id]);
  }, [elements.length]);

  const updateElement = useCallback((id, updates) => {
    setElements(prevElements =>
      prevElements.map(el => (el.id === id ? { ...el, ...updates } : el))
    );
  }, []);

  const updateMultipleElements = useCallback((ids, updatesMap) => {
    setElements(prevElements =>
      prevElements.map(el => {
        if (ids.includes(el.id)) {
          const updates = updatesMap[el.id];
          return { ...el, ...updates };
        }
        return el;
      })
    );
  }, []);

  const updateElementProps = useCallback((id, newProps) => {
    setElements(prevElements =>
      prevElements.map(el => (el.id === id ? { ...el, props: { ...el.props, ...newProps } } : el))
    );
  }, []);

  const deleteElement = useCallback((id) => {
    setElements(prevElements => prevElements.filter(el => el.id !== id));
    setSelectedElementIds(prevIds => prevIds.filter(prevId => prevId !== id));
  }, []);

  const deleteSelectedElements = useCallback(() => {
    if (selectedElementIds.length > 0 && window.confirm(`Вы уверены, что хотите удалить выбранные элементы (${selectedElementIds.length})?`)) {
      setElements(prevElements =>
        prevElements.filter(el => !selectedElementIds.includes(el.id))
      );
      setSelectedElementIds([]);
    }
  }, [selectedElementIds]);

  const saveCanvas = useCallback(() => {
    try {
      localStorage.setItem('canvasElements', JSON.stringify(elements));
      alert('Проект сохранен!');
    } catch (e) {
      console.error("Failed to save elements to localStorage", e);
      alert('Ошибка при сохранении проекта!');
    }
  }, [elements]);

  const clearCanvas = useCallback(() => {
    if (window.confirm('Вы уверены, что хотите очистить канвас? Все несохраненные изменения будут потеряны!')) {
      setElements([]);
      setSelectedElementIds([]);
      localStorage.removeItem('canvasElements');
      alert('Канвас очищен!');
    }
  }, []);

  const exportToHtmlCss = useCallback(() => {
    const { htmlContent, cssContent } = generateHtmlCss(elements);
    const zip = new JSZip();
    zip.file("index.html", htmlContent);
    zip.file("style.css", cssContent);
    zip.generateAsync({ type: "blob" })
      .then(function (content) {
        saveAs(content, "my_design.zip");
        alert('Дизайн экспортирован в ZIP-архив!');
      })
      .catch(e => {
        console.error("Error exporting to ZIP:", e);
        alert('Ошибка при экспорте дизайна!');
      });
  }, [elements]);

  const undo = useCallback(() => {
    if (historyIndex > 0) {
      const newIndex = historyIndex - 1;
      setHistoryIndex(newIndex);
      setElements(history[newIndex]);
      setSelectedElementIds([]);
    }
  }, [history, historyIndex]);

  const redo = useCallback(() => {
    if (historyIndex < history.length - 1) {
      const newIndex = historyIndex + 1;
      setHistoryIndex(newIndex);
      setElements(history[newIndex]);
      setSelectedElementIds([]);
    }
  }, [history, historyIndex]);

  const onMoveLayer = useCallback((fromIndex, toIndex) => {
    setElements(prevElements => {
      const newElements = [...prevElements];
      const [movedElement] = newElements.splice(fromIndex, 1);
      newElements.splice(toIndex, 0, movedElement);
      return newElements;
    });
  }, []);

  // --- Горячие клавиши ---
  const canUndo = historyIndex > 0;
  const canRedo = historyIndex < history.length - 1;

  const handleKeyDown = useCallback((e) => {
    // Не срабатывает, если фокус в input/textarea
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
      return;
    }
    const isCtrlOrCmd = e.metaKey || e.ctrlKey;
    // Undo: Ctrl+Z / Cmd+Z
    if (isCtrlOrCmd && e.key === 'z' && !e.shiftKey) {
      e.preventDefault();
      if (canUndo) undo();
    }
    // Redo: Ctrl+Shift+Z / Cmd+Shift+Z
    else if (isCtrlOrCmd && e.key.toLowerCase() === 'z' && e.shiftKey) {
      e.preventDefault();
      if (canRedo) redo();
    }
    // Redo alternative: Ctrl+Y / Cmd+Y
    else if (isCtrlOrCmd && e.key.toLowerCase() === 'y') {
      e.preventDefault();
      if (canRedo) redo();
    }
    // Delete/Backspace
    else if (e.key === 'Delete' || e.key === 'Backspace') {
      if (selectedElementIds.length > 0) {
        e.preventDefault();
        deleteSelectedElements();
      }
    }
    // Save: Ctrl+S / Cmd+S
    else if (isCtrlOrCmd && e.key.toLowerCase() === 's') {
      e.preventDefault();
      saveCanvas();
    }
  }, [canUndo, undo, canRedo, redo, selectedElementIds, deleteSelectedElements, saveCanvas]);

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleKeyDown]);

  // НОВАЯ ФУНКЦИЯ: Выравнивание элементов
  const alignElements = useCallback((alignment) => {
    if (selectedElementIds.length < 2) return; // Для выравнивания нужно хотя бы 2 элемента

    const selected = elements.filter(el => selectedElementIds.includes(el.id));

    // Находим ограничивающую рамку для всех выбранных элементов
    let minX = Infinity, minY = Infinity;
    let maxX = -Infinity, maxY = -Infinity;

    selected.forEach(el => {
      minX = Math.min(minX, el.x);
      minY = Math.min(minY, el.y);
      maxX = Math.max(maxX, el.x + el.width);
      maxY = Math.max(maxY, el.y + el.height);
    });

    const boundingBoxWidth = maxX - minX;
    const boundingBoxHeight = maxY - minY;
    const boundingBoxCenterX = minX + boundingBoxWidth / 2;
    const boundingBoxCenterY = minY + boundingBoxHeight / 2;

    setElements(prevElements => {
      return prevElements.map(el => {
        if (selectedElementIds.includes(el.id)) {
          let newX = el.x;
          let newY = el.y;

          switch (alignment) {
            case 'left':
              newX = minX;
              break;
            case 'center-h':
              newX = boundingBoxCenterX - el.width / 2;
              break;
            case 'right':
              newX = maxX - el.width;
              break;
            case 'top':
              newY = minY;
              break;
            case 'center-v':
              newY = boundingBoxCenterY - el.height / 2;
              break;
            case 'bottom':
              newY = maxY - el.height;
              break;
            default:
              break;
          }
          return { ...el, x: newX, y: newY };
        }
        return el;
      });
    });
  }, [elements, selectedElementIds]);

  // НОВАЯ ФУНКЦИЯ: Распределение элементов
  const distributeElements = useCallback((axis) => {
    if (selectedElementIds.length < 3) return; // Для распределения нужно хотя бы 3 элемента

    const selected = elements
      .filter(el => selectedElementIds.includes(el.id))
      .sort((a, b) => (axis === 'horizontal' ? a.x - b.x : a.y - b.y)); // Сортируем по оси

    if (selected.length < 2) return; // На всякий случай, если после фильтрации осталось мало элементов

    // Находим крайние точки для распределения
    const firstElement = selected[0];
    const lastElement = selected[selected.length - 1];

    setElements(prevElements => {
      const newElements = [...prevElements];
      const updatesMap = {};

      if (axis === 'horizontal') {
        const startX = firstElement.x;
        const endX = lastElement.x + lastElement.width;
        const totalWidth = endX - startX;
        let totalElementsWidth = 0;
        selected.forEach(el => totalElementsWidth += el.width);        const availableSpace = totalWidth - totalElementsWidth;
        const spacing = availableSpace / (selected.length - 1);

        let currentX = startX;
        selected.forEach((el, index) => {
          if (index === 0) {
            updatesMap[el.id] = { x: currentX };
          } else {
            currentX += selected[index - 1].width + spacing;
            updatesMap[el.id] = { x: currentX };
          }
        });
      } else { // vertical
        const startY = firstElement.y;
        const endY = lastElement.y + lastElement.height;
        const totalHeight = endY - startY;
        let totalElementsHeight = 0;
        selected.forEach(el => totalElementsHeight += el.height);

        const availableSpace = totalHeight - totalElementsHeight;
        const spacing = availableSpace / (selected.length - 1);

        let currentY = startY;
        selected.forEach((el, index) => {
          if (index === 0) {
            updatesMap[el.id] = { y: currentY };
          } else {
            currentY += selected[index - 1].height + spacing;
            updatesMap[el.id] = { y: currentY };
          }
        });
      }

      // Применяем обновления
      return prevElements.map(el => {
        if (updatesMap[el.id]) {
          return { ...el, ...updatesMap[el.id] };
        }
        return el;
      });
    });
  }, [elements, selectedElementIds]);

  const loadMySite = useCallback(async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      alert('Вы не авторизованы. Пожалуйста, войдите как администратор.');
      return;
    }
    if (!window.confirm('Вы уверены, что хотите загрузить сайт с сервера? Все несохраненные изменения будут потеряны!')) {
        return;
    }
    try {
      const response = await fetch(`${API_BASE_URL}/admin/load_my_site_data`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.msg || 'Ошибка при загрузке сайта с сервера');
      }
      let loadedElements = await response.json();
      // Ensure loaded elements have parentId, customClasses, customStyles, and new flex properties
      loadedElements = loadedElements.map(el => ({
          ...el,
          parentId: el.parentId === undefined ? null : el.parentId,
          props: {
              ...(el.props || {}),
              customClasses: el.props && el.props.customClasses === undefined ? [] : el.props.customClasses,
              customStyles: el.props && el.props.customStyles === undefined ? {} : el.props.customStyles,
              displayMode: el.type === 'group' && el.props && el.props.displayMode === undefined ? 'absolute' : (el.props ? el.props.displayMode : undefined),
              flexDirection: el.type === 'group' && el.props && el.props.flexDirection === undefined ? 'row' : (el.props ? el.props.flexDirection : undefined),
              justifyContent: el.type === 'group' && el.props && el.props.justifyContent === undefined ? 'flex-start' : (el.props ? el.props.justifyContent : undefined),
              alignItems: el.type === 'group' && el.props && el.props.alignItems === undefined ? 'stretch' : (el.props ? el.props.alignItems : undefined),
              gap: el.type === 'group' && el.props && el.props.gap === undefined ? '0px' : (el.props ? el.props.gap : undefined),
          }
      }));
      setElements(loadedElements);
      setHistory([loadedElements]);
      setHistoryIndex(0);
      setSelectedElementIds([]);
      alert('Сайт успешно загружен с сервера!');
    } catch (error) {
      console.error("Error loading site:", error);
      alert(`Ошибка загрузки сайта: ${error.message}`);
    }
  }, []);

  const groupSelectedElements = useCallback(() => {
      if (selectedElementIds.length < 2) return;
      const elementsToGroup = elements.filter(el => selectedElementIds.includes(el.id) && el.type !== 'group');
      if (elementsToGroup.length < 2) {
          alert('Для группировки выберите хотя бы два негруппированных элемента.');
          return;
      }
      const hasMixedParents = new Set(elementsToGroup.map(el => el.parentId)).size > 1;
      const hasParentGroupSelected = elementsToGroup.some(el => el.parentId && selectedElementIds.includes(el.parentId));
      if (hasMixedParents || hasParentGroupSelected) {
          alert('Нельзя группировать элементы из разных групп или элементы вместе с их родительскими группами. Сначала разгруппируйте их.');
          return;
      }
      let minX = Infinity, minY = Infinity;
      let maxX = -Infinity, maxY = -Infinity;
      elementsToGroup.forEach(el => {
          const absPos = getAbsolutePosition(el);
          minX = Math.min(minX, absPos.x);
          minY = Math.min(minY, absPos.y);
          maxX = Math.max(maxX, absPos.x + el.width);
          maxY = Math.max(maxY, absPos.y + el.height);
      });
      const newGroupId = generateUniqueId();
      const newGroup = {
          id: newGroupId,
          type: 'group',
          x: minX,
          y: minY,
          width: maxX - minX,
          height: maxY - minY,
          parentId: null,
          props: {
            name: `Группа ${elements.filter(el => el.type === 'group').length + 1}`,
            customClasses: [],
            customStyles: {},
            displayMode: 'absolute',
            flexDirection: 'row',
            justifyContent: 'flex-start',
            alignItems: 'stretch',
            gap: '0px',
          }
      };
      setElements(prevElements => {
          return [
              ...prevElements.filter(el => !selectedElementIds.includes(el.id)),
              newGroup,
              ...elementsToGroup.map(el => {
                  const absPos = getAbsolutePosition(el);
                  return {
                      ...el,
                      parentId: newGroupId,
                      x: absPos.x - newGroup.x,
                      y: absPos.y - newGroup.y,
                  };
              })
          ];
      });
      setSelectedElementIds([newGroupId]);
  }, [elements, selectedElementIds, getAbsolutePosition]);

  // Добавляем функцию getAbsolutePosition ДО всех её использований
  const getAbsolutePosition = useCallback((el) => {
    let currentX = el.x;
    let currentY = el.y;
    let parent = el.parentId ? elements.find(p => p.id === el.parentId) : null;
    while (parent) {
      currentX += parent.x;
      currentY += parent.y;
      parent = parent.parentId ? elements.find(p => p.id === parent.parentId) : null;
    }
    return { x: currentX, y: currentY };
  }, [elements]);

  return (
    <div className="editor-root">
      {/* Плавающие компоненты */}
      <FloatingCart />
      <FloatingCalculator />
      <FloatingLogo />
      <Header />
      <Sidebar onAddElement={addElement} clearCanvas={clearCanvas} saveCanvas={saveCanvas} exportToHtmlCss={exportToHtmlCss} deleteSelectedElements={deleteSelectedElements} />
      <main>
        <Canvas
          ref={canvasRef}
          elements={elements}
          setElements={setElements}
          selectedElementIds={selectedElementIds}
          setSelectedElementIds={setSelectedElementIds}
          updateElement={updateElement}
          updateMultipleElements={updateMultipleElements}
          updateElementProps={updateElementProps}
        />
        <PropertiesPanel
          selectedElement={selectedElement}
          updateElement={updateElement}
          updateElementProps={updateElementProps}
          deleteElement={deleteElement}
        />
        <LayersPanel
          elements={elements}
          selectedElementIds={selectedElementIds}
          setSelectedElementIds={setSelectedElementIds}
        />
        <AIColorPaletteGenerator
          elements={elements}
          setElements={setElements}
        />
      </main>
      <Footer />
    </div>
  );
}

export default Editor; 