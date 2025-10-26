import json
import logging
from typing import Any, Optional
from .redis_client import redis

log = logging.getLogger("cache")

def k_news(id_: int) -> str: return f"news:{id_}"
def k_news_list(page: int, limit: int) -> str: return f"news:list:{page}:{limit}"
def k_session(sid: str) -> str: return f"session:{sid}"
def k_user(uid: int) -> str: return f"user:{uid}"

async def cache_get(key: str) -> Optional[Any]:
    data = await redis.get(key)
    if data is not None:
        log.info("cache_hit key=%s", key)   # BẮT BUỘC log hit/miss theo yêu cầu kiểm tra
    else:
        log.info("cache_miss key=%s", key)
    return json.loads(data) if data else None

async def cache_set(key: str, value: Any, ttl: int) -> None:
    await redis.setex(key, ttl, json.dumps(value, ensure_ascii=False))
    log.info("cache_set key=%s ttl=%s", key, ttl)

async def cache_del(key: str) -> None:
    await redis.delete(key)
    log.info("cache_del key=%s", key)
