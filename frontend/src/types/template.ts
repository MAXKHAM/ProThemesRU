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
  elements: any[];
  settings: any;
  createdAt: string;
  updatedAt: string;
  author?: string;
  version?: string;
  compatibility?: string[];
  requirements?: {
    minWidth?: number;
    maxWidth?: number;
    features?: string[];
  };
}

export interface TemplateCategory {
  id: string;
  name: string;
  displayName: string;
  description: string;
  icon: string;
  count: number;
}

export interface TemplateFilter {
  category?: string;
  priceRange?: {
    min: number;
    max: number;
  };
  rating?: number;
  tags?: string[];
  features?: string[];
  sortBy?: 'popular' | 'rating' | 'price-low' | 'price-high' | 'newest';
} 