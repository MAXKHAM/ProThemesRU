import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  FaRocket, 
  FaUsers, 
  FaAward, 
  FaHeart,
  FaLightbulb,
  FaCog,
  FaGlobe,
  FaShieldAlt,
  FaStar,
  FaArrowRight
} from 'react-icons/fa';

const About: React.FC = () => {
  const team = [
    {
      name: "Александр Петров",
      position: "CEO & Основатель",
      photo: "/static/images/team/alexander.jpg",
      bio: "10+ лет опыта в веб-разработке. Создал более 200 успешных проектов.",
      social: {
        linkedin: "#",
        twitter: "#",
        github: "#"
      }
    },
    {
      name: "Мария Сидорова",
      position: "CTO & Технический директор",
      photo: "/static/images/team/maria.jpg",
      bio: "Эксперт по современным технологиям. Специалист по масштабированию систем.",
      social: {
        linkedin: "#",
        twitter: "#",
        github: "#"
      }
    },
    {
      name: "Дмитрий Козлов",
      position: "Дизайн-директор",
      photo: "/static/images/team/dmitry.jpg",
      bio: "UI/UX дизайнер с 8-летним стажем. Создал дизайн для 50+ проектов.",
      social: {
        linkedin: "#",
        twitter: "#",
        behance: "#"
      }
    },
    {
      name: "Елена Волкова",
      position: "Менеджер по развитию",
      photo: "/static/images/team/elena.jpg",
      bio: "Специалист по клиентскому сервису и развитию бизнеса.",
      social: {
        linkedin: "#",
        twitter: "#"
      }
    }
  ];

  const values = [
    {
      icon: <FaHeart className="w-8 h-8" />,
      title: "Любовь к делу",
      description: "Мы влюблены в то, что делаем, и это отражается в качестве наших продуктов"
    },
    {
      icon: <FaLightbulb className="w-8 h-8" />,
      title: "Инновации",
      description: "Постоянно следим за трендами и внедряем новые технологии"
    },
    {
      icon: <FaCog className="w-8 h-8" />,
      title: "Качество",
      description: "Не идем на компромиссы в вопросах качества и надежности"
    },
    {
      icon: <FaUsers className="w-8 h-8" />,
      title: "Команда",
      description: "Верим в силу команды и совместной работы над общими целями"
    }
  ];

  const achievements = [
    {
      number: "10,000+",
      label: "Созданных сайтов",
      icon: <FaGlobe className="w-6 h-6" />
    },
    {
      number: "500+",
      label: "Довольных клиентов",
      icon: <FaUsers className="w-6 h-6" />
    },
    {
      number: "99.9%",
      label: "Время работы",
      icon: <FaShieldAlt className="w-6 h-6" />
    },
    {
      number: "4.9",
      label: "Средний рейтинг",
      icon: <FaStar className="w-6 h-6" />
    }
  ];

  const timeline = [
    {
      year: "2018",
      title: "Основание компании",
      description: "Создание ProThemes с целью сделать веб-разработку доступной для всех"
    },
    {
      year: "2019",
      title: "Первый продукт",
      description: "Запуск конструктора сайтов с базовыми шаблонами"
    },
    {
      year: "2020",
      title: "Расширение команды",
      description: "Команда выросла до 10 человек, добавлены новые функции"
    },
    {
      year: "2021",
      title: "10,000 сайтов",
      description: "Достигнута отметка в 10,000 созданных сайтов"
    },
    {
      year: "2022",
      title: "AI интеграция",
      description: "Добавлены AI-функции для автоматизации создания контента"
    },
    {
      year: "2023",
      title: "Международное расширение",
      description: "Запуск платформы на международных рынках"
    }
  ];

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
              О компании ProThemes
            </motion.h1>
            <motion.p 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-xl max-w-3xl mx-auto"
            >
              Мы создаем технологии, которые помогают бизнесу расти в цифровом мире. 
              Наша миссия - сделать создание профессиональных сайтов простым и доступным.
            </motion.p>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
            >
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-6">
                Наша миссия
              </h2>
              <p className="text-lg text-gray-600 dark:text-gray-400 mb-6">
                Мы верим, что каждый бизнес заслуживает иметь профессиональный сайт. 
                Наша платформа объединяет простоту использования с мощными возможностями, 
                позволяя предпринимателям, дизайнерам и маркетологам создавать 
                потрясающие веб-сайты без необходимости изучать сложные технологии.
              </p>
              <p className="text-lg text-gray-600 dark:text-gray-400 mb-8">
                С 2018 года мы помогли более 10,000 клиентам создать их цифровое присутствие 
                и развить свой бизнес в интернете.
              </p>
              <Link
                to="/contact"
                className="bg-blue-600 text-white px-8 py-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors inline-flex items-center gap-2"
              >
                Связаться с нами
                <FaArrowRight />
              </Link>
            </motion.div>
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8 }}
              className="relative"
            >
              <img 
                src="/static/images/about/mission.jpg" 
                alt="Наша миссия"
                className="rounded-lg shadow-lg"
              />
            </motion.div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Наши ценности
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              Принципы, которые руководят нашей работой
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {values.map((value, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-white dark:bg-gray-800 p-8 rounded-lg shadow-lg text-center"
              >
                <div className="text-blue-600 dark:text-blue-400 mb-4">
                  {value.icon}
                </div>
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">
                  {value.title}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {value.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Achievements Section */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Наши достижения
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              Цифры, которыми мы гордимся
            </p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {achievements.map((achievement, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.8 }}
                whileInView={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="text-center"
              >
                <div className="text-blue-600 dark:text-blue-400 mb-4">
                  {achievement.icon}
                </div>
                <div className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-2">
                  {achievement.number}
                </div>
                <div className="text-gray-600 dark:text-gray-400">
                  {achievement.label}
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Timeline Section */}
      <section className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              История развития
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              Ключевые моменты нашего пути
            </p>
          </div>
          <div className="relative">
            <div className="absolute left-1/2 transform -translate-x-1/2 w-1 bg-blue-600 h-full"></div>
            <div className="space-y-12">
              {timeline.map((item, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                  className={`relative flex items-center ${
                    index % 2 === 0 ? 'flex-row' : 'flex-row-reverse'
                  }`}
                >
                  <div className={`w-1/2 ${index % 2 === 0 ? 'pr-8 text-right' : 'pl-8 text-left'}`}>
                    <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg">
                      <div className="text-2xl font-bold text-blue-600 dark:text-blue-400 mb-2">
                        {item.year}
                      </div>
                      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                        {item.title}
                      </h3>
                      <p className="text-gray-600 dark:text-gray-400">
                        {item.description}
                      </p>
                    </div>
                  </div>
                  <div className="absolute left-1/2 transform -translate-x-1/2 w-4 h-4 bg-blue-600 rounded-full border-4 border-white dark:border-gray-900"></div>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Наша команда
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              Профессионалы, которые создают будущее
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {team.map((member, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-white dark:bg-gray-700 rounded-lg shadow-lg overflow-hidden"
              >
                <img 
                  src={member.photo} 
                  alt={member.name}
                  className="w-full h-48 object-cover"
                />
                <div className="p-6">
                  <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-1">
                    {member.name}
                  </h3>
                  <p className="text-blue-600 dark:text-blue-400 mb-3">
                    {member.position}
                  </p>
                  <p className="text-gray-600 dark:text-gray-400 mb-4 text-sm">
                    {member.bio}
                  </p>
                  <div className="flex space-x-3">
                    {Object.entries(member.social).map(([platform, url]) => (
                      <a
                        key={platform}
                        href={url}
                        className="text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                      >
                        <i className={`fab fa-${platform}`}></i>
                      </a>
                    ))}
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
            Готовы работать с нами?
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
              to="/contact"
              className="bg-transparent border-2 border-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-white hover:text-gray-900 transition-colors"
            >
              Связаться с нами
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default About; 