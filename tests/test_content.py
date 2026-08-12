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


def test_resolve_concept_en(tmp_path, monkeypatch):
    """concept.md must resolve to the en variant when lang=en and it exists."""
    monkeypatch.setattr(content, "CONTENT_DIR", tmp_path)
    zh = tmp_path / "exhibits" / "limits"
    en = tmp_path / "en" / "exhibits" / "limits"
    zh.mkdir(parents=True)
    en.mkdir(parents=True)
    (zh / "concept.md").write_text("zh", encoding="utf-8")
    (en / "concept.md").write_text("en", encoding="utf-8")
    p = content._resolve_path("exhibits/limits/concept", "en")
    assert p == en / "concept.md"


def test_notebook_not_in_exhibits():
    """No exhibit may carry a 'notebook' field — concept content is per-exhibit now."""
    from server.content_data import exhibits
    for key, ex in exhibits.items():
        if key == "gaoshu":
            continue
        assert "notebook" not in ex, f"{key} still references a shared notebook"


def test_exhibits_metadata_shape():
    """Every parented exhibit carries the navigation metadata the redesign relies on."""
    from server.content_data import exhibits, mathematicians
    for key, ex in exhibits.items():
        if not ex.get("parent"):
            continue
        # mathematician links must point at real mathematician keys
        assert "mathematicians" in ex, f"{key} missing mathematicians links"
        for mk in ex["mathematicians"]:
            assert mk in mathematicians, f"{key} links to unknown mathematician {mk}"
        # narrative "up next" card must exist in both languages
        assert ex.get("next_note"), f"{key} missing next_note"
        assert ex.get("next_note_en"), f"{key} missing next_note_en"
        # home card accent color present
        assert ex.get("home_accent", "").startswith("#"), f"{key} missing home_accent"


def test_subjects_shape():
    """Every subject has the fields the home page and SubjectView render."""
    from server.content_data import subjects, exhibits
    assert subjects, "subjects dict must not be empty"
    for key, s in subjects.items():
        assert s.get("zh") and s.get("en"), f"subject {key} missing zh/en"
        assert s.get("icon"), f"subject {key} missing icon"
        assert s.get("accent", "").startswith("#"), f"subject {key} missing accent"
        assert s.get("order"), f"subject {key} missing order"
        assert s.get("desc") and s.get("desc_en"), f"subject {key} missing desc"
    # every parented exhibit must belong to a known subject
    for ekey, ex in exhibits.items():
        parent = ex.get("parent")
        if parent:
            assert parent in subjects, f"exhibit {ekey} has unknown parent {parent}"

