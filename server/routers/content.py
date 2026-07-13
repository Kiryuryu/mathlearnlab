"""
Content API — serve raw markdown content and search.
"""

from fastapi import APIRouter, Request
from server.main import CONTENT_DIR
from server.config import settings
import re, json

router = APIRouter()


@router.get("/api/content/{path:path}")
async def get_content(path: str):
    """Return raw markdown content for a given path."""
    filepath = CONTENT_DIR / f"{path}.md"
    if not filepath.exists():
        filepath = CONTENT_DIR / path
    if not filepath.exists():
        return {"error": "not found", "path": path}
    return {"content": filepath.read_text(encoding="utf-8"), "path": path}


@router.get("/api/search")
async def search_content(q: str = ""):
    """Search across all markdown content and exhibit/mathematician metadata."""
    query = q.strip().lower()
    if len(query) < 1:
        return {"results": []}

    results = []

    # Search markdown content files
    if CONTENT_DIR.exists():
        for md_file in CONTENT_DIR.rglob("*.md"):
            try:
                text = md_file.read_text(encoding="utf-8")
                lower_text = text.lower()
                if query in lower_text:
                    # Find a relevant snippet
                    idx = lower_text.find(query)
                    start = max(0, idx - 40)
                    end = min(len(text), idx + len(query) + 80)
                    snippet = text[start:end].replace("\n", " ").strip()
                    if start > 0:
                        snippet = "..." + snippet
                    if end < len(text):
                        snippet = snippet + "..."

                    # Derive title from file path
                    rel = str(md_file.relative_to(CONTENT_DIR))
                    title = rel.replace(".md", "").replace("-", " ").replace("/", " > ")
                    route = "/notebooks/" + rel.replace(".md", "")

                    results.append({
                        "title": title,
                        "excerpt": snippet[:160],
                        "route": route,
                        "section": "内容"
                    })
            except Exception:
                continue

    # Search exhibits
    for key, e in settings.exhibits.items():
        if key == "gaoshu":
            continue
        zh = e.get("zh", "")
        qs = e.get("big_question", "")
        if query in zh.lower() or query in qs.lower():
            results.append({
                "title": e.get("icon", "") + " " + zh,
                "excerpt": e.get("big_question", ""),
                "route": "/exhibit/" + key,
                "section": "微积分"
            })

    # Search mathematicians
    for key, m in settings.mathematicians.items():
        name = m.get("name", "") + " " + m.get("name_en", "")
        story = m.get("story", "")
        contrib = m.get("contributions", "")
        if query in name.lower() or query in story.lower() or query in contrib.lower():
            results.append({
                "title": m.get("icon", "") + " " + m.get("name", ""),
                "excerpt": m.get("contributions", ""),
                "route": "/mathematicians/" + key,
                "section": "数学家长廊"
            })

    # Limit results
    return {"results": results[:12]}
