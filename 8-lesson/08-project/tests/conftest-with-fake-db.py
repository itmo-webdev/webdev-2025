# import pytest
# import asyncio
# import os
# import asyncpg
# from time import time

# from sqlalchemy import create_mock_engine
# from httpx import AsyncClient, ASGITransport
# from asgi_lifespan import LifespanManager


# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()


# @pytest.fixture(scope="session")
# async def client():
#     from app.server import get_app

#     app = get_app(test=True)

#     async with AsyncClient(
#         transport=ASGITransport(app=app),
#         base_url="http://test",
#     ) as client:
#         async with LifespanManager(app) as manager:
#             yield client


# @pytest.mark.parametrize("limit", [i for i in range(30)])
# async def test_scrap(client, limit):
#     resp = await client.get("/public/scrap_users", params={"limit": limit})

#     assert resp.status_code == 200

#     assert len(resp.json()) == limit

#     for user in resp.json():
#         user_id = user["id"]
#         resp = await client.get(f"/admin/user/{user_id}")

#         assert resp.status_code == 200


