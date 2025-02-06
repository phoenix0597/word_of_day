import os

from pydantic_settings import BaseSettings, SettingsConfigDict

# from functools import lru_cache
from os.path import dirname, abspath


class Settings(BaseSettings):
    BASE_DIR: str = abspath(dirname(dirname(dirname(__file__))))

    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Word of Day Article API"

    # OpenAI settings
    PROXY_API_KEY: str = ""
    PROXY_API_BASE_URL: str = ""

    # External services
    RSS_FEED_URL: str = "https://wordsmith.org/awad/rss1.xml"
    OPENAI_API_KEY: str = ""

    # Redis settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None
    REDIS_MAX_KEYS: int = 5
    REDIS_TTL: int = 86400

    model_config = SettingsConfigDict(env_file=[".env", ".env.test"], extra="allow")


# @lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
