"""
Blog API — serve blog posts from markdown files with frontmatter.
"""

import re
from pathlib import Path
from fastapi import APIRouter, HTTPException
from server.main import CONTENT_DIR

router = APIRouter()
NEWS_DIR = CONTENT_DIR / "news"


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


@router.get("/api/blog/posts")
async def list_posts():
    """List all blog posts with summaries."""
    if not NEWS_DIR.exists():
        return {"posts": []}
    posts = []
    for md_file in NEWS_DIR.glob("*.md"):
        if md_file.name.startswith("._"): continue
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
    posts.sort(key=lambda p: (not p["date"], p["date"]), reverse=True)
    return {"posts": posts}


@router.get("/api/blog/posts/{slug}")
async def get_post(slug: str):
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
