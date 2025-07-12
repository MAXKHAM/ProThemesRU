import React, { useState, useRef, useEffect, useCallback, useMemo } from 'react';
import Sidebar from './Sidebar';
import Canvas from './Canvas';
import PropertiesPanel from './PropertiesPanel';
import AIColorPaletteGenerator from './AIColorPaletteGenerator';
import LayersPanel from './LayersPanel';
import ScrapePanel from './ScrapePanel';
import ContextMenu from './ContextMenu';
import MediaPanel from './MediaPanel';
import { generateUniqueId } from '../utils/idGenerator';
// Import generateHtmlCss from exportUtils.js (ensure it's updated to accept new props)
import { generateHtmlCss, cssStringToObject, objectToCssString } from '../utils/exportUtils';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import './Editor.css';

const MAX_HISTORY_SIZE = 50; // Максимальное количество состояний в истории
const API_BASE_URL = 'http://127.0.0.1:5000/api';

function Editor() {
  const [elements, setElements] = useState([]);
  const [selectedElementIds, setSelectedElementIds] = useState([]);
  const canvasRef = useRef(null);

  // НОВЫЕ СОСТОЯНИЯ ДЛЯ ИСТОРИИ
  const [history, setHistory] = useState([[]]); // История состояний элементов, начинаем с пустого канваса
  const [historyIndex, setHistoryIndex] = useState(0); // Текущий индекс в истории

  // NEW: States for Canvas/Page Background Properties
  const [canvasBackgroundColor, setCanvasBackgroundColor] = useState('#ffffff');
  const [canvasBackgroundImage, setCanvasBackgroundImage] = useState('');
  const [canvasBackgroundRepeat, setCanvasBackgroundRepeat] = useState('no-repeat');
  const [canvasBackgroundSize, setCanvasBackgroundSize] = useState('cover');
  const [canvasBackgroundPosition, setCanvasBackgroundPosition] = useState('center center');

  // NEW: States for advanced features
  const [copiedElementsData, setCopiedElementsData] = useState([]);
  const [showContextMenu, setShowContextMenu] = useState(false);
  const [contextMenuPos, setContextMenuPos] = useState({ x: 0, y: 0 });
  const [contextMenuElementId, setContextMenuElementId] = useState(null);
  const [showGrid, setShowGrid] = useState(false);
  const [gridSize, setGridSize] = useState(20);
  const [snapToGrid, setSnapToGrid] = useState(false);
  const [snapToElements, setSnapToElements] = useState(false);
  const [snapThreshold, setSnapThreshold] = useState(10);
  const [guides, setGuides] = useState({ vertical: [], horizontal: [] });
  const [isAdmin, setIsAdmin] = useState(false);

  // Helper functions for absolute positioning and element management
  const getElementById = useCallback((id) => {
    return elements.find(el => el.id === id);
  }, [elements]);

  const getAbsolutePosition = useCallback((element) => {
    let x = element.x;
    let y = element.y;
    
    if (element.parentId) {
      const parent = getElementById(element.parentId);
      if (parent) {
        const parentPos = getAbsolutePosition(parent);
        x += parentPos.x;
        y += parentPos.y;
      }
    }
    
    return { x, y };
  }, [getElementById]);

  // Active selection management
  const activeSelection = useMemo(() => {
    const selectedElements = elements.filter(el => selectedElementIds.includes(el.id));
    return {
      ids: selectedElementIds,
      elements: selectedElements
    };
  }, [elements, selectedElementIds]);

  // Эффект для сохранения состояния в историю при каждом изменении elements
  useEffect(() => {
    // Пропускаем первое монтирование, когда elements пуст
    if (history[historyIndex] === elements) {
        return; // Избегаем дублирования, если состояние не изменилось
    }

    // Обрезаем историю, если мы "вернулись в прошлое" и теперь делаем новое изменение
    const newHistory = history.slice(0, historyIndex + 1);
    
    // Добавляем текущее состояние в историю
    newHistory.push(elements);

    // Ограничиваем размер истории
    if (newHistory.length > MAX_HISTORY_SIZE) {
        newHistory.shift(); // Удаляем самое старое состояние
    }

    setHistory(newHistory);
    setHistoryIndex(newHistory.length - 1);
  }, [elements, history, historyIndex]); // Добавлены history и historyIndex в зависимости

  // Загрузка состояния при монтировании компонента (без изменений, но теперь оно станет первым состоянием в истории)
  useEffect(() => {
    try {
      const savedState = localStorage.getItem('canvasEditorState');
      if (savedState) {
        const loadedState = JSON.parse(savedState);
        setElements(loadedState.elements);
        setCanvasBackgroundColor(loadedState.canvasSettings.backgroundColor);
        setCanvasBackgroundImage(loadedState.canvasSettings.backgroundImage);
        setCanvasBackgroundRepeat(loadedState.canvasSettings.backgroundRepeat);
        setCanvasBackgroundSize(loadedState.canvasSettings.backgroundSize);
        setCanvasBackgroundPosition(loadedState.canvasSettings.backgroundPosition);
        // При загрузке, устанавливаем историю только с этим загруженным состоянием
        setHistory([loadedState.elements]);
        setHistoryIndex(0);
      }
    } catch (e) {
      console.error("Failed to load elements from localStorage", e);
    }
  }, []); // Пустой массив зависимостей, чтобы сработало только при монтировании

  // NEW: Check admin status on component mount
  useEffect(() => {
    const checkAdminStatus = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (token) {
          const response = await fetch(`${API_BASE_URL}/auth/me`, {
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });
          if (response.ok) {
            const userData = await response.json();
            setIsAdmin(userData.role === 'admin');
          }
        }
      } catch (error) {
        console.error('Error checking admin status:', error);
      }
    };

    checkAdminStatus();
  }, []);

  const selectedElement = selectedElementIds.length > 0
    ? elements.find(el => el.id === selectedElementIds[0])
    : null;

  const addElement = useCallback((type, x, y) => {
    const defaultProps = { name: `${type.charAt(0).toUpperCase() + type.slice(1)} ${elements.length + 1}` };
    
    const newElement = {
      id: generateUniqueId(),
      type,
      x,
      y,
      width: 150,
      height: 50,
      parentId: null,
      props: { ...defaultProps },
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
      case 'group':
        newElement.props = {
            ...newElement.props,
            name: `Группа ${elements.filter(el => el.type === 'group').length + 1}`,
            displayMode: 'absolute',
            flexDirection: 'row',
            justifyContent: 'flex-start',
            alignItems: 'stretch',
            gap: '0px',
            gridTemplateColumns: '1fr',
            gridTemplateRows: 'auto',
            gridGap: '0px',
            backgroundColor: 'rgba(255, 255, 255, 0.05)',
            borderStyle: 'dashed',
            borderColor: 'rgba(0, 0, 0, 0.1)',
            borderWidth: '1px',
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
    setElements(prevElements => {
        const elementToDelete = prevElements.find(el => el.id === id);
        if (!elementToDelete) return prevElements;

        let elementsAfterDelete = prevElements.filter(el => el.id !== id);

        if (elementToDelete.type === 'group') {
            elementsAfterDelete = elementsAfterDelete.filter(el => el.parentId !== id);
        }
        return elementsAfterDelete;
    });
    setSelectedElementIds(prevIds => prevIds.filter(prevId => prevId !== id));
  }, []);

  const deleteSelectedElements = useCallback(() => {
    if (activeSelection.ids.length > 0 && window.confirm(`Вы уверены, что хотите удалить выбранные элементы (${activeSelection.elements.length})?`)) {
      setElements(prevElements => {
        let newElements = prevElements;
        activeSelection.ids.forEach(id => {
            const elToDelete = newElements.find(el => el.id === id);
            if (elToDelete) {
                newElements = newElements.filter(el => el.id !== id);
                if (elToDelete.type === 'group') {
                    newElements = newElements.filter(el => el.parentId !== id);
                }
            }
        });
        return newElements;
      });
      setSelectedElementIds([]);
    }
  }, [activeSelection]);

  // UPDATED: onMoveLayer now also manages zIndex
  const onMoveLayer = useCallback((fromIndex, toIndex) => {
    setElements(prevElements => {
      const newElements = [...prevElements];
      const [movedElement] = newElements.splice(fromIndex, 1);
      newElements.splice(toIndex, 0, movedElement);

      // Reassign zIndex based on new order
      return newElements.map((el, index) => ({
        ...el,
        props: {
          ...(el.props || {}),
          zIndex: index + 1 // Assign zIndex from 1 to N based on order
        }
      }));
    });
  }, []);

  const saveCanvas = useCallback(() => {
    try {
      const stateToSave = {
        elements: elements,
        canvasSettings: {
          backgroundColor: canvasBackgroundColor,
          backgroundImage: canvasBackgroundImage,
          backgroundRepeat: canvasBackgroundRepeat,
          backgroundSize: canvasBackgroundSize,
          backgroundPosition: canvasBackgroundPosition,
        }
      };
      localStorage.setItem('canvasEditorState', JSON.stringify(stateToSave));
      alert('Проект сохранен!');
    } catch (e) {
      console.error("Failed to save elements to localStorage", e);
      alert('Ошибка при сохранении проекта!');
    }
  }, [elements, canvasBackgroundColor, canvasBackgroundImage, canvasBackgroundRepeat, canvasBackgroundSize, canvasBackgroundPosition]);

  const clearCanvas = useCallback(() => {
    if (window.confirm('Вы уверены, что хотите очистить канвас? Все несохраненные изменения будут потеряны!')) {
      setElements([]);
      setSelectedElementIds([]);
      setCanvasBackgroundColor('#ffffff'); // Reset canvas background
      setCanvasBackgroundImage('');
      setCanvasBackgroundRepeat('no-repeat');
      setCanvasBackgroundSize('cover');
      setCanvasBackgroundPosition('center center');
      localStorage.removeItem('canvasEditorState'); // Use new key
      alert('Канвас очищен!');
    }
  }, []);

  // NEW: Function to update canvas background properties
  const updateCanvasBackground = useCallback((propName, value) => {
    switch(propName) {
      case 'backgroundColor': setCanvasBackgroundColor(value); break;
      case 'backgroundImage': setCanvasBackgroundImage(value); break;
      case 'backgroundRepeat': setCanvasBackgroundRepeat(value); break;
      case 'backgroundSize': setCanvasBackgroundSize(value); break;
      case 'backgroundPosition': setCanvasBackgroundPosition(value); break;
      default: break;
    }
  }, []);

  const exportToHtmlCss = useCallback(() => {
    const { htmlContent, cssContent } = generateHtmlCss(elements, {
      backgroundColor: canvasBackgroundColor,
      backgroundImage: canvasBackgroundImage,
      backgroundRepeat: canvasBackgroundRepeat,
      backgroundSize: canvasBackgroundSize,
      backgroundPosition: canvasBackgroundPosition,
    });

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
  }, [elements, canvasBackgroundColor, canvasBackgroundImage, canvasBackgroundRepeat, canvasBackgroundSize, canvasBackgroundPosition]);

  const undo = useCallback(() => {
    if (historyIndex > 0) {
      const newIndex = historyIndex - 1;
      setHistoryIndex(newIndex);
      setElements(history[newIndex]);
      setSelectedElementIds([]);
      // Note: Undo/Redo for canvas settings is not implemented here.
      // For simplicity, it only affects elements history.
    }
  }, [history, historyIndex]);

  const redo = useCallback(() => {
    if (historyIndex < history.length - 1) {
      const newIndex = historyIndex + 1;
      setHistoryIndex(newIndex);
      setElements(history[newIndex]);
      setSelectedElementIds([]);
      // Note: Undo/Redo for canvas settings is not implemented here.
    }
  }, [history, historyIndex]);

  // Проверяем, доступны ли кнопки undo/redo
  const canUndo = historyIndex > 0;
  const canRedo = historyIndex < history.length - 1;

  // НОВАЯ ФУНКЦИЯ: Обработчик нажатия клавиш для удаления
  const handleKeyDown = useCallback((e) => {
    if (selectedElementIds.length > 0 && (e.key === 'Delete' || e.key === 'Backspace')) {
      e.preventDefault();
      deleteSelectedElements();
    }
  }, [selectedElementIds, deleteSelectedElements]);

  // Добавляем слушатель событий клавиатуры при монтировании/размонтировании
  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleKeyDown]);

  const alignElements = useCallback((alignment) => {
    if (activeSelection.elements.length < 2) return;

    const elementsToAlign = activeSelection.elements.filter(el => el.type !== 'group');

    if (elementsToAlign.length < 2) return;
    let minX = Infinity, minY = Infinity;
    let maxX = -Infinity, maxY = -Infinity;
    
    elementsToAlign.forEach(el => {
      const absPos = getAbsolutePosition(el);
      minX = Math.min(minX, absPos.x);
      minY = Math.min(minY, absPos.y);
      maxX = Math.max(maxX, absPos.x + el.width);
      maxY = Math.max(maxY, absPos.y + el.height);
    });

    const boundingBoxWidth = maxX - minX;
    const boundingBoxHeight = maxY - minY;
    const boundingBoxCenterX = minX + boundingBoxWidth / 2;
    const boundingBoxCenterY = minY + boundingBoxHeight / 2;

    setElements(prevElements => {
      return prevElements.map(el => {
        if (elementsToAlign.some(item => item.id === el.id)) {
          let newX = el.x;
          let newY = el.y;

          let currentAbsX = getAbsolutePosition(el).x;
          let currentAbsY = getAbsolutePosition(el).y;

          let newAbsX = currentAbsX;
          let newAbsY = currentAbsY;

          switch (alignment) {
            case 'left':
              newAbsX = minX;
              break;
            case 'center-h':
              newAbsX = boundingBoxCenterX - el.width / 2;
              break;
            case 'right':
              newAbsX = maxX - el.width;
              break;
            case 'top':
              newAbsY = minY;
              break;
            case 'center-v':
              newAbsY = boundingBoxCenterY - el.height / 2;
              break;
            case 'bottom':
              newAbsY = maxY - el.height;
              break;
            default:
              break;
          }

          if (el.parentId) {
            const parent = getElementById(el.parentId);
            if (parent) {
                newX = newAbsX - parent.x;
                newY = newAbsY - parent.y;
            }
          } else {
            newX = newAbsX;
            newY = newAbsY;
          }
          return { ...el, x: newX, y: newY };
        }
        return el;
      });
    });
  }, [elements, activeSelection.elements, getElementById, getAbsolutePosition]);

  const distributeElements = useCallback((axis) => {
    const elementsToDistribute = activeSelection.elements
        .filter(el => el.type !== 'group')
        .sort((a, b) => (axis === 'horizontal' ? getAbsolutePosition(a).x - getAbsolutePosition(b).x : getAbsolutePosition(a).y - getAbsolutePosition(b).y));

    if (elementsToDistribute.length < 3) return;

    setElements(prevElements => {
      const newElements = [...prevElements];
      const updatesMap = {};

      const firstElement = elementsToDistribute[0];
      const lastElement = elementsToDistribute[elementsToDistribute.length - 1];

      if (axis === 'horizontal') {
        const startX = getAbsolutePosition(firstElement).x;
        const endX = getAbsolutePosition(lastElement).x + lastElement.width;
        const totalWidthSpan = endX - startX;
        let totalElementsWidth = 0;
        elementsToDistribute.forEach(el => totalElementsWidth += el.width);

        const availableSpace = totalWidthSpan - totalElementsWidth;
        const spacing = availableSpace / (elementsToDistribute.length - 1);

        let currentAbsX = startX;
        elementsToDistribute.forEach((el, index) => {
          let newRelativeX = el.x;
          let newRelativeY = el.y;

          if (index !== 0) {
            currentAbsX += elementsToDistribute[index - 1].width + spacing;
          }

          if (el.parentId) {
              const parent = getElementById(el.parentId);
              if (parent) {
                  newRelativeX = currentAbsX - parent.x;
              }
          } else {
              newRelativeX = currentAbsX;
          }
          updatesMap[el.id] = { x: newRelativeX, y: newRelativeY };
        });
      } else { // vertical
        const startY = getAbsolutePosition(firstElement).y;
        const endY = getAbsolutePosition(lastElement).y + lastElement.height;
        const totalHeightSpan = endY - startY;
        let totalElementsHeight = 0;
        elementsToDistribute.forEach(el => totalElementsHeight += el.height);

        const availableSpace = totalHeightSpan - totalElementsHeight;
        const spacing = availableSpace / (elementsToDistribute.length - 1);

        let currentAbsY = startY;
        elementsToDistribute.forEach((el, index) => {
          let newRelativeX = el.x;
          let newRelativeY = el.y;

          if (index !== 0) {
            currentAbsY += elementsToDistribute[index - 1].height + spacing;
          }

          if (el.parentId) {
              const parent = getElementById(el.parentId);
              if (parent) {
                  newRelativeY = currentAbsY - parent.y;
              }
          } else {
              newRelativeY = currentAbsY;
          }
          updatesMap[el.id] = { x: newRelativeX, y: newRelativeY };
        });
      }

      return prevElements.map(el => {
        if (updatesMap[el.id]) {
          return { ...el, ...updatesMap[el.id] };
        }
        return el;
      });
    });
  }, [elements, activeSelection.elements, getElementById, getAbsolutePosition]);

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
      // Ensure loaded elements have default properties for new features
      loadedElements = loadedElements.map(el => ({
          ...el,
          parentId: el.parentId === undefined ? null : el.parentId,
          props: {
              ...(el.props || {}),
              customClasses: el.props && el.props.customClasses === undefined ? [] : el.props.customClasses,
              customStyles: el.props && el.props.customStyles === undefined ? {} : el.props.customStyles,
              zIndex: el.props && el.props.zIndex === undefined ? 1 : (el.props ? el.props.zIndex : 1),
              // Flex properties
              displayMode: el.type === 'group' && el.props && el.props.displayMode === undefined ? 'absolute' : (el.props ? el.props.displayMode : 'absolute'),
              flexDirection: el.type === 'group' && el.props && el.props.flexDirection === undefined ? 'row' : (el.props ? el.props.flexDirection : 'row'),
              justifyContent: el.type === 'group' && el.props && el.props.justifyContent === undefined ? 'flex-start' : (el.props ? el.props.justifyContent : 'flex-start'),
              alignItems: el.type === 'group' && el.props && el.props.alignItems === undefined ? 'stretch' : (el.props ? el.props.alignItems : 'stretch'),
              gap: el.type === 'group' && el.props && el.props.gap === undefined ? '0px' : (el.props ? el.props.gap : '0px'),
              // Grid properties
              gridTemplateColumns: el.type === 'group' && el.props && el.props.gridTemplateColumns === undefined ? '1fr' : (el.props ? el.props.gridTemplateColumns : '1fr'),
              gridTemplateRows: el.type === 'group' && el.props && el.props.gridTemplateRows === undefined ? 'auto' : (el.props ? el.props.gridTemplateRows : 'auto'),
              gridGap: el.props && el.props.gridGap === undefined ? '0px' : (el.props ? el.props.gridGap : '0px'),
              // Default border properties
              borderWidth: el.props && el.props.borderWidth === undefined ? '0px' : (el.props ? el.props.borderWidth : '0px'),
              borderStyle: el.props && el.props.borderStyle === undefined ? 'solid' : (el.props ? el.props.borderStyle : 'solid'),
              borderColor: el.props && el.props.borderColor === undefined ? '#000000' : (el.props ? el.props.borderColor : '#000000'),
              // Default box shadow properties
              boxShadowX: el.props && el.props.boxShadowX === undefined ? '0px' : (el.props ? el.props.boxShadowX : '0px'),
              boxShadowY: el.props && el.props.boxShadowY === undefined ? '0px' : (el.props ? el.props.boxShadowY : '0px'),
              boxShadowBlur: el.props && el.props.boxShadowBlur === undefined ? '0px' : (el.props ? el.props.boxShadowBlur : '0px'),
              boxShadowSpread: el.props && el.props.boxShadowSpread === undefined ? '0px' : (el.props ? el.props.boxShadowSpread : '0px'),
              boxShadowColor: el.props && el.props.boxShadowColor === undefined ? 'rgba(0,0,0,0.2)' : (el.props ? el.props.boxShadowColor : 'rgba(0,0,0,0.2)'),
              // Default background properties
              backgroundColor: el.props && el.props.backgroundColor === undefined ? '' : (el.props ? el.props.backgroundColor : ''),
              backgroundImage: el.props && el.props.backgroundImage === undefined ? '' : (el.props ? el.props.backgroundImage : ''),
              backgroundRepeat: el.props && el.props.backgroundRepeat === undefined ? 'no-repeat' : (el.props ? el.props.backgroundRepeat : 'no-repeat'),
              backgroundSize: el.props && el.props.backgroundSize === undefined ? 'cover' : (el.props ? el.props.backgroundSize : 'cover'),
              backgroundPosition: el.props && el.props.backgroundPosition === undefined ? 'center center' : (el.props ? el.props.backgroundPosition : 'center center'),
          }
      }));
      setElements(loadedElements);
      setHistory([loadedElements]);
      setHistoryIndex(0);
      setSelectedElementIds([]);
      // NEW: Load canvas settings from server response (if available)
      if (response.headers.get('X-Canvas-Settings')) {
          const serverCanvasSettings = JSON.parse(response.headers.get('X-Canvas-Settings'));
          setCanvasBackgroundColor(serverCanvasSettings.backgroundColor || '#ffffff');
          setCanvasBackgroundImage(serverCanvasSettings.backgroundImage || '');
          setCanvasBackgroundRepeat(serverCanvasSettings.backgroundRepeat || 'no-repeat');
          setCanvasBackgroundSize(serverCanvasSettings.backgroundSize || 'cover');
          setCanvasBackgroundPosition(serverCanvasSettings.backgroundPosition || 'center center');
      } else {
        // Reset to default if not provided by server
        setCanvasBackgroundColor('#ffffff');
        setCanvasBackgroundImage('');
        setCanvasBackgroundRepeat('no-repeat');
        setCanvasBackgroundSize('cover');
        setCanvasBackgroundPosition('center center');
      }
      alert('Сайт успешно загружен с сервера!');
    } catch (error) {
      console.error("Error loading site:", error);
      alert(`Ошибка загрузки сайта: ${error.message}`);
    }
  }, []);

  const publishMySite = useCallback(async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      alert('Вы не авторизованы. Пожалуйста, войдите как администратор.');
      return;
    }
    if (!window.confirm('Вы уверены, что хотите опубликовать текущий проект на свой сайт? Это перезапишет текущую версию сайта!')) {
        return;
    }

    try {
      const canvasSettings = {
        backgroundColor: canvasBackgroundColor,
        backgroundImage: canvasBackgroundImage,
        backgroundRepeat: canvasBackgroundRepeat,
        backgroundSize: canvasBackgroundSize,
        backgroundPosition: canvasBackgroundPosition,
      };

      const response = await fetch(`${API_BASE_URL}/admin/publish_my_site`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
          'X-Canvas-Settings': JSON.stringify(canvasSettings) // NEW: Send canvas settings to backend
        },
        body: JSON.stringify(elements)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.msg || 'Ошибка при публикации сайта');
      }

      const result = await response.json();
      alert(`Сайт успешно опубликован: ${result.msg}`);
    } catch (error) {
      console.error("Error publishing site:", error);
      alert(`Ошибка публикации сайта: ${error.message}`);
    }
  }, [elements, canvasBackgroundColor, canvasBackgroundImage, canvasBackgroundRepeat, canvasBackgroundSize, canvasBackgroundPosition]);

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
            zIndex: elements.length + 1, // Assign highest zIndex to new group
            displayMode: 'absolute',
            flexDirection: 'row',
            justifyContent: 'flex-start',
            alignItems: 'stretch',
            gap: '0px',
            gridTemplateColumns: '1fr',
            gridTemplateRows: 'auto',
            gridGap: '0px',
            backgroundColor: 'rgba(255, 255, 255, 0.05)',
            borderStyle: 'dashed',
            borderColor: 'rgba(0, 0, 0, 0.1)',
            borderWidth: '1px',
            boxShadowX: '0px',
            boxShadowY: '0px',
            boxShadowBlur: '0px',
            boxShadowSpread: '0px',
            boxShadowColor: 'rgba(0,0,0,0.2)',
            backgroundImage: '',
            backgroundRepeat: 'no-repeat',
            backgroundSize: 'cover',
            backgroundPosition: 'center center',
          }
      };

      // Update child elements to be part of the new group
      const updatedElements = elements.map(el => {
          if (selectedElementIds.includes(el.id)) {
              const absPos = getAbsolutePosition(el);
              return {
                  ...el,
                  parentId: newGroupId,
                  x: absPos.x - minX,
                  y: absPos.y - minY
              };
          }
          return el;
      });

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

  const ungroupElements = useCallback((groupId) => {
      const groupToUngroup = elements.find(el => el.id === groupId && el.type === 'group');
      if (!groupToUngroup) return;

      const children = elements.filter(el => el.parentId === groupId);

      setElements(prevElements => {
          const elementsWithoutGroup = prevElements.filter(el => el.id !== groupId);

          const updatedChildren = children.map(child => {
              const absPos = getAbsolutePosition(child);
              return {
                  ...child,
                  parentId: null,
                  x: absPos.x,
                  y: absPos.y,
              };
          });
          return [...elementsWithoutGroup, ...updatedChildren];
      });
      setSelectedElementIds(children.map(c => c.id));
  }, [elements, getAbsolutePosition]);

  // Function to copy selected elements
  const copySelectedElements = useCallback(() => {
      if (activeSelection.elements.length === 0) {
          setCopiedElementsData([]); // Clear clipboard if nothing selected
          return;
      }

      const elementsToCopy = activeSelection.elements;

      const newCopiedElements = [];
      const idMap = new Map(); // Maps old element IDs to new element IDs within the copied block

      // First pass: Create new elements with new IDs and build the ID map
      elementsToCopy.forEach(el => {
          const newId = generateUniqueId();
          idMap.set(el.id, newId);
          // Deep clone the element, but don't set parentId yet, will update later
          const clonedEl = { ...el, id: newId, props: { ...(el.props || {}) } }; // Deep copy props
          newCopiedElements.push(clonedEl);
      });

      // Second pass: Update parentIds for nested elements to refer to new parent IDs
      newCopiedElements.forEach(clonedEl => {
          if (clonedEl.parentId && idMap.has(clonedEl.parentId)) {
              clonedEl.parentId = idMap.get(clonedEl.parentId);
          } else {
              // If parentId existed but parent was not copied (e.g., copying only a child of an unselected group),
              // or if it was a root element, set parentId to null.
              clonedEl.parentId = null;
          }
      });
      setCopiedElementsData(newCopiedElements);
  }, [activeSelection.elements]);

  // Function to paste elements
  const pasteElements = useCallback(() => {
      if (copiedElementsData.length === 0) {
          return;
      }

      const pastedOffset = 20; // Offset for pasted elements

      const newElementsToAdd = [];
      const newSelectedIds = [];
      const idMap = new Map(); // Maps old IDs (from copiedElementsData) to new IDs (for new elements in canvas)

      // First pass: Generate new unique IDs for each element to be pasted and populate idMap
      copiedElementsData.forEach(copiedEl => {
          const newId = generateUniqueId();
          idMap.set(copiedEl.id, newId);
      });

      // Second pass: Create the actual new element objects with updated IDs and positions
      copiedElementsData.forEach(copiedEl => {
          const newEl = {
              ...copiedEl,
              id: idMap.get(copiedEl.id), // Assign the new ID
              x: copiedEl.x + pastedOffset,
              y: copiedEl.y + pastedOffset,
              props: {
                ...(copiedEl.props || {}),
                zIndex: elements.length + newElementsToAdd.length + 1 // Assign new zIndex
              } // Deep copy props to ensure independence
          };

          // Update parentId to refer to the new ID of its new parent, if it exists in idMap
          if (copiedEl.parentId && idMap.has(copiedEl.parentId)) {
              newEl.parentId = idMap.get(copiedEl.parentId);
          } else {
              // If parentId didn't exist or parent was not part of the copied block, it's a root element
              newEl.parentId = null;
          }
          newElementsToAdd.push(newEl);
          newSelectedIds.push(newEl.id); // Select the newly pasted elements
      });

      setElements(prevElements => [...prevElements, ...newElementsToAdd]);
      setSelectedElementIds(newSelectedIds);
  }, [copiedElementsData, elements.length]);

  // Function to duplicate selected elements
  const duplicateSelectedElements = useCallback(() => {
    if (activeSelection.elements.length === 0) {
      alert("Нет элементов для дублирования.");
      return;
    }
    copySelectedElements(); // Copies to internal clipboard
    pasteElements(); // Pastes from internal clipboard
  }, [activeSelection.elements, copySelectedElements, pasteElements]);

  // Function to bring selected element(s) to front
  const bringToFront = useCallback(() => {
    if (activeSelection.ids.length === 0) return;

    setElements(prevElements => {
      // Find elements to move and others
      const elementsToMove = prevElements.filter(el => activeSelection.ids.includes(el.id));
      const otherElements = prevElements.filter(el => !activeSelection.ids.includes(el.id));

      // Combine them, placing elementsToMove at the end
      const newOrder = [...otherElements, ...elementsToMove];

      // Reassign zIndex based on new order
      return newOrder.map((el, index) => ({
        ...el,
        props: {
          ...(el.props || {}),
          zIndex: index + 1
        }
      }));
    });
  }, [activeSelection.ids]);

  // Function to send selected element(s) to back
  const sendToBack = useCallback(() => {
    if (activeSelection.ids.length === 0) return;

    setElements(prevElements => {
      // Find elements to move and others
      const elementsToMove = prevElements.filter(el => activeSelection.ids.includes(el.id));
      const otherElements = prevElements.filter(el => !activeSelection.ids.includes(el.id));

      // Combine them, placing elementsToMove at the beginning
      const newOrder = [...elementsToMove, ...otherElements];

      // Reassign zIndex based on new order
      return newOrder.map((el, index) => ({
        ...el,
        props: {
          ...(el.props || {}),
          zIndex: index + 1
        }
      }));
    });
  }, [activeSelection.ids]);

  const canUndo = historyIndex > 0;
  const canRedo = historyIndex < history.length - 1;

  const handleKeyDown = useCallback((e) => {
    // Prevent shortcuts from firing when typing in input fields
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
      return;
    }

    const isCtrlOrCmd = e.metaKey || e.ctrlKey; // metaKey for Mac (Cmd), ctrlKey for Windows/Linux (Ctrl)

    if (isCtrlOrCmd && e.key === 'z') {
      e.preventDefault();
      if (canUndo) {
        undo();
      }
    } else if (isCtrlOrCmd && e.shiftKey && e.key === 'Z') {
      e.preventDefault();
      if (canRedo) {
        redo();
      }
    } else if (isCtrlOrCmd && e.key === 'y') { // Common alternative for redo
      e.preventDefault();
      if (canRedo) {
        redo();
      }
    } else if (e.key === 'Delete' || e.key === 'Backspace') {
      if (selectedElementIds.length > 0) {
        e.preventDefault();
        deleteSelectedElements();
      }
    } else if (isCtrlOrCmd && e.key === 's') {
      e.preventDefault();
      saveCanvas();
    } else if (isCtrlOrCmd && e.key === 'g') {
      e.preventDefault();
      if (selectedElementIds.length > 1) {
        groupSelectedElements();
      }
    } else if (isCtrlOrCmd && e.shiftKey && e.key === 'G') {
      e.preventDefault();
      if (selectedElementIds.length > 0) {
        const firstSelected = getElementById(selectedElementIds[0]);
        if (firstSelected && firstSelected.type === 'group') {
            ungroupElements(firstSelected.id);
        } else if (firstSelected && firstSelected.parentId) {
            ungroupElements(firstSelected.parentId);
        }
      }
    } else if (isCtrlOrCmd && e.key === 'c') { // Copy selected elements
        e.preventDefault();
        copySelectedElements();
    } else if (isCtrlOrCmd && e.key === 'v') { // Paste copied elements
        e.preventDefault();
        pasteElements();
    } else if (isCtrlOrCmd && e.key === 'd') { // Duplicate selected elements
        e.preventDefault();
        duplicateSelectedElements();
    }
  }, [canUndo, undo, canRedo, redo, selectedElementIds, deleteSelectedElements, saveCanvas, groupSelectedElements, ungroupElements, getElementById, copySelectedElements, pasteElements, duplicateSelectedElements]);

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleKeyDown]);

  // Context Menu handler for Canvas
  const handleCanvasContextMenu = useCallback((e, elementId = null) => {
    e.preventDefault(); // Prevent default browser context menu
    setShowContextMenu(true);
    setContextMenuPos({ x: e.clientX, y: e.clientY });
    setContextMenuElementId(elementId);
    setSelectedElementIds(elementId ? [elementId] : []); // Select element if right-clicked on it
  }, []);

  const handleCloseContextMenu = useCallback(() => {
    setShowContextMenu(false);
    setContextMenuElementId(null);
  }, []);

  const elementInContextMenu = contextMenuElementId ? getElementById(contextMenuElementId) : null;
  const canGroup = selectedElementIds.length > 1 && !activeSelection.elements.some(el => el.type === 'group' || (el.parentId && selectedElementIds.includes(el.parentId)));
  const canUngroup = selectedElementIds.length > 0 && activeSelection.elements.some(el => el.type === 'group' || el.parentId);

  return (
    <div className="editor">
      <LayersPanel
        elements={elements}
        selectedElementIds={selectedElementIds}
        setSelectedElementIds={setSelectedElementIds}
        updateElement={updateElement}
        updateElementProps={updateElementProps}
        onMoveLayer={onMoveLayer}
      />
      <Sidebar 
        addElement={addElement}
        showGrid={showGrid}
        setShowGrid={setShowGrid}
        snapToGrid={snapToGrid}
        setSnapToGrid={setSnapToGrid}
        gridSize={gridSize}
        setGridSize={setGridSize}
        snapToElements={snapToElements}
        setSnapToElements={setSnapToElements}
      />
      <Canvas
        ref={canvasRef}
        elements={elements}
        updateElement={updateElement}
        selectedElementIds={selectedElementIds}
        setSelectedElementIds={setSelectedElementIds}
        deleteElement={deleteElement}
        // NEW: Pass canvas background props to Canvas component
        canvasBackgroundColor={canvasBackgroundColor}
        canvasBackgroundImage={canvasBackgroundImage}
        canvasBackgroundRepeat={canvasBackgroundRepeat}
        canvasBackgroundSize={canvasBackgroundSize}
        canvasBackgroundPosition={canvasBackgroundPosition}
        // NEW: Pass context menu handler to Canvas
        onContextMenu={handleCanvasContextMenu}
      />
      <PropertiesPanel
        selectedElement={selectedElement}
        selectedElementIds={selectedElementIds}
        elements={elements}
        updateElementProps={updateElementProps}
        updateElement={updateElement}
        updateMultipleElements={updateMultipleElements}
        saveCanvas={saveCanvas}
        clearCanvas={clearCanvas}
        exportToHtmlCss={exportToHtmlCss}
        undo={undo}
        redo={redo}
        canUndo={canUndo}
        canRedo={canRedo}
        deleteSelectedElements={deleteSelectedElements}
        alignElements={alignElements}
        distributeElements={distributeElements}
        // NEW: Pass canvas background props and setter to PropertiesPanel
        canvasBackgroundColor={canvasBackgroundColor}
        canvasBackgroundImage={canvasBackgroundImage}
        canvasBackgroundRepeat={canvasBackgroundRepeat}
        canvasBackgroundSize={canvasBackgroundSize}
        canvasBackgroundPosition={canvasBackgroundPosition}
        updateCanvasBackground={updateCanvasBackground}
        // NEW: Pass site management functions to PropertiesPanel
        loadMySite={loadMySite}
        publishMySite={publishMySite}
        groupSelectedElements={groupSelectedElements}
        // NEW: Pass advanced functions to PropertiesPanel
        ungroupElements={ungroupElements}
        copySelectedElements={copySelectedElements}
        pasteElements={pasteElements}
        duplicateSelectedElements={duplicateSelectedElements}
        bringToFront={bringToFront}
        sendToBack={sendToBack}
        activeSelection={activeSelection}
        isAdmin={isAdmin}
      />
      <AIColorPaletteGenerator />
      <ScrapePanel isAdmin={isAdmin} />
      
      {/* Context Menu */}
      {showContextMenu && (
        <ContextMenu
          x={contextMenuPos.x}
          y={contextMenuPos.y}
          onClose={handleCloseContextMenu}
          actions={[
            {
              label: 'Копировать (Ctrl+C)',
              action: copySelectedElements,
              disabled: activeSelection.ids.length === 0
            },
            {
              label: 'Вставить (Ctrl+V)',
              action: pasteElements,
              disabled: copiedElementsData.length === 0
            },
            {
              label: 'Дублировать (Ctrl+D)',
              action: duplicateSelectedElements,
              disabled: activeSelection.ids.length === 0
            },
            { type: 'separator' },
            {
              label: 'Удалить (Del)',
              action: deleteSelectedElements,
              disabled: activeSelection.ids.length === 0
            },
            { type: 'separator' },
            {
              label: 'Группировать (Ctrl+G)',
              action: groupSelectedElements,
              disabled: !canGroup
            },
            {
              label: 'Разгруппировать (Ctrl+Shift+G)',
              action: () => ungroupElements(elementInContextMenu?.type === 'group' ? elementInContextMenu.id : elementInContextMenu?.parentId),
              disabled: !canUngroup
            },
            { type: 'separator' },
            {
              label: 'На передний план',
              action: bringToFront,
              disabled: activeSelection.ids.length === 0
            },
            {
              label: 'На задний план',
              action: sendToBack,
              disabled: activeSelection.ids.length === 0
            },
          ]}
        />
      )}
    </div>
  );
}

export default Editor; 