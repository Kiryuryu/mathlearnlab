"""Tests for grade helpers — image validation, problem storage (no network)."""

from types import SimpleNamespace
import pytest
from fastapi import HTTPException
from server.routers import grade
from server.models import problems as problems_mod


def test_validate_image_rejects_empty():
    with pytest.raises(HTTPException) as exc:
        grade._validate_image(b"")
    assert exc.value.status_code == 400


def test_validate_image_rejects_oversized(monkeypatch):
    monkeypatch.setattr(grade, "settings", SimpleNamespace(max_image_bytes=10))
    with pytest.raises(HTTPException) as exc:
        grade._validate_image(b"\xff\xd8\xff" + b"0" * 100)
    assert exc.value.status_code == 413


def test_validate_image_rejects_unsupported_type():
    with pytest.raises(HTTPException) as exc:
        grade._validate_image(b"\x00\x01\x02\x03 not an image at all")
    assert exc.value.status_code == 415


def test_validate_image_accepts_png():
    grade._validate_image(b"\x89PNG\r\n\x1a\n" + b"x" * 64)


def test_validate_image_accepts_jpeg():
    grade._validate_image(b"\xff\xd8\xff\xe0" + b"x" * 64)


def test_problem_storage_roundtrip(tmp_path, monkeypatch):
    """Generated problems persist to SQLite and load back by topic+id."""
    import server.models.database as database
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    # Fresh thread-local connection for the tmp DB (direct assignment — the
    # threading.local object doesn't support monkeypatch.setattr's getattr).
    database._mysql_local.sqlite = None
    database.init_db()

    problems_mod.persist_problem({"id": "GEN-T1", "difficulty": "exam", "problem_statement": "x"}, "limits")
    p = problems_mod.load_problem("limits", "GEN-T1")
    assert p is not None
    assert p["id"] == "GEN-T1"
    assert problems_mod.load_problem("limits", "GEN-MISSING") is None
    # Wrong topic → not found.
    assert problems_mod.load_problem("series", "GEN-T1") is None
