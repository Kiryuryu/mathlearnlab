"""
Auth utilities — password hashing (hashlib pbkdf2), JWT token creation/verification.
"""

import uuid
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from server.config import settings

CST = timezone(timedelta(hours=8))

# ── Password hashing (PBKDF2-SHA256, no external deps) ──

HASH_ITERATIONS = 600000  # OWASP recommended for PBKDF2-SHA256


def hash_password(password: str) -> str:
    """Hash password with PBKDF2-SHA256. Returns '$pbkdf2-sha256$iterations$salt$hash'."""
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("ascii"), HASH_ITERATIONS)
    return f"$pbkdf2-sha256${HASH_ITERATIONS}${salt}${dk.hex()}"


def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against pbkdf2 hash."""
    try:
        _, algo, iterations, salt, expected = hashed.split("$")
        if algo != "pbkdf2-sha256":
            return False
        dk = hashlib.pbkdf2_hmac("sha256", plain.encode("utf-8"), salt.encode("ascii"), int(iterations), dklen=32)
        return secrets.compare_digest(dk.hex(), expected)
    except Exception:
        return False


# ── JWT ──


def create_access_token(user_id: str, username: str) -> str:
    expire = datetime.now(CST) + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {
        "sub": user_id,
        "username": username,
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None


def generate_user_id() -> str:
    return uuid.uuid4().hex[:16]
