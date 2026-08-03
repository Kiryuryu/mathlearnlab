"""Tests for CORS config — no network."""

from server.config import Settings


def test_cors_origins_include_domain():
    s = Settings(cors_origins="https://mathlearnlab.cn,http://127.0.0.1:5173")
    origins = [o.strip() for o in s.cors_origins.split(",") if o.strip()]
    assert "https://mathlearnlab.cn" in origins


def test_cors_origins_default_not_wildcard():
    s = Settings()
    assert "*" not in s.cors_origins.split(",")
    assert "https://www.mathlearnlab.cn" in s.cors_origins


def test_cors_origins_empty_allowed():
    s = Settings(cors_origins="")
    assert [o for o in s.cors_origins.split(",") if o.strip()] == []
