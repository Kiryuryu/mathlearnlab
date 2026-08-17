"""
Rate limiting & AI usage quota.

- Auth endpoints: in-memory sliding-window failure tracking per IP.
  (In-memory is a deliberate trade-off: it resets on restart and is per-process.
  For a multi-worker deployment, front this with nginx limit_req.)
- AI endpoints: per-user per-day call quota, persisted in SQLite (ai_usage),
  so it survives restarts and is shared across workers.
"""

import time
from datetime import datetime
from server.config import settings
from server.models.auth import CST
from server.models.database import db_session

# {ip: [timestamps]}
_attempts: dict[str, list[float]] = {}
_WINDOW = 300  # 5 minutes
_MAX_ATTEMPTS = 10


def today_cst() -> str:
    """Current date in China Standard Time (UTC+8), as ISO string."""
    return datetime.now(CST).date().isoformat()


def is_blocked(ip: str) -> bool:
    now = time.time()
    timestamps = _attempts.get(ip, [])
    timestamps = [t for t in timestamps if now - t < _WINDOW]
    _attempts[ip] = timestamps
    return len(timestamps) >= _MAX_ATTEMPTS


def record_failure(ip: str):
    now = time.time()
    timestamps = _attempts.get(ip, [])
    timestamps = [t for t in timestamps if now - t < _WINDOW]
    timestamps.append(now)
    _attempts[ip] = timestamps


def record_success(ip: str):
    _attempts.pop(ip, None)


def use_ai_quota(user_id: str, day: str | None = None, limit: int | None = None) -> bool:
    """Atomically consume one AI call for the user.

    Returns True if the call is allowed (and counted), False if the daily
    quota is exhausted. The day defaults to today in CST.
    """
    day = day or today_cst()
    limit = limit if limit is not None else settings.ai_daily_limit
    with db_session() as conn:
        row = conn.execute(
            "SELECT calls FROM ai_usage WHERE user_id = ? AND day = ?", (user_id, day)
        ).fetchone()
        calls = row["calls"] if row else 0
        if calls >= limit:
            return False
        if row:
            conn.execute(
                "UPDATE ai_usage SET calls = calls + 1 WHERE user_id = ? AND day = ?",
                (user_id, day),
            )
        else:
            conn.execute(
                "INSERT INTO ai_usage (user_id, day, calls) VALUES (?, ?, 1)", (user_id, day)
            )
        return True


def ai_quota_left(user_id: str, day: str | None = None, limit: int | None = None) -> int:
    """How many AI calls remain today (>= 0)."""
    day = day or today_cst()
    limit = limit if limit is not None else settings.ai_daily_limit
    with db_session() as conn:
        row = conn.execute(
            "SELECT calls FROM ai_usage WHERE user_id = ? AND day = ?", (user_id, day)
        ).fetchone()
        calls = row["calls"] if row else 0
    return max(0, limit - calls)
