"""Tests for the daily problem router — no network, no real AI call."""

import json
from pathlib import Path
from unittest.mock import patch
from server.routers import daily


def test_daily_path(tmp_path, monkeypatch):
    monkeypatch.setattr(daily, "DAILY_DIR", tmp_path)
    p = daily._daily_path("2026-08-03")
    assert p == tmp_path / "2026-08-03.json"


def test_save_and_load_cached(tmp_path, monkeypatch):
    monkeypatch.setattr(daily, "DAILY_DIR", tmp_path)
    data = {"problem_statement": "x", "solution": {"steps": [], "final_answer": "1"}}
    daily._save("2026-08-03", data)
    loaded = daily._load_cached("2026-08-03")
    assert loaded["problem_statement"] == "x"


def test_load_cached_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(daily, "DAILY_DIR", tmp_path)
    assert daily._load_cached("2099-01-01") is None
