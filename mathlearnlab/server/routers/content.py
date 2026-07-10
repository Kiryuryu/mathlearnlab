"""
Content API — serve raw markdown content.
"""

from fastapi import APIRouter
from server.main import CONTENT_DIR

router = APIRouter()


@router.get("/api/content/{path:path}")
async def get_content(path: str):
    """Return raw markdown content for a given path."""
    filepath = CONTENT_DIR / f"{path}.md"
    if not filepath.exists():
        # Try without .md extension
        filepath = CONTENT_DIR / path
    if not filepath.exists():
        return {"error": "not found", "path": path}
    return {"content": filepath.read_text(encoding="utf-8"), "path": path}
