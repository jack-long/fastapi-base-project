import os

from typing import List
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    secret_key: str
    smtp_username: str
    smtp_password: str
    smtp_host: str = "smtp.office365.com"
    smtp_port: int = 587  # tls port
    emails_enabled: bool = True
    admin_email: str
    database_url: str = "sqlite:///./chest.sqlite"
    db_user: str = ""
    db_password: str = ""
    db_host: str = "localhost"
    db_name: str = "chest"
    api_url: str = "localhost:8000/api/v1"
    cors_origins: List[str] | None = None
    api_mode: str | None = None

    model_config = SettingsConfigDict(env_file='.env')


class DevSettings(Settings):
    cors_origins: List[str] = ["http://localhost:3000"]
    api_mode: str = "dev"


class ProductionSettings(Settings):
    api_mode: str = "production"


@lru_cache()
def get_settings() -> Settings:
    if os.environ["API_MODE"] == "dev":
        return DevSettings()
    else:
        return ProductionSettings()
