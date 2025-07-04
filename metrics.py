from prometheus_flask_exporter import PrometheusMetrics
from flask import request
from functools import wraps
import time

def init_metrics(app):
    """Инициализирует метрики Prometheus"""
    metrics = PrometheusMetrics(app)
    
    # Метрики для запросов
    metrics.info('app_info', 'Application info', version='1.0.0')
    
    # Метрики для аутентификации
    metrics.counter(
        'auth_attempts',
        'Number of authentication attempts',
        labels={'success': lambda: 'yes' if request.path == '/login' and request.method == 'POST' else 'no'}
    )
    
    # Метрики для генерации сайтов
    metrics.counter(
        'sites_generated',
        'Number of sites generated',
        labels={'status': lambda: 'success' if request.path == '/constructor' and request.method == 'POST' else 'failed'}
    )
    
    # Декоратор для измерения времени выполнения
    def timeit(f):
        @wraps(f)
        def timed(*args, **kw):
            ts = time.time()
            result = f(*args, **kw)
            te = time.time()
            metrics.histogram(
                'request_processing_time',
                'Time spent processing request',
                labels={'endpoint': request.path}
            ).observe(te - ts)
            return result
        return timed
    
    return metrics, timeit
