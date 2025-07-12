import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FaChevronDown, FaChevronUp, FaSearch } from 'react-icons/fa';

const FAQ: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [openItems, setOpenItems] = useState<number[]>([]);

  const faqCategories = [
    {
      title: "Общие вопросы",
      icon: "🔍",
      items: [
        {
          question: "Что такое ProThemes?",
          answer: "ProThemes - это современная платформа для создания профессиональных веб-сайтов без знания программирования. Мы предоставляем готовые шаблоны, конструктор сайтов и все необходимые инструменты для запуска вашего онлайн-присутствия."
        },
        {
          question: "Сколько стоит создание сайта?",
          answer: "У нас есть несколько тарифных планов: Базовый (бесплатно), Профессиональный (299₽/мес) и Бизнес (599₽/мес). Каждый план включает определенное количество сайтов, страниц и функций."
        },
        {
          question: "Можно ли попробовать платформу бесплатно?",
          answer: "Да, мы предоставляем 14 дней бесплатного пробного периода для всех тарифных планов. В течение этого времени вы можете протестировать все функции без ограничений."
        },
        {
          question: "Какие типы сайтов можно создать?",
          answer: "Вы можете создать любые типы сайтов: корпоративные сайты, интернет-магазины, портфолио, блоги, сайты ресторанов, медицинских центров, образовательных учреждений и многое другое."
        }
      ]
    },
    {
      title: "Технические вопросы",
      icon: "⚙️",
      items: [
        {
          question: "Нужны ли знания программирования?",
          answer: "Нет, для создания сайта с ProThemes не требуются знания программирования. Наш конструктор интуитивно понятен и позволяет создавать сайты с помощью drag-and-drop интерфейса."
        },
        {
          question: "Адаптивны ли созданные сайты?",
          answer: "Да, все сайты, созданные с помощью ProThemes, автоматически адаптируются под все устройства: компьютеры, планшеты и смартфоны."
        },
        {
          question: "Какие браузеры поддерживаются?",
          answer: "Наши сайты работают во всех современных браузерах: Chrome, Firefox, Safari, Edge и других. Мы регулярно тестируем совместимость."
        },
        {
          question: "Можно ли подключить собственный домен?",
          answer: "Да, вы можете подключить собственный домен к любому тарифному плану. Мы также предоставляем бесплатный домен на планах Профессиональный и Бизнес."
        },
        {
          question: "Есть ли SSL сертификат?",
          answer: "Да, все сайты автоматически получают бесплатный SSL сертификат, обеспечивающий безопасное соединение и защиту данных."
        }
      ]
    },
    {
      title: "Дизайн и шаблоны",
      icon: "🎨",
      items: [
        {
          question: "Сколько шаблонов доступно?",
          answer: "У нас более 100 профессиональных шаблонов для различных сфер бизнеса. Новые шаблоны добавляются регулярно."
        },
        {
          question: "Можно ли изменить дизайн шаблона?",
          answer: "Да, каждый шаблон полностью настраивается. Вы можете изменить цвета, шрифты, изображения, добавить или удалить элементы."
        },
        {
          question: "Есть ли эксклюзивные шаблоны?",
          answer: "Да, на тарифе Бизнес доступны эксклюзивные шаблоны, которые не используются другими клиентами."
        },
        {
          question: "Можно ли создать индивидуальный дизайн?",
          answer: "Да, мы создаем индивидуальные дизайны для клиентов с особыми потребностями. Свяжитесь с нами для обсуждения вашего проекта."
        }
      ]
    },
    {
      title: "Оплата и тарифы",
      icon: "💳",
      items: [
        {
          question: "Какие способы оплаты принимаются?",
          answer: "Мы принимаем оплату банковскими картами (Visa, MasterCard, МИР), электронными кошельками (ЮMoney, QIWI), банковскими переводами и криптовалютами."
        },
        {
          question: "Можно ли изменить тарифный план?",
          answer: "Да, вы можете изменить тарифный план в любое время. При переходе на более дорогой план доплата взимается пропорционально оставшемуся периоду."
        },
        {
          question: "Есть ли скидки при оплате за год?",
          answer: "Да, при оплате за год предоставляется скидка до 20% в зависимости от выбранного тарифного плана."
        },
        {
          question: "Можно ли отменить подписку?",
          answer: "Да, вы можете отменить подписку в любое время. При отмене вы сохраняете доступ к сайтам до конца оплаченного периода."
        },
        {
          question: "Есть ли возврат денег?",
          answer: "Да, мы предоставляем 30-дневную гарантию возврата денег. Если вы недовольны сервисом, мы вернем полную стоимость подписки."
        }
      ]
    },
    {
      title: "Поддержка и помощь",
      icon: "🆘",
      items: [
        {
          question: "Какая поддержка предоставляется?",
          answer: "Мы предоставляем техническую поддержку через email, чат и телефон. Время ответа зависит от выбранного тарифного плана."
        },
        {
          question: "Есть ли обучающие материалы?",
          answer: "Да, у нас есть подробная документация, видеоуроки и вебинары для обучения работе с платформой."
        },
        {
          question: "Можно ли получить персонального менеджера?",
          answer: "Да, персональный менеджер предоставляется на тарифе Бизнес. Он поможет с любыми вопросами и задачами."
        },
        {
          question: "Есть ли сообщество пользователей?",
          answer: "Да, у нас есть активное сообщество пользователей в Telegram и на форуме, где можно обмениваться опытом и получать помощь."
        }
      ]
    },
    {
      title: "SEO и продвижение",
      icon: "📈",
      items: [
        {
          question: "Оптимированы ли сайты для SEO?",
          answer: "Да, все наши шаблоны оптимизированы для поисковых систем. Мы также предоставляем инструменты для SEO-настройки."
        },
        {
          question: "Можно ли подключить Google Analytics?",
          answer: "Да, вы можете подключить Google Analytics и другие системы аналитики к вашему сайту."
        },
        {
          question: "Есть ли встроенная аналитика?",
          answer: "Да, на планах Профессиональный и Бизнес доступна встроенная аналитика с подробной статистикой посещений."
        },
        {
          question: "Можно ли настроить мета-теги?",
          answer: "Да, вы можете настроить все мета-теги, заголовки и описания для лучшего продвижения в поисковых системах."
        }
      ]
    }
  ];

  const toggleItem = (index: number) => {
    setOpenItems(prev => 
      prev.includes(index) 
        ? prev.filter(i => i !== index)
        : [...prev, index]
    );
  };

  const filteredCategories = faqCategories.map(category => ({
    ...category,
    items: category.items.filter(item =>
      item.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.answer.toLowerCase().includes(searchTerm.toLowerCase())
    )
  })).filter(category => category.items.length > 0);

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
              Часто задаваемые вопросы
            </motion.h1>
            <motion.p 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-xl max-w-3xl mx-auto"
            >
              Найдите ответы на популярные вопросы о нашей платформе. 
              Если вы не нашли ответ, свяжитесь с нашей поддержкой.
            </motion.p>
          </div>
        </div>
      </section>

      {/* Search Section */}
      <section className="py-12 bg-white dark:bg-gray-800">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="relative">
            <FaSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
            <input
              type="text"
              placeholder="Поиск по вопросам..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-12 pr-4 py-4 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:text-white"
            />
          </div>
        </div>
      </section>

      {/* FAQ Content */}
      <section className="py-20 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          {filteredCategories.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-xl text-gray-600 dark:text-gray-400 mb-4">
                По вашему запросу ничего не найдено
              </p>
              <button
                onClick={() => setSearchTerm('')}
                className="text-blue-600 dark:text-blue-400 hover:underline"
              >
                Очистить поиск
              </button>
            </div>
          ) : (
            <div className="space-y-12">
              {filteredCategories.map((category, categoryIndex) => (
                <motion.div
                  key={categoryIndex}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: categoryIndex * 0.1 }}
                >
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center">
                    <span className="mr-3">{category.icon}</span>
                    {category.title}
                  </h2>
                  <div className="space-y-4">
                    {category.items.map((item, itemIndex) => {
                      const globalIndex = categoryIndex * 100 + itemIndex;
                      const isOpen = openItems.includes(globalIndex);
                      
                      return (
                        <motion.div
                          key={itemIndex}
                          initial={{ opacity: 0, y: 20 }}
                          whileInView={{ opacity: 1, y: 0 }}
                          transition={{ duration: 0.3, delay: itemIndex * 0.05 }}
                          className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700"
                        >
                          <button
                            onClick={() => toggleItem(globalIndex)}
                            className="w-full px-6 py-4 text-left flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                          >
                            <span className="font-semibold text-gray-900 dark:text-white">
                              {item.question}
                            </span>
                            {isOpen ? (
                              <FaChevronUp className="text-gray-400 w-4 h-4" />
                            ) : (
                              <FaChevronDown className="text-gray-400 w-4 h-4" />
                            )}
                          </button>
                          {isOpen && (
                            <motion.div
                              initial={{ opacity: 0, height: 0 }}
                              animate={{ opacity: 1, height: 'auto' }}
                              exit={{ opacity: 0, height: 0 }}
                              transition={{ duration: 0.3 }}
                              className="px-6 pb-4"
                            >
                              <p className="text-gray-600 dark:text-gray-400 leading-relaxed">
                                {item.answer}
                              </p>
                            </motion.div>
                          )}
                        </motion.div>
                      );
                    })}
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Contact Section */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
            Не нашли ответ на свой вопрос?
          </h2>
          <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">
            Наша команда поддержки готова помочь вам с любыми вопросами
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="mailto:support@prothemes.ru"
              className="bg-blue-600 text-white px-8 py-4 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Написать в поддержку
            </a>
            <a
              href="/contact"
              className="bg-transparent border-2 border-blue-600 text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-blue-600 hover:text-white transition-colors"
            >
              Связаться с нами
            </a>
          </div>
        </div>
      </section>
    </div>
  );
};

export default FAQ; 