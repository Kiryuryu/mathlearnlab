"""
Bookmarks API — user bookmarks for exhibits, mathematicians, news.
"""
import json
import os
from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException
from server.routers.auth import require_user
from server.main import DATA_DIR

router = APIRouter()
BOOKMARKS_FILE = DATA_DIR / "bookmarks.json"


def _load_bookmarks():
    if BOOKMARKS_FILE.exists():
        try:
            return json.loads(BOOKMARKS_FILE.read_text())
        except Exception:
            return {}
    return {}


def _save_bookmarks(data):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BOOKMARKS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2))


@router.get("/api/bookmarks")
async def get_bookmarks(user: dict = Depends(require_user)):
    data = _load_bookmarks()
    return {"bookmarks": data.get(user["user_id"], [])}


@router.post("/api/bookmarks")
async def add_bookmark(body: dict, user: dict = Depends(require_user)):
    data = _load_bookmarks()
    uid = user["user_id"]
    if uid not in data:
        data[uid] = []
    bookmark = {
        "id": str(len(data[uid]) + 1),
        "route": body.get("route", ""),
        "title": body.get("title", ""),
        "created_at": _now(),
    }
    data[uid].append(bookmark)
    _save_bookmarks(data)
    return {"bookmark": bookmark}


@router.delete("/api/bookmarks/{bookmark_id}")
async def remove_bookmark(bookmark_id: str, user: dict = Depends(require_user)):
    data = _load_bookmarks()
    uid = user["user_id"]
    if uid in data:
        data[uid] = [b for b in data[uid] if b["id"] != bookmark_id]
        _save_bookmarks(data)
    return {"status": "deleted"}


def _now():
    from datetime import datetime
    return datetime.utcnow().isoformat()
