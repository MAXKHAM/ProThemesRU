export interface User {
  id: string;
  name: string;
  email: string;
  role: 'user' | 'admin';
  createdAt: string;
  updatedAt: string;
  avatar?: string;
  phone?: string;
  company?: string;
  preferences?: {
    language: 'ru' | 'en';
    theme: 'light' | 'dark';
    notifications: boolean;
  };
}

export interface AuthResponse {
  user: User;
  token: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
  confirmPassword: string;
  phone?: string;
  company?: string;
}

export interface UpdateUserRequest {
  name?: string;
  email?: string;
  phone?: string;
  company?: string;
  avatar?: string;
  preferences?: {
    language?: 'ru' | 'en';
    theme?: 'light' | 'dark';
    notifications?: boolean;
  };
} 