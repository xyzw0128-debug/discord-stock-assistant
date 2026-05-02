"""Application configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    database_url: str
    discord_bot_token: str
    app_env: str = "development"


def load_settings() -> Settings:
    """Load required settings from environment variables."""
    return Settings(
        database_url=os.getenv("DATABASE_URL", ""),
        discord_bot_token=os.getenv("DISCORD_BOT_TOKEN", ""),
        app_env=os.getenv("APP_ENV", "development"),
    )
