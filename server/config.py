"""
MathLearnLab server configuration via pydantic-settings.
Reads from environment variables or .env file.
"""

import os
from typing import ClassVar
from pydantic_settings import BaseSettings
from server.content_data import subjects, exhibits, quotes, difficulty, mathematicians, nav_tree


class Settings(BaseSettings):
    # ── Server ──
    app_name: str = "数学博物馆"
    app_subtitle: str = "知其然，知其所以然"
    debug: bool = False
    host: str = "127.0.0.1"
    port: int = 8000

    # ── Paths ──
    content_dir: str = "content"
    data_dir: str = "data"

    # ── AI / DeepSeek API ──
    deepseek_api_key: str = ""
    deepseek_model: str = "deepseek-chat"
    max_grading_tokens: int = 2000
    max_chat_tokens: int = 4096

    # ── Auth / JWT ──
    jwt_secret_key: str = ""
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24  # 24 hours

    # ── Email / SMTP ──
    smtp_host: str = ""
    smtp_user: str = ""
    smtp_pass: str = ""
    admin_email: str = ""

    # ── Database ──
    database_url: str = ""

    # ── CORS allowed origins (comma-separated) ──
    cors_origins: str = "https://mathlearnlab.cn,https://www.mathlearnlab.cn,http://127.0.0.1:5173,http://127.0.0.1:8000"

    # ── Static content data (from server.content_data) ──
    subjects: ClassVar[dict] = subjects
    exhibits: ClassVar[dict] = exhibits
    quotes: ClassVar[list] = quotes
    difficulty: ClassVar[dict] = difficulty
    mathematicians: ClassVar[dict] = mathematicians
    nav_tree: ClassVar[list] = nav_tree

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}
    """pydantic model config"""


def get_settings_dict() -> dict:
    """Return settings as plain dict for Jinja2 template context.
    Must convert nested dicts and non-serializable values to plain types."""
    s = settings
    return {
        "app_name": s.app_name,
        "app_subtitle": s.app_subtitle,
        "debug": s.debug,
        "content_dir": s.content_dir,
        "data_dir": s.data_dir,
        "deepseek_model": s.deepseek_model,
        "subjects": settings.subjects,
        "exhibits": settings.exhibits,
        "difficulty": s.difficulty,
        "nav_tree": s.nav_tree,
    }


def validate_settings():
    """Validate required settings. Raises RuntimeError if invalid.
    Skips in test/CI environments where real keys aren't needed."""
    is_testing = os.getenv("PYTEST_CURRENT_TEST") or os.getenv("CI") == "true"
    if is_testing:
        return
    if not Settings().debug:
        jwt_key = os.getenv("JWT_SECRET_KEY", "")
        if not jwt_key:
            raise RuntimeError(
                "JWT_SECRET_KEY environment variable is required in non-debug mode. "
                "Generate one with: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
            )
    if not os.getenv("DEEPSEEK_API_KEY", ""):
        raise RuntimeError(
            "DEEPSEEK_API_KEY environment variable is required. "
            "Set it to your DeepSeek API key (OpenAI-compatible endpoint)."
        )


# Singleton instance — validated lazily on first access
_settings_instance = None


def get_settings() -> Settings:
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
        if not _settings_instance.debug:
            validate_settings()
    return _settings_instance


settings = get_settings()


# ── Path constants (computed from settings; avoids circular imports from server.main) ──
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / settings.content_dir
DATA_DIR = BASE_DIR / settings.data_dir
STATIC_DIR = Path(__file__).resolve().parent / "static"
