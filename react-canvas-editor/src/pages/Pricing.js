import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Switch,
  FormControlLabel,
  Stack,
  Divider,
} from '@mui/material';
import { Check, Close } from '@mui/icons-material';

const plans = [
  {
    name: 'Базовый',
    price: { monthly: 990, yearly: 790 },
    description: 'Идеально для небольших проектов и личных сайтов',
    features: [
      '1 сайт',
      '5 страниц',
      'Базовые шаблоны',
      'Поддержка по email',
      'SSL-сертификат',
      'Мобильная версия',
    ],
    notIncluded: [
      'AI-помощник',
      'Приоритетная поддержка',
      'Кастомный домен',
      'Аналитика',
    ],
    popular: false,
  },
  {
    name: 'Профессиональный',
    price: { monthly: 1990, yearly: 1590 },
    description: 'Для растущего бизнеса с расширенными возможностями',
    features: [
      '5 сайтов',
      'Неограниченное количество страниц',
      'Все шаблоны',
      'AI-помощник',
      'Приоритетная поддержка',
      'Кастомный домен',
      'Базовая аналитика',
      'Резервное копирование',
      'SEO-оптимизация',
    ],
    notIncluded: [
      'Продвинутая аналитика',
      'API доступ',
    ],
    popular: true,
  },
  {
    name: 'Бизнес',
    price: { monthly: 3990, yearly: 3190 },
    description: 'Максимальные возможности для крупных проектов',
    features: [
      'Неограниченное количество сайтов',
      'Неограниченное количество страниц',
      'Все шаблоны и функции',
      'AI-помощник',
      '24/7 Поддержка',
      'Неограниченное количество доменов',
      'Продвинутая аналитика',
      'API доступ',
      'Белый лейбл',
      'Персональный менеджер',
    ],
    notIncluded: [],
    popular: false,
  },
];

const additionalServices = [
  {
    name: 'Кастомный дизайн',
    price: 'от 15,000 ₽',
    description: 'Уникальный дизайн под ваши требования',
  },
  {
    name: 'SEO-продвижение',
    price: 'от 8,000 ₽/мес',
    description: 'Комплексное продвижение в поисковых системах',
  },
  {
    name: 'Техническая поддержка',
    price: 'от 5,000 ₽/мес',
    description: 'Полное сопровождение и обновление сайта',
  },
  {
    name: 'Интеграция с CRM',
    price: 'от 10,000 ₽',
    description: 'Подключение к вашей системе управления',
  },
];

