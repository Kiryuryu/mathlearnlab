"""Tests for the second-round security & UX fixes.

Covers: server-AI config endpoint, API-key resolution, AI quota, SPA fallback,
registration honeypot, password reset flow, token refresh, and search routing.
No network calls (AI/deepseek/email paths are avoided or mocked).
"""

import asyncio
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient


# ── helpers: isolated SQLite DB per test ──

def _isolate_db(tmp_path, monkeypatch):
    import server.models.database as database
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    database._mysql_local.sqlite = None  # fresh thread-local connection
    database.init_db()
    return database


# ── /api/config/ai ──

def test_ai_config_endpoint():
    from server.main import app
    with TestClient(app) as client:
        r = client.get("/api/config/ai")
        assert r.status_code == 200
        d = r.json()
        assert "server_ai" in d and "ai_daily_limit" in d and "debug" in d


# ── resolve_api_key (production trusts only the server key) ──

def test_resolve_api_key_production_ignores_client(monkeypatch):
    from server.config import settings
    from server.services.deepseek import resolve_api_key
    monkeypatch.setattr(settings, "debug", False)
    monkeypatch.setattr(settings, "deepseek_api_key", "server-key")
    assert resolve_api_key("client-key") == "server-key"
    assert resolve_api_key(None) == "server-key"


def test_resolve_api_key_debug_prefers_client(monkeypatch):
    from server.config import settings
    from server.services.deepseek import resolve_api_key
    monkeypatch.setattr(settings, "debug", True)
    monkeypatch.setattr(settings, "deepseek_api_key", "server-key")
    assert resolve_api_key("client-key") == "client-key"
    assert resolve_api_key(None) == "server-key"


# ── per-user daily AI quota (persisted in SQLite) ──

def test_ai_quota_limits_and_counts(tmp_path, monkeypatch):
    _isolate_db(tmp_path, monkeypatch)
    from server.config import settings
    from server.services.ratelimit import use_ai_quota, ai_quota_left, today_cst
    monkeypatch.setattr(settings, "ai_daily_limit", 3)
    assert ai_quota_left("u1") == 3
    assert use_ai_quota("u1") is True
    assert use_ai_quota("u1") is True
    assert ai_quota_left("u1") == 1
    assert use_ai_quota("u1") is True
    assert use_ai_quota("u1") is False  # exhausted
    assert ai_quota_left("u1") == 0
    # Different user unaffected; same day counted.
    assert use_ai_quota("u2") is True
    assert ai_quota_left("u1") == 0


# ── SPA fallback + unknown API returns JSON 404 ──

def test_spa_fallback_and_api_404():
    from server.main import app
    with TestClient(app) as client:
        r = client.get("/exhibit/limits")
        assert r.status_code == 200
        assert "text/html" in r.headers["content-type"]
        assert client.get("/").status_code == 200
        r404 = client.get("/api/does-not-exist")
        assert r404.status_code == 404
        assert "json" in r404.headers["content-type"]


# ── registration honeypot: filled website field → no account created ──

def test_register_honeypot_creates_nothing(tmp_path, monkeypatch):
    _isolate_db(tmp_path, monkeypatch)
    from server.main import app
    from server.models.users import username_exists
    with TestClient(app) as client:
        r = client.post("/api/auth/register", json={
            "username": "botuser", "password": "password123",
            "email": "bot@example.com", "website": "http://spam.example",
        })
        assert r.status_code == 200  # pretend success
    assert not username_exists("botuser")


def test_register_rejects_invalid_email(tmp_path, monkeypatch):
    _isolate_db(tmp_path, monkeypatch)
    from server.main import app
    with TestClient(app) as client:
        r = client.post("/api/auth/register", json={
            "username": "validuser", "password": "password123", "email": "not-an-email",
        })
        assert r.status_code == 400


# ── password reset: token create → consume → password changed, one-time ──

def test_reset_password_flow(tmp_path, monkeypatch):
    _isolate_db(tmp_path, monkeypatch)
    from server.models.users import create_user, get_user_by_username
    from server.models.auth import hash_password, verify_password
    from server.models.reset_tokens import create_reset_token, consume_reset_token
    create_user("u1", "alice", "alice@example.com", hash_password("oldpass1"))

    token = create_reset_token("u1")
    assert consume_reset_token(token) == "u1"
    # One-time: second consume returns None.
    assert consume_reset_token(token) is None
    # Unknown token → None.
    assert consume_reset_token("nope") is None


def test_reset_password_router_endpoint(tmp_path, monkeypatch):
    _isolate_db(tmp_path, monkeypatch)
    from types import SimpleNamespace
    from server.models.users import create_user, get_user_by_username
    from server.models.auth import hash_password, verify_password
    from server.models.reset_tokens import create_reset_token
    from server.routers.auth import reset_password
    create_user("u1", "bob", "bob@example.com", hash_password("oldpass1"))
    token = create_reset_token("u1")

    resp = asyncio.run(reset_password(SimpleNamespace(token=token, password="newpass1")))
    assert "message" in resp
    u = get_user_by_username("bob")
    assert verify_password("newpass1", u["password_hash"])

    # Same token cannot be reused.
    with pytest.raises(HTTPException):
        asyncio.run(reset_password(SimpleNamespace(token=token, password="another1")))


def test_forgot_password_generic_response(tmp_path, monkeypatch):
    _isolate_db(tmp_path, monkeypatch)
    from server.main import app
    with TestClient(app) as client:
        # Unknown email: same generic message (no enumeration), no crash.
        r = client.post("/api/auth/forgot-password", json={"email": "ghost@example.com"})
        assert r.status_code == 200
        assert "已发送" in r.json()["message"] or "sent" in r.json()["message"].lower()


# ── token refresh: valid token → new token ──

def test_refresh_issues_new_token(tmp_path, monkeypatch):
    _isolate_db(tmp_path, monkeypatch)
    from server.main import app
    from server.models.users import create_user
    from server.models.auth import hash_password, create_access_token
    create_user("u1", "carol", "carol@example.com", hash_password("pass123"))
    with TestClient(app) as client:
        r = client.post("/api/auth/refresh", headers={"Authorization": f"Bearer {create_access_token('u1', 'carol')}"})
        assert r.status_code == 200
        assert r.json()["token"]
        # No token → 401.
        assert client.post("/api/auth/refresh").status_code == 401


# ── search only returns routable content ──

def test_search_excludes_unroutable_dirs():
    from server.services.search import search_all
    results = search_all("极限")
    assert results
    for r in results:
        assert not r["route"].startswith(("/notes/", "/problems/", "/error-log/", "/notebooks/"))
    assert any(r["route"].startswith("/exhibit/") for r in results)
