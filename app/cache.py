# app/cache.py
import json, time, threading
from typing import Any, Optional
from app.config import settings

_redis = None
if settings.REDIS_URL:
    try:
        import redis
        _redis = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
        # ping inicial (opcional)
        _redis.ping()
    except Exception:
        _redis = None  # fallback si Redis no responde

# Fallback simple en memoria si no hay Redis
_mem = {}
_lock = threading.Lock()

def cache_get(key: str) -> Optional[str]:
    if _redis:
        return _redis.get(key)
    with _lock:
        v = _mem.get(key)
        if not v: return None
        payload, exp = v
        if exp and exp < time.time():
            _mem.pop(key, None)
            return None
        return payload

def cache_setex(key: str, ttl_sec: int, value: str) -> None:
    if _redis:
        _redis.setex(key, ttl_sec, value)
        return
    with _lock:
        exp = time.time() + ttl_sec if ttl_sec else None
        _mem[key] = (value, exp)

def cache_del(key: str) -> None:
    if _redis:
        _redis.delete(key)
        return
    with _lock:
        _mem.pop(key, None)
