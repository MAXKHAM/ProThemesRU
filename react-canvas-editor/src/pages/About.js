import React from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  Avatar,
  Stack,
  Chip,
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
} from '@mui/material';
import {
  Business,
  EmojiEvents,
  Group,
  TrendingUp,
  Security,
  Support,
} from '@mui/icons-material';

const team = [
  {
    name: 'Александр Петров',
    position: 'CEO & Основатель',
    avatar: '/api/placeholder/120/120',
    bio: '10+ лет опыта в веб-разработке. Создал более 500 успешных проектов.',
    skills: ['Стратегия', 'Разработка', 'Менеджмент'],
  },
  {
    name: 'Мария Сидорова',
    position: 'CTO & Технический директор',
    avatar: '/api/placeholder/120/120',
    bio: 'Эксперт по современным технологиям. Архитектор платформы ProThemesRU.',
    skills: ['Архитектура', 'AI/ML', 'DevOps'],
  },
  {
    name: 'Дмитрий Козлов',
    position: 'Дизайн-директор',
    avatar: '/api/placeholder/120/120',
    bio: 'Создает уникальные дизайны, которые конвертируют посетителей в клиентов.',
    skills: ['UI/UX', 'Брендинг', 'Анимация'],
  },
  {
    name: 'Елена Волкова',
    position: 'Руководитель поддержки',
    avatar: '/api/placeholder/120/120',
    bio: 'Обеспечивает безупречный сервис и помогает клиентам достигать успеха.',
    skills: ['Поддержка', 'Обучение', 'Документация'],
  },
];

const values = [
  {
    icon: <Business sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'Инновации',
    description: 'Постоянно внедряем новые технологии для улучшения пользовательского опыта',
  },
  {
    icon: <Security sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'Надежность',
    description: 'Обеспечиваем стабильную работу платформы и безопасность данных клиентов',
  },
  {
    icon: <Support sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'Поддержка',
    description: '24/7 поддержка клиентов и помощь в решении любых вопросов',
  },
  {
    icon: <Group sx={{ fontSize: 40, color: 'primary.main' }} />,
    title: 'Сообщество',
    description: 'Создаем сообщество профессионалов и обмениваемся опытом',
  },
];

const milestones = [
  {
    year: '2020',
    title: 'Основание компании',
    description: 'Создание ProThemesRU с целью упростить создание сайтов',
  },
  {
    year: '2021',
    title: 'Запуск первой версии',
    description: 'Первый релиз конструктора сайтов с базовым функционалом',
  },
  {
    year: '2022',
    title: '1000+ клиентов',
    description: 'Достижение первой тысячи довольных клиентов',
  },
  {
    year: '2023',
    title: 'AI-интеграция',
    description: 'Внедрение искусственного интеллекта для автоматизации создания контента',
  },
  {
    year: '2024',
    title: 'Международная экспансия',
    description: 'Запуск платформы на международных рынках',
  },
];

const stats = [
  { number: '10,000+', label: 'Созданных сайтов' },
  { number: '500+', label: 'Довольных клиентов' },
  { number: '50+', label: 'Сотрудников' },
  { number: '99.9%', label: 'Время работы' },
];

