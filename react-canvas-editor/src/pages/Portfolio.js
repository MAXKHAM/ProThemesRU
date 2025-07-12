import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Button,
  Chip,
  Stack,
  TextField,
  InputAdornment,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material';
import { Search, FilterList } from '@mui/icons-material';

const categories = [
  'Все',
  'Бизнес',
  'E-commerce',
  'Портфолио',
  'Блог',
  'Лендинг',
  'Корпоративный',
];

const portfolioItems = [
  {
    id: 1,
    title: 'Цветочный магазин "Роза"',
    category: 'E-commerce',
    image: '/api/placeholder/400/300',
    description: 'Современный интернет-магазин цветов с онлайн-заказом и доставкой',
    tags: ['E-commerce', 'Онлайн-заказ', 'Доставка'],
    demoUrl: '#',
  },
  {
    id: 2,
    title: 'Автосервис "Мотор"',
    category: 'Бизнес',
    image: '/api/placeholder/400/300',
    description: 'Сайт автосервиса с онлайн-записью и прайс-листом услуг',
    tags: ['Бизнес', 'Онлайн-запись', 'Прайс-лист'],
    demoUrl: '#',
  },
  {
    id: 3,
    title: 'Студия красоты "Грация"',
    category: 'Бизнес',
    image: '/api/placeholder/400/300',
    description: 'Элегантный сайт салона красоты с галереей работ и расписанием',
    tags: ['Бизнес', 'Галерея', 'Расписание'],
    demoUrl: '#',
  },
  {
    id: 4,
    title: 'Фотограф Анна Петрова',
    category: 'Портфолио',
    image: '/api/placeholder/400/300',
    description: 'Персональный сайт фотографа с портфолио и блогом',
    tags: ['Портфолио', 'Блог', 'Галерея'],
    demoUrl: '#',
  },
  {
    id: 5,
    title: 'IT-компания "ТехноСофт"',
    category: 'Корпоративный',
    image: '/api/placeholder/400/300',
    description: 'Корпоративный сайт IT-компании с услугами и проектами',
    tags: ['Корпоративный', 'Услуги', 'Проекты'],
    demoUrl: '#',
  },
  {
    id: 6,
    title: 'Блог о путешествиях',
    category: 'Блог',
    image: '/api/placeholder/400/300',
    description: 'Персональный блог о путешествиях с красивыми фотографиями',
    tags: ['Блог', 'Путешествия', 'Фотографии'],
    demoUrl: '#',
  },
  {
    id: 7,
    title: 'Лендинг курсов английского',
    category: 'Лендинг',
    image: '/api/placeholder/400/300',
    description: 'Продающий лендинг для онлайн-курсов английского языка',
    tags: ['Лендинг', 'Образование', 'Онлайн-курсы'],
    demoUrl: '#',
  },
  {
    id: 8,
    title: 'Ресторан "Вкус"',
    category: 'Бизнес',
    image: '/api/placeholder/400/300',
    description: 'Сайт ресторана с меню, бронированием и отзывами',
    tags: ['Бизнес', 'Меню', 'Бронирование'],
    demoUrl: '#',
  },
];

function Portfolio() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('Все');

  const filteredItems = portfolioItems.filter((item) => {
    const matchesSearch = item.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         item.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'Все' || item.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <Box sx={{ py: 8 }}>
      <Container maxWidth="lg">
        {/* Header */}
        <Box textAlign="center" mb={8}>
          <Typography variant="h1" gutterBottom>
            Наши работы
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto' }}>
            Примеры сайтов, созданных на платформе ProThemesRU. Каждый проект уникален и адаптирован под потребности клиента.
          </Typography>
        </Box>

        {/* Filters */}
        <Box sx={{ mb: 6 }}>
          <Grid container spacing={3} alignItems="center">
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                placeholder="Поиск по названию или описанию..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Search />
                    </InputAdornment>
                  ),
                }}
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Категория</InputLabel>
                <Select
                  value={selectedCategory}
                  label="Категория"
                  onChange={(e) => setSelectedCategory(e.target.value)}
                  startAdornment={
                    <InputAdornment position="start">
                      <FilterList />
                    </InputAdornment>
                  }
                >
                  {categories.map((category) => (
                    <MenuItem key={category} value={category}>
                      {category}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </Box>

        {/* Portfolio Grid */}
        <Grid container spacing={4}>
          {filteredItems.map((item) => (
            <Grid item xs={12} md={6} lg={4} key={item.id}>
              <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                <CardMedia
                  component="img"
                  height="200"
                  image={item.image}
                  alt={item.title}
                  sx={{ objectFit: 'cover' }}
                />
                <CardContent sx={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
                  <Typography variant="h6" gutterBottom>
                    {item.title}
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2, flexGrow: 1 }}>
                    {item.description}
                  </Typography>
                  <Stack direction="row" spacing={1} sx={{ mb: 2 }} flexWrap="wrap" useFlexGap>
                    {item.tags.map((tag) => (
                      <Chip key={tag} label={tag} size="small" variant="outlined" />
                    ))}
                  </Stack>
                  <Stack direction="row" spacing={2}>
                    <Button
                      component="a"
                      href={item.demoUrl}
                      target="_blank"
                      variant="outlined"
                      size="small"
                      fullWidth
                    >
                      Демо
                    </Button>
                    <Button
                      component={Link}
                      to="/editor"
                      variant="contained"
                      size="small"
                      fullWidth
                    >
                      Использовать
                    </Button>
                  </Stack>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        {/* Empty State */}
        {filteredItems.length === 0 && (
          <Box textAlign="center" py={8}>
            <Typography variant="h6" color="text.secondary">
              По вашему запросу ничего не найдено
            </Typography>
            <Button
              onClick={() => {
                setSearchTerm('');
                setSelectedCategory('Все');
              }}
              sx={{ mt: 2 }}
            >
              Сбросить фильтры
            </Button>
          </Box>
        )}

        {/* CTA Section */}
        <Box sx={{ mt: 12, textAlign: 'center' }}>
          <Typography variant="h3" gutterBottom>
            Хотите создать похожий сайт?
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
            Начните создание прямо сейчас с нашим визуальным редактором
          </Typography>
          <Button
            component={Link}
            to="/editor"
            variant="contained"
            size="large"
            sx={{ mr: 2 }}
          >
            Начать создание
          </Button>
          <Button
            component={Link}
            to="/contact"
            variant="outlined"
            size="large"
          >
            Заказать разработку
          </Button>
        </Box>
      </Container>
    </Box>
  );
}

export default Portfolio; 