export interface Project {
  id: string;
  name: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
  status: 'draft' | 'published' | 'archived';
  elements: Element[];
  settings: ProjectSettings;
  publishedUrl?: string;
  thumbnail?: string;
}

export interface Element {
  id: string;
  type: string;
  content: string;
  style: React.CSSProperties;
  position: { x: number; y: number };
  size: { width: number; height: number };
  props?: Record<string, any>;
}

export interface ProjectSettings {
  canvasSize: { width: number; height: number };
  backgroundColor: string;
  theme: 'light' | 'dark';
  seo: {
    title: string;
    description: string;
    keywords: string[];
  };
}

export interface Template {
  id: string;
  name: string;
  category: string;
  description: string;
  price: number;
  isFree: boolean;
  image: string;
  features: string[];
  rating: number;
  downloads: number;
  tags: string[];
  elements: Element[];
  settings: ProjectSettings;
}

export interface Block {
  id: string;
  type: string;
  name: string;
  category: string;
  html: string;
  css: string;
  js?: string;
  properties: BlockProperty[];
  thumbnail?: string;
}

export interface BlockProperty {
  name: string;
  type: 'text' | 'number' | 'color' | 'select' | 'boolean' | 'image';
  label: string;
  defaultValue: any;
  options?: string[];
}

export interface Order {
  id: string;
  projectName: string;
  amount: number;
  status: 'pending' | 'processing' | 'completed' | 'cancelled';
  createdAt: string;
  items: OrderItem[];
  customerInfo: CustomerInfo;
}

export interface OrderItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
  type: 'template' | 'service' | 'addon';
}

export interface CustomerInfo {
  name: string;
  email: string;
  phone?: string;
  company?: string;
  address?: string;
} 