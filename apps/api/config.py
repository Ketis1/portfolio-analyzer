"""
Application settings loaded from environment variables / .env file.
Uses pydantic-settings for typed, validated configuration.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed settings mirroring every variable in docker/.env.example."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # ── Database ─────────────────────────────────────────────────────────
    database_url: str = "postgresql+asyncpg://dev:dev@localhost:5432/portfolio"

    # ── Redis / Celery ───────────────────────────────────────────────────
    redis_url: str = "redis://localhost:6379/0"

    # ── Qdrant ───────────────────────────────────────────────────────────
    qdrant_url: str = "http://localhost:6333"

    # ── GitHub OAuth ─────────────────────────────────────────────────────
    github_client_id: str = ""
    github_client_secret: str = ""

    # ── Auth / JWT ───────────────────────────────────────────────────────
    jwt_secret_key: str = "change-me-in-production"
    token_encryption_key: str = "change-me-in-production"

    # ── LLM Provider ─────────────────────────────────────────────────────
    llm_provider: Literal["anthropic", "ollama"] = "anthropic"
    anthropic_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (parsed once per process)."""
    return Settings()
