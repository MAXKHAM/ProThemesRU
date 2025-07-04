import React from 'react';
import { Box, Grid, Typography, Button, useTheme } from '@mui/material';
import { motion } from 'framer-motion';
import { useInView } from 'react-intersection-observer';

interface TemplateCardProps {
  title: string;
  category: string;
  image: string;
  features: string[];
}

const TemplateCard: React.FC<TemplateCardProps> = ({ title, category, image, features }) => {
  const theme = useTheme();
  const { ref, inView } = useInView({ threshold: 0.1 });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 20 }}
      animate={inView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }}
      transition={{ duration: 0.6 }}
    >
      <Box
        sx={{
          position: 'relative',
          borderRadius: '24px',
          overflow: 'hidden',
          boxShadow: theme.shadows[3],
          transition: 'transform 0.3s ease-in-out',
          '&:hover': {
            transform: 'translateY(-5px)',
          },
        }}
      >
        <Box
          sx={{
            width: '100%',
            height: '300px',
            background: `url(${image}) center/cover`,
            position: 'relative',
          }}
        >
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.5) 100%)',
            }}
          />
        </Box>
        <Box
          sx={{
            p: 4,
            background: theme.palette.background.paper,
          }}
        >
          <Typography variant="h4" gutterBottom>
            {title}
          </Typography>
          <Typography
            variant="subtitle1"
            color="text.secondary"
            gutterBottom
          >
            {category}
          </Typography>
          <Box sx={{ mb: 3 }}>
            {features.map((feature, index) => (
              <Typography
                key={index}
                variant="body2"
                sx={{
                  display: 'inline-block',
                  mr: 2,
                  mb: 1,
                  px: 2,
                  py: 0.5,
                  borderRadius: '12px',
                  background: theme.palette.primary.light,
                  color: theme.palette.primary.main,
                }}
              >
                {feature}
              </Typography>
            ))}
          </Box>
          <Button
            variant="contained"
            fullWidth
            sx={{
              backgroundColor: theme.palette.secondary.main,
              '&:hover': {
                backgroundColor: theme.palette.secondary.dark,
              },
            }}
          >
            Выбрать шаблон
          </Button>
        </Box>
      </Box>
    </motion.div>
  );
};

const TemplateGallery: React.FC = () => {
  const theme = useTheme();

  const templates = [
    {
      title: 'Модерн Бизнес',
      category: 'Бизнес',
      image: '/images/templates/business-modern.jpg',
      features: ['Адаптивный дизайн', 'SEO оптимизация', 'Быстрая загрузка'],
    },
    {
      title: 'Креатив Портфолио',
      category: 'Портфолио',
      image: '/images/templates/portfolio-creative.jpg',
      features: ['Галерея работ', 'Контактная форма', 'Социальные сети'],
    },
    {
      title: 'Элегантный Магазин',
      category: 'Э-коммерция',
      image: '/images/templates/ecommerce-elegant.jpg',
      features: ['Корзина', 'Система заказов', 'Интеграция платежей'],
    },
    // Добавьте больше шаблонов по аналогии
  ];

  return (
    <Box
      sx={{
        py: 8,
        background: theme.palette.background.paper,
      }}
    >
      <Container maxWidth="lg">
        <Typography
          variant="h2"
          align="center"
          sx={{
            mb: 6,
            fontWeight: 700,
            background: `linear-gradient(45deg, ${theme.palette.secondary.main}, ${theme.palette.accent.main})`,
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            color: 'transparent',
          }}
        >
          Наши шаблоны
        </Typography>
        <Grid container spacing={4}>
          {templates.map((template, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <TemplateCard {...template} />
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

export default TemplateGallery;
