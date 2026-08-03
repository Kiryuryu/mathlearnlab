"""Tests for the search service — no network, no database."""

from server.services.search import search_exhibits, search_mathematicians, _snippet


def test_snippet_adds_ellipsis_when_truncated():
    text = "a" * 100 + "KEYWORD" + "b" * 100
    idx = text.find("KEYWORD")
    s = _snippet(text, idx, len("KEYWORD"), around=5, tail=5)
    assert s.startswith("...")
    assert s.endswith("...")
    assert "KEYWORD" in s


def test_snippet_no_ellipsis_when_full():
    text = "KEYWORD"
    idx = 0
    s = _snippet(text, idx, len("KEYWORD"))
    assert s == "KEYWORD"


def test_search_exhibits_zh():
    results = search_exhibits("极限", "zh")
    assert any(r["route"] == "/exhibit/limits" for r in results)


def test_search_mathematicians_en():
    results = search_mathematicians("Euler", "en")
    assert any(r["route"] == "/mathematicians/euler" for r in results)


def test_search_empty_query():
    from server.services.search import search_all
    assert search_all("") == []
