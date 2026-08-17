"""
Schema migrations — versioned, idempotent. Applied by database.init_db.

Each migration must be safe to run on an existing legacy schema (e.g. check
for column existence before ALTER TABLE). Failures are logged and re-raised
so a broken migration is never silently marked as applied.
"""

import logging

logger = logging.getLogger(__name__)


def _column_exists(conn, table: str, column: str) -> bool:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(r["name"] == column for r in rows)


def _mig_0001(conn):
    """Add status column to users if missing."""
    if not _column_exists(conn, "users", "status"):
        conn.execute("ALTER TABLE users ADD COLUMN status TEXT NOT NULL DEFAULT 'pending'")


def _mig_0002(conn):
    """Index grade_records.timestamp for fast recent-history queries."""
    conn.execute("CREATE INDEX IF NOT EXISTS idx_grade_ts ON grade_records(timestamp)")


MIGRATIONS = [
    ("0001_add_users_status_column", _mig_0001),
    ("0002_grade_records_timestamp_index", _mig_0002),
]


def applied_migrations(conn) -> set:
    conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version TEXT PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT (datetime('now')))")
    conn.commit()
    return {row[0] for row in conn.execute("SELECT version FROM schema_migrations").fetchall()}


def apply_pending(conn):
    """Apply any migrations not yet recorded. Idempotent.

    Migrations themselves are written to be safe on legacy schemas, so a
    raised exception here is a real failure and must surface — swallowing it
    could leave the DB half-migrated while the version is marked applied.
    """
    applied = applied_migrations(conn)
    for version, fn in MIGRATIONS:
        if version in applied:
            continue
        try:
            fn(conn)
        except Exception:
            logger.exception("Migration %s failed; not marking as applied", version)
            raise
        conn.execute("INSERT OR IGNORE INTO schema_migrations (version) VALUES (?)", (version,))
    conn.commit()
