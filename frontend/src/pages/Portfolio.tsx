import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { FaEye, FaCode, FaMobile, FaGlobe, FaStar, FaUsers, FaCheck } from 'react-icons/fa';

const Portfolio: React.FC = () => {
  const [activeCategory, setActiveCategory] = useState('all');

  const categories = [
    { id: 'all', name: 'Все проекты' },
    { id: 'business', name: 'Бизнес' },
    { id: 'ecommerce', name: 'E-commerce' },
    { id: 'portfolio', name: 'Портфолио' },
    { id: 'restaurant', name: 'Рестораны' },
    { id: 'medical', name: 'Медицина' },
    { id: 'education', name: 'Образование' }
  ];

  const projects = [
    {
      id: 1,
      title: "Корпоративный сайт TechCorp",
      category: "business",
      description: "Современный корпоративный сайт для IT-компании с интеграцией CRM и аналитики",
      image: "/static/images/portfolio/techcorp.jpg",
      technologies: ["React", "Node.js", "MongoDB", "AWS"],
      features: ["Адаптивный дизайн", "CRM интеграция", "Аналитика", "SEO оптимизация"],
      rating: 4.9,
      views: 1250,
      demoUrl: "https://techcorp-demo.prothemes.ru",
      price: "299₽/мес"
    },
    {
      id: 2,
      title: "Интернет-магазин FashionStore",
      category: "ecommerce",
      description: "Полнофункциональный интернет-магазин с системой управления заказами",
      image: "/static/images/portfolio/fashionstore.jpg",
      technologies: ["Vue.js", "Laravel", "MySQL", "Stripe"],
      features: ["Каталог товаров", "Корзина покупок", "Онлайн оплата", "Личный кабинет"],
      rating: 4.8,
      views: 980,
      demoUrl: "https://fashionstore-demo.prothemes.ru",
      price: "399₽/мес"
    },
    {
      id: 3,
      title: "Портфолио дизайнера CreativeStudio",
      category: "portfolio",
      description: "Креативное портфолио для дизайн-студии с галереей работ",
      image: "/static/images/portfolio/creativestudio.jpg",
      technologies: ["React", "Framer Motion", "GSAP", "Netlify"],
      features: ["Анимации", "Галерея работ", "Контактная форма", "Блог"],
      rating: 4.7,
      views: 756,
      demoUrl: "https://creativestudio-demo.prothemes.ru",
      price: "199₽/мес"
    },
    {
      id: 4,
      title: "Сайт ресторана LaCuisine",
      category: "restaurant",
      description: "Элегантный сайт ресторана с онлайн-бронированием и меню",
      image: "/static/images/portfolio/lacuisine.jpg",
      technologies: ["Next.js", "Prisma", "PostgreSQL", "Vercel"],
      features: ["Онлайн бронирование", "Меню с фото", "Отзывы клиентов", "Доставка"],
      rating: 4.6,
      views: 634,
      demoUrl: "https://lacuisine-demo.prothemes.ru",
      price: "249₽/мес"
    },
    {
      id: 5,
      title: "Медицинский центр HealthCare",
      category: "medical",
      description: "Профессиональный сайт медицинского центра с онлайн-записью",
      image: "/static/images/portfolio/healthcare.jpg",
      technologies: ["Angular", "Django", "PostgreSQL", "Docker"],
      features: ["Онлайн запись", "Личный кабинет", "Медицинская карта", "Консультации"],
      rating: 4.9,
      views: 892,
      demoUrl: "https://healthcare-demo.prothemes.ru",
      price: "349₽/мес"
    },
    {
      id: 6,
      title: "Образовательная платформа EduTech",
      category: "education",
      description: "Инновационная платформа для онлайн-обучения с видеокурсами",
      image: "/static/images/portfolio/edutech.jpg",
      technologies: ["React", "Node.js", "MongoDB", "AWS S3"],
      features: ["Видеокурсы", "Тестирование", "Прогресс обучения", "Сертификаты"],
      rating: 4.8,
      views: 1100,
      demoUrl: "https://edutech-demo.prothemes.ru",
      price: "299₽/мес"
    },
    {
      id: 7,
      title: "Сайт агентства недвижимости RealEstate",
      category: "business",
      description: "Комплексный сайт агентства недвижимости с базой объектов",
      image: "/static/images/portfolio/realestate.jpg",
      technologies: ["Vue.js", "Laravel", "MySQL", "Algolia"],
      features: ["База объектов", "Поиск по карте", "Калькулятор ипотеки", "Консультации"],
      rating: 4.7,
      views: 678,
      demoUrl: "https://realestate-demo.prothemes.ru",
      price: "399₽/мес"
    },
    {
      id: 8,
      title: "Сайт фитнес-клуба FitLife",
      category: "business",
      description: "Динамичный сайт фитнес-клуба с расписанием и онлайн-записью",
      image: "/static/images/portfolio/fitlife.jpg",
      technologies: ["React", "Express.js", "MongoDB", "Stripe"],
      features: ["Расписание занятий", "Онлайн запись", "Личный кабинет", "Платежи"],
      rating: 4.6,
      views: 445,
      demoUrl: "https://fitlife-demo.prothemes.ru",
      price: "249₽/мес"
    }
  ];

  const filteredProjects = activeCategory === 'all' 
    ? projects 
    : projects.filter(project => project.category === activeCategory);

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
              Наши работы
            </motion.h1>
            <motion.p 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-xl max-w-3xl mx-auto"
            >
              Познакомьтесь с проектами, которые мы создали для наших клиентов. 
              Каждый сайт уникален и создан с учетом потребностей бизнеса.
            </motion.p>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                150+
              </div>
              <div className="text-gray-600 dark:text-gray-400">
                Реализованных проектов
              </div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                98%
              </div>
              <div className="text-gray-600 dark:text-gray-400">
                Довольных клиентов
              </div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                24/7
              </div>
              <div className="text-gray-600 dark:text-gray-400">
                Поддержка проектов
              </div>
            </div>
            <div className="text-center">
              <div className="text-3xl md:text-4xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                4.9
              </div>
              <div className="text-gray-600 dark:text-gray-400">
                Средний рейтинг
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Categories Filter */}
      <section className="py-8 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-wrap justify-center gap-4">
            {categories.map((category) => (
              <button
                key={category.id}
                onClick={() => setActiveCategory(category.id)}
                className={`px-6 py-3 rounded-lg font-semibold transition-colors ${
                  activeCategory === category.id
                    ? 'bg-blue-600 text-white'
                    : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                {category.name}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Projects Grid */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {filteredProjects.map((project, index) => (
              <motion.div
                key={project.id}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-white dark:bg-gray-700 rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
              >
                <div className="relative">
                  <img 
                    src={project.image} 
                    alt={project.title}
                    className="w-full h-48 object-cover"
                  />
                  <div className="absolute top-2 right-2 bg-yellow-400 text-gray-900 px-2 py-1 rounded text-sm font-semibold">
                    {project.price}
                  </div>
                </div>
                <div className="p-6">
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                    {project.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-4">
                    {project.description}
                  </p>
                  
                  <div className="mb-4">
                    <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-2">
                      Технологии:
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {project.technologies.map((tech, techIndex) => (
                        <span
                          key={techIndex}
                          className="bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 px-2 py-1 rounded text-xs"
                        >
                          {tech}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="mb-4">
                    <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-2">
                      Возможности:
                    </h4>
                    <ul className="space-y-1">
                      {project.features.map((feature, featureIndex) => (
                        <li key={featureIndex} className="text-sm text-gray-600 dark:text-gray-400 flex items-center">
                          <FaCheck className="text-green-500 mr-2 flex-shrink-0" />
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center">
                      <FaStar className="text-yellow-400 mr-1" />
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        {project.rating}
                      </span>
                    </div>
                    <div className="flex items-center">
                      <FaEye className="text-gray-400 mr-1" />
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        {project.views}
                      </span>
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <a
                      href={project.demoUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex-1 bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors text-center text-sm font-semibold"
                    >
                      Демо
                    </a>
                    <Link
                      to={`/templates/${project.id}`}
                      className="flex-1 bg-gray-200 dark:bg-gray-600 text-gray-900 dark:text-white py-2 px-4 rounded hover:bg-gray-300 dark:hover:bg-gray-500 transition-colors text-center text-sm font-semibold"
                    >
                      Использовать
                    </Link>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Готовы создать свой сайт?
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Выберите подходящий шаблон или закажите индивидуальную разработку
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/templates"
              className="bg-yellow-400 text-gray-900 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-yellow-300 transition-colors"
            >
              Выбрать шаблон
            </Link>
            <Link
              to="/contact"
              className="bg-transparent border-2 border-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-gray-900 transition-colors"
            >
              Заказать разработку
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Portfolio;
