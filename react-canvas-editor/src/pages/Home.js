import React from 'react';
import { Link } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Stack,
  Chip,
  Avatar,
} from '@mui/material';
import {
  Create,
  Palette,
  Speed,
  Security,
  Support,
  CloudUpload,
} from '@mui/icons-material';

const features = [
  {
    icon: <Create sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'Визуальный редактор',
    description: 'Создавайте сайты без знания кода с помощью интуитивного drag-and-drop интерфейса',
  },
  {
    icon: <Palette sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'Готовые шаблоны',
    description: 'Более 100 профессиональных шаблонов для различных отраслей бизнеса',
  },
  {
    icon: <Speed sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'Быстрая публикация',
    description: 'Опубликуйте ваш сайт в один клик с автоматической оптимизацией',
  },
  {
    icon: <Security sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'Безопасность',
    description: 'SSL-сертификаты, резервное копирование и защита от DDoS-атак',
  },
  {
    icon: <Support sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: '24/7 Поддержка',
    description: 'Наша команда экспертов готова помочь вам в любое время',
  },
  {
    icon: <CloudUpload sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'AI-интеграция',
    description: 'Искусственный интеллект поможет создать контент и оптимизировать сайт',
  },
];

const testimonials = [
  {
    name: 'Анна Петрова',
    company: 'ООО "Цветочный рай"',
    text: 'Создала красивый сайт для цветочного магазина за 2 часа. Клиенты в восторге!',
    avatar: '/api/placeholder/40/40',
  },
  {
    name: 'Дмитрий Сидоров',
    company: 'ИП "Автосервис"',
    text: 'Отличная платформа для создания сайта автосервиса. Все функции работают идеально.',
    avatar: '/api/placeholder/40/40',
  },
  {
    name: 'Елена Козлова',
    company: 'Студия красоты "Грация"',
    text: 'Профессиональный сайт с онлайн-записью. Доходы выросли на 30%!',
    avatar: '/api/placeholder/40/40',
  },
];

const stats = [
  { number: '10,000+', label: 'Созданных сайтов' },
  { number: '500+', label: 'Довольных клиентов' },
  { number: '99.9%', label: 'Время работы' },
  { number: '24/7', label: 'Поддержка' },
];

function Home() {
  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          py: 12,
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={6} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h1" gutterBottom>
                Создавайте сайты
                <br />
                <Box component="span" sx={{ color: '#fbbf24' }}>
                  за минуты
                </Box>
              </Typography>
              <Typography variant="h5" sx={{ mb: 4, opacity: 0.9 }}>
                Профессиональный конструктор сайтов с AI-помощником и готовыми шаблонами
              </Typography>
              <Stack direction="row" spacing={2} flexWrap="wrap" useFlexGap>
                <Button
                  component={Link}
                  to="/editor"
                  variant="contained"
                  size="large"
                  sx={{
                    bgcolor: '#fbbf24',
                    color: '#1f2937',
                    '&:hover': { bgcolor: '#f59e0b' },
                  }}
                >
                  Начать создание
                </Button>
                <Button
                  component={Link}
                  to="/portfolio"
                  variant="outlined"
                  size="large"
                  sx={{ color: 'white', borderColor: 'white' }}
                >
                  Посмотреть работы
                </Button>
              </Stack>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box
                component="img"
                src="/api/placeholder/600/400"
                alt="Website Builder"
                sx={{
                  width: '100%',
                  height: 'auto',
                  borderRadius: 4,
                  boxShadow: '0 20px 40px rgba(0,0,0,0.3)',
                }}
              />
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Stats Section */}
      <Box sx={{ py: 6, bgcolor: 'background.default' }}>
        <Container maxWidth="lg">
          <Grid container spacing={4} justifyContent="center">
            {stats.map((stat, index) => (
              <Grid item xs={6} md={3} key={index}>
                <Box textAlign="center">
                  <Typography variant="h3" color="primary" fontWeight="bold">
                    {stat.number}
                  </Typography>
                  <Typography variant="body1" color="text.secondary">
                    {stat.label}
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* Features Section */}
      <Box sx={{ py: 12 }}>
        <Container maxWidth="lg">
          <Box textAlign="center" mb={8}>
            <Typography variant="h2" gutterBottom>
              Почему выбирают ProThemesRU?
            </Typography>
            <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto' }}>
              Все необходимые инструменты для создания профессионального сайта в одном месте
            </Typography>
          </Box>
          <Grid container spacing={4}>
            {features.map((feature, index) => (
              <Grid item xs={12} md={4} key={index}>
                <Card sx={{ height: '100%', textAlign: 'center' }}>
                  <CardContent sx={{ p: 4 }}>
                    <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                    <Typography variant="h6" gutterBottom>
                      {feature.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {feature.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* Testimonials Section */}
      <Box sx={{ py: 12, bgcolor: 'background.default' }}>
        <Container maxWidth="lg">
          <Box textAlign="center" mb={8}>
            <Typography variant="h2" gutterBottom>
              Отзывы наших клиентов
            </Typography>
          </Box>
          <Grid container spacing={4}>
            {testimonials.map((testimonial, index) => (
              <Grid item xs={12} md={4} key={index}>
                <Card>
                  <CardContent sx={{ p: 4 }}>
                    <Typography variant="body1" sx={{ mb: 3, fontStyle: 'italic' }}>
                      "{testimonial.text}"
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      <Avatar src={testimonial.avatar} sx={{ mr: 2 }} />
                      <Box>
                        <Typography variant="subtitle1" fontWeight="bold">
                          {testimonial.name}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {testimonial.company}
                        </Typography>
                      </Box>
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* CTA Section */}
      <Box
        sx={{
          py: 12,
          background: 'linear-gradient(135deg, #2563eb 0%, #7c3aed 100%)',
          color: 'white',
        }}
      >
        <Container maxWidth="md">
          <Box textAlign="center">
            <Typography variant="h2" gutterBottom>
              Готовы создать свой сайт?
            </Typography>
            <Typography variant="h6" sx={{ mb: 4, opacity: 0.9 }}>
              Присоединяйтесь к тысячам довольных клиентов уже сегодня
            </Typography>
            <Stack direction="row" spacing={2} justifyContent="center" flexWrap="wrap" useFlexGap>
              <Button
                component={Link}
                to="/editor"
                variant="contained"
                size="large"
                sx={{
                  bgcolor: '#fbbf24',
                  color: '#1f2937',
                  '&:hover': { bgcolor: '#f59e0b' },
                }}
              >
                Начать бесплатно
              </Button>
              <Button
                component={Link}
                to="/pricing"
                variant="outlined"
                size="large"
                sx={{ color: 'white', borderColor: 'white' }}
              >
                Посмотреть тарифы
              </Button>
            </Stack>
          </Box>
        </Container>
      </Box>
    </Box>
  );
}

export default Home; 