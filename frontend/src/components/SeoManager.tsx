import React, { useState } from 'react';
import { motion } from 'framer-motion';
import SeoMeta from './SeoMeta';

interface SeoData {
  title: string;
  description: string;
  keywords: string[];
  image: string;
  url: string;
  type: 'website' | 'article' | 'product';
}

interface SeoManagerProps {
  initialData: SeoData;
  onUpdate: (data: SeoData) => void;
}

const SeoManager: React.FC<SeoManagerProps> = ({ initialData, onUpdate }) => {
  const [seoData, setSeoData] = useState<SeoData>(initialData);
  const [showAdvanced, setShowAdvanced] = useState(false);

  const handleInputChange = (field: keyof SeoData, value: any) => {
    setSeoData(prev => ({
      ...prev,
      [field]: value
    }));
    onUpdate({ ...seoData, [field]: value });
  };

  const handleKeywordsChange = (keywords: string) => {
    const cleanedKeywords = keywords
      .split(',')
      .map(k => k.trim())
      .filter(k => k.length > 0);
    
    handleInputChange('keywords', cleanedKeywords);
  };

  const validateSeo = () => {
    const issues: string[] = [];

    // Проверка заголовка
    if (seoData.title.length < 10 || seoData.title.length > 60) {
      issues.push('Заголовок должен быть от 10 до 60 символов');
    }

    // Проверка описания
    if (seoData.description.length < 50 || seoData.description.length > 160) {
      issues.push('Описание должно быть от 50 до 160 символов');
    }

    // Проверка ключевых слов
    if (seoData.keywords.length < 3) {
      issues.push('Добавьте хотя бы 3 ключевых слова');
    }

    // Проверка изображения
    if (!seoData.image) {
      issues.push('Добавьте изображение для социальных сетей');
    }

    return issues;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
      className="fixed right-0 top-16 w-96 bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6 overflow-y-auto max-h-[90vh]"
    >
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold">SEO-оптимизация</h2>
        <button
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="text-sm text-gray-600 dark:text-gray-300 hover:text-gray-800 dark:hover:text-white"
        >
          {showAdvanced ? 'Основные' : 'Расширенные'}
        </button>
      </div>

      {/* Базовые настройки */}
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Заголовок страницы</label>
          <input
            type="text"
            value={seoData.title}
            onChange={(e) => handleInputChange('title', e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-700 shadow-sm focus:border-primary-500 dark:focus:border-primary-400 focus:ring-primary-500 dark:focus:ring-primary-400"
            placeholder="Максимум 60 символов"
          />
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {seoData.title.length}/60
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Описание страницы</label>
          <textarea
            value={seoData.description}
            onChange={(e) => handleInputChange('description', e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-700 shadow-sm focus:border-primary-500 dark:focus:border-primary-400 focus:ring-primary-500 dark:focus:ring-primary-400"
            rows={3}
            placeholder="Максимум 160 символов"
          />
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {seoData.description.length}/160
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Ключевые слова</label>
          <input
            type="text"
            value={seoData.keywords.join(',')}
            onChange={(e) => handleKeywordsChange(e.target.value)}
            className="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-700 shadow-sm focus:border-primary-500 dark:focus:border-primary-400 focus:ring-primary-500 dark:focus:ring-primary-400"
            placeholder="Разделяйте запятыми"
          />
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Добавлено {seoData.keywords.length} ключевых слов
          </p>
        </div>

        {showAdvanced && (
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Изображение для социальных сетей</label>
            <input
              type="text"
              value={seoData.image}
              onChange={(e) => handleInputChange('image', e.target.value)}
              className="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-700 shadow-sm focus:border-primary-500 dark:focus:border-primary-400 focus:ring-primary-500 dark:focus:ring-primary-400"
              placeholder="URL изображения"
            />
          </div>
        )}
      </div>

      {/* SEO анализ */}
      <div className="mt-6">
        <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">SEO анализ</h3>
        <div className="space-y-2">
          {validateSeo().map((issue, index) => (
            <div
              key={index}
              className="flex items-center p-2 bg-red-50 dark:bg-red-900 text-red-700 dark:text-red-300 rounded-md"
            >
              <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              {issue}
            </div>
          ))}
        </div>
      </div>

      {/* Предпросмотр */}
      <div className="mt-6">
        <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Предпросмотр</h3>
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
          <SeoMeta
            title={seoData.title}
            description={seoData.description}
            keywords={seoData.keywords}
            image={seoData.image}
            url={seoData.url}
            type={seoData.type}
          />
        </div>
      </div>
    </motion.div>
  );
};

export default SeoManager;
