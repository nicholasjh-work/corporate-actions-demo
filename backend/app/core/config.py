"""Core application configuration."""
import os
from functools import lru_cache
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Corporate Actions API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database
    db_host: str = "mysql"
    db_port: int = 3306
    db_user: str = "corpactions"
    db_password: str = "corpactions_pass"
    db_name: str = "corporate_actions"
    
    # API
    api_v1_prefix: str = "/api/v1"
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Security
    api_key: str = "demo_api_key_change_in_production"
    
    @property
    def database_url(self) -> str:
        """Construct database URL."""
        return (
            f"mysql+mysqlconnector://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
