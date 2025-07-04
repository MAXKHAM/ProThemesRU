import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

interface Project {
  id: string;
  title: string;
  description: string;
  category: string;
  images: string[];
  features: string[];
  link: string;
  price: number;
  isFeatured: boolean;
}

const projects: Project[] = [
  {
    id: '1',
    title: 'Корпоративный сайт',
    description: 'Профессиональный сайт для бизнеса с современным дизайном и функционалом',
    category: 'Бизнес',
    images: ['portfolio/business1.jpg', 'portfolio/business2.jpg'],
    features: ['Адаптивный дизайн', 'SEO оптимизация', 'CRM интеграция', 'Блог'],
    link: '/templates/business',
    price: 9990,
    isFeatured: true
  },
  {
    id: '2',
    title: 'Портфолио дизайнера',
    description: 'Стильный сайт-портфолио для творческих профессий',
    category: 'Креатив',
    images: ['portfolio/portfolio1.jpg', 'portfolio/portfolio2.jpg'],
    features: ['Галерея работ', 'Блог', 'Контактная форма', 'Социальные сети'],
    link: '/templates/portfolio',
    price: 7990,
    isFeatured: true
  },
  {
    id: '3',
    title: 'Интернет-магазин',
    description: 'Многофункциональный шаблон для электронной коммерции',
    category: 'E-commerce',
    images: ['portfolio/ecommerce1.jpg', 'portfolio/ecommerce2.jpg'],
    features: ['Корзина', 'Система заказов', 'Админ панель', 'Интеграция платежей'],
    link: '/templates/ecommerce',
    price: 14990,
    isFeatured: true
  },
  // Добавьте больше проектов по необходимости
];

const Portfolio: React.FC = () => {
  const [featuredProjects] = useState(projects.filter(p => p.isFeatured));
  const [categories, setCategories] = useState<string[]>(['Все']);
  const [selectedCategory, setSelectedCategory] = useState('Все');

  useEffect(() => {
    const uniqueCategories = [...new Set(projects.map(p => p.category))];
    setCategories(['Все', ...uniqueCategories]);
  }, []);

  const filteredProjects = selectedCategory === 'Все' 
    ? projects 
    : projects.filter(p => p.category === selectedCategory);

  return (
    <div className="py-12 bg-white dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-extrabold text-gray-900 dark:text-white text-center mb-8">
          Наше портфолио
        </h2>

        {/* Фильтры */}
        <div className="mb-8">
          <div className="flex flex-wrap gap-2 justify-center">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-4 py-2 rounded-md ${
                  selectedCategory === category 
                    ? 'bg-primary-600 text-white' 
                    : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-200'
                }`}
              >
                {category}
              </button>
            ))}
          </div>
        </div>

        {/* Проекты */}
        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          {filteredProjects.map((project) => (
            <motion.div
              key={project.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden"
            >
              {/* Галерея */}
              <div className="relative h-64">
                <div className="absolute inset-0">
                  <img
                    src={project.images[0]}
                    alt={project.title}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center">
                  <button
                    onClick={() => window.open(project.link, '_blank')}
                    className="px-4 py-2 bg-white text-black rounded-full hover:bg-gray-100"
                  >
                    Просмотреть
                  </button>
                </div>
              </div>

              {/* Описание */}
              <div className="p-6">
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                  {project.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-300 mb-4">
                  {project.description}
                </p>
                <div className="flex items-center justify-between mb-4">
                  <span className="text-gray-500 dark:text-gray-400">
                    {project.category}
                  </span>
                  <span className="text-primary-600 dark:text-primary-400 font-semibold">
                    ₽{project.price.toLocaleString()}
                  </span>
                </div>
                <Link
                  to={project.link}
                  className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 dark:bg-primary-400 dark:hover:bg-primary-500"
                >
                  Подробнее
                </Link>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Фича: Создание сайта за 5 минут */}
        <div className="mt-16">
          <div className="bg-gradient-to-r from-primary-600 to-primary-700 p-8 rounded-lg text-center">
            <h3 className="text-2xl font-bold text-white mb-4">
              Создайте сайт за 5 минут!
            </h3>
            <p className="text-white/90 mb-6">
              Выберите шаблон, настройте его под себя и получите готовый сайт без кодирования
            </p>
            <Link
              to="/create"
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-white hover:bg-gray-100 transform transition-all duration-300 hover:scale-105"
            >
              Начать бесплатно
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Portfolio;
