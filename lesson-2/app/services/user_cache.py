
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.cache import cache_get, cache_set, k_user
from app.core.config import settings

async def get_user_public(uid: int, db: AsyncSession) -> Optional[dict]:
    key = k_user(uid)
    cached = await cache_get(key)
    if cached is not None:
        return cached

    row = (await db.execute(
        text("SELECT id, username, role, is_active FROM users WHERE id=:i"),
        {"i": uid}
    )).mappings().first()
    if not row:
        return None
    data = dict(row)
    await cache_set(key, data, settings.USER_CACHE_TTL_SECONDS)
    return data
