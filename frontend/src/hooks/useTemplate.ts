import { useState, useEffect } from 'react';
import axios from 'axios';

interface Template {
  id: string;
  name: string;
  description: string;
  category: string;
  preview_image: string;
  blocks: Array<{
    id: string;
    type: string;
    content: any;
    settings: any;
  }>;
  created_at: string;
  updated_at: string;
  is_featured: boolean;
  price: number;
  features: string[];
  tags: string[];
}

export const useTemplate = (templateId: string) => {
  const [template, setTemplate] = useState<Template | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTemplate = async () => {
      try {
        const response = await axios.get(`/api/templates/${templateId}`);
        setTemplate(response.data);
      } catch (err) {
        setError('Не удалось загрузить шаблон');
      } finally {
        setLoading(false);
      }
    };

    fetchTemplate();
  }, [templateId]);

  const updateTemplate = async (updatedTemplate: Partial<Template>) => {
    try {
      const response = await axios.patch(`/api/templates/${templateId}`, updatedTemplate);
      setTemplate(response.data);
    } catch (err) {
      setError('Не удалось обновить шаблон');
    }
  };

  const addBlock = async (block: {
    type: string;
    content: any;
    settings: any;
  }) => {
    try {
      const newBlock = {
        id: Date.now().toString(),
        ...block
      };

      const response = await axios.patch(`/api/templates/${templateId}`, {
        blocks: [...(template?.blocks || []), newBlock]
      });
      setTemplate(response.data);
    } catch (err) {
      setError('Не удалось добавить блок');
    }
  };

  const deleteBlock = async (blockId: string) => {
    try {
      const response = await axios.patch(`/api/templates/${templateId}`, {
        blocks: template?.blocks.filter(block => block.id !== blockId) || []
      });
      setTemplate(response.data);
    } catch (err) {
      setError('Не удалось удалить блок');
    }
  };

  const updateBlock = async (blockId: string, updates: any) => {
    try {
      const response = await axios.patch(`/api/templates/${templateId}`, {
        blocks: template?.blocks.map(block =>
          block.id === blockId ? { ...block, ...updates } : block
        ) || []
      });
      setTemplate(response.data);
    } catch (err) {
      setError('Не удалось обновить блок');
    }
  };

  return {
    template,
    loading,
    error,
    updateTemplate,
    addBlock,
    deleteBlock,
    updateBlock
  };
};

export default useTemplate;
