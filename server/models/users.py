"""
User data access — single home for user-related SQL so the routers stay thin
and queries aren't duplicated across auth.py / admin.py.
"""

from server.models.database import db_session


def get_user_by_username(username: str) -> dict | None:
    with db_session() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
    return dict(row) if row else None


def get_user_by_id(user_id: str) -> dict | None:
    with db_session() as conn:
        row = conn.execute(
            "SELECT id, username, email, password_hash, status, created_at "
            "FROM users WHERE id = ?", (user_id,)
        ).fetchone()
    return dict(row) if row else None


def username_exists(username: str) -> bool:
    with db_session() as conn:
        row = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    return row is not None


def create_user(user_id: str, username: str, email: str, password_hash: str, status: str = "pending"):
    with db_session() as conn:
        conn.execute(
            "INSERT INTO users (id, username, email, password_hash, status) VALUES (?, ?, ?, ?, ?)",
            (user_id, username, email, password_hash, status),
        )


def list_users(status: str | None = None, limit: int = 50) -> list[dict]:
    with db_session() as conn:
        if status is None or status == "all":
            rows = conn.execute(
                "SELECT id, username, email, status, created_at FROM users ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, username, email, status, created_at FROM users "
                "WHERE status = ? ORDER BY created_at DESC LIMIT ?",
                (status, limit),
            ).fetchall()
    return [dict(r) for r in rows]


def update_user_status(user_id: str, status: str):
    with db_session() as conn:
        conn.execute("UPDATE users SET status = ? WHERE id = ?", (status, user_id))
