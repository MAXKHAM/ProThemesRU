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

function TermsOfService() {
  return (
    <Box sx={{ py: 8 }}>
      <Container maxWidth="lg">
        <Typography variant="h1" gutterBottom>
          Условия использования
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
              Настоящие Условия использования (далее — "Условия") регулируют использование 
              платформы ProThemesRU, предоставляемой ООО "ПроТемесРУ" (далее — "Компания", "мы", "нас"). 
              Используя нашу платформу, вы соглашаетесь с настоящими Условиями.
            </Typography>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              2. Описание услуг
            </Typography>
            <Typography variant="body1" paragraph>
              ProThemesRU предоставляет следующие услуги:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Конструктор сайтов"
                  secondary="Визуальный редактор для создания веб-сайтов"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Хостинг сайтов"
                  secondary="Размещение и обслуживание созданных сайтов"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Готовые шаблоны"
                  secondary="Библиотека профессиональных шаблонов"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Техническая поддержка"
                  secondary="Помощь в использовании платформы"
                />
              </ListItem>
            </List>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              3. Регистрация и аккаунт
            </Typography>
            <Typography variant="body1" paragraph>
              Для использования платформы необходимо:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Создать аккаунт"
                  secondary="Предоставить достоверную информацию при регистрации"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Подтвердить email"
                  secondary="Подтвердить указанный email-адрес"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Соблюдать безопасность"
                  secondary="Не передавать данные аккаунта третьим лицам"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Уведомлять о нарушениях"
                  secondary="Сообщать о несанкционированном использовании аккаунта"
                />
              </ListItem>
            </List>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              4. Правила использования
            </Typography>
            <Typography variant="body1" paragraph>
              При использовании платформы запрещается:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Нарушение закона"
                  secondary="Создание контента, нарушающего законодательство РФ"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Нарушение прав"
                  secondary="Использование чужих материалов без разрешения"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Вредоносный контент"
                  secondary="Распространение вирусов, спама, фишинга"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Нарушение работы"
                  secondary="Попытки взлома, DDoS-атак, нарушения стабильности"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Неподобающий контент"
                  secondary="Порнография, насилие, дискриминация, оскорбления"
                />
              </ListItem>
            </List>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              5. Интеллектуальная собственность
            </Typography>
            <Typography variant="body1" paragraph>
              В отношении интеллектуальной собственности действуют следующие правила:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Платформа"
                  secondary="Все права на платформу принадлежат Компании"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Шаблоны"
                  secondary="Шаблоны предоставляются по лицензии для использования"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Пользовательский контент"
                  secondary="Права на созданный пользователем контент остаются у пользователя"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Лицензия"
                  secondary="Предоставляется ограниченная лицензия на использование платформы"
                />
              </ListItem>
            </List>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              6. Оплата и тарифы
            </Typography>
            <Typography variant="body1" paragraph>
              Условия оплаты и тарифы:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Тарифы"
                  secondary="Действующие тарифы указаны на сайте и могут изменяться"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Оплата"
                  secondary="Оплата производится авансом за выбранный период"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Автопродление"
                  secondary="Подписка автоматически продлевается, если не отменена"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Возврат средств"
                  secondary="Возврат возможен в течение 14 дней с момента оплаты"
                />
              </ListItem>
            </List>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              7. Ограничение ответственности
            </Typography>
            <Typography variant="body1" paragraph>
              Компания не несет ответственности за:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Пользовательский контент"
                  secondary="Содержимое, созданное пользователями"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Потерю данных"
                  secondary="Потерю данных по причинам, не зависящим от Компании"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Косвенные убытки"
                  secondary="Косвенные, случайные или последующие убытки"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Действия третьих лиц"
                  secondary="Действия провайдеров, партнеров или других третьих лиц"
                />
              </ListItem>
            </List>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              8. Прекращение использования
            </Typography>
            <Typography variant="body1" paragraph>
              Использование платформы может быть прекращено:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="По инициативе пользователя"
                  secondary="Отмена подписки или удаление аккаунта"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="По инициативе Компании"
                  secondary="При нарушении Условий или неоплате"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Доступ к данным"
                  secondary="После прекращения доступ к данным ограничивается"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Экспорт данных"
                  secondary="Пользователь может экспортировать свои данные"
                />
              </ListItem>
            </List>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              9. Техническая поддержка
            </Typography>
            <Typography variant="body1" paragraph>
              Условия технической поддержки:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Время работы"
                  secondary="Пн-Пт 9:00-18:00 МСК (для базового тарифа)"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Каналы связи"
                  secondary="Email, телефон, чат, мессенджеры"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Приоритет"
                  secondary="Приоритетная поддержка для премиум-тарифов"
                />
              </ListItem>
              <ListItem>
                <ListItemText
                  primary="Ответственность"
                  secondary="Поддержка только по вопросам работы платформы"
                />
              </ListItem>
            </List>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              10. Изменения в условиях
            </Typography>
            <Typography variant="body1" paragraph>
              Компания оставляет за собой право изменять настоящие Условия. 
              О значительных изменениях пользователи будут уведомлены по email 
              или через уведомления на платформе. Продолжение использования 
              платформы означает согласие с новыми условиями.
            </Typography>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              11. Применимое право
            </Typography>
            <Typography variant="body1" paragraph>
              Настоящие Условия регулируются законодательством Российской Федерации. 
              Все споры разрешаются в соответствии с российским правом в судах 
              по месту нахождения Компании.
            </Typography>

            <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
              12. Контактная информация
            </Typography>
            <Typography variant="body1" paragraph>
              По вопросам, связанным с настоящими Условиями, обращайтесь:
            </Typography>
            <List>
              <ListItem>
                <ListItemText
                  primary="Email"
                  secondary="legal@prothemesru.com"
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

export default TermsOfService; 