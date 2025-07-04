import redis
from datetime import datetime, timedelta
from typing import Any, Optional
from functools import wraps
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

class CacheService:
    def __init__(self):
        self.client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        
    def cache(self, timeout: int = 3600):
        """
        Декоратор для кэширования результатов функции
        
        Args:
            timeout: Время жизни кэша в секундах (по умолчанию 1 час)
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Формируем ключ кэша
                cache_key = f"cache:{func.__name__}:{str(args)}:{str(kwargs)}"
                
                # Проверяем наличие в кэше
                cached_result = self.client.get(cache_key)
                if cached_result:
                    return json.loads(cached_result)
                
                # Выполняем функцию
                result = func(*args, **kwargs)
                
                # Сохраняем в кэш
                self.client.set(cache_key, json.dumps(result), ex=timeout)
                
                return result
            return wrapper
        return decorator

    def get(self, key: str) -> Optional[Any]:
        """Получает значение из кэша"""
        value = self.client.get(key)
        return json.loads(value) if value else None

    def set(self, key: str, value: Any, timeout: int = 3600) -> None:
        """Устанавливает значение в кэш"""
        self.client.set(key, json.dumps(value), ex=timeout)

    def delete(self, key: str) -> None:
        """Удаляет значение из кэша"""
        self.client.delete(key)

    def clear(self, pattern: str = "*") -> None:
        """Очищает кэш по паттерну"""
        for key in self.client.scan_iter(pattern):
            self.client.delete(key)

    def get_stats(self) -> Dict[str, Any]:
        """Получает статистику кэша"""
        stats = self.client.info('memory')
        return {
            'used_memory': stats.get('used_memory', 0),
            'used_memory_human': stats.get('used_memory_human', '0B'),
            'memory_peak': stats.get('used_memory_peak', 0),
            'memory_peak_human': stats.get('used_memory_peak_human', '0B'),
            'keyspace_hits': stats.get('keyspace_hits', 0),
            'keyspace_misses': stats.get('keyspace_misses', 0),
            'total_keys': len(self.client.keys())
        }

# Создаем экземпляр сервиса
cache_service = CacheService()
