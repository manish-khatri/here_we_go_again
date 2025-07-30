import redis
import json
from flask import current_app
from functools import wraps
import hashlib

# Redis connection
redis_client = None

def init_cache(app):
    """Initialize Redis cache"""
    global redis_client
    redis_url = app.config.get('REDIS_URL', 'redis://localhost:6379/1')
    redis_client = redis.from_url(redis_url, decode_responses=True)
    return redis_client

def get_cache_key(*args, **kwargs):
    """Generate cache key from arguments"""
    key_data = f"{args}{kwargs}"
    return hashlib.md5(key_data.encode()).hexdigest()

def cache(timeout=300, key_prefix=""):
    """Cache decorator for functions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not redis_client:
                # If Redis is not available, execute function normally
                return func(*args, **kwargs)
            
            try:
                # Generate cache key
                cache_key = f"{key_prefix}:{func.__name__}:{get_cache_key(*args, **kwargs)}"
                
                # Try to get from cache
                cached_result = redis_client.get(cache_key)
                if cached_result:
                    return json.loads(cached_result)
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                redis_client.setex(cache_key, timeout, json.dumps(result, default=str))
                return result
                
            except Exception as e:
                current_app.logger.warning(f"Cache error: {e}")
                # If cache fails, execute function normally
                return func(*args, **kwargs)
        
        return wrapper
    return decorator

def invalidate_cache(pattern):
    """Invalidate cache keys matching pattern"""
    if not redis_client:
        return
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
    except Exception as e:
        current_app.logger.warning(f"Cache invalidation error: {e}")

def set_cache(key, value, timeout=300):
    """Set cache value"""
    if not redis_client:
        return
    try:
        redis_client.setex(key, timeout, json.dumps(value, default=str))
    except Exception as e:
        current_app.logger.warning(f"Cache set error: {e}")

def get_cache(key):
    """Get cache value"""
    if not redis_client:
        return None
    try:
        cached_value = redis_client.get(key)
        return json.loads(cached_value) if cached_value else None
    except Exception as e:
        current_app.logger.warning(f"Cache get error: {e}")
        return None
