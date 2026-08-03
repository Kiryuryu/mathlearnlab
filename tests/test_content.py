"""Tests for content router helpers — no network."""

from server.routers import content


def test_resolve_path_md(tmp_path, monkeypatch):
    monkeypatch.setattr(content, "CONTENT_DIR", tmp_path)
    (tmp_path / "exhibits").mkdir()
    (tmp_path / "exhibits" / "limits.md").write_text("hi", encoding="utf-8")
    p = content._resolve_path("exhibits/limits", "zh")
    assert p.exists()


def test_read_cached_returns_content(tmp_path, monkeypatch):
    monkeypatch.setattr(content, "CONTENT_DIR", tmp_path)
    f = tmp_path / "a.md"
    f.write_text("hello", encoding="utf-8")
    assert content._read_cached(f) == "hello"


def test_read_cached_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(content, "CONTENT_DIR", tmp_path)
    assert content._read_cached(tmp_path / "nope.md") is None


def test_read_cached_invalidated_on_change(tmp_path, monkeypatch):
    monkeypatch.setattr(content, "CONTENT_DIR", tmp_path)
    f = tmp_path / "b.md"
    f.write_text("v1", encoding="utf-8")
    assert content._read_cached(f) == "v1"
    # Modify file — mtime changes, cache should refresh
    f.write_text("v2", encoding="utf-8")
    assert content._read_cached(f) == "v2"
