import React from 'react';
import {
  Box,
  Container,
  Typography,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemText,
  Divider,
  Chip,
  Alert,
  Grid,
  Stack,
} from '@mui/material';
import {
  CheckCircle,
  Cancel,
  Warning,
  Info,
} from '@mui/icons-material';

function RefundPolicy() {
  return (
    <Box sx={{ py: 8 }}>
      <Container maxWidth="lg">
        <Typography variant="h1" gutterBottom>
          Политика возврата средств
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ mb: 6 }}>
          Последнее обновление: {new Date().toLocaleDateString('ru-RU')}
        </Typography>

        <Alert severity="info" sx={{ mb: 4 }}>
          <Typography variant="body1">
            Мы стремимся обеспечить полную удовлетворенность наших клиентов. 
            Если вы недовольны нашими услугами, мы готовы рассмотреть возврат средств.
          </Typography>
        </Alert>

        <Grid container spacing={4}>
          {/* Основная информация */}
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent sx={{ p: 4 }}>
                <Typography variant="h5" gutterBottom>
                  1. Общие условия возврата
                </Typography>
                <Typography variant="body1" paragraph>
                  ООО "ПроТемесРУ" предоставляет возможность возврата средств в соответствии 
                  с настоящей Политикой возврата. Возврат возможен в течение 14 дней с момента 
                  оплаты при соблюдении определенных условий.
                </Typography>

                <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
                  2. Когда возможен возврат
                </Typography>
                <List>
                  <ListItem>
                    <ListItemText
                      primary="Технические проблемы"
                      secondary="Если платформа не работает корректно и проблемы не решены в течение 48 часов"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Ошибка при оплате"
                      secondary="Двойная оплата или оплата неправильного тарифа"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Несоответствие описанию"
                      secondary="Если услуги не соответствуют описанию на сайте"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Отмена в течение 14 дней"
                      secondary="Отмена подписки в течение 14 дней с момента оплаты"
                    />
                  </ListItem>
                </List>

                <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
                  3. Когда возврат невозможен
                </Typography>
                <List>
                  <ListItem>
                    <ListItemText
                      primary="Истечение срока"
                      secondary="Прошло более 14 дней с момента оплаты"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Нарушение условий"
                      secondary="Нарушение Условий использования или Политики конфиденциальности"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Злоупотребление"
                      secondary="Попытки обмана или злоупотребления системой возврата"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Кастомные услуги"
                      secondary="Услуги, выполненные по индивидуальному заказу"
                    />
                  </ListItem>
                </List>

                <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
                  4. Процедура возврата
                </Typography>
                <Typography variant="body1" paragraph>
                  Для оформления возврата необходимо:
                </Typography>
                <List>
                  <ListItem>
                    <ListItemText
                      primary="Обращение в поддержку"
                      secondary="Связаться с поддержкой через email или телефон"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Предоставление информации"
                      secondary="Указать номер заказа, причину возврата, контактные данные"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Рассмотрение заявки"
                      secondary="Рассмотрение заявки в течение 3 рабочих дней"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Выполнение возврата"
                      secondary="Возврат средств на тот же способ оплаты в течение 5-10 дней"
                    />
                  </ListItem>
                </List>

                <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
                  5. Сумма возврата
                </Typography>
                <Typography variant="body1" paragraph>
                  Сумма возврата зависит от периода использования:
                </Typography>
                <List>
                  <ListItem>
                    <ListItemText
                      primary="Полный возврат"
                      secondary="100% суммы при отмене в течение 7 дней"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Частичный возврат"
                      secondary="50% суммы при отмене в течение 8-14 дней"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Комиссии"
                      secondary="Комиссии платежных систем не возвращаются"
                    />
                  </ListItem>
                </List>

                <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
                  6. Сроки возврата
                </Typography>
                <Typography variant="body1" paragraph>
                  Сроки возврата средств зависят от способа оплаты:
                </Typography>
                <List>
                  <ListItem>
                    <ListItemText
                      primary="Банковские карты"
                      secondary="5-10 рабочих дней"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Электронные кошельки"
                      secondary="1-3 рабочих дня"
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemText
                      primary="Банковские переводы"
                      secondary="3-7 рабочих дней"
                    />
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Боковая панель */}
          <Grid item xs={12} md={4}>
            <Stack spacing={3}>
              {/* Быстрые ссылки */}
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Быстрые ссылки
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemText
                        primary="Подать заявку на возврат"
                        secondary="Оформить возврат средств"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Проверить статус"
                        secondary="Узнать статус заявки"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Связаться с поддержкой"
                        secondary="Получить помощь"
                      />
                    </ListItem>
                  </List>
                </CardContent>
              </Card>

              {/* Контактная информация */}
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Контактная информация
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemText
                        primary="Email"
                        secondary="refund@prothemesru.com"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Телефон"
                        secondary="+7 (800) 555-35-35"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Время работы"
                        secondary="Пн-Пт 9:00-18:00 МСК"
                      />
                    </ListItem>
                  </List>
                </CardContent>
              </Card>

              {/* Важные примечания */}
              <Card>
                <CardContent sx={{ p: 3 }}>
                  <Typography variant="h6" gutterBottom>
                    Важные примечания
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemText
                        primary="Сохраняйте чеки"
                        secondary="Храните подтверждения оплаты"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Быстрое обращение"
                        secondary="Обращайтесь в течение 14 дней"
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Документируйте проблемы"
                        secondary="Делайте скриншоты ошибок"
                      />
                    </ListItem>
                  </List>
                </CardContent>
              </Card>
            </Stack>
          </Grid>
        </Grid>

        {/* Дополнительная информация */}
        <Box sx={{ mt: 6 }}>
          <Typography variant="h4" gutterBottom>
            Часто задаваемые вопросы о возврате
          </Typography>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Можно ли вернуть деньги за неиспользованный период?
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Да, если вы отменили подписку в течение 14 дней с момента оплаты. 
                    Сумма возврата зависит от периода использования.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Что делать, если платформа не работает?
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Сначала обратитесь в техническую поддержку. Если проблема не решена 
                    в течение 48 часов, можно оформить возврат средств.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Возвращаются ли комиссии платежных систем?
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Нет, комиссии платежных систем (банков, электронных кошельков) 
                    не возвращаются, так как они взимаются третьими лицами.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Можно ли вернуть деньги за кастомную разработку?
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Возврат за кастомные услуги возможен только до начала выполнения работ. 
                    После начала работ возврат не производится.
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>

        <Divider sx={{ my: 6 }} />

        <Box sx={{ textAlign: 'center' }}>
          <Chip label="Документ актуален" color="success" />
          <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
            Последнее обновление: {new Date().toLocaleDateString('ru-RU')}
          </Typography>
        </Box>
      </Container>
    </Box>
  );
}

export default RefundPolicy; 