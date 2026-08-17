"""
Search service — search markdown content, exhibits, and mathematicians.
Pure functions so they can be unit-tested without network/database.
"""

import time
from pathlib import Path
from server.config import CONTENT_DIR, settings

SECTION_ZH = {"content": "内容", "subjects": "学科", "exhibits": "微积分", "mathematicians": "数学家长廊"}
SECTION_EN = {"content": "Content", "subjects": "Subjects", "exhibits": "Calculus", "mathematicians": "Mathematicians"}

# Cache of scanned .md files: {path_str: (mtime_ns, text, text_lower)}.
# Lowercased text is cached so per-request .lower() over every file is avoided.
_FILE_CACHE: dict[str, tuple[int, str, str]] = {}
_FILE_CACHE_TS = 0.0
_CACHE_TTL = 30  # seconds


def _section(key: str, lang: str) -> str:
    return SECTION_EN.get(key, key) if lang == "en" else SECTION_ZH.get(key, key)


def _refresh_file_cache():
    """Rebuild the in-memory file cache if stale (new/changed files)."""
    global _FILE_CACHE_TS
    now = time.monotonic()
    if now - _FILE_CACHE_TS < _CACHE_TTL:
        return
    _FILE_CACHE_TS = now
    cache: dict[str, tuple[int, str, str]] = {}
    base = Path(CONTENT_DIR)
    for directory in (base, base / "en"):
        if not directory.exists():
            continue
        for md_file in directory.rglob("*.md"):
            if md_file.name.startswith("._"):
                continue
            try:
                st = md_file.stat()
                path_str = str(md_file)
                cached = _FILE_CACHE.get(path_str)
                if cached and cached[0] == st.st_mtime_ns:
                    cache[path_str] = cached
                    continue
                text = md_file.read_text(encoding="utf-8")
                cache[path_str] = (st.st_mtime_ns, text, text.lower())
            except Exception:
                continue
    _FILE_CACHE.clear()
    _FILE_CACHE.update(cache)


def _snippet(text: str, idx: int, query_len: int, around: int = 40, tail: int = 80) -> str:
    start = max(0, idx - around)
    end = min(len(text), idx + query_len + tail)
    snippet = text[start:end].replace("\n", " ").strip()
    if start > 0:
        snippet = "..." + snippet
    if end < len(text):
        snippet = snippet + "..."
    return snippet


# Only content that maps to a real SPA route is searchable. The legacy
# notebooks/notes/problems/error-log directories have no frontend route, so
# returning them would produce dead links.
_SEARCHABLE_ROOTS = ("exhibits/", "news/")


def _route_for(rel: str) -> str:
    rel = rel.replace(".md", "")
    if rel.startswith("exhibits/"):
        return "/exhibit/" + rel.split("/")[1]
    if rel.startswith("news/"):
        return "/news/" + rel[len("news/"):]
    return "/" + rel


def search_content_files(query: str, lang: str) -> list[dict]:
    """Search searchable .md files in CONTENT_DIR and CONTENT_DIR/en (cached)."""
    results = []
    query = query.lower()
    base = Path(CONTENT_DIR)
    _refresh_file_cache()

    for path_str, (_mtime, text, text_lower) in _FILE_CACHE.items():
        try:
            rel = str(Path(path_str).relative_to(base))
            en = rel.startswith("en/")
            rel2 = rel[3:] if en else rel
            if not rel2.startswith(_SEARCHABLE_ROOTS):
                continue
            idx = text_lower.find(query)
            if idx == -1:
                continue
            title = rel2.replace(".md", "").replace("-", " ").replace("/", " > ")
            if en:
                title += " (EN)"
            results.append({
                "title": title,
                "excerpt": _snippet(text, idx, len(query))[:160],
                "route": _route_for(rel2),
                "section": _section("content", "en" if en else lang),
            })
        except Exception:
            continue
    return results


def search_exhibits(query: str, lang: str) -> list[dict]:
    results = []
    query = query.lower()
    for key, e in settings.exhibits.items():
        zh = e.get("zh", "")
        qs = e.get("big_question", "")
        en = e.get("en", "")
        qs_en = e.get("big_question_en", "")
        match_zh = query in zh.lower() or query in qs.lower()
        match_en = lang == "en" and (query in en.lower() or query in qs_en.lower())
        if match_zh or match_en:
            results.append({
                "title": e.get("icon", "") + " " + (en if lang == "en" and en else zh),
                "excerpt": qs_en if lang == "en" and qs_en else qs,
                "route": "/exhibit/" + key,
                "section": _section("exhibits", lang),
            })
    return results


def search_mathematicians(query: str, lang: str) -> list[dict]:
    results = []
    query = query.lower()
    for key, m in settings.mathematicians.items():
        name = m.get("name", "") + " " + m.get("name_en", "")
        story = m.get("story", "") + " " + m.get("story_en", "")
        contrib = m.get("contributions", "") + " " + m.get("contributions_en", "")
        if query in name.lower() or query in story.lower() or query in contrib.lower():
            results.append({
                "title": m.get("icon", "") + " " + (m.get("name_en", "") if lang == "en" else m.get("name", "")),
                "excerpt": m.get("contributions_en", "") if lang == "en" else m.get("contributions", ""),
                "route": "/mathematicians/" + key,
                "section": _section("mathematicians", lang),
            })
    return results


def search_subjects(query: str, lang: str) -> list[dict]:
    results = []
    query = query.lower()
    for key, s in settings.subjects.items():
        zh = s.get("zh", "")
        desc = s.get("desc", "")
        en = s.get("en", "")
        desc_en = s.get("desc_en", "")
        match_zh = query in zh.lower() or query in desc.lower()
        match_en = lang == "en" and (query in en.lower() or query in desc_en.lower())
        if match_zh or match_en:
            results.append({
                "title": s.get("icon", "") + " " + (en if lang == "en" and en else zh),
                "excerpt": desc_en if lang == "en" and desc_en else desc,
                "route": "/subject/" + key,
                "section": _section("subjects", lang),
            })
    return results


def search_all(q: str, lang: str = "zh", limit: int = 12) -> list[dict]:
    query = q.strip().lower()
    if len(query) < 1:
        return []
    results = search_content_files(query, lang)
    results += search_subjects(query, lang)
    results += search_exhibits(query, lang)
    results += search_mathematicians(query, lang)
    return results[:limit]
