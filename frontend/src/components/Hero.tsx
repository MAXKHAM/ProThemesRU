import React from 'react';
import { Box, Container, Typography, Button, Grid, useTheme } from '@mui/material';
import { motion } from 'framer-motion';

const Hero: React.FC = () => {
  const theme = useTheme();

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: `linear-gradient(135deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Плавающие элементы */}
      <Box
        sx={{
          position: 'absolute',
          top: '20%',
          left: '-15%',
          width: '50%',
          height: '50%',
          background: 'rgba(255, 255, 255, 0.05)',
          borderRadius: '50%',
          pointerEvents: 'none',
        }}
      />
      <Box
        sx={{
          position: 'absolute',
          bottom: '-15%',
          right: '-15%',
          width: '60%',
          height: '60%',
          background: 'rgba(255, 255, 255, 0.03)',
          borderRadius: '50%',
          pointerEvents: 'none',
        }}
      />

      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
        <Grid container spacing={4} alignItems="center" sx={{ height: '100%' }}>
          <Grid item xs={12} md={6}>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <Typography
                variant="h1"
                sx={{
                  mb: 4,
                  fontWeight: 700,
                  background: `linear-gradient(45deg, ${theme.palette.secondary.main}, ${theme.palette.accent.main})`,
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  color: 'transparent',
                }}
              >
                Создайте сайт мечты
              </Typography>
              <Typography
                variant="h3"
                sx={{
                  mb: 6,
                  fontWeight: 600,
                  color: theme.palette.primary.light,
                }}
              >
                Более 1000 уникальных шаблонов для любого бизнеса
              </Typography>
              <Button
                variant="contained"
                size="large"
                sx={{
                  backgroundColor: theme.palette.secondary.main,
                  '&:hover': {
                    backgroundColor: theme.palette.secondary.dark,
                  },
                }}
              >
                Начать создание
              </Button>
            </motion.div>
          </Grid>
          <Grid item xs={12} md={6}>
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              <Box
                sx={{
                  width: '100%',
                  height: '400px',
                  background: `url('/images/hero-preview.png') center/cover`,
                  borderRadius: '24px',
                  boxShadow: theme.shadows[4],
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
                    background: `linear-gradient(0deg, rgba(0,0,0,0.2), rgba(0,0,0,0))`,
                  }}
                />
              </Box>
            </motion.div>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Hero;
