import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

interface Feature {
  title: string;
  description: string;
  isAvailable: boolean;
}

interface Plan {
  title: string;
  price: number;
  features: Feature[];
  isPopular: boolean;
}

const plans: Plan[] = [
  {
    title: 'Базовый',
    price: 0,
    features: [
      { title: '1 шаблон', description: 'Базовый шаблон сайта', isAvailable: true },
      { title: 'Кастомизация', description: 'Основные настройки дизайна', isAvailable: true },
      { title: 'Поддержка', description: 'Базовая техническая поддержка', isAvailable: true },
      { title: 'Домен', description: 'Бесплатный поддомен', isAvailable: true },
      { title: 'Хостинг', description: 'Базовый хостинг', isAvailable: true },
      { title: 'SSL', description: 'Бесплатный SSL сертификат', isAvailable: true },
    ],
    isPopular: false
  },
  {
    title: 'Профессиональный',
    price: 9990,
    features: [
      { title: '5 шаблонов', description: 'Выбор из 5 профессиональных шаблонов', isAvailable: true },
      { title: 'Кастомизация', description: 'Полная настройка дизайна', isAvailable: true },
      { title: 'Поддержка', description: 'Приоритетная техническая поддержка', isAvailable: true },
      { title: 'Домен', description: 'Бесплатный поддомен', isAvailable: true },
      { title: 'Хостинг', description: 'Профессиональный хостинг', isAvailable: true },
      { title: 'SSL', description: 'Бесплатный SSL сертификат', isAvailable: true },
      { title: 'SEO', description: 'Базовая SEO оптимизация', isAvailable: true },
      { title: 'Аналитика', description: 'Базовый набор инструментов аналитики', isAvailable: true },
    ],
    isPopular: true
  },
  {
    title: 'Бизнес',
    price: 19990,
    features: [
      { title: '10 шаблонов', description: 'Выбор из 10 профессиональных шаблонов', isAvailable: true },
      { title: 'Кастомизация', description: 'Полная настройка дизайна', isAvailable: true },
      { title: 'Поддержка', description: '24/7 техническая поддержка', isAvailable: true },
      { title: 'Домен', description: 'Бесплатный поддомен', isAvailable: true },
      { title: 'Хостинг', description: 'Премиум хостинг', isAvailable: true },
      { title: 'SSL', description: 'Бесплатный SSL сертификат', isAvailable: true },
      { title: 'SEO', description: 'Продвинутая SEO оптимизация', isAvailable: true },
      { title: 'Аналитика', description: 'Полный набор инструментов аналитики', isAvailable: true },
      { title: 'CRM', description: 'Интеграция с CRM', isAvailable: true },
      { title: 'API', description: 'Доступ к API', isAvailable: true },
    ],
    isPopular: false
  }
];

const Pricing: React.FC = () => {
  return (
    <div className="py-12 bg-white dark:bg-gray-900">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-extrabold text-gray-900 dark:text-white text-center mb-12">
          Тарифы
        </h2>

        {/* Преимущества */}
        <div className="mb-16">
          <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-6">
            Почему стоит выбрать нас?
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
              <div className="text-4xl text-primary-600 mb-4">⚡</div>
              <h4 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Быстро и легко
              </h4>
              <p className="text-gray-600 dark:text-gray-300">
                Создайте профессиональный сайт за несколько минут без знания кодирования
              </p>
            </div>
            <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
              <div className="text-4xl text-primary-600 mb-4">💰</div>
              <h4 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Доступная цена
              </h4>
              <p className="text-gray-600 dark:text-gray-300">
                Начните с бесплатного плана и выберите подходящий тариф по мере роста вашего бизнеса
              </p>
            </div>
            <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow">
              <div className="text-4xl text-primary-600 mb-4">🌟</div>
              <h4 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
                Профессиональный дизайн
              </h4>
              <p className="text-gray-600 dark:text-gray-300">
                Выбирайте из профессиональных шаблонов, созданных экспертами дизайна
              </p>
            </div>
          </div>
        </div>

        {/* Тарифы */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {plans.map((plan) => (
            <motion.div
              key={plan.title}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className={`bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden ${
                plan.isPopular ? 'ring-4 ring-primary-600 dark:ring-primary-400' : ''
              }`}
            >
              {/* Шапка */}
              <div className="p-6">
                <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                  {plan.title}
                </h3>
                <div className="flex items-baseline">
                  <p className="text-4xl font-bold text-primary-600 dark:text-primary-400">
                    ₽{plan.price.toLocaleString()}
                  </p>
                  <p className="ml-1 text-sm text-gray-500 dark:text-gray-400">
                    в месяц
                  </p>
                </div>
              </div>

              {/* Фичи */}
              <div className="border-t border-gray-200 dark:border-gray-700">
                {plan.features.map((feature, index) => (
                  <div
                    key={index}
                    className="flex items-center py-4 px-6 border-b border-gray-200 dark:border-gray-700 last:border-0"
                  >
                    {feature.isAvailable ? (
                      <svg className="w-5 h-5 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                    ) : (
                      <svg className="w-5 h-5 text-red-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    )}
                    <div>
                      <h4 className="text-sm font-medium text-gray-900 dark:text-white">
                        {feature.title}
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {feature.description}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Кнопка */}
              <div className="p-6">
                <Link
                  to="/signup"
                  className={`inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md ${
                    plan.isPopular 
                      ? 'bg-primary-600 text-white hover:bg-primary-700 dark:bg-primary-400 dark:hover:bg-primary-500'
                      : 'bg-white text-primary-600 hover:bg-gray-100 dark:bg-gray-800 dark:text-primary-400'
                  }`}
                >
                  {plan.isPopular ? 'Выбрать' : 'Подробнее'}
                </Link>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Преимущества платной версии */}
        <div className="mt-16">
          <h3 className="text-2xl font-semibold text-gray-900 dark:text-white mb-8">
            Преимущества платной версии
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
              <h4 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                Полная кастомизация
              </h4>
              <ul className="space-y-2">
                <li className="flex items-center">
                  <svg className="w-5 h-5 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  Полный доступ к настройкам дизайна
                </li>
                <li className="flex items-center">
                  <svg className="w-5 h-5 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  Создание уникальных компонентов
                </li>
                <li className="flex items-center">
                  <svg className="w-5 h-5 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  Неограниченное количество страниц
                </li>
              </ul>
            </div>
            <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
              <h4 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                Профессиональная поддержка
              </h4>
              <ul className="space-y-2">
                <li className="flex items-center">
                  <svg className="w-5 h-5 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  24/7 техническая поддержка
                </li>
                <li className="flex items-center">
                  <svg className="w-5 h-5 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  Приоритетный доступ к обновлениям
                </li>
                <li className="flex items-center">
                  <svg className="w-5 h-5 text-green-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                  Обучение и консультации
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Pricing;
