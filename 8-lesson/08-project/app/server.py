"""Определение app."""

from fastapi import FastAPI

from contextlib import asynccontextmanager

from .abc import ABCScrapClient, ABCScrapDataRepository, ABCScrapService
from .client import ScrapClient, FakeScrapClient
from .repo import ScrapDataRepository, ScrapDataDictRepository
from .service import ScrapService
from .api import router
from .deps import add_dep
from .settings import Settings


@asynccontextmanager
async def lifespan(app):
    settings = Settings()
    repo = ScrapDataRepository(settings.POSTGRES_DSN)
    if not app.test and not settings.CLIENT_FAKE:
        client = ScrapClient(settings.CLIENT_URL)
        repo = ScrapDataRepository(settings.POSTGRES_DSN)
    else:
        client = FakeScrapClient()
        # repo = ScrapDataDictRepository()


    add_dep(ABCScrapClient, client)
    add_dep(ABCScrapDataRepository, repo)
    add_dep(ABCScrapService, ScrapService(repo=repo, client=client))
    yield


def get_app(test: bool = False):
    app = FastAPI(lifespan=lifespan)
    app.test = test

    app.include_router(router)

    return app
