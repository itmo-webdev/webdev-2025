import uuid, time
from typing import Optional
from app.core.cache import cache_get, cache_set, cache_del, k_session
from app.core.config import settings

def new_session_id() -> str:
    return uuid.uuid4().hex

async def create_session(user_id: int, role: str) -> str:
    sid = new_session_id()
    payload = {"sid": sid, "user_id": user_id, "role": role, "created_at": int(time.time())}
    await cache_set(k_session(sid), payload, settings.REFRESH_TTL_SECONDS)
    return sid

async def get_session(sid: str) -> Optional[dict]:
    return await cache_get(k_session(sid))

async def delete_session(sid: str) -> None:
    await cache_del(k_session(sid))