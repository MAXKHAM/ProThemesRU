import React, { createContext, useContext, useState, useEffect } from 'react';
import { Block } from '../types/block';

interface EditorContextType {
  blocks: Block[];
  selectedBlock: Block | null;
  selectedElement: any | null;
  previewMode: boolean;
  undoStack: Block[][];
  redoStack: Block[][];
  
  addBlock: (block: Block) => void;
  updateBlock: (block: Block) => void;
  deleteBlock: (id: string) => void;
  selectBlock: (block: Block | null) => void;
  selectElement: (element: any | null) => void;
  togglePreview: () => void;
  undo: () => void;
  redo: () => void;
  saveLayout: () => Promise<void>;
}

const EditorContext = createContext<EditorContextType | undefined>(undefined);

export const EditorProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [blocks, setBlocks] = useState<Block[]>([]);
  const [selectedBlock, setSelectedBlock] = useState<Block | null>(null);
  const [selectedElement, setSelectedElement] = useState<any | null>(null);
  const [previewMode, setPreviewMode] = useState(false);
  const [undoStack, setUndoStack] = useState<Block[][]>([]);
  const [redoStack, setRedoStack] = useState<Block[][]>([]);

  const addBlock = (block: Block) => {
    setBlocks(prev => [...prev, block]);
    setUndoStack(prev => [...prev, [...prev]]);
    setRedoStack([]);
  };

  const updateBlock = (block: Block) => {
    setBlocks(prev => 
      prev.map(b => b.id === block.id ? block : b)
    );
    setUndoStack(prev => [...prev, [...prev]]);
    setRedoStack([]);
  };

  const deleteBlock = (id: string) => {
    setBlocks(prev => prev.filter(b => b.id !== id));
    setUndoStack(prev => [...prev, [...prev]]);
    setRedoStack([]);
  };

  const selectBlock = (block: Block | null) => {
    setSelectedBlock(block);
  };

  const selectElement = (element: any | null) => {
    setSelectedElement(element);
  };

  const togglePreview = () => {
    setPreviewMode(prev => !prev);
  };

  const undo = () => {
    if (undoStack.length > 0) {
      const lastState = undoStack[undoStack.length - 1];
      setBlocks(lastState);
      setRedoStack(prev => [...prev, [...blocks]]);
      setUndoStack(prev => prev.slice(0, -1));
    }
  };

  const redo = () => {
    if (redoStack.length > 0) {
      const lastState = redoStack[redoStack.length - 1];
      setBlocks(lastState);
      setUndoStack(prev => [...prev, [...blocks]]);
      setRedoStack(prev => prev.slice(0, -1));
    }
  };

  const saveLayout = async () => {
    try {
      const response = await fetch('/api/layouts/save', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ blocks }),
      });

      if (!response.ok) throw new Error('Ошибка сохранения макета');

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Ошибка при сохранении макета:', error);
      throw error;
    }
  };

  return (
    <EditorContext.Provider 
      value={{ 
        blocks, 
        selectedBlock, 
        selectedElement, 
        previewMode,
        undoStack,
        redoStack,
        addBlock,
        updateBlock,
        deleteBlock,
        selectBlock,
        selectElement,
        togglePreview,
        undo,
        redo,
        saveLayout,
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
