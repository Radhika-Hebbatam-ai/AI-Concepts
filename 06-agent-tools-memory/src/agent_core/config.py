from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """App settings loaded from environment variables or .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    groq_api_key: SecretStr
    groq_model: str = "openai/gpt-oss-20b"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
