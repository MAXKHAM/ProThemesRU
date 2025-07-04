import React, { useState } from 'react';
import {
  Box,
  Container,
  Paper,
  TextField,
  Button,
  Typography,
  Alert,
  Avatar,
  useTheme,
} from '@mui/material';
import { useAuth } from '../../contexts/AuthContext';
import { User } from '../../types/user';

const Profile: React.FC = () => {
  const theme = useTheme();
  const { user, updateUser, logout } = useAuth();
  const [formData, setFormData] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  React.useEffect(() => {
    if (user) {
      setFormData({ ...user });
    }
  }, [user]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData) return;

    setError(null);
    setLoading(true);

    try {
      await updateUser(formData);
      setSuccess(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Произошла ошибка при обновлении профиля');
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return <div>Загрузка...</div>;
  }

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Paper
          sx={{
            p: 3,
            display: 'flex',
            flexDirection: 'column',
            borderRadius: 2,
            boxShadow: theme.shadows[6],
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
            <Avatar sx={{ mr: 2 }}>
              {user.name.charAt(0).toUpperCase()}
            </Avatar>
            <Typography variant="h5">{user.name}</Typography>
          </Box>

          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          {success && (
            <Alert severity="success" sx={{ mb: 2 }}>
              Профиль успешно обновлен
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit}>
            <TextField
              margin="normal"
              fullWidth
              id="name"
              label="Имя"
              name="name"
              value={formData?.name || ''}
              onChange={(e) =>
                setFormData((prev) => prev && { ...prev, name: e.target.value })
              }
            />
            <TextField
              margin="normal"
              fullWidth
              id="email"
              label="Email"
              name="email"
              disabled
              value={user.email}
            />
            <TextField
              margin="normal"
              fullWidth
              id="companyName"
              label="Название компании"
              name="companyName"
              value={formData?.companyName || ''}
              onChange={(e) =>
                setFormData((prev) => prev && { ...prev, companyName: e.target.value })
              }
            />
            <TextField
              margin="normal"
              fullWidth
              id="phone"
              label="Телефон"
              name="phone"
              value={formData?.phone || ''}
              onChange={(e) =>
                setFormData((prev) => prev && { ...prev, phone: e.target.value })
              }
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{
                mt: 3,
                mb: 2,
                backgroundColor: theme.palette.secondary.main,
                '&:hover': {
                  backgroundColor: theme.palette.secondary.dark,
                },
              }}
              disabled={loading}
            >
              {loading ? 'Сохранение...' : 'Сохранить'}
            </Button>
            <Button
              fullWidth
              variant="outlined"
              color="error"
              sx={{ mt: 2 }}
              onClick={logout}
            >
              Выйти из системы
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default Profile;
