import pytest
import asyncio

async def fetch_data():
    await asyncio.sleep(0.1)
    return {"status": "ok", "data": [1, 2, 3]}


async def add_async(a: int, b: int) -> int:
    await asyncio.sleep(0.05)
    return a + b

@pytest.mark.asyncio
async def test_fetch_data():
    result = await fetch_data()
    assert result["status"] == "ok"
    assert result["data"] == [1, 2, 3]


@pytest.mark.asyncio
async def test_add_async():
    result = await add_async(2, 3)
    assert result == 5


@pytest.mark.asyncio
async def test_multiple_awaits():
    result1 = await add_async(1, 2)
    result2 = await add_async(3, 4)
    assert result1 + result2 == 10


@pytest.fixture
async def async_client():
    await asyncio.sleep(0.01)
    client = {"connected": True}
    yield client
    await asyncio.sleep(0.01)
    print(f"finalizing {client}")
    client["connected"] = False


@pytest.mark.asyncio
async def test_with_async_fixture(async_client):
    assert async_client["connected"] is True