function Pricing() {
  const [isYearly, setIsYearly] = useState(false);

  return (
    <Box sx={{ py: 8 }}>
      <Container maxWidth="lg">
        {/* Header */}
        <Box textAlign="center" mb={8}>
          <Typography variant="h1" gutterBottom>
            Тарифы и цены
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto', mb: 4 }}>
            Выберите подходящий тариф для вашего проекта. Все планы включают бесплатный пробный период.
          </Typography>
          
          {/* Billing Toggle */}
          <FormControlLabel
            control={
              <Switch
                checked={isYearly}
                onChange={(e) => setIsYearly(e.target.checked)}
              />
            }
            label={
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Typography>Ежемесячно</Typography>
                <Typography>Ежегодно</Typography>
                <Chip label="Экономия 20%" color="success" size="small" />
              </Box>
            }
          />
        </Box>

        {/* Pricing Plans */}
        <Grid container spacing={4} justifyContent="center">
          {plans.map((plan, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card
                sx={{
                  height: '100%',
                  position: 'relative',
                  transform: plan.popular ? 'scale(1.05)' : 'none',
                  border: plan.popular ? '2px solid' : '1px solid',
                  borderColor: plan.popular ? 'primary.main' : 'divider',
                }}
              >
                {plan.popular && (
                  <Chip
                    label="Популярный"
                    color="primary"
                    sx={{
                      position: 'absolute',
                      top: -12,
                      left: '50%',
                      transform: 'translateX(-50%)',
                      zIndex: 1,
                    }}
                  />
                )}
                <CardContent sx={{ p: 4 }}>
                  <Typography variant="h4" gutterBottom>
                    {plan.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                    {plan.description}
                  </Typography>
                  
                  <Box sx={{ mb: 4 }}>
                    <Typography variant="h2" component="span" color="primary">
                      {isYearly ? plan.price.yearly : plan.price.monthly}
                    </Typography>
                    <Typography variant="h6" component="span" color="text.secondary">
                      ₽/мес
                    </Typography>
                    {isYearly && (
                      <Typography variant="body2" color="success.main">
                        Оплата за год
                      </Typography>
                    )}
                  </Box>

                  <Button
                    component={Link}
                    to="/editor"
                    variant={plan.popular ? 'contained' : 'outlined'}
                    fullWidth
                    size="large"
                    sx={{ mb: 3 }}
                  >
                    Начать бесплатно
                  </Button>

                  <Divider sx={{ my: 3 }} />

                  <Typography variant="h6" gutterBottom>
                    Что включено:
                  </Typography>
                  <List dense>
                    {plan.features.map((feature, featureIndex) => (
                      <ListItem key={featureIndex} sx={{ px: 0 }}>
                        <ListItemIcon sx={{ minWidth: 32 }}>
                          <Check color="success" />
                        </ListItemIcon>
                        <ListItemText primary={feature} />
                      </ListItem>
                    ))}
                    {plan.notIncluded.map((feature, featureIndex) => (
                      <ListItem key={featureIndex} sx={{ px: 0 }}>
                        <ListItemIcon sx={{ minWidth: 32 }}>
                          <Close color="disabled" />
                        </ListItemIcon>
                        <ListItemText 
                          primary={feature} 
                          sx={{ '& .MuiListItemText-primary': { color: 'text.disabled' } }}
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        {/* Additional Services */}
        <Box sx={{ mt: 12 }}>
          <Typography variant="h2" textAlign="center" gutterBottom>
            Дополнительные услуги
          </Typography>
          <Typography variant="h6" color="text.secondary" textAlign="center" sx={{ mb: 6 }}>
            Индивидуальные решения для вашего бизнеса
          </Typography>
          
          <Grid container spacing={4}>
            {additionalServices.map((service, index) => (
              <Grid item xs={12} md={6} lg={3} key={index}>
                <Card sx={{ height: '100%' }}>
                  <CardContent sx={{ p: 3, textAlign: 'center' }}>
                    <Typography variant="h6" gutterBottom>
                      {service.name}
                    </Typography>
                    <Typography variant="h5" color="primary" gutterBottom>
                      {service.price}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {service.description}
                    </Typography>
                    <Button
                      component={Link}
                      to="/contact"
                      variant="outlined"
                      size="small"
                      sx={{ mt: 2 }}
                    >
                      Заказать
                    </Button>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* FAQ Section */}
        <Box sx={{ mt: 12 }}>
          <Typography variant="h2" textAlign="center" gutterBottom>
            Часто задаваемые вопросы
          </Typography>
          
          <Grid container spacing={4} sx={{ mt: 4 }}>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Есть ли бесплатный пробный период?
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Да, все тарифы включают 14-дневный бесплатный пробный период без ограничений.
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Можно ли изменить тариф позже?
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Да, вы можете изменить тариф в любое время. Изменения вступят в силу со следующего периода оплаты.
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Что происходит при отмене подписки?
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Ваш сайт останется доступным до конца оплаченного периода. После этого вы можете экспортировать данные.
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Typography variant="h6" gutterBottom>
                Поддерживается ли перенос с других платформ?
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Да, мы помогаем перенести сайты с других платформ. Свяжитесь с нашей поддержкой для деталей.
              </Typography>
            </Grid>
          </Grid>
        </Box>

        {/* CTA Section */}
        <Box sx={{ mt: 12, textAlign: 'center' }}>
          <Typography variant="h3" gutterBottom>
            Готовы начать?
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
            Создайте свой первый сайт уже сегодня
          </Typography>
          <Stack direction="row" spacing={2} justifyContent="center" flexWrap="wrap" useFlexGap>
            <Button
              component={Link}
              to="/editor"
              variant="contained"
              size="large"
            >
              Начать бесплатно
            </Button>
            <Button
              component={Link}
              to="/contact"
              variant="outlined"
              size="large"
            >
              Связаться с нами
            </Button>
          </Stack>
        </Box>
      </Container>
    </Box>
  );
}

export default Pricing; 