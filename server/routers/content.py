"""
Content API — serve raw markdown content and search.
"""

from fastapi import APIRouter
from server.config import CONTENT_DIR
from server.services.search import search_all

router = APIRouter()


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
    return {"results": search_all(q, lang)}
