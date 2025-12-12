from typing import Any
from functools import lru_cache
from urllib.parse import urlparse, parse_qs

from sqlalchemy import MetaData, String
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from .dto import User


@lru_cache
def create_engine(dsn: str) -> AsyncEngine:
    """Создаёт асинхронный движок SQLAlchemy для PostgreSQL.
    
    Args:
        dsn: строка подключения вида postgresql+asyncpg://user:pass@host:port/db
             можно добавить ?search_path=schema для указания схемы
    
    Returns:
        AsyncEngine для работы с базой данных
    """
    connect_args = {}
    
    # Извлекаем search_path из query-параметров URL (если есть)
    parsed = urlparse(dsn)
    if parsed.query:
        params = parse_qs(parsed.query)
        if "search_path" in params:
            # asyncpg требует передачи search_path через server_settings
            connect_args["server_settings"] = {
                "search_path": params["search_path"][0]
            }
        # Убираем query-параметры из DSN, т.к. они уже обработаны
        dsn = dsn.split("?")[0]
    
    return create_async_engine(dsn, connect_args=connect_args)


@lru_cache
def make_sessionmaker(engine: AsyncEngine) -> sessionmaker:
    """Создаёт фабрику сессий для работы с БД.
    
    Args:
        engine: асинхронный движок SQLAlchemy
    
    Returns:
        sessionmaker для создания AsyncSession
    """
    return sessionmaker(
        engine,
        class_=AsyncSession,
    )


# Метаданные для всех таблиц
meta = MetaData()


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""

    metadata = meta

    # Маппинг Python-типов на типы PostgreSQL
    type_annotation_map = {
        dict[str, Any]: JSONB,
        list[str]: ARRAY(String()),
    }


class UserModel(Base):
    """Модель пользователя в базе данных."""
    
    __tablename__ = "site_user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str]
    username: Mapped[str]
    email: Mapped[str]

    def to_dto(self) -> User:
        """Преобразует модель в DTO."""
        return User(
            id=self.id,
            full_name=self.full_name,
            username=self.username,
            email=self.email,
        )
