import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  FaEye, 
  FaCode, 
  FaMobile, 
  FaGlobe, 
  FaStar, 
  FaUsers, 
  FaCheck,
  FaFilter,
  FaSearch
} from 'react-icons/fa';

interface Template {
  id: string;
  title: string;
  category: string;
  image: string;
  features: string[];
  rating: number;
  downloads: number;
  price: number;
  isFree: boolean;
  tags: string[];
}

const TemplateGallery: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('popular');

  const categories = [
    { id: 'all', name: 'Все шаблоны' },
    { id: 'business', name: 'Бизнес' },
    { id: 'portfolio', name: 'Портфолио' },
    { id: 'ecommerce', name: 'E-commerce' },
    { id: 'restaurant', name: 'Рестораны' },
    { id: 'medical', name: 'Медицина' },
    { id: 'education', name: 'Образование' },
    { id: 'blog', name: 'Блоги' }
  ];

  const templates: Template[] = [
    {
      id: '1',
      title: 'Модерн Бизнес',
      category: 'business',
      image: '/static/images/templates/business_landing.jpg',
      features: ['Адаптивный дизайн', 'SEO оптимизация', 'Быстрая загрузка', 'CMS система'],
      rating: 4.8,
      downloads: 1250,
      price: 299,
      isFree: false,
      tags: ['responsive', 'seo', 'fast']
    },
    {
      id: '2',
      title: 'Креатив Портфолио',
      category: 'portfolio',
      image: '/static/images/templates/portfolio-creative.jpg',
      features: ['Галерея работ', 'Контактная форма', 'Социальные сети', 'Анимации'],
      rating: 4.9,
      downloads: 890,
      price: 199,
      isFree: false,
      tags: ['portfolio', 'gallery', 'creative']
    },
    {
      id: '3',
      title: 'Элегантный Магазин',
      category: 'ecommerce',
      image: '/static/images/templates/ecommerce-elegant.jpg',
      features: ['Корзина', 'Система заказов', 'Интеграция платежей', 'Управление товарами'],
      rating: 4.7,
      downloads: 2100,
      price: 499,
      isFree: false,
      tags: ['ecommerce', 'shop', 'payments']
    },
    {
      id: '4',
      title: 'Ресторан Премиум',
      category: 'restaurant',
      image: '/static/images/templates/restaurant-premium.jpg',
      features: ['Меню онлайн', 'Бронирование столов', 'Доставка', 'Отзывы клиентов'],
      rating: 4.6,
      downloads: 650,
      price: 399,
      isFree: false,
      tags: ['restaurant', 'menu', 'booking']
    },
    {
      id: '5',
      title: 'Медицинский Центр',
      category: 'medical',
      image: '/static/images/templates/medical-center.jpg',
      features: ['Запись к врачу', 'Онлайн консультации', 'Медицинская карта', 'Результаты анализов'],
      rating: 4.8,
      downloads: 420,
      price: 599,
      isFree: false,
      tags: ['medical', 'appointment', 'consultation']
    },
    {
      id: '6',
      title: 'Образовательная Платформа',
      category: 'education',
      image: '/static/images/templates/education-platform.jpg',
      features: ['Онлайн курсы', 'Видео уроки', 'Тесты', 'Сертификаты'],
      rating: 4.9,
      downloads: 780,
      price: 449,
      isFree: false,
      tags: ['education', 'courses', 'video']
    },
    {
      id: '7',
      title: 'Блог Стартер',
      category: 'blog',
      image: '/static/images/templates/blog-starter.jpg',
      features: ['Редактор статей', 'Комментарии', 'Подписка', 'Социальные сети'],
      rating: 4.5,
      downloads: 1500,
      price: 0,
      isFree: true,
      tags: ['blog', 'articles', 'free']
    },
    {
      id: '8',
      title: 'Корпоративный Портальный',
      category: 'business',
      image: '/static/images/templates/corporate-portal.jpg',
      features: ['Внутренний портал', 'Документооборот', 'Новости компании', 'Контакты сотрудников'],
      rating: 4.7,
      downloads: 320,
      price: 799,
      isFree: false,
      tags: ['corporate', 'portal', 'internal']
    }
  ];

  const filteredTemplates = templates.filter(template => {
    const matchesCategory = selectedCategory === 'all' || template.category === selectedCategory;
    const matchesSearch = template.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         template.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchesCategory && matchesSearch;
  });

  const sortedTemplates = [...filteredTemplates].sort((a, b) => {
    switch (sortBy) {
      case 'popular':
        return b.downloads - a.downloads;
      case 'rating':
        return b.rating - a.rating;
      case 'price-low':
        return a.price - b.price;
      case 'price-high':
        return b.price - a.price;
      case 'newest':
        return parseInt(b.id) - parseInt(a.id);
      default:
        return 0;
    }
  });

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-800">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.h1 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-4xl md:text-5xl font-bold mb-6"
            >
              Готовые шаблоны сайтов
            </motion.h1>
            <motion.p 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-xl max-w-3xl mx-auto"
            >
              Выберите профессиональный шаблон для вашего бизнеса. 
              Все шаблоны адаптивные, SEO-оптимизированные и готовы к использованию.
            </motion.p>
          </div>
        </div>
      </section>

      {/* Filters Section */}
      <section className="py-12 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col lg:flex-row gap-6 items-center justify-between">
            {/* Search */}
            <div className="relative flex-1 max-w-md">
              <FaSearch className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="Поиск шаблонов..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              />
            </div>

            {/* Categories */}
            <div className="flex flex-wrap gap-2">
              {categories.map((category) => (
                <button
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    selectedCategory === category.id
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                  }`}
                >
                  {category.name}
                </button>
              ))}
            </div>

            {/* Sort */}
            <div className="flex items-center gap-2">
              <FaFilter className="text-gray-400" />
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
              >
                <option value="popular">По популярности</option>
                <option value="rating">По рейтингу</option>
                <option value="price-low">По цене (дешевле)</option>
                <option value="price-high">По цене (дороже)</option>
                <option value="newest">По дате</option>
              </select>
            </div>
          </div>
        </div>
      </section>

      {/* Templates Grid */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          {sortedTemplates.length === 0 ? (
            <div className="text-center py-20">
              <div className="text-gray-400 text-6xl mb-4">🔍</div>
              <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                Шаблоны не найдены
              </h3>
              <p className="text-gray-600 dark:text-gray-400">
                Попробуйте изменить критерии поиска или категорию
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
              {sortedTemplates.map((template, index) => (
                <motion.div
                  key={template.id}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
                >
                  {/* Template Image */}
                  <div className="relative h-48 overflow-hidden">
                    <img
                      src={template.image}
                      alt={template.title}
                      className="w-full h-full object-cover"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />
                    
                    {/* Price Badge */}
                    <div className="absolute top-4 right-4">
                      {template.isFree ? (
                        <span className="bg-green-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                          Бесплатно
                        </span>
                      ) : (
                        <span className="bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-semibold">
                          {template.price}₽
                        </span>
                      )}
                    </div>

                    {/* Rating */}
                    <div className="absolute bottom-4 left-4 flex items-center gap-1">
                      <FaStar className="text-yellow-400" />
                      <span className="text-white text-sm font-semibold">
                        {template.rating}
                      </span>
                    </div>
                  </div>

                  {/* Template Info */}
                  <div className="p-6">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                      {template.title}
                    </h3>
                    
                    <div className="flex items-center gap-4 text-sm text-gray-600 dark:text-gray-400 mb-4">
                      <span className="flex items-center gap-1">
                        <FaUsers />
                        {template.downloads}
                      </span>
                      <span className="flex items-center gap-1">
                        <FaEye />
                        {Math.floor(template.downloads * 10)}
                      </span>
                    </div>

                    {/* Features */}
                    <div className="mb-6">
                      <div className="flex flex-wrap gap-2">
                        {template.features.slice(0, 3).map((feature, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded-md"
                          >
                            {feature}
                          </span>
                        ))}
                        {template.features.length > 3 && (
                          <span className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 text-xs rounded-md">
                            +{template.features.length - 3}
                          </span>
                        )}
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex gap-2">
                      <Link
                        to={`/editor?template=${template.id}`}
                        className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors text-center"
                      >
                        Использовать
                      </Link>
                      <button className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                        <FaEye />
                      </button>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Не нашли подходящий шаблон?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Создайте уникальный дизайн с помощью нашего конструктора сайтов
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/editor"
              className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
            >
              Создать с нуля
            </Link>
            <Link
              to="/contact"
              className="border border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
            >
              Заказать индивидуальный дизайн
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default TemplateGallery;
