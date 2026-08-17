"""Tests for the AI tour-guide chat mode — prompt construction and routing."""

import pytest
from server.services import chat_service


def test_exhibit_context_limits():
    info = chat_service.exhibit_context("limits")
    assert info is not None
    assert "极限" in info["name_zh"]
    assert info["big_question"] and info["historian"]
    assert "柯西" in info["historian"]
    assert "derivatives" in info["related"] or any("导数" in r for r in info["related"])


def test_exhibit_context_unknown_returns_none():
    assert chat_service.exhibit_context("nonexistent") is None


def test_build_system_prompt_default_matches_legacy():
    # Without guide, behavior is identical to the old prompt (context_info is the
    # same Chinese/English literal the original inline code produced).
    zh = chat_service.build_system_prompt("zh", context_route="展区")
    assert "AI 导览员" in zh
    assert "当前访客在浏览: 展区" in zh
    en = chat_service.build_system_prompt("en", context_route="Exhibits")
    assert "tour guide" in en
    assert "当前访客在浏览: Exhibits" in en


def test_build_system_prompt_guide_mode():
    info = chat_service.exhibit_context("limits")
    guide = {"mode": True, "key": "limits", "name": "极限 — 无限逼近的艺术"}
    zh = chat_service.build_system_prompt("zh", guide=guide, exhibit_info=info)
    assert "专职讲解员" in zh
    assert "极限" in zh
    assert "柯西" in zh  # historian injected
    assert "馆内相关展品" in zh
    en = chat_service.build_system_prompt("en", guide=guide, exhibit_info=info)
    assert "dedicated tour guide" in en
    assert "Limits" in en


def test_stream_chat_route_passes_guide(monkeypatch):
    from fastapi.testclient import TestClient
    from server.main import app
    from server.routers import chat as chat_router

    captured = {}

    async def fake_stream_chat(**kwargs):
        captured.update(kwargs)
        yield "data: hi\n\n"
        yield "data: [DONE]\n\n"

    monkeypatch.setattr(chat_router.chat_service, "stream_chat", fake_stream_chat)

    # `with` triggers the app lifespan so the SQLite tables (incl. ai_usage)
    # exist before the quota check runs.
    with TestClient(app) as client:
        # Build a valid auth token.
        from server.models.auth import create_access_token
        token = create_access_token("1", "testuser")
        # Debug mode accepts a client-supplied API key.
        headers = {"Authorization": f"Bearer {token}", "X-API-Key": "test-key"}
        r = client.post("/api/chat/stream", json={
            "messages": [{"role": "user", "content": "讲一讲 ε-δ"}],
            "guide_mode": True,
            "exhibit_key": "limits",
            "exhibit_name": "极限 — 无限逼近的艺术",
            "lang": "zh",
        }, headers=headers)
        assert r.status_code == 200
        assert captured.get("guide", {}).get("key") == "limits"
        assert captured.get("guide", {}).get("mode") is True
