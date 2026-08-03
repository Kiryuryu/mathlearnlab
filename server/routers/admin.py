"""
Admin API — user management (approve/reject pending registrations).
Authenticated via a shared ADMIN_SECRET sent in the JSON body.
"""

import os
import secrets
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from server.models.database import db_session

router = APIRouter()

ADMIN_SECRET = os.getenv("ADMIN_SECRET") or secrets.token_urlsafe(32)


class AdminSecretRequest(BaseModel):
    secret: str


def _check_secret(body: AdminSecretRequest):
    if body.secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Unauthorized")


@router.post("/api/admin/users")
async def list_pending_users(body: AdminSecretRequest, status: str = "pending"):
    _check_secret(body)
    with db_session() as conn:
        if status == "all":
            rows = conn.execute("SELECT id, username, email, status, created_at FROM users ORDER BY created_at DESC LIMIT 50").fetchall()
        else:
            rows = conn.execute("SELECT id, username, email, status, created_at FROM users WHERE status = ? ORDER BY created_at DESC", (status,)).fetchall()
    return {"users": [dict(r) for r in rows]}


@router.post("/api/admin/users/{user_id}/approve")
async def approve_user(user_id: str, body: AdminSecretRequest):
    _check_secret(body)
    with db_session() as conn:
        conn.execute("UPDATE users SET status = 'active' WHERE id = ?", (user_id,))
        conn.commit()
    return {"status": "approved"}


@router.post("/api/admin/users/{user_id}/reject")
async def reject_user(user_id: str, body: AdminSecretRequest):
    _check_secret(body)
    with db_session() as conn:
        conn.execute("UPDATE users SET status = 'rejected' WHERE id = ?", (user_id,))
        conn.commit()
    return {"status": "rejected"}
