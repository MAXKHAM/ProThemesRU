import React, { createContext, useContext, useState, useEffect } from 'react';
import { Template } from '../types/template';

interface TemplateContextType {
  templates: Template[];
  loading: boolean;
  error: string | null;
  fetchTemplates: (category?: string) => Promise<void>;
  saveTemplate: (template: Template) => Promise<void>;
  updateTemplate: (template: Partial<Template>) => Promise<void>;
  deleteTemplate: (id: string) => Promise<void>;
  selectedTemplate: Template | null;
  selectTemplate: (template: Template | null) => void;
}

const TemplateContext = createContext<TemplateContextType | undefined>(undefined);

export const TemplateProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<Template | null>(null);

  const fetchTemplates = async (category?: string) => {
    try {
      setLoading(true);
      setError(null);
      
      const response = await fetch(`/api/templates${category ? `?category=${category}` : ''}`);
      if (!response.ok) throw new Error('Ошибка загрузки шаблонов');

      const data = await response.json();
      setTemplates(data.templates);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Произошла ошибка');
    } finally {
      setLoading(false);
    }
  };

  const saveTemplate = async (template: Template) => {
    try {
      const response = await fetch('/api/templates', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(template),
      });

      if (!response.ok) throw new Error('Ошибка сохранения шаблона');

      const data = await response.json();
      setTemplates(prev => [...prev, data.template]);
    } catch (error) {
      console.error('Ошибка при сохранении шаблона:', error);
      throw error;
    }
  };

  const updateTemplate = async (template: Partial<Template>) => {
    try {
      const response = await fetch(`/api/templates/${template.id}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(template),
      });

      if (!response.ok) throw new Error('Ошибка обновления шаблона');

      const data = await response.json();
      setTemplates(prev => 
        prev.map(t => t.id === template.id ? data.template : t)
      );
    } catch (error) {
      console.error('Ошибка при обновлении шаблона:', error);
      throw error;
    }
  };

  const deleteTemplate = async (id: string) => {
    try {
      const response = await fetch(`/api/templates/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Ошибка удаления шаблона');

      setTemplates(prev => prev.filter(t => t.id !== id));
    } catch (error) {
      console.error('Ошибка при удалении шаблона:', error);
      throw error;
    }
  };

  const selectTemplate = (template: Template | null) => {
    setSelectedTemplate(template);
  };

  useEffect(() => {
    fetchTemplates();
  }, []);

  return (
    <TemplateContext.Provider 
      value={{ 
        templates, 
        loading, 
        error, 
        fetchTemplates, 
        saveTemplate, 
        updateTemplate, 
        deleteTemplate, 
        selectedTemplate, 
        selectTemplate 
      }}
    >
      {children}
    </TemplateContext.Provider>
  );
};

export const useTemplate = () => {
  const context = useContext(TemplateContext);
  if (context === undefined) {
    throw new Error('useTemplate должен использоваться внутри TemplateProvider');
  }
  return context;
};
