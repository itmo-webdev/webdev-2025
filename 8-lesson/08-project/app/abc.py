import abc


from .dto import User, ScrappedUser


class ABCScrapClient(abc.ABC):
    @abc.abstractmethod
    async def user(self) -> ScrappedUser: ...


class ABCScrapDataRepository(abc.ABC):
    @abc.abstractmethod
    async def users(self, limit: int, offset: int) -> list[User]: ...
    @abc.abstractmethod
    async def user(self, id: int) -> User | None: ...
    @abc.abstractmethod
    async def user_create(
        self,
        full_name: str,
        username: str,
        email: str,
    ) -> User: ...
    @abc.abstractmethod
    async def user_delete(self, id: int) -> User | None: ...

    @abc.abstractmethod
    async def user_change(
        self,
        id: int,
        full_name: str,
        username: str,
        email: str,
    ) -> User: ...


class ABCScrapService(abc.ABC):
    @abc.abstractmethod
    async def scrap_user(self) -> User: ...
