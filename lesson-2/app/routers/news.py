from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.cache import cache_get, cache_set, k_news, k_news_list
from app.core.config import settings
from app.database import get_db

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/{news_id}")
async def get_news(news_id: int, db: AsyncSession = Depends(get_db)):
    key = k_news(news_id)
    cached = await cache_get(key)
    if cached is not None:
        return cached

    row = (await db.execute(
        text("SELECT id, title, body, created_at FROM news WHERE id = :i"),
        {"i": news_id}
    )).mappings().first()

    if not row:
        raise HTTPException(status_code=404, detail="Not found")

    dto = dict(row)
    if dto.get("created_at"):
        dto["created_at"] = dto["created_at"].isoformat()
    await cache_set(key, dto, settings.NEWS_TTL_SECONDS)
    return dto

@router.get("")
async def list_news(page: int = 1, limit: int = 10, db: AsyncSession = Depends(get_db)):
    key = k_news_list(page, limit)
    cached = await cache_get(key)
    if cached is not None:
        return cached

    rows = (await db.execute(
        text("""
            SELECT id, title, body, created_at
            FROM news
            ORDER BY id DESC
            LIMIT :limit OFFSET :offset
        """),
        {"limit": limit, "offset": (page - 1) * limit}
    )).mappings().all()

    data = [dict(r) for r in rows]
    for d in data:
        if d.get("created_at"):
            d["created_at"] = d["created_at"].isoformat()
    await cache_set(key, data, settings.NEWS_TTL_SECONDS)
    return data
