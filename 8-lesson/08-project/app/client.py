import httpx

from pydantic import TypeAdapter

from polyfactory.factories.pydantic_factory import ModelFactory

from .abc import ABCScrapClient
from .dto import ScrappedUser


class ScrapClient(ABCScrapClient):
    _adapter = TypeAdapter(ScrappedUser)

    def __init__(self, base_url: str):
        self._url = f"{base_url}/users"

    async def user(self) -> ScrappedUser:
        async with httpx.AsyncClient() as client:
            resp = await client.get(self._url)

            if resp.status_code != 200:
                raise ValueError({"status_code": resp.status_code, "text": resp.text})

            return self._adapter.validate_json(resp.text)


# class FakeScrapClient(ABCScrapClient):
#     async def user(self) -> ScrappedUser:
#         return ScrappedUser(
#             first_name="John",
#             last_name="Doe",
#             username="john.doe",
#             email="john.doe@example.com",
#         )


class FakeScrapClient(ABCScrapClient):
    class FakeScrappedUser(ModelFactory[ScrappedUser]):
        @classmethod
        def email(cls) -> str:
            return cls.__faker__.email()

    async def user(self) -> ScrappedUser:
        return self.FakeScrappedUser.build()

