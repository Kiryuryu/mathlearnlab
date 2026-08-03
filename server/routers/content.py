"""
Content API — serve raw markdown content and search.
"""

import time
from fastapi import APIRouter
from server.config import CONTENT_DIR
from server.services.search import search_all

router = APIRouter()

# In-memory content cache: {path_str: (mtime_ns, content)}. Invalidated when file changes.
_content_cache: dict[str, tuple[int, str]] = {}
_CACHE_TTL = 30


def _resolve_path(path: str, lang: str):
    """Resolve a content path to the actual file (handles lang= en variant)."""
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
    return filepath


def _read_cached(filepath) -> str | None:
    """Read file content with mtime-based caching."""
    if not filepath.exists():
        return None
    key = str(filepath)
    try:
        st = filepath.stat()
        cached = _content_cache.get(key)
        if cached and cached[0] == st.st_mtime_ns:
            return cached[1]
        text = filepath.read_text(encoding="utf-8")
        _content_cache[key] = (st.st_mtime_ns, text)
        return text
    except Exception:
        return None


@router.get("/api/content/{path:path}")
def get_content(path: str, lang: str = "zh"):
    """Return raw markdown content for a given path. Supports ?lang=en for English."""
    filepath = _resolve_path(path, lang)
    content = _read_cached(filepath)
    if content is None:
        return {"error": "not found", "path": path}
    return {"content": content, "path": path}


@router.get("/api/search")
def search_content(q: str = "", lang: str = "zh"):
    """Search across all markdown content and exhibit/mathematician metadata."""
    return {"results": search_all(q, lang)}
