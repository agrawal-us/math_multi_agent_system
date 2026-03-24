from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Math Multi-Agent API"
    APP_VERSION: str = "0.1.0"
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = Field(
        default="postgresql+psycopg://postgres:postgres@localhost:5432/math_multi_agent"
    )

    JWT_SECRET_KEY: str = Field(default="change-me", min_length=8)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
