import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  Stack,
  TextField,
  InputAdornment,
  Grid,
  Card,
  CardContent,
  Button,
} from '@mui/material';
import {
  ExpandMore,
  Search,
  Help,
  Payment,
  Security,
  Settings,
  Support,
} from '@mui/icons-material';

const faqCategories = [
  {
    name: 'Общие вопросы',
    icon: <Help color="primary" />,
    questions: [
      {
        question: 'Что такое ProThemesRU?',
        answer: 'ProThemesRU - это современная платформа для создания профессиональных веб-сайтов без знания программирования. Мы предоставляем визуальный редактор, готовые шаблоны и AI-помощника для создания красивых и функциональных сайтов.',
      },
      {
        question: 'Нужны ли знания программирования?',
        answer: 'Нет, знания программирования не требуются. Наш визуальный редактор позволяет создавать сайты с помощью drag-and-drop интерфейса. Все элементы можно настраивать через удобные панели свойств.',
      },
      {
        question: 'Сколько времени нужно для создания сайта?',
        answer: 'Время создания зависит от сложности проекта. Простой лендинг можно создать за 1-2 часа, а сложный многостраничный сайт - за несколько дней. Наша платформа значительно ускоряет процесс разработки.',
      },
    ],
  },
  {
    name: 'Тарифы и оплата',
    icon: <Payment color="primary" />,
    questions: [
      {
        question: 'Какие тарифы доступны?',
        answer: 'У нас есть три основных тарифа: Базовый (990₽/мес), Профессиональный (1990₽/мес) и Бизнес (3990₽/мес). Каждый тариф включает определенное количество сайтов, страниц и функций.',
      },
      {
        question: 'Есть ли бесплатный пробный период?',
        answer: 'Да, все тарифы включают 14-дневный бесплатный пробный период без ограничений. Вы можете протестировать все функции платформы перед покупкой.',
      },
      {
        question: 'Можно ли отменить подписку?',
        answer: 'Да, вы можете отменить подписку в любое время. Ваш сайт останется доступным до конца оплаченного периода. После отмены вы можете экспортировать данные.',
      },
      {
        question: 'Какие способы оплаты принимаются?',
        answer: 'Мы принимаем оплату банковскими картами (Visa, MasterCard, МИР), электронными кошельками (ЮMoney, QIWI) и банковскими переводами. Все платежи защищены SSL-шифрованием.',
      },
    ],
  },
  {
    name: 'Техническая поддержка',
    icon: <Support color="primary" />,
    questions: [
      {
        question: 'Как получить техническую поддержку?',
        answer: 'Вы можете связаться с нами через email (support@prothemesru.com), телефон (+7 800 555-35-35), WhatsApp или Telegram. Время работы: Пн-Пт 9:00-18:00 МСК.',
      },
      {
        question: 'Какая поддержка включена в тарифы?',
        answer: 'Базовый тариф включает поддержку по email, Профессиональный - приоритетную поддержку, Бизнес - 24/7 поддержку с персональным менеджером.',
      },
      {
        question: 'Помогаете ли с переносом сайта?',
        answer: 'Да, мы помогаем перенести сайты с других платформ. Наша команда может перенести контент, дизайн и функциональность. Стоимость зависит от сложности проекта.',
      },
    ],
  },
  {
    name: 'Безопасность и надежность',
    icon: <Security color="primary" />,
    questions: [
      {
        question: 'Безопасны ли мои данные?',
        answer: 'Да, мы обеспечиваем максимальную безопасность данных. Все сайты защищены SSL-сертификатами, данные хранятся на защищенных серверах с регулярным резервным копированием.',
      },
      {
        question: 'Какое время работы серверов?',
        answer: 'Мы гарантируем 99.9% время работы серверов. В случае технических работ мы заранее уведомляем клиентов. Мониторинг ведется 24/7.',
      },
      {
        question: 'Есть ли резервное копирование?',
        answer: 'Да, все данные автоматически резервируются ежедневно. Резервные копии хранятся в течение 30 дней. Вы также можете создать резервную копию вручную.',
      },
    ],
  },
  {
    name: 'Функции и возможности',
    icon: <Settings color="primary" />,
    questions: [
      {
        question: 'Какие шаблоны доступны?',
        answer: 'У нас более 100 профессиональных шаблонов для различных отраслей: бизнес, e-commerce, портфолио, блоги, лендинги. Все шаблоны адаптивные и оптимизированы для мобильных устройств.',
      },
      {
        question: 'Можно ли использовать свой домен?',
        answer: 'Да, начиная с Профессионального тарифа вы можете подключить свой домен. Мы предоставляем инструкции по настройке DNS-записей.',
      },
      {
        question: 'Есть ли SEO-инструменты?',
        answer: 'Да, платформа включает встроенные SEO-инструменты: редактирование мета-тегов, карта сайта, оптимизация изображений, интеграция с Google Analytics.',
      },
      {
        question: 'Поддерживается ли интеграция с внешними сервисами?',
        answer: 'Да, мы поддерживаем интеграцию с популярными сервисами: Google Analytics, Яндекс.Метрика, CRM-системы, платежные системы, социальные сети.',
      },
    ],
  },
];

