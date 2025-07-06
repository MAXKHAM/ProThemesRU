// Генератор уникальных ID для элементов
export const generateUniqueId = () => {
  return 'element_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
};

// Альтернативная функция для обратной совместимости
export const generateId = () => {
  return generateUniqueId();
}; 