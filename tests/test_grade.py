"""Tests for grade helpers — no network, no database."""

import json
from unittest.mock import patch
from server.routers import grade


def test_load_generated_problem_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(grade, "GENERATED_DIR", tmp_path)
    assert grade._load_generated_problem("limits", "GEN-X") is None


def test_load_generated_problem_found(tmp_path, monkeypatch):
    monkeypatch.setattr(grade, "GENERATED_DIR", tmp_path)
    (tmp_path / "limits_problems.json").write_text(
        json.dumps([{"id": "GEN-A", "problem_statement": "x"}]),
        encoding="utf-8",
    )
    p = grade._load_generated_problem("limits", "GEN-A")
    assert p is not None
    assert p["id"] == "GEN-A"


def test_load_generated_problem_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr(grade, "GENERATED_DIR", tmp_path)
    (tmp_path / "limits_problems.json").write_text(
        json.dumps([{"id": "GEN-A", "problem_statement": "x"}]),
        encoding="utf-8",
    )
    assert grade._load_generated_problem("limits", "GEN-OTHER") is None