function FAQ() {
  const [searchTerm, setSearchTerm] = useState('');
  const [expandedCategory, setExpandedCategory] = useState(null);

  const handleCategoryChange = (category) => (event, isExpanded) => {
    setExpandedCategory(isExpanded ? category : null);
  };

  const filteredCategories = faqCategories.map(category => ({
    ...category,
    questions: category.questions.filter(q =>
      q.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
      q.answer.toLowerCase().includes(searchTerm.toLowerCase())
    )
  })).filter(category => category.questions.length > 0);

  return (
    <Box sx={{ py: 8 }}>
      <Container maxWidth="lg">
        {/* Header */}
        <Box textAlign="center" mb={8}>
          <Typography variant="h1" gutterBottom>
            Часто задаваемые вопросы
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto' }}>
            Найдите ответы на самые популярные вопросы о платформе ProThemesRU
          </Typography>
        </Box>

        {/* Search */}
        <Box sx={{ mb: 6 }}>
          <TextField
            fullWidth
            placeholder="Поиск по вопросам..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search />
                </InputAdornment>
              ),
            }}
            sx={{ maxWidth: 600, mx: 'auto', display: 'block' }}
          />
        </Box>

        {/* FAQ Categories */}
        <Stack spacing={3}>
          {filteredCategories.map((category, categoryIndex) => (
            <Card key={categoryIndex}>
              <CardContent sx={{ p: 0 }}>
                <Accordion
                  expanded={expandedCategory === category.name}
                  onChange={handleCategoryChange(category.name)}
                >
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      {category.icon}
                      <Typography variant="h6">
                        {category.name}
                      </Typography>
                      <Chip label={category.questions.length} size="small" />
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Stack spacing={2}>
                      {category.questions.map((faq, faqIndex) => (
                        <Accordion key={faqIndex}>
                          <AccordionSummary expandIcon={<ExpandMore />}>
                            <Typography variant="subtitle1" fontWeight="medium">
                              {faq.question}
                            </Typography>
                          </AccordionSummary>
                          <AccordionDetails>
                            <Typography variant="body2" color="text.secondary">
                              {faq.answer}
                            </Typography>
                          </AccordionDetails>
                        </Accordion>
                      ))}
                    </Stack>
                  </AccordionDetails>
                </Accordion>
              </CardContent>
            </Card>
          ))}
        </Stack>

        {/* Empty State */}
        {filteredCategories.length === 0 && searchTerm && (
          <Box textAlign="center" py={8}>
            <Typography variant="h6" color="text.secondary" gutterBottom>
              По вашему запросу ничего не найдено
            </Typography>
            <Button
              onClick={() => setSearchTerm('')}
              variant="outlined"
            >
              Очистить поиск
            </Button>
          </Box>
        )}

        {/* Contact Section */}
        <Box sx={{ mt: 12, textAlign: 'center' }}>
          <Typography variant="h3" gutterBottom>
            Не нашли ответ на свой вопрос?
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
            Наша команда поддержки готова помочь вам
          </Typography>
          <Stack direction="row" spacing={2} justifyContent="center" flexWrap="wrap" useFlexGap>
            <Button
              variant="contained"
              size="large"
              href="/contact"
            >
              Связаться с поддержкой
            </Button>
            <Button
              variant="outlined"
              size="large"
              href="mailto:support@prothemesru.com"
            >
              Написать на email
            </Button>
          </Stack>
        </Box>

        {/* Quick Links */}
        <Box sx={{ mt: 12 }}>
          <Typography variant="h4" textAlign="center" gutterBottom>
            Полезные ссылки
          </Typography>
          <Grid container spacing={3} sx={{ mt: 4 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Card sx={{ height: '100%', textAlign: 'center' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Документация
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    Подробные инструкции по использованию платформы
                  </Typography>
                  <Button variant="outlined" size="small">
                    Открыть
                  </Button>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card sx={{ height: '100%', textAlign: 'center' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Видеоуроки
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    Обучающие видео по созданию сайтов
                  </Typography>
                  <Button variant="outlined" size="small">
                    Смотреть
                  </Button>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card sx={{ height: '100%', textAlign: 'center' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Сообщество
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    Форум пользователей и обмен опытом
                  </Typography>
                  <Button variant="outlined" size="small">
                    Присоединиться
                  </Button>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card sx={{ height: '100%', textAlign: 'center' }}>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Статус сервиса
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    Мониторинг работы платформы
                  </Typography>
                  <Button variant="outlined" size="small">
                    Проверить
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>
      </Container>
    </Box>
  );
}

export default FAQ; 