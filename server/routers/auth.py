"""
Auth API — registration, login, user info.
"""

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from server.models.database import get_db, db_session, init_db
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
    """Register a new user account."""
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
            "INSERT INTO users (id, username, email, password_hash) VALUES (?, ?, ?, ?)",
            (user_id, body.username, body.email, pwd_hash),
        )
        conn.commit()

    token = create_access_token(user_id, body.username)
    return {
        "token": token,
        "user": {"id": user_id, "username": body.username, "email": body.email},
    }


@router.post("/api/auth/login")
async def login(body: LoginRequest):
    """Login and get JWT token."""
    conn = get_db()
    row = conn.execute("SELECT * FROM users WHERE username = ?", (body.username,)).fetchone()
    conn.close()

    if row is None or not verify_password(body.password, row["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

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
        "created_at": row["created_at"],
    }
