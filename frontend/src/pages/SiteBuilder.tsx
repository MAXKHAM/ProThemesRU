import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useToast } from 'react-hot-toast';

interface Block {
  id: string;
  type: string;
  content: string;
  style: {
    backgroundColor?: string;
    color?: string;
    padding?: string;
    textAlign?: string;
  };
}

interface SiteBuilderProps {
  onSave: (blocks: Block[]) => void;
}

const SiteBuilder: React.FC<SiteBuilderProps> = ({ onSave }) => {
  const [blocks, setBlocks] = useState<Block[]>([]);
  const [selectedBlock, setSelectedBlock] = useState<string | null>(null);
  const [previewMode, setPreviewMode] = useState(false);
  const toast = useToast();

  const addBlock = (type: string) => {
    const newBlock: Block = {
      id: Date.now().toString(),
      type,
      content: '',
      style: {
        backgroundColor: 'white',
        color: 'black',
        padding: '20px',
        textAlign: 'left',
      },
    };
    setBlocks([...blocks, newBlock]);
  };

  const updateBlock = (id: string, updates: Partial<Block>) => {
    setBlocks(blocks.map(block =>
      block.id === id ? { ...block, ...updates } : block
    ));
  };

  const deleteBlock = (id: string) => {
    setBlocks(blocks.filter(block => block.id !== id));
  };

  const handleSave = () => {
    onSave(blocks);
    toast.success('Сайт успешно сохранен!');
  };

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <div className="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
        <div className="p-4">
          <h2 className="text-lg font-semibold mb-4">Элементы</h2>
          <div className="space-y-2">
            <button
              onClick={() => addBlock('header')}
              className="w-full px-4 py-2 rounded-md text-left hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              Заголовок
            </button>
            <button
              onClick={() => addBlock('text')}
              className="w-full px-4 py-2 rounded-md text-left hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              Текст
            </button>
            <button
              onClick={() => addBlock('image')}
              className="w-full px-4 py-2 rounded-md text-left hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              Изображение
            </button>
            <button
              onClick={() => addBlock('button')}
              className="w-full px-4 py-2 rounded-md text-left hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              Кнопка
            </button>
          </div>
        </div>
      </div>

      {/* Builder Area */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-xl font-semibold">Конструктор сайта</h2>
          <div className="flex space-x-2">
            <button
              onClick={() => setPreviewMode(!previewMode)}
              className="px-4 py-2 rounded-md bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600"
            >
              {previewMode ? 'Редактировать' : 'Предпросмотр'}
            </button>
            <button
              onClick={handleSave}
              className="px-4 py-2 rounded-md bg-primary-600 text-white hover:bg-primary-700"
            >
              Сохранить
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4">
          <AnimatePresence>
            {blocks.map((block) => (
              <motion.div
                key={block.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className={`mb-4 ${previewMode ? '' : 'border border-gray-200 dark:border-gray-700 rounded-lg p-4'}`}
                style={block.style}
              >
                {!previewMode && (
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm text-gray-500 dark:text-gray-400">{block.type}</span>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => setSelectedBlock(block.id)}
                        className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                        </svg>
                      </button>
                      <button
                        onClick={() => deleteBlock(block.id)}
                        className="p-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700 text-red-500"
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </div>
                )}
                <div className="content" dangerouslySetInnerHTML={{ __html: block.content }} />
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </div>

      {/* Properties Panel */}
      <div className="w-64 bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700">
        <div className="p-4">
          <h2 className="text-lg font-semibold mb-4">Свойства</h2>
          {selectedBlock && (
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Текст
                </label>
                <textarea
                  value={blocks.find(b => b.id === selectedBlock)?.content || ''}
                  onChange={(e) => updateBlock(selectedBlock, { content: e.target.value })}
                  className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded-md"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Цвет фона
                </label>
                <input
                  type="color"
                  value={blocks.find(b => b.id === selectedBlock)?.style.backgroundColor || '#ffffff'}
                  onChange={(e) => updateBlock(selectedBlock, { style: { backgroundColor: e.target.value } })}
                  className="w-full h-8 rounded-md"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Цвет текста
                </label>
                <input
                  type="color"
                  value={blocks.find(b => b.id === selectedBlock)?.style.color || '#000000'}
                  onChange={(e) => updateBlock(selectedBlock, { style: { color: e.target.value } })}
                  className="w-full h-8 rounded-md"
                />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default SiteBuilder;
