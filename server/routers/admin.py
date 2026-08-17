"""
Admin API — user management (approve/reject pending registrations).
Authenticated via a shared ADMIN_SECRET sent in the `Authorization: Bearer`
header (never in the JSON body). Missing ADMIN_SECRET fails startup in
non-debug mode — see server.config.validate_settings.
"""

import secrets
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from server.config import settings
from server.models.users import list_users, update_user_status

router = APIRouter()
security = HTTPBearer(auto_error=False)


def _check_secret(raw_secret: str):
    """Constant-time comparison to avoid timing side-channel attacks."""
    expected = settings.admin_secret
    if not expected:
        raise HTTPException(status_code=500, detail="Admin secret not configured")
    if not secrets.compare_digest(raw_secret.encode(), expected.encode()):
        raise HTTPException(status_code=403, detail="Unauthorized")


def _require_secret(credentials: HTTPAuthorizationCredentials | None = Depends(security)):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Admin secret required (Authorization: Bearer <secret>)")
    _check_secret(credentials.credentials)
    return credentials.credentials


@router.post("/api/admin/users")
async def list_pending_users(status: str = "pending", _: str = Depends(_require_secret)):
    return {"users": list_users(status=status, limit=50)}


@router.post("/api/admin/users/{user_id}/approve")
async def approve_user(user_id: str, _: str = Depends(_require_secret)):
    update_user_status(user_id, "active")
    return {"status": "approved"}


@router.post("/api/admin/users/{user_id}/reject")
async def reject_user(user_id: str, _: str = Depends(_require_secret)):
    update_user_status(user_id, "rejected")
    return {"status": "rejected"}
