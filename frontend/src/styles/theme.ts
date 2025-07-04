import { createTheme } from '@mui/material/styles';

// Палитра цветов (вдохновленная современным минимализмом с акцентами)
const palette = {
  primary: {
    main: '#2A363B', // Темно-синий
    light: '#455A64',
    dark: '#1C2833',
  },
  secondary: {
    main: '#F7DC6F', // Золотистый
    light: '#FFF3E0',
    dark: '#D7B84A',
  },
  accent: {
    main: '#FF6B6B', // Коралловый
    light: '#FF8E8E',
    dark: '#E64A4A',
  },
  background: {
    default: '#F5F5F5',
    paper: '#FFFFFF',
  },
  text: {
    primary: '#2A363B',
    secondary: '#455A64',
  },
};

// Типографика
const typography = {
  fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
  h1: {
    fontSize: '2.5rem',
    fontWeight: 700,
    lineHeight: 1.2,
    letterSpacing: '-0.015em',
  },
  h2: {
    fontSize: '2rem',
    fontWeight: 600,
    lineHeight: 1.3,
  },
  h3: {
    fontSize: '1.75rem',
    fontWeight: 600,
    lineHeight: 1.4,
  },
  h4: {
    fontSize: '1.5rem',
    fontWeight: 600,
    lineHeight: 1.5,
  },
  body1: {
    fontSize: '1rem',
    lineHeight: 1.6,
    letterSpacing: '0.009375em',
  },
  body2: {
    fontSize: '0.875rem',
    lineHeight: 1.43,
    letterSpacing: '0.01071em',
  },
};

// Шейдеры и тени
const shadows = [
  'none',
  '0px 1px 3px rgba(0,0,0,0.12), 0px 1px 2px rgba(0,0,0,0.24)',
  '0px 2px 4px rgba(0,0,0,0.14), 0px 3px 4px rgba(0,0,0,0.2)',
  '0px 3px 5px rgba(0,0,0,0.16), 0px 3px 10px rgba(0,0,0,0.23)',
  '0px 4px 6px rgba(0,0,0,0.18), 0px 4px 12px rgba(0,0,0,0.28)',
];

// Тема
export const theme = createTheme({
  palette,
  typography,
  shadows,
  shape: {
    borderRadius: 12,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '24px',
          textTransform: 'none',
          padding: '8px 24px',
          fontWeight: 600,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: '16px',
          boxShadow: '0px 4px 6px rgba(0,0,0,0.05)',
          transition: 'transform 0.2s ease-in-out',
          '&:hover': {
            transform: 'translateY(-2px)',
          },
        },
      },
    },
    MuiInputBase: {
      styleOverrides: {
        root: {
          borderRadius: '10px',
          padding: '12px 16px',
        },
      },
    },
  },
});
