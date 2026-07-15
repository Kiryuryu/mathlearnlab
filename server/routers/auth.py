"""
Auth API — registration, login, user info.
"""
import os
from fastapi import APIRouter, HTTPException, Depends
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


# ── Model schemas (inline pydantic, no ORM needed) ──

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


# ── Dependency: get current user (optional) ──


def get_current_user(credentials: HTTPAuthorizationCredentials | None = Depends(security)) -> dict | None:
    """Extract user from JWT bearer token. Returns None if no token or invalid."""
    if credentials is None:
        return None
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        return None
    return {"user_id": payload["sub"], "username": payload["username"]}


def require_user(user: dict | None = Depends(get_current_user)) -> dict:
    """Require a valid user. Raises 401 if missing."""
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user


# ── Routes ──


@router.post("/api/auth/register")
async def register(body: RegisterRequest):
    """Register a new user account (pending admin approval)."""
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

    # Send email to admin
    from server.services.email import send_admin_notification
    approve_url = f"https://www.mathlearnlab.cn/admin"
    send_admin_notification(
        subject=f"数学博物馆 - 新用户注册: {body.username}",
        body=f"<h3>新用户注册</h3><p>用户名: {body.username}</p><p>邮箱: {body.email}</p><p>ID: {user_id}</p><p>请登录管理后台审核: <a href=\"{approve_url}\">{approve_url}</a></p>"
    )

    return {
        "message": "注册成功，请等待管理员审核",
        "status": "pending",
    }


@router.post("/api/auth/login")
async def login(body: LoginRequest):
    """Login and get JWT token. Requires admin-approved account."""
    with db_session() as conn:
        row = conn.execute("SELECT * FROM users WHERE username = ?", (body.username,)).fetchone()

    if row is None or not verify_password(body.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    status = row.get("status", "active")
    if status == "pending":
        raise HTTPException(status_code=403, detail="账号正在审核中，请等待管理员通过")
    if status == "rejected":
        raise HTTPException(status_code=403, detail="账号审核未通过")

    token = create_access_token(row["id"], row["username"])
    return {
        "token": token,
        "user": {"id": row["id"], "username": row["username"], "email": row["email"]},
    }


@router.get("/api/auth/me")
async def me(user: dict = Depends(require_user)):
    """Get current user info."""
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


ADMIN_SECRET = os.getenv("ADMIN_SECRET", "mathlab-admin-2026")


@router.get("/api/admin/users")
async def list_pending_users(secret: str = "", status: str = "pending"):
    """List users by status (admin only)."""
    if secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Unauthorized")
    with db_session() as conn:
        if status == "all":
            rows = conn.execute("SELECT id, username, email, status, created_at FROM users ORDER BY created_at DESC LIMIT 50").fetchall()
        else:
            rows = conn.execute("SELECT id, username, email, status, created_at FROM users WHERE status = ? ORDER BY created_at DESC", (status,)).fetchall()
    return {"users": [dict(r) for r in rows]}


@router.post("/api/admin/users/{user_id}/approve")
async def approve_user(user_id: str, secret: str = ""):
    """Approve a pending user."""
    if secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Unauthorized")
    with db_session() as conn:
        conn.execute("UPDATE users SET status = 'active' WHERE id = ?", (user_id,))
        conn.commit()
    return {"status": "approved"}


@router.post("/api/admin/users/{user_id}/reject")
async def reject_user(user_id: str, secret: str = ""):
    """Reject a pending user."""
    if secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Unauthorized")
    with db_session() as conn:
        conn.execute("UPDATE users SET status = 'rejected' WHERE id = ?", (user_id,))
        conn.commit()
    return {"status": "rejected"}

