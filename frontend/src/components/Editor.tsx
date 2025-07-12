import React, { useState, useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  FaPlus, 
  FaTrash, 
  FaSave, 
  FaEye, 
  FaCode, 
  FaUndo, 
  FaRedo,
  FaPalette,
  FaTextHeight,
  FaImage,
  FaLink,
  FaColumns,
  FaHeading,
  FaParagraph,
  FaList,
  FaTable,
  FaVideo,
  FaMusic,
  FaMapMarkerAlt,
  FaPhone,
  FaEnvelope,
  FaGlobe,
  FaFacebook,
  FaTwitter,
  FaInstagram,
  FaYoutube
} from 'react-icons/fa';

interface Element {
  id: string;
  type: string;
  content: string;
  style: React.CSSProperties;
  position: { x: number; y: number };
  size: { width: number; height: number };
}

const Editor: React.FC = () => {
  const [elements, setElements] = useState<Element[]>([]);
  const [selectedElement, setSelectedElement] = useState<Element | null>(null);
  const [canvasSize, setCanvasSize] = useState({ width: 1200, height: 800 });
  const [zoom, setZoom] = useState(100);
  const [history, setHistory] = useState<Element[][]>([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const canvasRef = useRef<HTMLDivElement>(null);

  const elementTypes = [
    { type: 'heading', icon: <FaHeading />, name: 'Заголовок' },
    { type: 'paragraph', icon: <FaParagraph />, name: 'Текст' },
    { type: 'image', icon: <FaImage />, name: 'Изображение' },
    { type: 'button', icon: <FaLink />, name: 'Кнопка' },
    { type: 'container', icon: <FaColumns />, name: 'Контейнер' },
    { type: 'list', icon: <FaList />, name: 'Список' },
    { type: 'table', icon: <FaTable />, name: 'Таблица' },
    { type: 'video', icon: <FaVideo />, name: 'Видео' },
    { type: 'audio', icon: <FaMusic />, name: 'Аудио' },
    { type: 'map', icon: <FaMapMarkerAlt />, name: 'Карта' },
    { type: 'contact', icon: <FaPhone />, name: 'Контакты' },
    { type: 'social', icon: <FaFacebook />, name: 'Соц. сети' }
  ];

  const addElement = (type: string) => {
    const newElement: Element = {
      id: `element-${Date.now()}`,
      type,
      content: getDefaultContent(type),
      style: getDefaultStyle(type),
      position: { x: 50, y: 50 },
      size: getDefaultSize(type)
    };

    const newElements = [...elements, newElement];
    setElements(newElements);
    addToHistory(newElements);
    setSelectedElement(newElement);
  };

  const getDefaultContent = (type: string): string => {
    switch (type) {
      case 'heading': return 'Заголовок';
      case 'paragraph': return 'Введите текст здесь...';
      case 'button': return 'Кнопка';
      case 'list': return 'Элемент списка';
      case 'contact': return 'Контакты';
      case 'social': return 'Социальные сети';
      default: return '';
    }
  };

  const getDefaultStyle = (type: string): React.CSSProperties => {
    switch (type) {
      case 'heading':
        return {
          fontSize: '2rem',
          fontWeight: 'bold',
          color: '#333',
          textAlign: 'center'
        };
      case 'paragraph':
        return {
          fontSize: '1rem',
          color: '#666',
          lineHeight: '1.6'
        };
      case 'button':
        return {
          backgroundColor: '#3B82F6',
          color: 'white',
          padding: '12px 24px',
          borderRadius: '8px',
          border: 'none',
          cursor: 'pointer',
          fontSize: '1rem',
          fontWeight: '600'
        };
      case 'image':
        return {
          maxWidth: '100%',
          height: 'auto',
          borderRadius: '8px'
        };
      default:
        return {};
    }
  };

  const getDefaultSize = (type: string) => {
    switch (type) {
      case 'heading': return { width: 300, height: 60 };
      case 'paragraph': return { width: 400, height: 100 };
      case 'button': return { width: 150, height: 50 };
      case 'image': return { width: 300, height: 200 };
      case 'container': return { width: 500, height: 300 };
      default: return { width: 200, height: 100 };
    }
  };

  const updateElement = (id: string, updates: Partial<Element>) => {
    const newElements = elements.map(el => 
      el.id === id ? { ...el, ...updates } : el
    );
    setElements(newElements);
    addToHistory(newElements);
  };

  const deleteElement = (id: string) => {
    const newElements = elements.filter(el => el.id !== id);
    setElements(newElements);
    addToHistory(newElements);
    setSelectedElement(null);
  };

  const addToHistory = (newElements: Element[]) => {
    const newHistory = history.slice(0, historyIndex + 1);
    newHistory.push(newElements);
    setHistory(newHistory);
    setHistoryIndex(newHistory.length - 1);
  };

  const undo = () => {
    if (historyIndex > 0) {
      setHistoryIndex(historyIndex - 1);
      setElements(history[historyIndex - 1]);
    }
  };

  const redo = () => {
    if (historyIndex < history.length - 1) {
      setHistoryIndex(historyIndex + 1);
      setElements(history[historyIndex + 1]);
    }
  };

  const saveProject = () => {
    const projectData = {
      elements,
      canvasSize,
      timestamp: new Date().toISOString()
    };
    localStorage.setItem('savedProject', JSON.stringify(projectData));
    alert('Проект сохранен!');
  };

  const loadProject = () => {
    const saved = localStorage.getItem('savedProject');
    if (saved) {
      const projectData = JSON.parse(saved);
      setElements(projectData.elements);
      setCanvasSize(projectData.canvasSize);
      addToHistory(projectData.elements);
    }
  };

  const exportHTML = () => {
    const html = `
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Созданный сайт</title>
    <style>
        body { margin: 0; padding: 20px; font-family: Arial, sans-serif; }
        .element { position: relative; }
        ${elements.map(el => `
        #${el.id} {
            position: absolute;
            left: ${el.position.x}px;
            top: ${el.position.y}px;
            width: ${el.size.width}px;
            height: ${el.size.height}px;
            ${Object.entries(el.style).map(([key, value]) => `${key}: ${value};`).join('')}
        }
        `).join('')}
    </style>
</head>
<body>
    <div style="width: ${canvasSize.width}px; height: ${canvasSize.height}px; position: relative; margin: 0 auto;">
        ${elements.map(el => `
        <div id="${el.id}" class="element">
            ${el.type === 'image' ? `<img src="${el.content}" alt="Image" style="width: 100%; height: 100%; object-fit: cover;">` : el.content}
        </div>
        `).join('')}
    </div>
</body>
</html>`;

    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'website.html';
    a.click();
    URL.revokeObjectURL(url);
  };

  const renderElement = (element: Element) => {
    const isSelected = selectedElement?.id === element.id;

    return (
      <motion.div
        key={element.id}
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        className={`absolute cursor-move ${isSelected ? 'ring-2 ring-blue-500' : ''}`}
        style={{
          left: element.position.x,
          top: element.position.y,
          width: element.size.width,
          height: element.size.height,
          ...element.style
        }}
        onClick={() => setSelectedElement(element)}
        draggable
        onDragEnd={(e) => {
          const rect = canvasRef.current?.getBoundingClientRect();
          if (rect) {
            updateElement(element.id, {
              position: {
                x: e.clientX - rect.left,
                y: e.clientY - rect.top
              }
            });
          }
        }}
      >
        {element.type === 'image' ? (
          <img 
            src={element.content || '/static/images/placeholder.jpg'} 
            alt="Element" 
            className="w-full h-full object-cover"
          />
        ) : (
          <div 
            contentEditable={isSelected}
            onBlur={(e) => updateElement(element.id, { content: e.currentTarget.textContent || '' })}
            className="w-full h-full"
          >
            {element.content}
          </div>
        )}
        
        {isSelected && (
          <div className="absolute -top-8 left-0 bg-blue-500 text-white px-2 py-1 rounded text-xs">
            {element.type}
          </div>
        )}
      </motion.div>
    );
  };

  return (
    <div className="h-screen flex bg-gray-100 dark:bg-gray-900">
      {/* Toolbar */}
      <div className="w-16 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col items-center py-4 space-y-4">
        <button
          onClick={undo}
          disabled={historyIndex <= 0}
          className="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          <FaUndo />
        </button>
        <button
          onClick={redo}
          disabled={historyIndex >= history.length - 1}
          className="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-50"
        >
          <FaRedo />
        </button>
        <div className="w-8 h-px bg-gray-200 dark:bg-gray-700" />
        <button
          onClick={saveProject}
          className="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
          title="Сохранить"
        >
          <FaSave />
        </button>
        <button
          onClick={loadProject}
          className="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
          title="Загрузить"
        >
          <FaEye />
        </button>
        <button
          onClick={exportHTML}
          className="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
          title="Экспорт HTML"
        >
          <FaCode />
        </button>
      </div>

      {/* Elements Panel */}
      <div className="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 p-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Элементы
        </h3>
        <div className="grid grid-cols-2 gap-2">
          {elementTypes.map((item) => (
            <button
              key={item.type}
              onClick={() => addElement(item.type)}
              className="p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 flex flex-col items-center gap-2 text-sm"
            >
              <div className="text-gray-600 dark:text-gray-400">
                {item.icon}
              </div>
              <span className="text-xs text-gray-600 dark:text-gray-400">
                {item.name}
              </span>
            </button>
          ))}
        </div>

        {selectedElement && (
          <div className="mt-6 p-4 border border-gray-200 dark:border-gray-700 rounded-lg">
            <h4 className="font-semibold text-gray-900 dark:text-white mb-3">
              Свойства
            </h4>
            <div className="space-y-3">
              <div>
                <label className="block text-xs text-gray-600 dark:text-gray-400 mb-1">
                  Размер шрифта
                </label>
                <input
                  type="range"
                  min="12"
                  max="72"
                  value={parseInt(selectedElement.style.fontSize as string) || 16}
                  onChange={(e) => updateElement(selectedElement.id, {
                    style: { ...selectedElement.style, fontSize: `${e.target.value}px` }
                  })}
                  className="w-full"
                />
              </div>
              <div>
                <label className="block text-xs text-gray-600 dark:text-gray-400 mb-1">
                  Цвет
                </label>
                <input
                  type="color"
                  value={selectedElement.style.color as string || '#000000'}
                  onChange={(e) => updateElement(selectedElement.id, {
                    style: { ...selectedElement.style, color: e.target.value }
                  })}
                  className="w-full h-8 rounded border border-gray-300 dark:border-gray-600"
                />
              </div>
              <button
                onClick={() => deleteElement(selectedElement.id)}
                className="w-full bg-red-500 text-white py-2 px-3 rounded text-sm hover:bg-red-600"
              >
                <FaTrash className="inline mr-1" />
                Удалить
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Canvas */}
      <div className="flex-1 flex flex-col">
        {/* Canvas Controls */}
        <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 p-4 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <span className="text-sm text-gray-600 dark:text-gray-400">
              Размер: {canvasSize.width} x {canvasSize.height}
            </span>
            <span className="text-sm text-gray-600 dark:text-gray-400">
              Масштаб: {zoom}%
            </span>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setZoom(Math.max(50, zoom - 10))}
              className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm"
            >
              -
            </button>
            <span className="text-sm">{zoom}%</span>
            <button
              onClick={() => setZoom(Math.min(200, zoom + 10))}
              className="px-3 py-1 border border-gray-300 dark:border-gray-600 rounded text-sm"
            >
              +
            </button>
          </div>
        </div>

        {/* Canvas Area */}
        <div className="flex-1 overflow-auto p-8">
          <div className="flex justify-center">
            <div
              ref={canvasRef}
              className="bg-white shadow-lg relative"
              style={{
                width: canvasSize.width * (zoom / 100),
                height: canvasSize.height * (zoom / 100),
                transform: `scale(${zoom / 100})`,
                transformOrigin: 'top left'
              }}
            >
              {elements.map(renderElement)}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Editor; 