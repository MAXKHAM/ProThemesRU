import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

interface RedirectRule {
  from: string;
  to: string;
  status: number;
}

const redirectRules: RedirectRule[] = [
  // Старые URL на новые
  { from: '/old-templates', to: '/templates', status: 301 },
  { from: '/old-builder', to: '/builder', status: 301 },
  { from: '/old-portfolio', to: '/portfolio', status: 301 },
  
  // Обработка ошибок
  { from: '/error', to: '/404', status: 404 },
  { from: '/maintenance', to: '/503', status: 503 },
  
  // Сезонные редиректы
  { from: '/summer-sale', to: '/templates?category=summer', status: 302 },
  { from: '/christmas-offer', to: '/templates?category=christmas', status: 302 },
];

const RedirectManager: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  React.useEffect(() => {
    const rule = redirectRules.find(r => r.from === location.pathname);
    
    if (rule) {
      navigate(rule.to, { replace: true, state: { status: rule.status } });
    }
  }, [location, navigate]);

  return null;
};

export default RedirectManager;
