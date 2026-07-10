"""
Stats API — grade history and statistics.
"""

from fastapi import APIRouter
from server.services import history as history_svc

router = APIRouter()


@router.get("/api/stats")
async def get_stats():
    return history_svc.get_stats()


@router.get("/api/stats/history")
async def get_history(n: int = 10):
    return {"recent": history_svc.get_recent(n)}


@router.get("/api/stats/errors")
async def get_errors():
    """Return problems with incorrect or partial verdicts."""
    recent = history_svc.get_recent(200)
    errors = [h for h in recent if h.get("verdict") in ("incorrect", "partially_correct")]
    return {"errors": errors, "count": len(errors)}
