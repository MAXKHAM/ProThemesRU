import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

interface Order {
  id: string;
  orderNumber: string;
  projectName: string;
  amount: number;
  status: 'pending' | 'processing' | 'completed' | 'cancelled';
  createdAt: string;
  updatedAt: string;
  items: Array<{
    id: string;
    name: string;
    type: 'template' | 'service';
    price: number;
    quantity: number;
  }>;
  customer: {
    firstName: string;
    lastName: string;
    email: string;
    phone?: string;
    company?: string;
  };
}

const OrderHistory: React.FC = () => {
  const { user } = useAuth();
  const location = useLocation();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);

  useEffect(() => {
    // Показываем сообщение об успешном заказе, если оно есть
    if (location.state?.message) {
      alert(location.state.message);
      // Очищаем state после показа сообщения
      window.history.replaceState({}, document.title);
    }

    // Загрузка истории заказов
    const fetchOrders = async () => {
      try {
        // Здесь будет API-вызов для загрузки заказов пользователя
        // Пока используем моковые данные
        const mockOrders: Order[] = [
          {
            id: '1',
            orderNumber: 'ORD-2024-001',
            projectName: 'Бизнес-лендинг',
            amount: 5000,
            status: 'completed',
            createdAt: '2024-01-18T10:30:00Z',
            updatedAt: '2024-01-20T14:15:00Z',
            items: [
              {
                id: '1',
                name: 'Бизнес-лендинг',
                type: 'template',
                price: 5000,
                quantity: 1
              }
            ],
            customer: {
              firstName: 'Иван',
              lastName: 'Иванов',
              email: 'ivan@example.com',
              phone: '+7 (999) 123-45-67'
            }
          },
          {
            id: '2',
            orderNumber: 'ORD-2024-002',
            projectName: 'Интернет-магазин',
            amount: 15000,
            status: 'processing',
            createdAt: '2024-01-25T09:15:00Z',
            updatedAt: '2024-01-25T16:45:00Z',
            items: [
              {
                id: '2',
                name: 'Интернет-магазин',
                type: 'template',
                price: 12000,
                quantity: 1
              },
              {
                id: '3',
                name: 'Настройка платежей',
                type: 'service',
                price: 3000,
                quantity: 1
              }
            ],
            customer: {
              firstName: 'Иван',
              lastName: 'Иванов',
              email: 'ivan@example.com',
              phone: '+7 (999) 123-45-67'
            }
          }
        ];

        setOrders(mockOrders);
      } catch (error) {
        console.error('Ошибка загрузки заказов:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, [location.state]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'processing':
        return 'bg-blue-100 text-blue-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusText = (status: string) => {
    switch (status) {
      case 'completed':
        return 'Завершён';
      case 'processing':
        return 'В обработке';
      case 'pending':
        return 'Ожидает оплаты';
      case 'cancelled':
        return 'Отменён';
      default:
        return 'Неизвестно';
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ru-RU', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">История заказов</h1>
          <p className="mt-2 text-gray-600">
            Просматривайте статус и детали ваших заказов
          </p>
        </div>

        {orders.length === 0 ? (
          <div className="text-center py-12">
            <svg className="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">Нет заказов</h3>
            <p className="mt-1 text-sm text-gray-500">
              У вас пока нет заказов. Начните создавать свой первый сайт!
            </p>
            <div className="mt-6">
              <a
                href="/"
                className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700"
              >
                Перейти к покупкам
              </a>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {orders.map((order) => (
              <div key={order.id} className="bg-white shadow rounded-lg overflow-hidden">
                {/* Order Header */}
                <div className="px-6 py-4 border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-lg font-medium text-gray-900">
                        Заказ #{order.orderNumber}
                      </h3>
                      <p className="text-sm text-gray-500">
                        Создан {formatDate(order.createdAt)}
                      </p>
                    </div>
                    <div className="flex items-center space-x-4">
                      <span className={`px-3 py-1 text-sm font-medium rounded-full ${getStatusColor(order.status)}`}>
                        {getStatusText(order.status)}
                      </span>
                      <span className="text-lg font-semibold text-gray-900">
                        {order.amount.toLocaleString('ru-RU')} ₽
                      </span>
                    </div>
                  </div>
                </div>

                {/* Order Details */}
                <div className="px-6 py-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* Items */}
                    <div>
                      <h4 className="text-sm font-medium text-gray-900 mb-3">Товары</h4>
                      <div className="space-y-3">
                        {order.items.map((item) => (
                          <div key={item.id} className="flex justify-between items-center">
                            <div>
                              <p className="text-sm font-medium text-gray-900">{item.name}</p>
                              <p className="text-xs text-gray-500">
                                {item.type === 'template' ? 'Шаблон' : 'Услуга'}
                              </p>
                            </div>
                            <div className="text-right">
                              <p className="text-sm font-medium text-gray-900">
                                {item.price.toLocaleString('ru-RU')} ₽
                              </p>
                              <p className="text-xs text-gray-500">
                                x{item.quantity}
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Customer Info */}
                    <div>
                      <h4 className="text-sm font-medium text-gray-900 mb-3">Информация о заказе</h4>
                      <div className="space-y-2 text-sm">
                        <p>
                          <span className="text-gray-500">Клиент:</span>{' '}
                          {order.customer.firstName} {order.customer.lastName}
                        </p>
                        <p>
                          <span className="text-gray-500">Email:</span>{' '}
                          {order.customer.email}
                        </p>
                        {order.customer.phone && (
                          <p>
                            <span className="text-gray-500">Телефон:</span>{' '}
                            {order.customer.phone}
                          </p>
                        )}
                        {order.customer.company && (
                          <p>
                            <span className="text-gray-500">Компания:</span>{' '}
                            {order.customer.company}
                          </p>
                        )}
                        <p>
                          <span className="text-gray-500">Последнее обновление:</span>{' '}
                          {formatDate(order.updatedAt)}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="mt-6 pt-6 border-t border-gray-200">
                    <div className="flex space-x-4">
                      <button
                        onClick={() => setSelectedOrder(selectedOrder?.id === order.id ? null : order)}
                        className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                      >
                        {selectedOrder?.id === order.id ? 'Скрыть детали' : 'Показать детали'}
                      </button>
                      {order.status === 'pending' && (
                        <button className="text-green-600 hover:text-green-800 text-sm font-medium">
                          Оплатить
                        </button>
                      )}
                      {order.status === 'processing' && (
                        <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                          Связаться с поддержкой
                        </button>
                      )}
                    </div>
                  </div>

                  {/* Expanded Details */}
                  {selectedOrder?.id === order.id && (
                    <div className="mt-6 pt-6 border-t border-gray-200">
                      <h4 className="text-sm font-medium text-gray-900 mb-3">Дополнительная информация</h4>
                      <div className="bg-gray-50 rounded-lg p-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                          <div>
                            <p className="text-gray-500">ID заказа:</p>
                            <p className="font-mono">{order.id}</p>
                          </div>
                          <div>
                            <p className="text-gray-500">Номер заказа:</p>
                            <p className="font-mono">{order.orderNumber}</p>
                          </div>
                          <div>
                            <p className="text-gray-500">Дата создания:</p>
                            <p>{formatDate(order.createdAt)}</p>
                          </div>
                          <div>
                            <p className="text-gray-500">Последнее обновление:</p>
                            <p>{formatDate(order.updatedAt)}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default OrderHistory; 