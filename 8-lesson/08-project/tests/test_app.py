import pytest

from app.dto import User

from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory.pytest_plugin import register_fixture


@register_fixture
class UserFactory(ModelFactory[User]):
    @classmethod
    def email(cls) -> str:
        return cls.__faker__.email()


@pytest.mark.parametrize("limit", [i for i in range(30)])
async def test_scrap(client, limit, raw_pool):
    resp = await client.get("/public/scrap_users", params={"limit": limit})

    assert resp.status_code == 200

    assert len(resp.json()) == limit

    for user in resp.json():
        user_id = user["id"]
        db_users = await raw_pool.fetch(
            "select id from site_user where id = $1", user_id
        )

        assert len(db_users) == 1

    return resp.json()


async def test_change_user_invalid(client, raw_pool, user_factory):
    users = await test_scrap(client, 1, raw_pool)

    user = users[0]
    user_id = user["id"]

    new_user_data = user_factory.build().model_dump()
    new_user_data["id"] = user_id

    resp = await client.put(f"/admin/user/{user_id}", json=new_user_data)

    assert resp.status_code == 422

    assert resp.json() == new_user_data

    assert new_user_data != user

