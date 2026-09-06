from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "agent-redteam-backend"
    app_version: str = "0.1.0"
    app_env: str = "local"
    database_url: str = Field(default="postgresql+psycopg://redteam:redteam@localhost:5432/redteam")
    redis_url: str = "redis://localhost:6379/0"


@lru_cache
def get_settings() -> Settings:
    return Settings()
