"""
Content API — serve raw markdown content and search.
"""

from fastapi import APIRouter, Request
from server.main import CONTENT_DIR
from server.config import settings
import re, json

router = APIRouter()

SECTION_ZH = {"content": "内容", "exhibits": "微积分", "mathematicians": "数学家长廊"}
SECTION_EN = {"content": "Content", "exhibits": "Calculus", "mathematicians": "Mathematicians"}


def _section(key: str, lang: str) -> str:
    return SECTION_EN.get(key, key) if lang == "en" else SECTION_ZH.get(key, key)


@router.get("/api/content/{path:path}")
async def get_content(path: str, lang: str = "zh"):
    """Return raw markdown content for a given path. Supports ?lang=en for English."""
    filepath = CONTENT_DIR / f"{path}.md"
    if lang != "zh":
        en_path = CONTENT_DIR / "en" / f"{path}.md"
        if en_path.exists():
            filepath = en_path
    if not filepath.exists():
        filepath = CONTENT_DIR / path
    if lang != "zh" and not str(filepath).startswith(str(CONTENT_DIR / "en")):
        en_path = CONTENT_DIR / "en" / path
        if en_path.exists():
            filepath = en_path
    if not filepath.exists():
        return {"error": "not found", "path": path}
    return {"content": filepath.read_text(encoding="utf-8"), "path": path}


@router.get("/api/search")
async def search_content(q: str = "", lang: str = "zh"):
    """Search across all markdown content and exhibit/mathematician metadata."""
    query = q.strip().lower()
    if len(query) < 1:
        return {"results": []}

    results = []

    if CONTENT_DIR.exists():
        for md_file in CONTENT_DIR.rglob("*.md"):
            if md_file.name.startswith("._"): continue
            try:
                text = md_file.read_text(encoding="utf-8")
                lower_text = text.lower()
                if query in lower_text:
                    idx = lower_text.find(query)
                    start = max(0, idx - 40)
                    end = min(len(text), idx + len(query) + 80)
                    snippet = text[start:end].replace("\n", " ").strip()
                    if start > 0:
                        snippet = "..." + snippet
                    if end < len(text):
                        snippet = snippet + "..."
                    rel = str(md_file.relative_to(CONTENT_DIR))
                    title = rel.replace(".md", "").replace("-", " ").replace("/", " > ")
                    if rel.startswith("problems/"): route = "/problems/" + rel.replace(".md", "")
                    elif rel.startswith("notes/"): route = "/notes/" + rel.replace(".md", "")
                    elif rel.startswith("error-log/"): route = "/error-log/" + rel.replace(".md", "").rsplit("/",1)[-1]
                    elif rel.startswith("exhibits/"): route = "/exhibit/" + rel.split("/")[1]
                    else: route = "/notebooks/" + rel.replace(".md", "")
                    results.append({
                        "title": title,
                        "excerpt": snippet[:160],
                        "route": route,
                        "section": _section("content", lang),
                    })
            except Exception:
                continue

    for key, e in settings.exhibits.items():
        if key == "gaoshu":
            continue
        zh = e.get("zh", "")
        qs = e.get("big_question", "")
        en = e.get("en", "")
        qs_en = e.get("big_question_en", "")
        match_zh = query in zh.lower() or query in qs.lower()
        match_en = lang == "en" and (query in en.lower() or query in qs_en.lower())
        if match_zh or match_en:
            title = e.get("icon", "") + " " + (en if lang == "en" and en else zh)
            excerpt = qs_en if lang == "en" and qs_en else qs
            results.append({
                "title": title,
                "excerpt": excerpt,
                "route": "/exhibit/" + key,
                "section": _section("exhibits", lang),
            })

    for key, m in settings.mathematicians.items():
        name = m.get("name", "") + " " + m.get("name_en", "")
        story = m.get("story", "") + " " + m.get("story_en", "")
        contrib = m.get("contributions", "") + " " + m.get("contributions_en", "")
        if query in name.lower() or query in story.lower() or query in contrib.lower():
            title = m.get("icon", "") + " " + (m.get("name_en", "") if lang == "en" else m.get("name", ""))
            excerpt = m.get("contributions_en", "") if lang == "en" else m.get("contributions", "")
            results.append({
                "title": title,
                "excerpt": excerpt,
                "route": "/mathematicians/" + key,
                "section": _section("mathematicians", lang),
            })

    return {"results": results[:12]}
