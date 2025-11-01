from redis.asyncio import from_url
from .config import settings

redis = from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
