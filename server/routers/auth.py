"""
Auth API — registration, login, user info.
"""
import logging
import re
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.concurrency import run_in_threadpool
from server.models.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
    generate_user_id,
)
from server.models.users import username_exists, create_user, get_user_by_username, get_user_by_id, get_user_by_email, update_user_password
from server.models.reset_tokens import create_reset_token, consume_reset_token, cleanup_expired_tokens
from server.services.ratelimit import is_blocked, record_failure, record_success

logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer(auto_error=False)

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _client_ip(request: Request) -> str:
    fwd = request.headers.get("X-Forwarded-For", "")
    if fwd:
        return fwd.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


from pydantic import BaseModel


class RegisterRequest(BaseModel):
    username: str
    password: str
    email: str = ""
    # Honeypot field — real browsers never fill it; bots often do.
    website: str = ""


class LoginRequest(BaseModel):
    username: str
    password: str


class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    password: str


class UserInfo(BaseModel):
    id: str
    username: str
    email: str
    created_at: str


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
    return {"available": not username_exists(username), "reason": "taken" if username_exists(username) else None}


@router.post("/api/auth/register")
async def register(body: RegisterRequest, request: Request):
    ip = _client_ip(request)
    if is_blocked(ip):
        raise HTTPException(status_code=429, detail="Too many attempts, please try later")
    if len(body.username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
    if len(body.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    if body.email and not _EMAIL_RE.match(body.email):
        raise HTTPException(status_code=400, detail="Invalid email address")
    if body.website:
        # Honeypot tripped — silently pretend success without creating an account.
        logger.info("Registration honeypot triggered from %s (username=%s)", ip, body.username)
        return {"message": "Registration submitted, awaiting admin approval", "status": "pending"}

    if username_exists(body.username):
        raise HTTPException(status_code=409, detail="Username already taken")

    user_id = generate_user_id()
    create_user(user_id, body.username, body.email, hash_password(body.password))

    from server.services.email import send_admin_notification
    approve_url = "https://www.mathlearnlab.cn/admin"
    # Send asynchronously and never let SMTP failure fail the registration.
    try:
        await run_in_threadpool(
            send_admin_notification,
            subject=f"Math Museum - New Registration: {body.username}",
            body=f"<h3>New User Registration</h3><p>Username: {body.username}</p><p>Email: {body.email}</p><p>ID: {user_id}</p><p>Review at: <a href=\"{approve_url}\">{approve_url}</a></p>",
        )
    except Exception:
        logger.exception("Admin notification email failed for user %s", user_id)

    return {
        "message": "Registration submitted, awaiting admin approval",
        "status": "pending",
    }


@router.post("/api/auth/login")
async def login(body: LoginRequest, request: Request):
    ip = _client_ip(request)
    if is_blocked(ip):
        raise HTTPException(status_code=429, detail="Too many attempts, please try later")
    row = get_user_by_username(body.username)

    if row is None or not verify_password(body.password, row["password_hash"]):
        record_failure(ip)
        raise HTTPException(status_code=401, detail="Invalid username or password")

    status = row.get("status", "active")
    if status == "pending":
        record_failure(ip)
        raise HTTPException(status_code=403, detail="Account is pending admin approval")
    if status == "rejected":
        record_failure(ip)
        raise HTTPException(status_code=403, detail="Account registration was rejected")

    record_success(ip)
    token = create_access_token(row["id"], row["username"])
    return {
        "token": token,
        "user": {"id": row["id"], "username": row["username"], "email": row["email"]},
    }


@router.get("/api/auth/me")
async def me(user: dict = Depends(require_user)):
    row = get_user_by_id(user["user_id"])
    if row is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": row["id"],
        "username": row["username"],
        "email": row["email"],
    }


@router.post("/api/auth/forgot-password")
async def forgot_password(body: ForgotPasswordRequest, request: Request):
    """Email a one-time reset link if the address belongs to a registered user.

    Always returns the same message to avoid user enumeration; rate-limited
    per IP like the other auth endpoints.
    """
    ip = _client_ip(request)
    if is_blocked(ip):
        raise HTTPException(status_code=429, detail="Too many attempts, please try later")
    if not body.email or not _EMAIL_RE.match(body.email):
        raise HTTPException(status_code=400, detail="Invalid email address")

    user = get_user_by_email(body.email)
    if user:
        token = create_reset_token(user["id"])
        cleanup_expired_tokens()
        reset_url = f"https://www.mathlearnlab.cn/reset-password?token={token}"
        try:
            from server.services.email import send_email
            await run_in_threadpool(
                send_email,
                body.email,
                "Math Museum - Password Reset",
                f"<p>你好 {user['username']}，</p>"
                f"<p>请点击以下链接重置你的密码（30 分钟内有效）：</p>"
                f"<p><a href=\"{reset_url}\">{reset_url}</a></p>"
                f"<p>如果这不是你本人的操作，请忽略此邮件。</p>",
            )
        except Exception:
            logger.exception("Password reset email failed for user %s", user["id"])

    return {"message": "如果该邮箱已注册，重置链接已发送至你的邮箱"}


@router.post("/api/auth/reset-password")
async def reset_password(body: ResetPasswordRequest):
    """Reset a password using a one-time token from the reset email."""
    if len(body.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
    user_id = consume_reset_token(body.token)
    if user_id is None:
        raise HTTPException(status_code=400, detail="重置链接无效或已过期，请重新申请")
    update_user_password(user_id, hash_password(body.password))
    return {"message": "密码已重置，请使用新密码登录"}


@router.post("/api/auth/refresh")
async def refresh(user: dict = Depends(require_user)):
    """Issue a fresh token for a still-valid session (sliding expiry).

    Requires the current (non-expired) token in the Authorization header;
    returns a new token so active users are not logged out every 24h.
    """
    row = get_user_by_id(user["user_id"])
    if row is None:
        raise HTTPException(status_code=401, detail="User not found")
    token = create_access_token(row["id"], row["username"])
    return {
        "token": token,
        "user": {"id": row["id"], "username": row["username"], "email": row["email"]},
    }
