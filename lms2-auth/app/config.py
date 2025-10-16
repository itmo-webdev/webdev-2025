from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(...)
    JWT_SECRET: str = Field(...)
    JWT_ALG: str = "HS256"
    ACCESS_EXPIRES_MIN: int = 15
    REFRESH_EXPIRES_DAYS: int = 14
    GITHUB_CLIENT_ID: str = Field(...)
    GITHUB_CLIENT_SECRET: str = Field(...)
    GITHUB_REDIRECT_URL: str = Field(...)

    class Config:
        env_file = ".env"

settings = Settings()
