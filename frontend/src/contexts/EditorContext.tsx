import React, { createContext, useContext, useState, useRef } from 'react';
import { Element, Project } from '../types/project';

interface EditorContextType {
  // Project state
  project: Project | null;
  elements: Element[];
  selectedElement: Element | null;
  canvasSize: { width: number; height: number };
  zoom: number;
  
  // Project actions
  createProject: (name: string, templateId?: string) => void;
  saveProject: () => Promise<void>;
  loadProject: (projectId: string) => Promise<void>;
  exportProject: () => void;
  
  // Element actions
  addElement: (type: string, position?: { x: number; y: number }) => void;
  updateElement: (id: string, updates: Partial<Element>) => void;
  deleteElement: (id: string) => void;
  selectElement: (element: Element | null) => void;
  duplicateElement: (id: string) => void;
  
  // Canvas actions
  updateCanvasSize: (size: { width: number; height: number }) => void;
  setZoom: (zoom: number) => void;
  
  // History
  undo: () => void;
  redo: () => void;
  canUndo: boolean;
  canRedo: boolean;
  
  // UI state
  isSaving: boolean;
  error: string | null;
}

const EditorContext = createContext<EditorContextType | undefined>(undefined);

export const EditorProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [project, setProject] = useState<Project | null>(null);
  const [elements, setElements] = useState<Element[]>([]);
  const [selectedElement, setSelectedElement] = useState<Element | null>(null);
  const [canvasSize, setCanvasSize] = useState({ width: 1200, height: 800 });
  const [zoom, setZoom] = useState(100);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  // History management
  const [history, setHistory] = useState<Element[][]>([]);
  const [historyIndex, setHistoryIndex] = useState(-1);
  const historyRef = useRef<Element[][]>([]);
  const historyIndexRef = useRef(-1);

  const addToHistory = (newElements: Element[]) => {
    const newHistory = historyRef.current.slice(0, historyIndexRef.current + 1);
    newHistory.push(newElements);
    historyRef.current = newHistory;
    historyIndexRef.current = newHistory.length - 1;
    setHistory(newHistory);
    setHistoryIndex(newHistory.length - 1);
  };

  const createProject = (name: string, templateId?: string) => {
    const newProject: Project = {
      id: `project-${Date.now()}`,
      name,
      description: '',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      status: 'draft',
      elements: [],
      settings: {
        canvasSize,
        backgroundColor: '#ffffff',
        theme: 'light',
        seo: {
          title: name,
          description: '',
          keywords: []
        }
      }
    };

    setProject(newProject);
    setElements([]);
    setSelectedElement(null);
    setHistory([]);
    setHistoryIndex(-1);
    historyRef.current = [];
    historyIndexRef.current = -1;
  };

  const saveProject = async () => {
    if (!project) return;

    setIsSaving(true);
    setError(null);

    try {
      const updatedProject = {
        ...project,
        elements,
        settings: {
          ...project.settings,
          canvasSize
        },
        updatedAt: new Date().toISOString()
      };

      const response = await fetch(`/api/projects/${project.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(updatedProject)
      });

      if (!response.ok) throw new Error('Ошибка сохранения проекта');

      setProject(updatedProject);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Произошла ошибка при сохранении');
    } finally {
      setIsSaving(false);
    }
  };

  const loadProject = async (projectId: string) => {
    try {
      const response = await fetch(`/api/projects/${projectId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) throw new Error('Ошибка загрузки проекта');

      const projectData = await response.json();
      setProject(projectData);
      setElements(projectData.elements);
      setCanvasSize(projectData.settings.canvasSize);
      setSelectedElement(null);
      
      // Reset history
      setHistory([]);
      setHistoryIndex(-1);
      historyRef.current = [];
      historyIndexRef.current = -1;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Произошла ошибка при загрузке');
    }
  };

  const exportProject = () => {
    if (!project) return;

    const html = generateHTML();
    const blob = new Blob([html], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${project.name}.html`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const generateHTML = () => {
    const css = generateCSS();
    const elementsHTML = elements.map(element => generateElementHTML(element)).join('\n');

    return `<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${project?.settings.seo.title || 'Созданный сайт'}</title>
    <meta name="description" content="${project?.settings.seo.description || ''}">
    <style>${css}</style>
</head>
<body>
    <div class="canvas" style="width: ${canvasSize.width}px; height: ${canvasSize.height}px; position: relative; margin: 0 auto; background-color: ${project?.settings.backgroundColor || '#ffffff'};">
        ${elementsHTML}
    </div>
</body>
</html>`;
  };

  const generateCSS = () => {
    return elements.map(element => `
#${element.id} {
    position: absolute;
    left: ${element.position.x}px;
    top: ${element.position.y}px;
    width: ${element.size.width}px;
    height: ${element.size.height}px;
    ${Object.entries(element.style).map(([key, value]) => `${key}: ${value};`).join('')}
}`).join('');
  };

  const generateElementHTML = (element: Element) => {
    switch (element.type) {
      case 'heading':
        return `<h1 id="${element.id}">${element.content}</h1>`;
      case 'paragraph':
        return `<p id="${element.id}">${element.content}</p>`;
      case 'image':
        return `<img id="${element.id}" src="${element.content}" alt="Image">`;
      case 'button':
        return `<button id="${element.id}">${element.content}</button>`;
      case 'container':
        return `<div id="${element.id}">${element.content}</div>`;
      default:
        return `<div id="${element.id}">${element.content}</div>`;
    }
  };

  const addElement = (type: string, position?: { x: number; y: number }) => {
    const newElement: Element = {
      id: `element-${Date.now()}`,
      type,
      content: getDefaultContent(type),
      style: getDefaultStyle(type),
      position: position || { x: 50, y: 50 },
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
      case 'container': return '';
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

  const selectElement = (element: Element | null) => {
    setSelectedElement(element);
  };

  const duplicateElement = (id: string) => {
    const element = elements.find(el => el.id === id);
    if (!element) return;

    const duplicatedElement: Element = {
      ...element,
      id: `element-${Date.now()}`,
      position: {
        x: element.position.x + 20,
        y: element.position.y + 20
      }
    };

    const newElements = [...elements, duplicatedElement];
    setElements(newElements);
    addToHistory(newElements);
    setSelectedElement(duplicatedElement);
  };

  const updateCanvasSize = (size: { width: number; height: number }) => {
    setCanvasSize(size);
  };

  const undo = () => {
    if (historyIndexRef.current > 0) {
      historyIndexRef.current--;
      setElements(historyRef.current[historyIndexRef.current]);
      setHistoryIndex(historyIndexRef.current);
    }
  };

  const redo = () => {
    if (historyIndexRef.current < historyRef.current.length - 1) {
      historyIndexRef.current++;
      setElements(historyRef.current[historyIndexRef.current]);
      setHistoryIndex(historyIndexRef.current);
    }
  };

  return (
    <EditorContext.Provider
      value={{
        project,
        elements,
        selectedElement,
        canvasSize,
        zoom,
        createProject,
        saveProject,
        loadProject,
        exportProject,
        addElement,
        updateElement,
        deleteElement,
        selectElement,
        duplicateElement,
        updateCanvasSize,
        setZoom,
        undo,
        redo,
        canUndo: historyIndexRef.current > 0,
        canRedo: historyIndexRef.current < historyRef.current.length - 1,
        isSaving,
        error
      }}
    >
      {children}
    </EditorContext.Provider>
  );
};

export const useEditor = () => {
  const context = useContext(EditorContext);
  if (context === undefined) {
    throw new Error('useEditor должен использоваться внутри EditorProvider');
  }
  return context;
};
