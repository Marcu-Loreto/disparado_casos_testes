"""
Application settings for the Disparado_Casos_testes workflow.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Google Sheets Configuration
    GOOGLE_SHEETS_DOCUMENT_ID: str = Field(
        default="1xpK1xFnkETsLBk5jCOnEzV9xrplSPigmlaATUZweTCM",
        env="GOOGLE_SHEETS_DOCUMENT_ID",
    )

    GOOGLE_SHEETS_TESTES_2026_SHEET_ID: str = Field(
        default="882495635", env="GOOGLE_SHEETS_TESTES_2026_SHEET_ID"
    )

    # Evolution API Configuration
    EVOLUTION_API_URL: str = Field(
        default="https://evolution.etechats.com.br", env="EVOLUTION_API_URL"
    )
    EVOLUTION_API_KEY: str = Field(
        default="43248376731B-4E40-9799-0C45BDF43A55", env="EVOLUTION_API_KEY"
    )
    EVOLUTION_INSTANCE: str = Field(
        default="TESTE_AUTO_MGI", env="EVOLUTION_INSTANCE"
    )

    # Application Configuration
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")

    # Webhook Configuration
    WEBHOOK_HOST: str = Field(default="0.0.0.0", env="WEBHOOK_HOST")
    WEBHOOK_PORT: int = Field(default=8000, env="WEBHOOK_PORT")
    WEBHOOK_PATH: str = Field(default="/webhook/:test_cases_auto", env="WEBHOOK_PATH")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()
