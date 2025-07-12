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
} from '@mui/material';

function PrivacyPolicy() {
  return (
    <Box sx={{ py: 8 }}>
      <Container maxWidth="lg">
        <Typography variant="h1" gutterBottom>
          Политика конфиденциальности
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ mb: 6 }}>
          Последнее обновление: {new Date().toLocaleDateString('ru-RU')}
        </Typography>

        <Card>
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h5" gutterBottom>
              1. Общие положения
            </Typography>
            <Typography variant="body1" paragraph>
              ООО "ПроТемесРУ" (далее — "Компания", "мы", "нас", "наш") уважает вашу конфиденциальность 
              и обязуется защищать ваши персональные данные. Настоящая Политика конфиденциальности 
              описывает, как мы собираем, используем, храним и защищаем информацию, которую вы 
              предоставляете нам при использовании платформы ProThemesRU.
            </Typography>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              2. Собираемая информация
            </Typography>
            <Typography variant="body1" paragraph>
              Мы собираем следующие типы информации:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Персональные данные"
                  secondary="Имя, email, телефон, адрес для связи"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Данные аккаунта"
                  secondary="Логин, пароль, настройки профиля"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Данные сайтов"
                  secondary="Контент, дизайн, настройки созданных сайтов"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Технические данные"
                  secondary="IP-адрес, браузер, операционная система, время посещения"
                />
              </ListItem>
            </List>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              3. Цели использования данных
            </Typography>
            <Typography variant="body1" paragraph>
              Мы используем собранную информацию для следующих целей:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Предоставление услуг"
                  secondary="Создание и хостинг ваших сайтов, техническая поддержка"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Улучшение сервиса"
                  secondary="Анализ использования платформы для улучшения функциональности"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Коммуникация"
                  secondary="Отправка уведомлений, обновлений, ответы на запросы поддержки"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Безопасность"
                  secondary="Защита от мошенничества, обеспечение безопасности платформы"
                />
              </ListItem>
            </List>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              4. Передача данных третьим лицам
            </Typography>
            <Typography variant="body1" paragraph>
              Мы не продаем, не обмениваем и не передаем ваши персональные данные третьим лицам, 
              за исключением следующих случаев:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="С вашего согласия"
                  secondary="Только при получении вашего явного согласия"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Провайдеры услуг"
                  secondary="Надежные партнеры, помогающие нам предоставлять услуги (хостинг, платежи)"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Законные требования"
                  secondary="При требовании закона или для защиты наших прав"
                />
              </ListItem>
            </List>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              5. Безопасность данных
            </Typography>
            <Typography variant="body1" paragraph>
              Мы принимаем следующие меры для защиты ваших данных:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Шифрование"
                  secondary="Все данные передаются и хранятся с использованием SSL-шифрования"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Регулярные обновления"
                  secondary="Постоянное обновление систем безопасности"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Контроль доступа"
                  secondary="Ограниченный доступ к персональным данным только для уполномоченных сотрудников"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Резервное копирование"
                  secondary="Регулярное создание резервных копий данных"
                />
              </ListItem>
            </List>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              6. Ваши права
            </Typography>
            <Typography variant="body1" paragraph>
              Вы имеете следующие права в отношении ваших персональных данных:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Право на доступ"
                  secondary="Получить информацию о том, какие данные мы храним"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Право на исправление"
                  secondary="Исправить неточные или неполные данные"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Право на удаление"
                  secondary="Удалить ваши данные (с ограничениями)"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Право на ограничение"
                  secondary="Ограничить обработку ваших данных"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Право на переносимость"
                  secondary="Получить ваши данные в структурированном формате"
                />
              </ListItem>
            </List>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              7. Cookies и отслеживание
            </Typography>
            <Typography variant="body1" paragraph>
              Мы используем cookies и аналогичные технологии для:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Функциональность"
                  secondary="Обеспечение работы платформы и запоминание настроек"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Аналитика"
                  secondary="Понимание того, как используется платформа"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Безопасность"
                  secondary="Защита от мошенничества и обеспечение безопасности"
                />
              </ListItem>
            </List>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              8. Хранение данных
            </Typography>
            <Typography variant="body1" paragraph>
              Мы храним ваши данные в течение времени, необходимого для предоставления услуг 
              и выполнения наших обязательств. Данные удаляются в следующих случаях:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="По истечении срока хранения"
                  secondary="После прекращения использования услуг"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="По вашему запросу"
                  secondary="При получении запроса на удаление"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="По законным основаниям"
                  secondary="При требовании закона или для защиты прав"
                />
              </ListItem>
            </List>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              9. Международная передача данных
            </Typography>
            <Typography variant="body1" paragraph>
              Ваши данные могут передаваться и обрабатываться в странах, отличных от вашей 
              страны проживания. Мы обеспечиваем соответствующий уровень защиты данных 
              в соответствии с применимым законодательством.
            </Typography>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              10. Изменения в политике
            </Typography>
            <Typography variant="body1" paragraph>
              Мы можем время от времени обновлять настоящую Политику конфиденциальности. 
              О значительных изменениях мы будем уведомлять вас по email или через уведомления 
              на платформе.
            </Typography>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              11. Контактная информация
            </Typography>
            <Typography variant="body1" paragraph>
              Если у вас есть вопросы о настоящей Политике конфиденциальности или вы хотите 
              реализовать свои права, свяжитесь с нами:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Email"
                  secondary="privacy@prothemesru.com"
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
                  primary="Адрес"
                  secondary="г. Москва, ул. Примерная, д. 123, ООО 'ПроТемесРУ'"
                />
              </ListItem>
            </List>

            <Divider sx={{ my: 4 }} />

            <Box sx={{ textAlign: 'center', mt: 4 }}>
              <Chip label="Документ актуален" color="success" />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
                Последнее обновление: {new Date().toLocaleDateString('ru-RU')}
              </Typography>
            </Box>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
}

export default PrivacyPolicy; 