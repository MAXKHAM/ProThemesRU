from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sqlalchemy import create_engine
from config import DATABASE_URI

class AnalyticsService:
    def __init__(self):
        self.engine = create_engine(DATABASE_URI)
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)

    def get_user_analytics(self, user_id: int) -> Dict:
        """
        Получает аналитику по пользователю
        
        Args:
            user_id: ID пользователя
            
        Returns:
            Словарь с аналитическими данными
        """
        # Загружаем данные пользователя
        user_data = self._load_user_data(user_id)
        
        # Анализируем активность
        activity = self._analyze_activity(user_data)
        
        # Анализируем эффективность сайтов
        site_metrics = self._analyze_site_metrics(user_data)
        
        # Генерируем визуализации
        visualizations = self._generate_visualizations(user_data)
        
        return {
            'activity': activity,
            'site_metrics': site_metrics,
            'visualizations': visualizations
        }

    def _load_user_data(self, user_id: int) -> pd.DataFrame:
        """Загружает данные пользователя из базы"""
        query = f"""
            SELECT 
                s.id as site_id,
                s.created_at,
                s.last_updated,
                s.views,
                s.conversions,
                s.bounce_rate,
                s.avg_session_duration
            FROM sites s
            WHERE s.user_id = {user_id}
        """
        return pd.read_sql(query, self.engine)

    def _analyze_activity(self, user_data: pd.DataFrame) -> Dict:
        """Анализирует активность пользователя"""
        # Количество созданных сайтов
        sites_count = len(user_data)
        
        # Среднее время между созданием сайтов
        if sites_count > 1:
            timestamps = pd.to_datetime(user_data['created_at'])
            avg_time_between = (timestamps.max() - timestamps.min()) / (sites_count - 1)
        else:
            avg_time_between = pd.Timedelta(0)
            
        return {
            'total_sites': sites_count,
            'avg_time_between': str(avg_time_between),
            'active_days': len(user_data['created_at'].dt.date.unique())
        }

    def _analyze_site_metrics(self, user_data: pd.DataFrame) -> Dict:
        """Анализирует метрики сайтов"""
        metrics = user_data[['views', 'conversions', 'bounce_rate', 'avg_session_duration']].mean()
        
        # Рассчитываем эффективность
        conversion_rate = metrics['conversions'] / metrics['views'] if metrics['views'] > 0 else 0
        engagement_score = (1 - metrics['bounce_rate']) * metrics['avg_session_duration']
        
        return {
            'avg_metrics': metrics.to_dict(),
            'conversion_rate': conversion_rate,
            'engagement_score': engagement_score
        }

    def _generate_visualizations(self, user_data: pd.DataFrame) -> Dict:
        """Генерирует визуализации"""
        visualizations = {}
        
        # График просмотров по времени
        if not user_data.empty:
            fig = px.line(
                user_data,
                x='created_at',
                y='views',
                title='История просмотров'
            )
            visualizations['views_over_time'] = fig.to_html(full_html=False)
            
            # График конверсий
            fig = px.bar(
                user_data,
                x='created_at',
                y='conversions',
                title='История конверсий'
            )
            visualizations['conversions_over_time'] = fig.to_html(full_html=False)
            
            # Тренд метрик
            metrics = ['views', 'conversions', 'bounce_rate', 'avg_session_duration']
            fig = go.Figure()
            for metric in metrics:
                fig.add_trace(go.Scatter(
                    x=user_data['created_at'],
                    y=user_data[metric],
                    name=metric
                ))
            fig.update_layout(title='Тренд метрик')
            visualizations['metrics_trend'] = fig.to_html(full_html=False)

        return visualizations

    def get_site_analytics(self, site_id: int) -> Dict:
        """
        Получает аналитику по конкретному сайту
        
        Args:
            site_id: ID сайта
            
        Returns:
            Словарь с аналитическими данными
        """
        # Загружаем данные сайта
        site_data = self._load_site_data(site_id)
        
        # Анализируем трафик
        traffic = self._analyze_traffic(site_data)
        
        # Анализируем поведение пользователей
        user_behavior = self._analyze_user_behavior(site_data)
        
        # Генерируем рекомендации
        recommendations = self._generate_recommendations(site_data)
        
        return {
            'traffic': traffic,
            'user_behavior': user_behavior,
            'recommendations': recommendations
        }

    def _load_site_data(self, site_id: int) -> pd.DataFrame:
        """Загружает данные сайта из базы"""
        query = f"""
            SELECT 
                v.timestamp,
                v.page,
                v.duration,
                v.referrer,
                v.device,
                v.browser,
                v.country,
                c.timestamp as conversion_time,
                c.type as conversion_type
            FROM views v
            LEFT JOIN conversions c ON v.session_id = c.session_id
            WHERE v.site_id = {site_id}
        """
        return pd.read_sql(query, self.engine)

    def _analyze_traffic(self, site_data: pd.DataFrame) -> Dict:
        """Анализирует трафик сайта"""
        # Источники трафика
        referrers = site_data['referrer'].value_counts()
        
        # Устройства
        devices = site_data['device'].value_counts()
        
        # Браузеры
        browsers = site_data['browser'].value_counts()
        
        # Страны
        countries = site_data['country'].value_counts()
        
        return {
            'referrers': referrers.to_dict(),
            'devices': devices.to_dict(),
            'browsers': browsers.to_dict(),
            'countries': countries.to_dict()
        }

    def _analyze_user_behavior(self, site_data: pd.DataFrame) -> Dict:
        """Анализирует поведение пользователей"""
        # Средняя продолжительность сессии
        avg_duration = site_data['duration'].mean()
        
        # Популярные страницы
        page_views = site_data['page'].value_counts()
        
        # Конверсии
        conversions = site_data[pd.notna(site_data['conversion_type'])]
        conversion_rate = len(conversions) / len(site_data)
        
        return {
            'avg_session_duration': avg_duration,
            'popular_pages': page_views.to_dict(),
            'conversion_rate': conversion_rate
        }

    def _generate_recommendations(self, site_data: pd.DataFrame) -> List[str]:
        """Генерирует рекомендации по улучшению"""
        recommendations = []
        
        # Анализируем конверсию
        if 'conversion_type' in site_data.columns:
            conversion_rate = len(site_data[pd.notna(site_data['conversion_type'])]) / len(site_data)
            if conversion_rate < 0.02:
                recommendations.append("Рассмотрите улучшение UX сайта")

        # Анализируем трафик
        if 'referrer' in site_data.columns:
            top_referrer = site_data['referrer'].value_counts().idxmax()
            if top_referrer == 'direct':
                recommendations.append("Рассмотрите активацию контент-маркетинга")

        # Анализируем устройства
        if 'device' in site_data.columns:
            mobile_users = (site_data['device'] == 'mobile').mean()
            if mobile_users > 0.5:
                recommendations.append("Оптимизируйте мобильную версию сайта")

        return recommendations

# Создаем экземпляр сервиса
analytics_service = AnalyticsService()
