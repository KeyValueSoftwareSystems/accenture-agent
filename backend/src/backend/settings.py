from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env", extra="ignore")

    model: str = "gpt-4.1-mini"
    openai_api_key: str
    openai_base_url: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings()