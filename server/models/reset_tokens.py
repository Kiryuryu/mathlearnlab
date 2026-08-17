"""
Password reset tokens — one-time, expiring, stored as SHA-256 hashes
(so a leaked DB never exposes usable tokens).
"""

import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from server.models.database import db_session

TOKEN_TTL_MINUTES = 30
UTC = timezone.utc


def _hash(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_reset_token(user_id: str) -> str:
    """Create a reset token for the user; returns the raw token (shown once)."""
    token = secrets.token_urlsafe(32)
    expires_at = (datetime.now(UTC) + timedelta(minutes=TOKEN_TTL_MINUTES)).isoformat()
    with db_session() as conn:
        conn.execute(
            "INSERT INTO password_reset_tokens (token_hash, user_id, expires_at) VALUES (?, ?, ?)",
            (_hash(token), user_id, expires_at),
        )
    return token


def consume_reset_token(token: str) -> str | None:
    """Validate + atomically consume a token; returns the user_id, or None."""
    if not token:
        return None
    h = _hash(token)
    with db_session() as conn:
        row = conn.execute(
            "SELECT user_id, expires_at, used FROM password_reset_tokens WHERE token_hash = ?", (h,)
        ).fetchone()
        if row is None or row["used"]:
            return None
        try:
            expires = datetime.fromisoformat(row["expires_at"])
        except ValueError:
            return None
        if expires < datetime.now(UTC):
            return None
        conn.execute("UPDATE password_reset_tokens SET used = 1 WHERE token_hash = ?", (h,))
    return row["user_id"]


def cleanup_expired_tokens():
    """Remove expired/used tokens (cheap housekeeping; called on creation)."""
    with db_session() as conn:
        conn.execute("DELETE FROM password_reset_tokens WHERE expires_at < ? OR used = 1",
                     (datetime.now(UTC).isoformat(),))
