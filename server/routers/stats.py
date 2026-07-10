"""
Stats API — grade history and statistics (per-user).
"""

from fastapi import APIRouter, Depends
from server.routers.auth import require_user
from server.services import history as history_svc

router = APIRouter()


@router.get("/api/stats")
async def get_stats(user: dict = Depends(require_user)):
    return history_svc.get_stats(user["user_id"])


@router.get("/api/stats/history")
async def get_history(n: int = 10, user: dict = Depends(require_user)):
    return {"recent": history_svc.get_recent(user["user_id"], n)}


@router.get("/api/stats/errors")
async def get_errors(user: dict = Depends(require_user)):
    """Return problems with incorrect or partial verdicts."""
    errors = history_svc.get_errors(user["user_id"])
    return {"errors": errors, "count": len(errors)}
