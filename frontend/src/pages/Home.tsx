import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const Home: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-800">
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero section */}
        <div className="text-center">
          <h1 className="text-4xl tracking-tight font-extrabold text-gray-900 dark:text-white sm:text-5xl md:text-6xl">
            <span className="block">Создайте профессиональный сайт</span>
            <span className="block text-primary-600">без знания кодирования</span>
          </h1>
          <p className="mt-3 max-w-md mx-auto text-base text-gray-500 dark:text-gray-400 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            Выбирайте из профессиональных шаблонов, настраивайте дизайн и получайте готовый сайт за несколько минут
          </p>
          <div className="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
            <div className="rounded-md shadow">
              <Link
                to="/templates"
                className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 md:py-4 md:text-lg md:px-10"
              >
                Выбрать шаблон
              </Link>
            </div>
            <div className="mt-3 rounded-md shadow sm:mt-0 sm:ml-3">
              <Link
                to="/pricing"
                className="w-full flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-primary-600 bg-white hover:bg-gray-50 md:py-4 md:text-lg md:px-10 dark:bg-gray-800 dark:text-white dark:hover:bg-gray-700"
              >
                Цены
              </Link>
            </div>
          </div>
        </div>

        {/* Features section */}
        <div className="mt-16">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900 dark:text-white sm:text-4xl">
              Почему стоит выбрать нас
            </h2>
            <p className="mt-4 max-w-2xl mx-auto text-xl text-gray-600 dark:text-gray-300">
              Создайте профессиональный сайт быстро и легко
            </p>
          </div>
          <div className="mt-12 max-w-lg mx-auto grid gap-5 lg:grid-cols-3 lg:max-w-none lg:gap-8">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
              <div className="p-6">
                <div className="text-4xl text-primary-600">⚡</div>
                <h3 className="mt-2 text-xl font-semibold text-gray-900 dark:text-white">
                  Быстро и легко
                </h3>
                <p className="mt-3 text-base text-gray-600 dark:text-gray-300">
                  Создайте профессиональный сайт за несколько минут без знания кодирования
                </p>
              </div>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
              <div className="p-6">
                <div className="text-4xl text-primary-600">🌟</div>
                <h3 className="mt-2 text-xl font-semibold text-gray-900 dark:text-white">
                  Профессиональный дизайн
                </h3>
                <p className="mt-3 text-base text-gray-600 dark:text-gray-300">
                  Выбирайте из профессиональных шаблонов, созданных экспертами дизайна
                </p>
              </div>
            </div>
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
              <div className="p-6">
                <div className="text-4xl text-primary-600">💰</div>
                <h3 className="mt-2 text-xl font-semibold text-gray-900 dark:text-white">
                  Доступная цена
                </h3>
                <p className="mt-3 text-base text-gray-600 dark:text-gray-300">
                  Начните с бесплатного плана и выберите подходящий тариф по мере роста вашего бизнеса
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* How it works section */}
        <div className="mt-16">
          <div className="text-center">
            <h2 className="text-3xl font-extrabold text-gray-900 dark:text-white sm:text-4xl">
              Как это работает
            </h2>
            <p className="mt-4 max-w-2xl mx-auto text-xl text-gray-600 dark:text-gray-300">
              Создайте профессиональный сайт за 5 простых шагов
            </p>
          </div>
          <div className="mt-12 max-w-4xl mx-auto">
            <div className="space-y-12">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-600 text-white">
                    <span className="text-xl font-semibold">1</span>
                  </div>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                    Выберите шаблон
                  </h3>
                  <p className="mt-1 text-base text-gray-600 dark:text-gray-300">
                    Выбирайте из множества профессиональных шаблонов для вашего бизнеса
                  </p>
                </div>
              </div>
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-600 text-white">
                    <span className="text-xl font-semibold">2</span>
                  </div>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                    Настройте дизайн
                  </h3>
                  <p className="mt-1 text-base text-gray-600 dark:text-gray-300">
                    Изменяйте цвета, шрифты и компоненты сайта по вашему вкусу
                  </p>
                </div>
              </div>
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-600 text-white">
                    <span className="text-xl font-semibold">3</span>
                  </div>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                    Добавьте контент
                  </h3>
                  <p className="mt-1 text-base text-gray-600 dark:text-gray-300">
                    Добавляйте текст, изображения и другие элементы на ваш сайт
                  </p>
                </div>
              </div>
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className="flex items-center justify-center h-12 w-12 rounded-md bg-primary-600 text-white">
                    <span className="text-xl font-semibold">4</span>
                  </div>
                </div>
                <div className="ml-4">
                  <h3 className="text-lg font-medium text-gray-900 dark:text-white">
                    Опубликуйте сайт
                  </h3>
                  <p className="mt-1 text-base text-gray-600 dark:text-gray-300">
                    Опубликуйте ваш сайт с помощью нашего хостинга или своего домена
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* CTA section */}
        <div className="mt-16 bg-primary-600 dark:bg-primary-400">
          <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:py-16 lg:px-8">
            <div className="text-center">
              <h2 className="text-3xl font-extrabold text-white sm:text-4xl">
                Готовы начать?
              </h2>
              <p className="mt-4 text-lg leading-6 text-white">
                Создайте профессиональный сайт за несколько минут
              </p>
              <div className="mt-8 flex justify-center">
                <Link
                  to="/templates"
                  className="inline-flex items-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-700 hover:bg-primary-800 dark:bg-primary-500 dark:hover:bg-primary-600"
                >
                  Выбрать шаблон
                </Link>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;
