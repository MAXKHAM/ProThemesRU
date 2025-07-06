import React, { useState, useRef, useEffect, useCallback } from 'react';
import Sidebar from './Sidebar';
import Canvas from './Canvas';
import PropertiesPanel from './PropertiesPanel';
import AIColorPaletteGenerator from './AIColorPaletteGenerator';
import LayersPanel from './LayersPanel';
import { generateUniqueId } from '../utils/idGenerator';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import './Editor.css';

const MAX_HISTORY_SIZE = 50; // Максимальное количество состояний в истории

function Editor() {
  const [elements, setElements] = useState([]);
  const [selectedElementIds, setSelectedElementIds] = useState([]);
  const canvasRef = useRef(null);

  // НОВЫЕ СОСТОЯНИЯ ДЛЯ ИСТОРИИ
  const [history, setHistory] = useState([[]]); // История состояний элементов, начинаем с пустого канваса
  const [historyIndex, setHistoryIndex] = useState(0); // Текущий индекс в истории

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
      const savedElements = localStorage.getItem('canvasElements');
      if (savedElements) {
        const loadedElements = JSON.parse(savedElements);
        setElements(loadedElements);
        // При загрузке, устанавливаем историю только с этим загруженным состоянием
        setHistory([loadedElements]);
        setHistoryIndex(0);
      }
    } catch (e) {
      console.error("Failed to load elements from localStorage", e);
    }
  }, []); // Пустой массив зависимостей, чтобы сработало только при монтировании

  const selectedElement = selectedElementIds.length > 0
    ? elements.find(el => el.id === selectedElementIds[0])
    : null;

  const addElement = useCallback((type, x, y) => {
    const newElement = {
      id: generateUniqueId(),
      type,
      x,
      y,
      width: 150,
      height: 50,
      props: { name: `${type.charAt(0).toUpperCase() + type.slice(1)} ${elements.length + 1}` },
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

  // НОВАЯ ФУНКЦИЯ: Перемещение элемента в массиве (для изменения Z-index)
  const onMoveLayer = useCallback((fromIndex, toIndex) => {
    setElements(prevElements => {
      const newElements = [...prevElements];
      const [movedElement] = newElements.splice(fromIndex, 1);
      newElements.splice(toIndex, 0, movedElement);
      return newElements;
    });
  }, []);

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
    const zip = new JSZip();
    let htmlContent = `<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Мой Дизайн</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
`;
    let cssContent = `
body {
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    min-height: 100vh;
    position: relative;
}

.canvas-element {
    position: absolute;
    box-sizing: border-box;
    overflow: hidden;
}
`;

    elements.forEach(el => {
      cssContent += `
#${el.id} {
    left: ${el.x}px;
    top: ${el.y}px;
    width: ${el.width}px;
    height: ${el.height}px;
`;

      let elementHtml = '';
      switch (el.type) {
        case 'text':
          elementHtml = `<div class="text-element">${el.props.content}</div>`;
          cssContent += `
    font-size: ${el.props.fontSize};
    color: ${el.props.color};
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    word-break: break-word;
    padding: 5px;
`;
          break;
        case 'image':
          elementHtml = `<img src="${el.props.src}" alt="${el.props.alt}" class="image-element">`;
          cssContent += `
    display: block;
    object-fit: contain;
`;
          break;
        case 'button':
          elementHtml = `<button class="button-element">${el.props.label}</button>`;
          cssContent += `
    background-color: ${el.props.bgColor};
    color: ${el.props.textColor};
    padding: 8px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    white-space: nowrap;
    display: flex;
    align-items: center;
    justify-content: center;
`;
          break;
        case 'shape':
          elementHtml = `<div class="shape-element"></div>`;
          cssContent += `
    background-color: ${el.props.bgColor};
    border-radius: ${el.props.borderRadius};
`;
          break;
        default:
          elementHtml = `<div>Неизвестный элемент</div>`;
      }
      cssContent += `}\n`; // Закрываем ID-селектор

      htmlContent += `    <div id="${el.id}" class="canvas-element">${elementHtml}</div>\n`;
    });

    htmlContent += `</body>\n</html>`;

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

  // НОВАЯ ФУНКЦИЯ: Отменить последнее действие
  const undo = useCallback(() => {
    if (historyIndex > 0) {
      const newIndex = historyIndex - 1;
      setHistoryIndex(newIndex);
      setElements(history[newIndex]);
      setSelectedElementIds([]);
    }
  }, [history, historyIndex]);

  // НОВАЯ ФУНКЦИЯ: Повторить отмененное действие
  const redo = useCallback(() => {
    if (historyIndex < history.length - 1) {
      const newIndex = historyIndex + 1;
      setHistoryIndex(newIndex);
      setElements(history[newIndex]);
      setSelectedElementIds([]);
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
        selected.forEach(el => totalElementsWidth += el.width);
        const availableSpace = totalWidth - totalElementsWidth;
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
      <Sidebar addElement={addElement} />
      <Canvas
        ref={canvasRef}
        elements={elements}
        updateElement={updateElement}
        selectedElementIds={selectedElementIds}
        setSelectedElementIds={setSelectedElementIds}
        deleteElement={deleteElement}
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
      />
      <AIColorPaletteGenerator />
    </div>
  );
}

export default Editor; 