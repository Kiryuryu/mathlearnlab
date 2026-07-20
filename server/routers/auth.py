"""
Auth API — registration, login, user info.
"""
import os
import secrets
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from server.models.database import get_db, db_session
from server.models.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    generate_user_id,
)

router = APIRouter()
security = HTTPBearer(auto_error=False)


from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str = ""


class LoginRequest(BaseModel):
    username: str
    password: str


class UserInfo(BaseModel):
    id: str
    username: str
    email: str
    created_at: str


class AdminSecretRequest(BaseModel):
    secret: str


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> dict | None:
    if credentials is None:
        return None
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        return None
    return {"user_id": payload["sub"], "username": payload["username"]}


def require_user(user: dict | None = Depends(get_current_user)) -> dict:
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


@router.get("/api/auth/check-username")
async def check_username(username: str):
    if len(username) < 3:
        return {"available": False, "reason": "too_short"}
    with db_session() as conn:
        existing = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    return {"available": existing is None, "reason": "taken" if existing else None}


@router.post("/api/auth/register")
async def register(body: RegisterRequest):
    if len(body.username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
    if len(body.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    with db_session() as conn:
        existing = conn.execute("SELECT id FROM users WHERE username = ?", (body.username,)).fetchone()
        if existing:
            raise HTTPException(status_code=409, detail="Username already taken")

        user_id = generate_user_id()
        pwd_hash = hash_password(body.password)
        conn.execute(
            "INSERT INTO users (id, username, email, password_hash, status) VALUES (?, ?, ?, ?, 'pending')",
            (user_id, body.username, body.email, pwd_hash),
        )
        conn.commit()

    from server.services.email import send_admin_notification
    approve_url = "https://www.mathlearnlab.cn/admin"
    send_admin_notification(
        subject=f"Math Museum - New Registration: {body.username}",
        body=f"<h3>New User Registration</h3><p>Username: {body.username}</p><p>Email: {body.email}</p><p>ID: {user_id}</p><p>Review at: <a href=\"{approve_url}\">{approve_url}</a></p>"
    )

    return {
        "message": "Registration submitted, awaiting admin approval",
        "status": "pending",
    }


@router.post("/api/auth/login")
async def login(body: LoginRequest):
    with db_session() as conn:
        row = conn.execute("SELECT * FROM users WHERE username = ?", (body.username,)).fetchone()

    if row is None or not verify_password(body.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    status = row.get("status", "active")
    if status == "pending":
        raise HTTPException(status_code=403, detail="Account is pending admin approval")
    if status == "rejected":
        raise HTTPException(status_code=403, detail="Account registration was rejected")

    token = create_access_token(row["id"], row["username"])
    return {
        "token": token,
        "user": {"id": row["id"], "username": row["username"], "email": row["email"]},
    }


@router.get("/api/auth/me")
async def me(user: dict = Depends(require_user)):
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE id = ?", (user["user_id"],)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": row["id"],
        "username": row["username"],
        "email": row["email"],
    }


ADMIN_SECRET = os.getenv("ADMIN_SECRET") or secrets.token_urlsafe(32)


@router.post("/api/admin/users")
async def list_pending_users(body: AdminSecretRequest, status: str = "pending"):
    if body.secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Unauthorized")
    with db_session() as conn:
        if status == "all":
            rows = conn.execute("SELECT id, username, email, status, created_at FROM users ORDER BY created_at DESC LIMIT 50").fetchall()
        else:
            rows = conn.execute("SELECT id, username, email, status, created_at FROM users WHERE status = ? ORDER BY created_at DESC", (status,)).fetchall()
    return {"users": [dict(r) for r in rows]}


@router.post("/api/admin/users/{user_id}/approve")
async def approve_user(user_id: str, body: AdminSecretRequest):
    if body.secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Unauthorized")
    with db_session() as conn:
        conn.execute("UPDATE users SET status = 'active' WHERE id = ?", (user_id,))
        conn.commit()
    return {"status": "approved"}


@router.post("/api/admin/users/{user_id}/reject")
async def reject_user(user_id: str, body: AdminSecretRequest):
    if body.secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Unauthorized")
    with db_session() as conn:
        conn.execute("UPDATE users SET status = 'rejected' WHERE id = ?", (user_id,))
        conn.commit()
    return {"status": "rejected"}
