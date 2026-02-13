"""Application configuration from environment variables."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # App
    app_name: str = "Log Root Cause Analyzer"
    debug: bool = False

    # API
    api_v1_prefix: str = "/api/v1"

    # Database (PostgreSQL)
    database_url: Optional[str] = None


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""
    return Settings()
