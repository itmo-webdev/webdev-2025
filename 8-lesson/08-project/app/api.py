from fastapi import APIRouter, Depends
from pydantic import BaseModel
from pydantic import EmailStr

from .deps import Dependency
from .abc import ABCScrapService, ABCScrapDataRepository
from .dto import User

router = APIRouter()


@router.get("/public/scrap_users")
async def scrap_users(
    limit: int = 1,
    service: ABCScrapService = Depends(Dependency(ABCScrapService)),
) -> list[User]:
    resp = []
    for _ in range(limit):
        u = await service.scrap_user()
        resp.append(u)

    return resp


@router.get("/admin/users")
async def users(
    limit: int = 10,
    offset: int = 0,
    repo: ABCScrapDataRepository = Depends(Dependency(ABCScrapDataRepository)),
) -> list[User]:
    return await repo.users(limit, offset)


@router.get("/admin/user/{id}")
async def user(
    id: int, repo: ABCScrapDataRepository = Depends(Dependency(ABCScrapDataRepository))
) -> User | None:
    return await repo.user(id)


class ChangeUser(BaseModel):
    full_name: str
    username: str
    email: EmailStr


@router.put("/admin/user/{id}")
async def change_user(
    id: int,
    changes: ChangeUser,
    repo: ABCScrapDataRepository = Depends(Dependency(ABCScrapDataRepository)),
) -> User | None:
    return await repo.user_change(
        id, changes.full_name, changes.username, changes.email
    )


@router.delete("/admin/user/{id}")
async def delete_user(
    id: int,
    repo: ABCScrapDataRepository = Depends(Dependency(ABCScrapDataRepository)),
) -> User | None:
    return await repo.user_delete(id)
