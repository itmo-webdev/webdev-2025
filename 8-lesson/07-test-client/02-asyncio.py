from httpx import AsyncClient, ASGITransport
import pytest
from contextlib import asynccontextmanager
import asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from asgi_lifespan import LifespanManager

@asynccontextmanager
async def lifespan(app):
    try:
        print("starting")
        yield
    finally:
        print("stopping")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app),
        base_url="http://testserver"
    ) as client:
        async with LifespanManager(app):
            yield client

async def test_read_root(client):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}