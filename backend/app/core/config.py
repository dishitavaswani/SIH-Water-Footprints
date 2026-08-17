"""Environment and CORS configuration."""

from __future__ import annotations

import os
from pathlib import Path
from functools import lru_cache
from typing import List

from dotenv import load_dotenv

# Load .env from the backend/ directory (two levels up from this file)
_env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(_env_path)


class Settings:
    """Centralised application settings populated from environment variables."""

    # ── Application ──────────────────────────────────────────────────────
    APP_NAME: str = os.getenv("APP_NAME", "SIH-Water-Footprint-API")
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")
    APP_SECRET_KEY: str = os.getenv("APP_SECRET_KEY", "change-me-in-production")

    # ── Server ───────────────────────────────────────────────────────────
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))

    # ── CORS ─────────────────────────────────────────────────────────────
    CORS_ORIGINS: List[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:3000,http://localhost:8080,http://127.0.0.1:8000,http://10.0.2.2:8000",
        ).split(",")
        if origin.strip()
    ]

    # ── Database ─────────────────────────────────────────────────────────
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./database/data/water_footprint.sqlite"
    )

    # ── ML Model ─────────────────────────────────────────────────────────
    ML_MODEL_PATH: str = os.getenv("ML_MODEL_PATH", "../ml_model/models")
    ML_CONFIDENCE_THRESHOLD: float = float(
        os.getenv("ML_CONFIDENCE_THRESHOLD", "0.6")
    )
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))

    # ── Translation ──────────────────────────────────────────────────────
    GOOGLE_TRANSLATE_API_KEY: str = os.getenv("GOOGLE_TRANSLATE_API_KEY", "")
    TRANSLATION_CACHE_TTL_SECONDS: int = int(
        os.getenv("TRANSLATION_CACHE_TTL_SECONDS", "3600")
    )
    DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "en")
    SUPPORTED_LANGUAGES: List[str] = [
        lang.strip()
        for lang in os.getenv("SUPPORTED_LANGUAGES", "en,hi").split(",")
        if lang.strip()
    ]
    TRANSLATION_OVERRIDES_PATH: str = os.getenv(
        "TRANSLATION_OVERRIDES_PATH", "../multilingual/data/overrides.json"
    )

    # ── Logging ──────────────────────────────────────────────────────────
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")

    # ── Rate Limiting ────────────────────────────────────────────────────
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))

    # ── Temporary Uploads ────────────────────────────────────────────────
    TEMP_UPLOAD_DIR: str = os.getenv("TEMP_UPLOAD_DIR", "./tmp/uploads")

    @property
    def is_production(self) -> bool:
        return self.APP_ENV.lower() == "production"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached Settings singleton."""
    return Settings()
