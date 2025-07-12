import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  FaCheck, 
  FaTimes, 
  FaStar, 
  FaRocket, 
  FaCrown, 
  FaGem,
  FaArrowRight,
  FaHeadset,
  FaShieldAlt,
  FaGlobe,
  FaMobile,
  FaPalette
} from 'react-icons/fa';

const Pricing: React.FC = () => {
  const [billingPeriod, setBillingPeriod] = useState<'monthly' | 'yearly'>('monthly');

  const plans = [
    {
      name: "Базовый",
      icon: <FaRocket className="w-8 h-8" />,
      description: "Идеально для начинающих и небольших проектов",
      monthlyPrice: 0,
      yearlyPrice: 0,
      features: [
        "1 сайт",
        "5 страниц",
        "Базовые шаблоны (10 шт.)",
        "Поддержка по email",
        "SSL сертификат",
        "Базовая аналитика",
        "Мобильная версия",
        "SEO базовые настройки"
      ],
      notIncluded: [
        "Доменное имя",
        "Приоритетная поддержка",
        "Расширенная аналитика",
        "API доступ",
        "Белый лейбл"
      ],
      popular: false,
      color: "blue"
    },
    {
      name: "Профессиональный",
      icon: <FaCrown className="w-8 h-8" />,
      description: "Для растущего бизнеса и профессионалов",
      monthlyPrice: 299,
      yearlyPrice: 2990,
      features: [
        "5 сайтов",
        "Неограниченное количество страниц",
        "Все шаблоны (100+ шт.)",
        "Приоритетная поддержка",
        "Доменное имя в подарок",
        "Расширенная аналитика",
        "Интеграции с CRM",
        "API доступ",
        "Белый лейбл",
        "Персональный менеджер",
        "Резервное копирование",
        "CDN ускорение"
      ],
      notIncluded: [
        "Неограниченное количество сайтов",
        "Эксклюзивные шаблоны"
      ],
      popular: true,
      color: "purple"
    },
    {
      name: "Бизнес",
      icon: <FaGem className="w-8 h-8" />,
      description: "Для крупных компаний и агентств",
      monthlyPrice: 599,
      yearlyPrice: 5990,
      features: [
        "Неограниченное количество сайтов",
        "Неограниченное количество страниц",
        "Все шаблоны + эксклюзивные",
        "Персональный менеджер 24/7",
        "Белый лейбл",
        "API доступ",
        "Интеграции с CRM",
        "Расширенная аналитика",
        "CDN ускорение",
        "Резервное копирование",
        "Техническая поддержка",
        "Обучение команды",
        "Индивидуальная настройка",
        "Приоритетная разработка"
      ],
      notIncluded: [],
      popular: false,
      color: "green"
    }
  ];

  const features = [
    {
      icon: <FaShieldAlt className="w-6 h-6" />,
      title: "Безопасность",
      description: "SSL сертификаты, защита от DDoS атак, регулярные обновления"
    },
    {
      icon: <FaGlobe className="w-6 h-6" />,
      title: "Глобальная доступность",
      description: "CDN сеть, 99.9% время работы, быстрая загрузка"
    },
    {
      icon: <FaMobile className="w-6 h-6" />,
      title: "Адаптивность",
      description: "Все сайты автоматически адаптируются под любые устройства"
    },
    {
      icon: <FaPalette className="w-6 h-6" />,
      title: "Готовые шаблоны",
      description: "100+ профессиональных шаблонов для любых сфер бизнеса"
    },
    {
      icon: <FaHeadset className="w-6 h-6" />,
      title: "Поддержка",
      description: "Техническая поддержка 24/7, обучающие материалы, видеоуроки"
    },
    {
      icon: <FaStar className="w-6 h-6" />,
      title: "Качество",
      description: "Современные технологии, оптимизация производительности"
    }
  ];

  const faq = [
    {
      question: "Можно ли изменить тарифный план?",
      answer: "Да, вы можете изменить тарифный план в любое время. При переходе на более дорогой план доплата взимается пропорционально оставшемуся периоду. При переходе на более дешевый план разница возвращается на счет."
    },
    {
      question: "Что входит в поддержку?",
      answer: "Поддержка включает помощь с настройкой сайта, решением технических вопросов, обновлениями и консультации по использованию платформы. Время ответа зависит от выбранного тарифа."
    },
    {
      question: "Можно ли отменить подписку?",
      answer: "Да, вы можете отменить подписку в любое время. При отмене вы сохраняете доступ к сайтам до конца оплаченного периода. После окончания периода сайты переходят в архив."
    },
    {
      question: "Есть ли пробный период?",
      answer: "Да, мы предоставляем 14 дней бесплатного пробного периода для всех тарифных планов. В течение этого времени вы можете протестировать все функции без ограничений."
    },
    {
      question: "Что такое белый лейбл?",
      answer: "Белый лейбл позволяет убрать наши логотипы и брендинг с сайтов, заменив их на ваши собственные. Это идеально для агентств и фрилансеров."
    },
    {
      question: "Какие способы оплаты принимаются?",
      answer: "Мы принимаем оплату банковскими картами (Visa, MasterCard, МИР), электронными кошельками (ЮMoney, QIWI), банковскими переводами и криптовалютами."
    }
  ];

  const getPrice = (plan: any) => {
    return billingPeriod === 'monthly' ? plan.monthlyPrice : plan.yearlyPrice;
  };

  const getSavings = (plan: any) => {
    if (billingPeriod === 'yearly' && plan.monthlyPrice > 0) {
      const monthlyTotal = plan.monthlyPrice * 12;
      const yearlyPrice = plan.yearlyPrice;
      return Math.round(((monthlyTotal - yearlyPrice) / monthlyTotal) * 100);
    }
    return 0;
  };

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
              Выберите подходящий тариф
            </motion.h1>
            <motion.p 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-xl max-w-3xl mx-auto mb-8"
            >
              Гибкие тарифы для любых потребностей. Начните бесплатно или выберите план для роста вашего бизнеса.
            </motion.p>
            
            {/* Billing Toggle */}
            <motion.div 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="flex items-center justify-center gap-4"
            >
              <span className={`text-sm ${billingPeriod === 'monthly' ? 'text-white' : 'text-gray-300'}`}>
                Ежемесячно
              </span>
              <button
                onClick={() => setBillingPeriod(billingPeriod === 'monthly' ? 'yearly' : 'monthly')}
                className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                  billingPeriod === 'yearly' ? 'bg-yellow-400' : 'bg-gray-300'
                }`}
              >
                <span
                  className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                    billingPeriod === 'yearly' ? 'translate-x-6' : 'translate-x-1'
                  }`}
                />
              </button>
              <span className={`text-sm ${billingPeriod === 'yearly' ? 'text-white' : 'text-gray-300'}`}>
                Ежегодно
                {billingPeriod === 'yearly' && (
                  <span className="ml-2 bg-yellow-400 text-gray-900 px-2 py-1 rounded text-xs font-semibold">
                    Экономия до 20%
                  </span>
                )}
              </span>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Pricing Plans */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {plans.map((plan, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className={`relative bg-white dark:bg-gray-700 rounded-lg shadow-lg p-8 ${
                  plan.popular ? 'ring-2 ring-purple-500 scale-105' : ''
                }`}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                    <span className="bg-purple-500 text-white px-4 py-1 rounded-full text-sm font-semibold">
                      Популярный
                    </span>
                  </div>
                )}

                <div className="text-center mb-8">
                  <div className="text-purple-600 dark:text-purple-400 mb-4">
                    {plan.icon}
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                    {plan.name}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-400 mb-6">
                    {plan.description}
                  </p>
                  
                  <div className="mb-4">
                    <span className="text-4xl font-bold text-gray-900 dark:text-white">
                      {getPrice(plan) === 0 ? 'Бесплатно' : `${getPrice(plan)}₽`}
                    </span>
                    {getPrice(plan) > 0 && (
                      <span className="text-gray-600 dark:text-gray-400">
                        /{billingPeriod === 'monthly' ? 'мес' : 'год'}
                      </span>
                    )}
                  </div>
                  
                  {getSavings(plan) > 0 && (
                    <div className="text-green-600 dark:text-green-400 text-sm font-semibold">
                      Экономия {getSavings(plan)}%
                    </div>
                  )}
                </div>

                <div className="space-y-4 mb-8">
                  <h4 className="font-semibold text-gray-900 dark:text-white">Включено:</h4>
                  {plan.features.map((feature, featureIndex) => (
                    <div key={featureIndex} className="flex items-center">
                      <FaCheck className="text-green-500 mr-3 flex-shrink-0" />
                      <span className="text-gray-700 dark:text-gray-300 text-sm">
                        {feature}
                      </span>
                    </div>
                  ))}
                  
                  {plan.notIncluded.length > 0 && (
                    <>
                      <h4 className="font-semibold text-gray-900 dark:text-white mt-6">Не включено:</h4>
                      {plan.notIncluded.map((feature, featureIndex) => (
                        <div key={featureIndex} className="flex items-center">
                          <FaTimes className="text-red-500 mr-3 flex-shrink-0" />
                          <span className="text-gray-500 dark:text-gray-500 text-sm">
                            {feature}
                          </span>
                        </div>
                      ))}
                    </>
                  )}
                </div>

                <Link
                  to={getPrice(plan) === 0 ? "/register" : "/checkout"}
                  className={`w-full py-3 px-6 rounded-lg font-semibold transition-colors text-center ${
                    plan.popular
                      ? 'bg-purple-600 text-white hover:bg-purple-700'
                      : 'bg-gray-200 text-gray-900 hover:bg-gray-300 dark:bg-gray-600 dark:text-white dark:hover:bg-gray-500'
                  }`}
                >
                  {getPrice(plan) === 0 ? 'Начать бесплатно' : 'Выбрать план'}
                </Link>
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
              Все тарифы включают
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              Базовые функции, необходимые для создания профессионального сайта
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-lg"
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

      {/* FAQ Section */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Часто задаваемые вопросы
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-400">
              Ответы на популярные вопросы о наших тарифах
            </p>
          </div>
          <div className="space-y-8">
            {faq.map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-gray-50 dark:bg-gray-700 p-6 rounded-lg"
              >
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">
                  {item.question}
                </h3>
                <p className="text-gray-600 dark:text-gray-400">
                  {item.answer}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-700 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Готовы начать?
          </h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto">
            Выберите подходящий тариф и создайте свой первый сайт уже сегодня
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/register"
              className="bg-yellow-400 text-gray-900 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-yellow-300 transition-colors inline-flex items-center gap-2"
            >
              Начать бесплатно
              <FaArrowRight />
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

export default Pricing;
