"""Tests for blog post sorting — no network, no database."""

from server.routers.blog import sort_posts


def test_sort_posts_newest_first():
    posts = [
        {"date": "2026-07-14", "title": "old"},
        {"date": "2026-07-20", "title": "new"},
        {"date": "2026-07-15", "title": "mid"},
    ]
    result = [p["title"] for p in sort_posts(posts)]
    assert result == ["new", "mid", "old"]


def test_sort_posts_undated_last():
    posts = [
        {"date": "", "title": "undated"},
        {"date": "2026-07-20", "title": "dated"},
    ]
    result = [p["title"] for p in sort_posts(posts)]
    assert result == ["dated", "undated"]


def test_sort_posts_mixed():
    posts = [
        {"date": "", "title": "a-no-date"},
        {"date": "2026-07-10", "title": "b"},
        {"date": "2026-07-19", "title": "c"},
    ]
    result = [p["title"] for p in sort_posts(posts)]
    assert result == ["c", "b", "a-no-date"]


def test_sort_posts_empty():
    assert sort_posts([]) == []
