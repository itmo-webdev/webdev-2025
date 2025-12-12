"""Настройки проекта."""

from functools import cached_property

from pydantic_settings import BaseSettings
from pydantic import AliasChoices, Field
from pydantic_settings import SettingsConfigDict


model_config = SettingsConfigDict(
    env_nested_delimiter="__",
    ignored_types=(cached_property, property),
    extra="allow",
    env_file=".env",
    case_sensitive=True,
)


class Settings(BaseSettings):
    """Все настройки."""

    model_config = model_config

    POSTGRES_DSN: str = Field(
        "postgresql+asyncpg://postgres:postgres@postgres:5432/postgres",
        description="DSN мастер БД",
        examples=["postgresql+asyncpg://postgres:postgres@postgres,db:5432/postgres"],
        validation_alias=AliasChoices("POSTGRES_DSN", "POSTGRES_RW_DSN"),
    )

    CLIENT_FAKE: bool = Field(False)
    CLIENT_URL: str = Field("https://random-data-api.com/api/v2")
