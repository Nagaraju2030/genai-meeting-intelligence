"""Configuration management for the application."""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    # Application Configuration
    app_title: str = "GenAI Meeting Intelligence"
    app_version: str = "1.0.0"
    app_description: str = (
        "Transform meeting transcripts into structured operational intelligence"
    )
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")

    class Config:
        """Pydantic config."""

        case_sensitive = False
        env_file = ".env"
        extra = "ignore"

    def __init__(self, **data):
        """Validate configuration on initialization."""
        super().__init__(**data)
        if not self.openai_api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable is required. "
                "Please set it or create a .env file with OPENAI_API_KEY=your_key"
            )


# Global settings instance
settings = Settings()
