from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    NEWS_TTL_SECONDS: int = 300
    REFRESH_TTL_SECONDS: int = 604800
    USER_CACHE_TTL_SECONDS: int = 900

    class Config:
        env_file = ".env"

settings = Settings()
