import { useState, useEffect } from 'react';
import axios from 'axios';

interface ImageOptimizationOptions {
  width?: number;
  height?: number;
  quality?: number;
  format?: 'webp' | 'jpeg' | 'png';
}

export const useImageOptimization = (src: string, options: ImageOptimizationOptions = {}) => {
  const [optimizedSrc, setOptimizedSrc] = useState<string>(src);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const optimizeImage = async () => {
      try {
        const response = await axios.post('/api/images/optimize', {
          src,
          ...options,
          format: options.format || 'webp',
        });

        setOptimizedSrc(response.data.optimizedUrl);
        setIsLoading(false);
      } catch (err) {
        setError('Ошибка оптимизации изображения');
        setIsLoading(false);
      }
    };

    optimizeImage();
  }, [src, options]);

  return {
    optimizedSrc,
    isLoading,
    error,
  };
};

export default useImageOptimization;
