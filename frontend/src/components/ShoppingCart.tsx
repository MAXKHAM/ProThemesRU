import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Link } from 'react-router-dom';
import { 
  FaShoppingCart, 
  FaTrash, 
  FaPlus, 
  FaMinus, 
  FaCreditCard,
  FaPaypal,
  FaBitcoin,
  FaLock,
  FaTruck,
  FaShieldAlt,
  FaUndo,
  FaHeart
} from 'react-icons/fa';

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
  image: string;
  category: string;
  description: string;
}

const ShoppingCart: React.FC = () => {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [couponCode, setCouponCode] = useState('');
  const [discount, setDiscount] = useState(0);
  const [loading, setLoading] = useState(false);

  // Mock cart items
  useEffect(() => {
    setCartItems([
      {
        id: '1',
        name: 'Бизнес-шаблон "Модерн"',
        price: 299,
        quantity: 1,
        image: '/static/images/templates/business_landing.jpg',
        category: 'Бизнес',
        description: 'Современный шаблон для корпоративных сайтов'
      },
      {
        id: '2',
        name: 'Портфолио "Креатив"',
        price: 199,
        quantity: 1,
        image: '/static/images/templates/portfolio-creative.jpg',
        category: 'Портфолио',
        description: 'Креативный шаблон для портфолио'
      }
    ]);
  }, []);

  const updateQuantity = (id: string, newQuantity: number) => {
    if (newQuantity <= 0) {
      removeItem(id);
      return;
    }
    
    setCartItems(items =>
      items.map(item =>
        item.id === id ? { ...item, quantity: newQuantity } : item
      )
    );
  };

  const removeItem = (id: string) => {
    setCartItems(items => items.filter(item => item.id !== id));
  };

  const applyCoupon = () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      if (couponCode.toLowerCase() === 'welcome10') {
        setDiscount(10);
        alert('Купон применен! Скидка 10%');
      } else {
        alert('Неверный код купона');
      }
      setLoading(false);
    }, 1000);
  };

  const subtotal = cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const discountAmount = (subtotal * discount) / 100;
  const total = subtotal - discountAmount;
  const itemCount = cartItems.reduce((sum, item) => sum + item.quantity, 0);

  const paymentMethods = [
    { id: 'card', name: 'Банковская карта', icon: <FaCreditCard /> },
    { id: 'paypal', name: 'PayPal', icon: <FaPaypal /> },
    { id: 'crypto', name: 'Криптовалюта', icon: <FaBitcoin /> }
  ];

  if (cartItems.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
        <div className="text-center">
          <div className="text-gray-400 text-6xl mb-4">🛒</div>
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
            Корзина пуста
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-8">
            Добавьте товары в корзину, чтобы продолжить покупки
          </p>
          <Link
            to="/templates"
            className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            Перейти к шаблонам
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-700 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.h1 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-4xl md:text-5xl font-bold mb-6"
            >
              Корзина покупок
            </motion.h1>
            <motion.p 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-xl max-w-3xl mx-auto"
            >
              Проверьте выбранные товары и оформите заказ
            </motion.p>
          </div>
        </div>
      </section>

      {/* Cart Content */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Cart Items */}
            <div className="lg:col-span-2">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  Товары в корзине ({itemCount})
                </h2>
                
                <div className="space-y-6">
                  <AnimatePresence>
                    {cartItems.map((item, index) => (
                      <motion.div
                        key={item.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 20 }}
                        transition={{ duration: 0.3, delay: index * 0.1 }}
                        className="flex items-center gap-4 p-4 border border-gray-200 dark:border-gray-700 rounded-lg"
                      >
                        <img
                          src={item.image}
                          alt={item.name}
                          className="w-20 h-20 object-cover rounded-lg"
                        />
                        
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900 dark:text-white">
                            {item.name}
                          </h3>
                          <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                            {item.description}
                          </p>
                          <span className="inline-block px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-xs rounded">
                            {item.category}
                          </span>
                        </div>
                        
                        <div className="flex items-center gap-2">
                          <button
                            onClick={() => updateQuantity(item.id, item.quantity - 1)}
                            className="w-8 h-8 flex items-center justify-center border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-700"
                          >
                            <FaMinus className="w-3 h-3" />
                          </button>
                          <span className="w-12 text-center font-semibold">
                            {item.quantity}
                          </span>
                          <button
                            onClick={() => updateQuantity(item.id, item.quantity + 1)}
                            className="w-8 h-8 flex items-center justify-center border border-gray-300 dark:border-gray-600 rounded hover:bg-gray-50 dark:hover:bg-gray-700"
                          >
                            <FaPlus className="w-3 h-3" />
                          </button>
                        </div>
                        
                        <div className="text-right">
                          <div className="font-semibold text-gray-900 dark:text-white">
                            {item.price * item.quantity}₽
                          </div>
                          <div className="text-sm text-gray-600 dark:text-gray-400">
                            {item.price}₽ за шт.
                          </div>
                        </div>
                        
                        <button
                          onClick={() => removeItem(item.id)}
                          className="p-2 text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded"
                        >
                          <FaTrash />
                        </button>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                </div>

                {/* Coupon Code */}
                <div className="mt-8 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-3">
                    Промокод
                  </h3>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={couponCode}
                      onChange={(e) => setCouponCode(e.target.value)}
                      placeholder="Введите код купона"
                      className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-600 dark:text-white"
                    />
                    <button
                      onClick={applyCoupon}
                      disabled={loading || !couponCode}
                      className="px-6 py-2 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {loading ? '...' : 'Применить'}
                    </button>
                  </div>
                  {discount > 0 && (
                    <div className="mt-2 text-sm text-green-600 dark:text-green-400">
                      ✓ Купон применен! Скидка {discount}%
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Order Summary */}
            <div className="lg:col-span-1">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 sticky top-8">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                  Итого заказа
                </h2>
                
                <div className="space-y-4 mb-6">
                  <div className="flex justify-between text-gray-600 dark:text-gray-400">
                    <span>Подытог ({itemCount} товаров)</span>
                    <span>{subtotal}₽</span>
                  </div>
                  {discount > 0 && (
                    <div className="flex justify-between text-green-600 dark:text-green-400">
                      <span>Скидка ({discount}%)</span>
                      <span>-{discountAmount}₽</span>
                    </div>
                  )}
                  <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
                    <div className="flex justify-between text-lg font-semibold text-gray-900 dark:text-white">
                      <span>Итого</span>
                      <span>{total}₽</span>
                    </div>
                  </div>
                </div>

                {/* Payment Methods */}
                <div className="mb-6">
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-3">
                    Способ оплаты
                  </h3>
                  <div className="space-y-2">
                    {paymentMethods.map((method) => (
                      <label key={method.id} className="flex items-center gap-3 p-3 border border-gray-200 dark:border-gray-700 rounded-lg cursor-pointer hover:bg-gray-50 dark:hover:bg-gray-700">
                        <input
                          type="radio"
                          name="payment"
                          value={method.id}
                          defaultChecked={method.id === 'card'}
                          className="text-blue-600"
                        />
                        <div className="flex items-center gap-2">
                          {method.icon}
                          <span className="text-gray-900 dark:text-white">{method.name}</span>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Security Info */}
                <div className="mb-6 p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-700 rounded-lg">
                  <div className="flex items-center gap-2 text-green-800 dark:text-green-200 mb-2">
                    <FaLock />
                    <span className="font-semibold">Безопасная оплата</span>
                  </div>
                  <p className="text-sm text-green-700 dark:text-green-300">
                    Ваши данные защищены SSL-шифрованием
                  </p>
                </div>

                {/* Checkout Button */}
                <Link
                  to="/checkout"
                  className="w-full bg-blue-600 text-white py-4 px-6 rounded-lg font-semibold hover:bg-blue-700 transition-colors text-center block"
                >
                  Оформить заказ
                </Link>

                {/* Additional Info */}
                <div className="mt-6 space-y-3 text-sm text-gray-600 dark:text-gray-400">
                  <div className="flex items-center gap-2">
                    <FaTruck />
                    <span>Бесплатная доставка</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <FaShieldAlt />
                    <span>Гарантия возврата 30 дней</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <FaUndo />
                    <span>Возможность отмены</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Continue Shopping */}
          <div className="mt-12 text-center">
            <Link
              to="/templates"
              className="inline-flex items-center gap-2 text-blue-600 dark:text-blue-400 hover:text-blue-700 dark:hover:text-blue-300 font-semibold"
            >
              <FaHeart />
              Продолжить покупки
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default ShoppingCart;
