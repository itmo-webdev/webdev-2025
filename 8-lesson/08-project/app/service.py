from .dto import User

from .abc import ABCScrapDataRepository, ABCScrapClient, ABCScrapService


class ScrapService(ABCScrapService):
    repo: ABCScrapDataRepository
    client: ABCScrapClient

    def __init__(self, repo: ABCScrapDataRepository, client: ABCScrapClient):
        self.repo = repo
        self.client = client

    async def scrap_user(self) -> User:
        sc_user = await self.client.user()

        user = await self.repo.user_create(
            f"{sc_user.first_name} {sc_user.last_name}", sc_user.username, sc_user.email
        )

        return user
