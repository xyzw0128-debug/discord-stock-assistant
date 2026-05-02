"""App-level entrypoint helpers."""

from .config import load_settings


def startup_message() -> str:
    """Return a small startup message for smoke checks."""
    settings = load_settings()
    env = settings.app_env or "development"
    return f"discord stock assistant ready ({env})"
