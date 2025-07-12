import React, { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Grid,
  Card,
  CardContent,
  TextField,
  Button,
  Stack,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
} from '@mui/material';
import {
  Email,
  Phone,
  LocationOn,
  AccessTime,
  Send,
  WhatsApp,
  Telegram,
} from '@mui/icons-material';

const contactInfo = [
  {
    icon: <Email color="primary" />,
    title: 'Email',
    value: 'info@prothemesru.com',
    description: 'Основной канал связи',
  },
  {
    icon: <Phone color="primary" />,
    title: 'Телефон',
    value: '+7 (800) 555-35-35',
    description: 'Пн-Пт 9:00-18:00',
  },
  {
    icon: <WhatsApp color="success" />,
    title: 'WhatsApp',
    value: '+7 (900) 123-45-67',
    description: 'Быстрые ответы',
  },
  {
    icon: <Telegram color="info" />,
    title: 'Telegram',
    value: '@prothemesru_support',
    description: 'Поддержка в мессенджере',
  },
];

const supportTopics = [
  'Техническая поддержка',
  'Вопросы по тарифам',
  'Помощь с созданием сайта',
  'Интеграция с внешними сервисами',
  'Перенос сайта с другой платформы',
  'Кастомная разработка',
  'SEO и продвижение',
  'Обучение и консультации',
];

function Contact() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: '',
  });
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (field) => (event) => {
    setFormData({
      ...formData,
      [field]: event.target.value,
    });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // Здесь будет логика отправки формы
    console.log('Form submitted:', formData);
    setSubmitted(true);
    setFormData({
      name: '',
      email: '',
      phone: '',
      subject: '',
      message: '',
    });
  };

  return (
    <Box sx={{ py: 8 }}>
      <Container maxWidth="lg">
        {/* Header */}
        <Box textAlign="center" mb={8}>
          <Typography variant="h1" gutterBottom>
            Свяжитесь с нами
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ maxWidth: 600, mx: 'auto' }}>
            У вас есть вопросы? Мы готовы помочь! Свяжитесь с нами любым удобным способом.
          </Typography>
        </Box>

        <Grid container spacing={6}>
          {/* Contact Form */}
          <Grid item xs={12} lg={8}>
            <Card>
              <CardContent sx={{ p: 4 }}>
                <Typography variant="h4" gutterBottom>
                  Отправить сообщение
                </Typography>
                
                {submitted && (
                  <Alert severity="success" sx={{ mb: 3 }}>
                    Спасибо! Ваше сообщение отправлено. Мы свяжемся с вами в ближайшее время.
                  </Alert>
                )}

                <Box component="form" onSubmit={handleSubmit}>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        label="Ваше имя"
                        value={formData.name}
                        onChange={handleChange('name')}
                        required
                      />
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        label="Email"
                        type="email"
                        value={formData.email}
                        onChange={handleChange('email')}
                        required
                      />
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        label="Телефон"
                        value={formData.phone}
                        onChange={handleChange('phone')}
                      />
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <TextField
                        fullWidth
                        label="Тема"
                        value={formData.subject}
                        onChange={handleChange('subject')}
                        required
                      />
                    </Grid>
                    <Grid item xs={12}>
                      <TextField
                        fullWidth
                        label="Сообщение"
                        multiline
                        rows={6}
                        value={formData.message}
                        onChange={handleChange('message')}
                        required
                      />
                    </Grid>
                    <Grid item xs={12}>
                      <Button
                        type="submit"
                        variant="contained"
                        size="large"
                        startIcon={<Send />}
                        sx={{ minWidth: 200 }}
                      >
                        Отправить сообщение
                      </Button>
                    </Grid>
                  </Grid>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Contact Information */}
          <Grid item xs={12} lg={4}>
            <Stack spacing={3}>
              {/* Contact Details */}
              <Card>
                <CardContent sx={{ p: 4 }}>
                  <Typography variant="h5" gutterBottom>
                    Контактная информация
                  </Typography>
                  <List>
                    {contactInfo.map((contact, index) => (
                      <ListItem key={index} sx={{ px: 0 }}>
                        <ListItemIcon>{contact.icon}</ListItemIcon>
                        <ListItemText
                          primary={contact.title}
                          secondary={
                            <Box>
                              <Typography variant="body1" fontWeight="bold">
                                {contact.value}
                              </Typography>
                              <Typography variant="body2" color="text.secondary">
                                {contact.description}
                              </Typography>
                            </Box>
                          }
                        />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>

              {/* Office Hours */}
              <Card>
                <CardContent sx={{ p: 4 }}>
                  <Typography variant="h5" gutterBottom>
                    Время работы
                  </Typography>
                  <List>
                    <ListItem sx={{ px: 0 }}>
                      <ListItemIcon>
                        <AccessTime color="primary" />
                      </ListItemIcon>
                      <ListItemText
                        primary="Понедельник - Пятница"
                        secondary="9:00 - 18:00 (МСК)"
                      />
                    </ListItem>
                    <ListItem sx={{ px: 0 }}>
                      <ListItemIcon>
                        <AccessTime color="primary" />
                      </ListItemIcon>
                      <ListItemText
                        primary="Суббота"
                        secondary="10:00 - 16:00 (МСК)"
                      />
                    </ListItem>
                    <ListItem sx={{ px: 0 }}>
                      <ListItemIcon>
                        <AccessTime color="primary" />
                      </ListItemIcon>
                      <ListItemText
                        primary="Воскресенье"
                        secondary="Выходной"
                      />
                    </ListItem>
                  </List>
                </CardContent>
              </Card>

              {/* Address */}
              <Card>
                <CardContent sx={{ p: 4 }}>
                  <Typography variant="h5" gutterBottom>
                    Адрес офиса
                  </Typography>
                  <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                    <LocationOn color="primary" />
                    <Box>
                      <Typography variant="body1" fontWeight="bold">
                        ООО "ПроТемесРУ"
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        г. Москва, ул. Примерная, д. 123
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Бизнес-центр "Инновации", офис 456
                      </Typography>
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            </Stack>
          </Grid>
        </Grid>

        {/* Support Topics */}
        <Box sx={{ mt: 12 }}>
          <Typography variant="h2" textAlign="center" gutterBottom>
            Чем мы можем помочь?
          </Typography>
          <Typography variant="h6" color="text.secondary" textAlign="center" sx={{ mb: 6 }}>
            Наши специалисты готовы помочь вам с любыми вопросами
          </Typography>
          
          <Grid container spacing={2}>
            {supportTopics.map((topic, index) => (
              <Grid item xs={12} sm={6} md={4} lg={3} key={index}>
                <Card sx={{ height: '100%' }}>
                  <CardContent sx={{ p: 3, textAlign: 'center' }}>
                    <Typography variant="body1">
                      {topic}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>

        {/* FAQ Link */}
        <Box sx={{ mt: 12, textAlign: 'center' }}>
          <Typography variant="h4" gutterBottom>
            Не нашли ответ на свой вопрос?
          </Typography>
          <Typography variant="h6" color="text.secondary" sx={{ mb: 4 }}>
            Посмотрите раздел часто задаваемых вопросов
          </Typography>
          <Button
            variant="outlined"
            size="large"
            href="/faq"
          >
            Перейти к FAQ
          </Button>
        </Box>
      </Container>
    </Box>
  );
}

export default Contact; 