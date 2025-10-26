import logging
from fastapi import FastAPI, Request
from app.core.config import settings
from app.core.redis_client import redis
from app.routers import news, auth

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("cache.log", encoding="utf-8")]
)

def create_app() -> FastAPI:
    app = FastAPI(title="LMS 2.0 - lesson 2")

    @app.middleware("http")
    async def log_cache_usage(request: Request, call_next):
        resp = await call_next(request)
        logging.getLogger("access").info(
            "path=%s method=%s status=%s",
            request.url.path, request.method, resp.status_code
        )
        return resp

    app.include_router(news.router, prefix="/api")
    app.include_router(auth.router, prefix="/api")

    @app.get("/healthz")
    async def healthz():
        ok = await redis.ping()
        return {"ok": True, "redis": ok}

    @app.on_event("startup")
    async def _startup():
        try:
            await redis.ping()
            logging.getLogger("startup").info("Connected to Redis: %s", settings.REDIS_URL)
        except Exception as e:
            logging.getLogger("startup").warning("Redis unreachable: %s", e)

    return app

app = create_app()