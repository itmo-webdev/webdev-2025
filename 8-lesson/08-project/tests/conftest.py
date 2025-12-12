import pytest
import asyncio
import os
import asyncpg
from time import time

from sqlalchemy import create_mock_engine
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def db_schema():
    return f"test_{hash(time())}"


@pytest.fixture(scope="session")
def _settings(db_schema):
    from app.settings import Settings

    s = Settings()
    os.environ["POSTGRES_DSN"] = s.POSTGRES_DSN + f"?search_path={db_schema}"

    return s


@pytest.fixture(scope="session")
async def raw_pool(db_schema, _settings):
    dsn = _settings.POSTGRES_DSN.replace("+asyncpg", "")
    pool = await asyncpg.create_pool(
        dsn,
        server_settings={"search_path": db_schema},
    )
    print("create schema", db_schema)
    await pool.execute(
        f"""
        create schema "{db_schema}";
    """
    )
    yield pool

    print("drop schema", db_schema)
    await pool.execute(
        f"""
        drop schema "{db_schema}" cascade;
    """
    )
    await pool.close()


@pytest.fixture(autouse=True, scope="session")
async def tables(_settings, raw_pool):
    from app.db import meta

    event_loop = asyncio.get_event_loop()

    tasks = []

    def run(sql, *multiparams, **params):
        tasks.append(
            event_loop.create_task(
                raw_pool.execute(str(sql.compile(dialect=engine.dialect)))
            )
        )

    engine = create_mock_engine(_settings.POSTGRES_DSN, run)

    print("create tables")
    meta.create_all(engine, checkfirst=False)
    await asyncio.wait(tasks)
    yield

    tasks = []
    print("drop tables")
    meta.drop_all(engine, checkfirst=False)
    await asyncio.wait(tasks)


@pytest.fixture(scope="session")
async def client():
    from app.server import get_app

    app = get_app(test=True)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        async with LifespanManager(app) as manager:
            yield client
