from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncResult, AsyncSession

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from .db import make_sessionmaker, UserModel, create_engine

from .abc import ABCScrapDataRepository
from .dto import User


class ScrapDataRepository(ABCScrapDataRepository):
    def __init__(self, dsn: str):
        self.engine = create_engine(dsn)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """

        Examples:

            async with db.sesstion() as s:
                await s.execute(text('select 1'))
        """
        maker = make_sessionmaker(self.engine)
        async with maker.begin() as session:  # type: ignore
            try:
                yield session
            except Exception:
                await session.rollback()
                raise

    async def users(self, limit: int, offset: int) -> list[User]:
        dsl = select(UserModel).limit(limit).offset(offset)

        async with self.session() as s:
            result: AsyncResult = await s.execute(dsl)
            return [u.to_dto() for u in result.scalars()]

    async def user(self, id: int) -> User | None:
        dsl = select(UserModel).where(UserModel.id == id)

        async with self.session() as s:
            result: AsyncResult = await s.execute(dsl)
            u = result.scalar_one_or_none()
            if not u:
                return None
            return u.to_dto()

    async def user_create(
        self,
        full_name: str,
        username: str,
        email: str,
    ) -> User:
        dsl = (
            insert(UserModel)
            .values(full_name=full_name, username=username, email=email)
            .returning(UserModel)
        )

        async with self.session() as s:
            result: AsyncResult = await s.execute(dsl)
            u = result.scalar()
            return u.to_dto()

    async def user_delete(self, id: int) -> User | None:
        dsl = delete(UserModel).where(UserModel.id == id).returning(UserModel)

        async with self.session() as s:
            result: AsyncResult = await s.execute(dsl)
            u = result.scalar_one_or_none()
            if not u:
                return None
            return u.to_dto()

    async def user_change(
        self,
        id: int,
        full_name: str,
        username: str,
        email: str,
    ) -> User:
        dsl = (
            update(UserModel)
            .where(UserModel.id == id)
            .values(full_name=full_name, username=username, email=email)
            .returning(UserModel)
        )

        async with self.session() as s:
            await s.execute(dsl)
            result: AsyncResult = await s.execute(dsl)
            u = result.scalar()
            return u.to_dto()


class ScrapDataDictRepository(ABCScrapDataRepository):
    def __init__(self):
        self.db = {}
        self.last_id = 0

    async def users(self, limit: int, offset: int) -> list[User]:
        resp = []
        for i, key in enumerate(self.db.keys()):
            if i < offset:
                continue

            if len(resp) >= limit:
                break
            resp.append(self.db[key])
        return resp

    async def user(self, id: int) -> User | None:
        return self.db.get(id)

    async def user_create(
        self,
        full_name: str,
        username: str,
        email: str,
    ) -> User:
        u = User(id=self.last_id, full_name=full_name, username=username, email=email)
        self.db[self.last_id] = u
        self.last_id += 1
        return u

    async def user_delete(self, id: int) -> User | None:
        resp = self.db.get(self.last_id)
        if resp:
            del self.db[self.last_id]
        return resp

    async def user_change(
        self,
        id: int,
        full_name: str,
        username: str,
        email: str,
    ) -> User:
        if id is not self.db:
            raise ValueError
        u = User(id=id, full_name=full_name, username=username, email=email)
        self.db[id] = u
        return u
