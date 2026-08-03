"""
Blog API — serve blog posts from markdown files with frontmatter.
"""

import re
import time
from pathlib import Path
from fastapi import APIRouter, HTTPException
from server.config import CONTENT_DIR

router = APIRouter()
NEWS_DIR = CONTENT_DIR / "news"

# Simple list cache: rebuild only when directory contents change.
_posts_cache = []
_posts_cache_ts = 0.0
_CACHE_TTL = 30


def _list_cached():
    global _posts_cache, _posts_cache_ts
    now = time.monotonic()
    if _posts_cache and now - _posts_cache_ts < _CACHE_TTL:
        return _posts_cache
    _posts_cache_ts = now
    posts = []
    if NEWS_DIR.exists():
        for md_file in NEWS_DIR.glob("*.md"):
            if md_file.name.startswith("._"): continue
            try:
                text = md_file.read_text(encoding="utf-8")
                meta, body = parse_frontmatter(text)
                posts.append({
                    "slug": md_file.stem,
                    "title": meta.get("title", md_file.stem),
                    "date": meta.get("date", ""),
                    "category": meta.get("category", "数学"),
                    "summary": body[:200].replace("\n", " ") + "...",
                    "author": meta.get("author", ""),
                })
            except Exception:
                continue
    _posts_cache = sort_posts(posts)
    return _posts_cache


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML-like frontmatter from markdown text."""
    meta, body = {}, text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
            body = parts[2].strip()
    return meta, body


def sort_posts(posts: list[dict]) -> list[dict]:
    """Sort posts by date descending; posts without a date go last."""
    return sorted(posts, key=lambda p: p["date"] or "0000-00-00", reverse=True)


@router.get("/api/blog/posts")
def list_posts():
    """List all blog posts with summaries (cached)."""
    return {"posts": _list_cached()}


@router.get("/api/blog/posts/{slug}")
def get_post(slug: str):
    """Get a single blog post with full content."""
    filepath = NEWS_DIR / f"{slug}.md"
    if not filepath.exists() or filepath.name.startswith("._"):
        raise HTTPException(status_code=404, detail="Post not found")
    text = filepath.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    return {
        "slug": slug,
        "title": meta.get("title", slug),
        "date": meta.get("date", ""),
        "category": meta.get("category", "数学"),
        "author": meta.get("author", ""),
        "content": body,
    }
