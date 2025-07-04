import React, { useState, useEffect, useRef } from 'react';
import { motion } from 'framer-motion';
import { Draggable } from 'react-beautiful-dnd';
import { useTemplate } from '../hooks/useTemplate';

interface Block {
  id: string;
  type: string;
  content: any;
  settings: any;
}

interface TemplateBuilderProps {
  templateId: string;
}

const blockTypes = [
  { id: 'header', label: 'Шапка', icon: '📑' },
  { id: 'hero', label: 'Герой', icon: '🌟' },
  { id: 'features', label: 'Преимущества', icon: '✨' },
  { id: 'pricing', label: 'Цены', icon: '💰' },
  { id: 'portfolio', label: 'Портфолио', icon: '🎨' },
  { id: 'blog', label: 'Блог', icon: '📝' },
  { id: 'contact', label: 'Контакты', icon: '📞' },
  { id: 'cta', label: 'Призыв к действию', icon: '🎯' },
];

const TemplateBuilder: React.FC<TemplateBuilderProps> = ({ templateId }) => {
  const { template, updateTemplate } = useTemplate(templateId);
  const [selectedBlock, setSelectedBlock] = useState<Block | null>(null);
  const [editingBlock, setEditingBlock] = useState<Block | null>(null);
  const [showSettings, setShowSettings] = useState(false);
  const previewRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (previewRef.current) {
      const observer = new ResizeObserver(() => {
        updateTemplate({
          ...template,
          previewWidth: previewRef.current?.clientWidth || 1200
        });
      });

      observer.observe(previewRef.current);
      return () => observer.disconnect();
    }
  }, [previewRef.current]);

  const handleBlockClick = (block: Block) => {
    setSelectedBlock(block);
    setEditingBlock(block);
    setShowSettings(true);
  };

  const handleBlockSettingsChange = (block: Block) => {
    updateTemplate({
      ...template,
      blocks: template.blocks.map(b =>
        b.id === block.id ? { ...b, ...block } : b
      )
    });
  };

  const handleBlockDelete = (blockId: string) => {
    updateTemplate({
      ...template,
      blocks: template.blocks.filter(b => b.id !== blockId)
    });
  };

  const handleBlockAdd = (type: string) => {
    const newBlock: Block = {
      id: Date.now().toString(),
      type,
      content: {},
      settings: {}
    };

    updateTemplate({
      ...template,
      blocks: [...template.blocks, newBlock]
    });
  };

  const renderBlock = (block: Block) => {
    const blockTypes = {
      header: HeaderBlock,
      hero: HeroBlock,
      features: FeaturesBlock,
      pricing: PricingBlock,
      portfolio: PortfolioBlock,
      blog: BlogBlock,
      contact: ContactBlock,
      cta: CTABlock
    };

    const BlockComponent = blockTypes[block.type];
    return BlockComponent ? (
      <BlockComponent
        block={block}
        isSelected={selectedBlock?.id === block.id}
        onDelete={() => handleBlockDelete(block.id)}
        onSettings={() => handleBlockClick(block)}
      />
    ) : null;
  };

  return (
    <div className="flex h-screen">
      {/* Панель инструментов */}
      <div className="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700">
        <div className="p-4">
          <h2 className="text-lg font-semibold mb-4">Блоки</h2>
          <div className="space-y-2">
            {blockTypes.map((type) => (
              <button
                key={type.id}
                onClick={() => handleBlockAdd(type.id)}
                className="flex items-center px-4 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                <span className="text-xl mr-2">{type.icon}</span>
                {type.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Рабочая область */}
      <div className="flex-1 flex flex-col">
        <div className="flex-1 overflow-y-auto p-8">
          <div ref={previewRef} className="max-w-4xl mx-auto">
            {template.blocks.map((block, index) => (
              <Draggable key={block.id} draggableId={block.id} index={index}>
                {(provided) => (
                  <div
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    {...provided.dragHandleProps}
                    className="mb-8"
                  >
                    {renderBlock(block)}
                  </div>
                )}
              </Draggable>
            ))}
          </div>
        </div>

        {/* Панель настроек */}
        <div className="h-24 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between px-4">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setShowSettings(!showSettings)}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
            <button
              onClick={() => handleBlockAdd('header')}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
              </svg>
            </button>
          </div>
          <button
            onClick={() => updateTemplate({ ...template, isPublished: true })}
            className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
          >
            Опубликовать
          </button>
        </div>
      </div>

      {/* Панель настроек */}
      {showSettings && editingBlock && (
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: 20 }}
          className="w-96 bg-white dark:bg-gray-800 border-l border-gray-200 dark:border-gray-700 flex flex-col"
        >
          <div className="p-4 border-b border-gray-200 dark:border-gray-700">
            <h2 className="text-lg font-semibold">Настройки блока</h2>
          </div>
          <div className="flex-1 overflow-y-auto p-4">
            <BlockSettings
              block={editingBlock}
              onChange={handleBlockSettingsChange}
            />
          </div>
        </motion.div>
      )}
    </div>
  );
};

// Компоненты блоков
const HeaderBlock: React.FC<{ block: Block; isSelected: boolean; onDelete: () => void; onSettings: () => void }> = ({ block, isSelected, onDelete, onSettings }) => {
  return (
    <div className={`p-4 rounded-lg ${isSelected ? 'border-2 border-primary-600' : 'border border-gray-200 dark:border-gray-700'}`}>
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold">Шапка</h3>
        <div className="flex space-x-2">
          <button onClick={onSettings} className="p-2 text-gray-500 hover:text-gray-700">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </button>
          <button onClick={onDelete} className="p-2 text-red-500 hover:text-red-700">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 1116.138 21H7.862a2 2 0 11-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
      <div className="space-y-4">
        <div className="flex items-center space-x-4">
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 dark:text-white truncate">Логотип</p>
            <p className="text-sm text-gray-500 dark:text-gray-400">Загрузите логотип вашего бренда</p>
          </div>
          <button className="px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700">
            Загрузить
          </button>
        </div>
        <div className="flex items-center space-x-4">
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 dark:text-white truncate">Меню</p>
            <p className="text-sm text-gray-500 dark:text-gray-400">Добавьте пункты меню</p>
          </div>
          <button className="px-4 py-2 border border-gray-200 dark:border-gray-700 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700">
            Редактировать
          </button>
        </div>
      </div>
    </div>
  );
};

// Другие компоненты блоков...

const BlockSettings: React.FC<{ block: Block; onChange: (block: Block) => void }> = ({ block, onChange }) => {
  const handleChange = (field: string, value: any) => {
    onChange({
      ...block,
      settings: {
        ...block.settings,
        [field]: value
      }
    });
  };

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Заголовок</label>
        <input
          type="text"
          value={block.settings.title || ''}
          onChange={(e) => handleChange('title', e.target.value)}
          className="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-700 shadow-sm focus:border-primary-500 dark:focus:border-primary-400 focus:ring-primary-500 dark:focus:ring-primary-400"
        />
      </div>
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Цвет фона</label>
        <input
          type="color"
          value={block.settings.backgroundColor || '#ffffff'}
          onChange={(e) => handleChange('backgroundColor', e.target.value)}
          className="mt-1 block w-full rounded-md"
        />
      </div>
    </div>
  );
};

export default TemplateBuilder;