function About() {
  return (
    <Box sx={{ py: 8 }}>
      <Container maxWidth="lg">
        {/* Hero Section */}
        <Box textAlign="center" mb={8}>
          <Typography variant="h1" gutterBottom>
            О компании
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 800, mx: 'auto' }}>
            ProThemesRU - это инновационная платформа для создания профессиональных сайтов, 
            которая объединяет простоту использования с мощными возможностями.
          </Typography>
        </Box>

        {/* Mission Section */}
        <Box sx={{ mb: 12 }}>
          <Grid container spacing={6} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h2" gutterBottom>
                Наша миссия
              </Typography>
              <Typography variant="h6" color="text.secondary" paragraph>
                Демократизировать создание веб-сайтов, сделав профессиональные инструменты 
                доступными для каждого предпринимателя и творческого человека.
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                Мы верим, что каждый должен иметь возможность создать красивый и функциональный 
                сайт без необходимости изучать сложные технологии или нанимать дорогих разработчиков.
              </Typography>
              <Stack direction="row" spacing={2} flexWrap="wrap" useFlexGap>
                <Chip icon={<EmojiEvents />} label="Лучшие практики" />
                <Chip icon={<TrendingUp />} label="Постоянное развитие" />
                <Chip icon={<Support />} label="Поддержка 24/7" />
              </Stack>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box
                component="img"
                src="/api/placeholder/600/400"
                alt="Our Mission"
                sx={{
                  width: '100%',
                  height: 'auto',
                  borderRadius: 4,
                  boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
                }}
              />
            </Grid>
          </Grid>
        </Box>

        {/* Stats Section */}
        <Box sx={{ mb: 12, py: 6, bgcolor: 'background.default', borderRadius: 4 }}>
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
        </Box>

        {/* Values Section */}
        <Box sx={{ mb: 12 }}>
          <Typography variant="h2" textAlign="center" gutterBottom>
            Наши ценности
          </Typography>
          <Grid container spacing={4} sx={{ mt: 4 }}>
            {values.map((value, index) => (
              <Grid item xs={12} md={6} lg={3} key={index}>
                <Card sx={{ height: '100%', textAlign: 'center' }}>
                  <CardContent sx={{ p: 4 }}>
                    <Box sx={{ mb: 2 }}>{value.icon}</Box>
                    <Typography variant="h6" gutterBottom>
                      {value.title}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {value.description}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* Timeline Section */}
        <Box sx={{ mb: 12 }}>
          <Typography variant="h2" textAlign="center" gutterBottom>
            История развития
          </Typography>
          <Timeline position="alternate" sx={{ mt: 4 }}>
            {milestones.map((milestone, index) => (
              <TimelineItem key={index}>
                <TimelineSeparator>
                  <TimelineDot color="primary" />
                  {index < milestones.length - 1 && <TimelineConnector />}
                </TimelineSeparator>
                <TimelineContent>
                  <Card>
                    <CardContent>
                      <Typography variant="h6" color="primary" gutterBottom>
                        {milestone.year}
                      </Typography>
                      <Typography variant="h6" gutterBottom>
                        {milestone.title}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {milestone.description}
                      </Typography>
                    </CardContent>
                  </Card>
                </TimelineContent>
              </TimelineItem>
            ))}
          </Timeline>
        </Box>

        {/* Team Section */}
        <Box sx={{ mb: 12 }}>
          <Typography variant="h2" textAlign="center" gutterBottom>
            Наша команда
          </Typography>
          <Typography variant="h6" color="text.secondary" textAlign="center" sx={{ mb: 6 }}>
            Профессионалы, которые делают ProThemesRU лучшей платформой для создания сайтов
          </Typography>
          
          <Grid container spacing={4}>
            {team.map((member, index) => (
              <Grid item xs={12} md={6} lg={3} key={index}>
                <Card sx={{ height: '100%', textAlign: 'center' }}>
                  <CardContent sx={{ p: 4 }}>
                    <Avatar
                      src={member.avatar}
                      sx={{ width: 120, height: 120, mx: 'auto', mb: 3 }}
                    />
                    <Typography variant="h6" gutterBottom>
                      {member.name}
                    </Typography>
                    <Typography variant="body2" color="primary" gutterBottom>
                      {member.position}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
                      {member.bio}
                    </Typography>
                    <Stack direction="row" spacing={1} justifyContent="center" flexWrap="wrap" useFlexGap>
                      {member.skills.map((skill) => (
                        <Chip key={skill} label={skill} size="small" variant="outlined" />
                      ))}
                    </Stack>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* CTA Section */}
        <Box sx={{ textAlign: 'center' }}>
          <Typography variant="h3" gutterBottom>
            Присоединяйтесь к нам
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
            Создавайте профессиональные сайты вместе с ProThemesRU
          </Typography>
          <Stack direction="row" spacing={2} justifyContent="center" flexWrap="wrap" useFlexGap>
            <Typography variant="body1" color="text.secondary">
              Готовы начать? Создайте свой первый сайт уже сегодня!
            </Typography>
          </Stack>
        </Box>
      </Container>
    </Box>
  );
}

export default About; 