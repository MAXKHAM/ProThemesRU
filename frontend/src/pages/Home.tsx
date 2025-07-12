import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  FaRocket, 
  FaPalette, 
  FaMobile, 
  FaGlobe, 
  FaShieldAlt, 
  FaHeadset,
  FaStar,
  FaUsers,
  FaCheck,
  FaArrowRight,
  FaPlay
} from 'react-icons/fa';

const Home: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [currentTestimonial, setCurrentTestimonial] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  const features = [
    {
      icon: <FaRocket className="w-8 h-8" />,
      title: "Быстрый старт",
      description: "Создайте профессиональный сайт за 5 минут с помощью нашего конструктора"
    },
    {
      icon: <FaPalette className="w-8 h-8" />,
      title: "Готовые шаблоны",
      description: "100+ профессиональных шаблонов для любых сфер бизнеса"
    },
    {
      icon: <FaMobile className="w-8 h-8" />,
      title: "Адаптивный дизайн",
      description: "Ваш сайт будет отлично выглядеть на всех устройствах"
    },
    {
      icon: <FaGlobe className="w-8 h-8" />,
      title: "SEO оптимизация",
      description: "Встроенные инструменты для продвижения в поисковых системах"
    },
    {
      icon: <FaShieldAlt className="w-8 h-8" />,
      title: "Безопасность",
      description: "SSL сертификаты и защита от DDoS атак включены"
    },
    {
      icon: <FaHeadset className="w-8 h-8" />,
      title: "24/7 поддержка",
      description: "Наша команда всегда готова помочь вам"
    }
  ];

  const templates = [
    {
      id: 1,
      name: "Корпоративный сайт",
      category: "business",
      image: "/static/images/templates/business_landing.jpg",
      price: "Бесплатно",
      rating: 4.8,
      downloads: 1250
    },
    {
      id: 2,
      name: "Интернет-магазин",
      category: "ecommerce",
      image: "/static/images/templates/ecommerce_modern.jpg",
      price: "299₽/мес",
      rating: 4.9,
      downloads: 890
    },
    {
      id: 3,
      name: "Портфолио дизайнера",
      category: "portfolio",
      image: "/static/images/templates/portfolio_creative.jpg",
      price: "199₽/мес",
      rating: 4.7,
      downloads: 567
    },
    {
      id: 4,
      name: "Ресторан",
      category: "restaurant",
      image: "/static/images/templates/restaurant_elegant.jpg",
      price: "249₽/мес",
      rating: 4.6,
      downloads: 423
    }
  ];

  const testimonials = [
    {
      name: "Анна Петрова",
      company: "Дизайн-студия 'Креатив'",
      text: "ProThemes помог нам создать потрясающий сайт для нашей студии. Клиенты в восторге от современного дизайна!",
      rating: 5,
      avatar: "/static/images/avatars/anna.jpg"
    },
    {
      name: "Михаил Соколов",
      company: "ООО 'ТехноСервис'",
      text: "Благодаря ProThemes мы запустили корпоративный сайт за неделю. Отличная платформа для бизнеса!",
      rating: 5,
      avatar: "/static/images/avatars/mikhail.jpg"
    },
    {
      name: "Елена Козлова",
      company: "Интернет-магазин 'Мода'",
      text: "Создали интернет-магазин с нуля за 3 дня. Продажи выросли на 40% в первый месяц!",
      rating: 5,
      avatar: "/static/images/avatars/elena.jpg"
    }
  ];

  const stats = [
    { number: "10,000+", label: "Созданных сайтов" },
    { number: "500+", label: "Довольных клиентов" },
    { number: "99.9%", label: "Время работы" },
    { number: "24/7", label: "Поддержка" }
  ];

  const pricingPlans = [
    {
      name: "Базовый",
      price: "0₽",
      period: "навсегда",
      features: [
        "1 сайт",
        "5 страниц",
        "Базовые шаблоны",
        "Поддержка по email",
        "SSL сертификат"
      ],
      popular: false
    },
    {
      name: "Профессиональный",
      price: "299₽",
      period: "в месяц",
      features: [
        "5 сайтов",
        "Неограниченное количество страниц",
        "Все шаблоны",
        "Приоритетная поддержка",
        "Доменное имя в подарок",
        "SEO инструменты",
        "Аналитика"
      ],
      popular: true
    },
    {
      name: "Бизнес",
      price: "599₽",
      period: "в месяц",
      features: [
        "Неограниченное количество сайтов",
        "Неограниченное количество страниц",
        "Все шаблоны + эксклюзивные",
        "Персональный менеджер",
        "Белый лейбл",
        "API доступ",
        "Интеграции с CRM"
      ],
      popular: false
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-800">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-r from-blue-600 to-purple-700 text-white">
        <div className="absolute inset-0 bg-black opacity-20"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
          <div className="text-center">
            <motion.h1 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-4xl md:text-6xl font-bold mb-6"
            >
              Создайте профессиональный сайт
              <span className="block text-yellow-300">без знания кодирования</span>
            </motion.h1>
            <motion.p 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto"
            >
              Выбирайте из 100+ профессиональных шаблонов, настраивайте дизайн и получайте готовый сайт за несколько минут
            </motion.p>
            <motion.div 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="flex flex-col sm:flex-row gap-4 justify-center"
            >
              <Link
                to="/editor"
                className="bg-yellow-400 text-gray-900 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-yellow-300 transition-colors flex items-center justify-center gap-2"
              >
                <FaRocket />
                Начать создание
              </Link>
              <button className="bg-transparent border-2 border-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-gray-900 transition-colors flex items-center justify-center gap-2">
                <FaPlay />
                Смотреть демо
              </button>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="text-center"
              >
                <div className="text-3xl md:text-4xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                  {stat.number}
                </div>
                <div className="text-gray-600 dark:text-gray-400">
                  {stat.label}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Почему выбирают ProThemes?
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
              Мы создали платформу, которая делает создание сайтов простым и доступным для каждого
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-lg hover:shadow-xl transition-shadow"
              >
                <div className="text-blue-600 dark:text-blue-400 mb-4">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Templates Section */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Популярные шаблоны
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              Выбирайте из сотен профессиональных шаблонов
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {templates.map((template, index) => (
              <motion.div
                key={template.id}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-white dark:bg-gray-700 rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow"
              >
                <div className="relative">
                  <img 
                    src={template.image} 
                    alt={template.name}
                    className="w-full h-48 object-cover"
                  />
                  <div className="absolute top-2 right-2 bg-yellow-400 text-gray-900 px-2 py-1 rounded text-sm font-semibold">
                    {template.price}
                  </div>
                </div>
                <div className="p-6">
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
                    {template.name}
                  </h3>
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center">
                      <FaStar className="text-yellow-400 mr-1" />
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        {template.rating}
                      </span>
                    </div>
                    <span className="text-sm text-gray-600 dark:text-gray-400">
                      {template.downloads} загрузок
                    </span>
                  </div>
                  <Link
                    to={`/templates/${template.id}`}
                    className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors text-center block"
                  >
                    Использовать шаблон
                  </Link>
                </div>
              </motion.div>
            ))}
          </div>
          <div className="text-center mt-12">
            <Link
              to="/templates"
              className="bg-transparent border-2 border-blue-600 text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-600 hover:text-white transition-colors inline-flex items-center gap-2"
            >
              Смотреть все шаблоны
              <FaArrowRight />
            </Link>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Что говорят наши клиенты
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              Отзывы от реальных пользователей нашей платформы
            </p>
          </div>
          <div className="relative">
            <div className="flex transition-transform duration-500 ease-in-out">
              {testimonials.map((testimonial, index) => (
                <div
                  key={index}
                  className={`w-full flex-shrink-0 ${index === currentTestimonial ? 'block' : 'hidden'}`}
                >
                  <div className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-lg max-w-2xl mx-auto">
                    <div className="flex items-center mb-6">
                      <img 
                        src={testimonial.avatar} 
                        alt={testimonial.name}
                        className="w-16 h-16 rounded-full mr-4"
                      />
                      <div>
                        <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
                          {testimonial.name}
                        </h4>
                        <p className="text-gray-600 dark:text-gray-400">
                          {testimonial.company}
                        </p>
                      </div>
                    </div>
                    <p className="text-gray-700 dark:text-gray-300 text-lg italic mb-4">
                      "{testimonial.text}"
                    </p>
                    <div className="flex">
                      {[...Array(testimonial.rating)].map((_, i) => (
                        <FaStar key={i} className="text-yellow-400" />
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <div className="flex justify-center mt-8">
              {testimonials.map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentTestimonial(index)}
                  className={`w-3 h-3 rounded-full mx-1 ${
                    index === currentTestimonial ? 'bg-blue-600' : 'bg-gray-300'
                  }`}
                />
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Выберите подходящий тариф
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              Гибкие тарифы для любых потребностей
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {pricingPlans.map((plan, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className={`relative bg-white dark:bg-gray-700 p-8 rounded-lg shadow-lg ${
                  plan.popular ? 'ring-2 ring-blue-500 scale-105' : ''
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-blue-500 text-white px-4 py-1 rounded-full text-sm font-semibold">
                      Популярный
                    </span>
                  </div>
                )}
                <div className="text-center mb-8">
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                    {plan.name}
                  </h3>
                  <div className="text-4xl font-bold text-blue-600 dark:text-blue-400 mb-1">
                    {plan.price}
                  </div>
                  <div className="text-gray-600 dark:text-gray-400">
                    {plan.period}
                  </div>
                </div>
                <ul className="space-y-4 mb-8">
                  {plan.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-center">
                      <FaCheck className="text-green-500 mr-3 flex-shrink-0" />
                      <span className="text-gray-700 dark:text-gray-300">
                        {feature}
                      </span>
                    </li>
                  ))}
                </ul>
                <button className={`w-full py-3 px-6 rounded-lg font-semibold transition-colors ${
                  plan.popular
                    ? 'bg-blue-600 text-white hover:bg-blue-700'
                    : 'bg-gray-200 text-gray-900 hover:bg-gray-300 dark:bg-gray-600 dark:text-white dark:hover:bg-gray-500'
                }`}>
                  Выбрать тариф
                </button>
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
            Присоединяйтесь к тысячам довольных клиентов, которые уже создали свои сайты с ProThemes
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="bg-yellow-400 text-gray-900 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-yellow-300 transition-colors"
            >
              Начать бесплатно
            </Link>
            <Link
              to="/templates"
              className="bg-transparent border-2 border-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-gray-900 transition-colors"
            >
              Посмотреть шаблоны
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
