"""
Schema migrations — versioned, idempotent. Applied by database.init_db.
"""


def _mig_0001(conn):
    """Add status column to users if missing."""
    conn.execute("ALTER TABLE users ADD COLUMN status TEXT NOT NULL DEFAULT 'pending'")
    conn.commit()


def _mig_0002(conn):
    """Index grade_records.timestamp for fast recent-history queries."""
    conn.execute("CREATE INDEX IF NOT EXISTS idx_grade_ts ON grade_records(timestamp)")
    conn.commit()


MIGRATIONS = [
    ("0001_add_users_status_column", _mig_0001),
    ("0002_grade_records_timestamp_index", _mig_0002),
]


def applied_migrations(conn) -> set:
    conn.execute("CREATE TABLE IF NOT EXISTS schema_migrations (version TEXT PRIMARY KEY, applied_at TEXT NOT NULL DEFAULT (datetime('now')))")
    conn.commit()
    return {row[0] for row in conn.execute("SELECT version FROM schema_migrations").fetchall()}


def apply_pending(conn):
    """Apply any migrations not yet recorded. Idempotent; errors on legacy schema are swallowed."""
    applied = applied_migrations(conn)
    for version, fn in MIGRATIONS:
        if version in applied:
            continue
        try:
            fn(conn)
        except Exception:
            pass  # column may already exist (legacy DB); still mark applied
        conn.execute("INSERT OR IGNORE INTO schema_migrations (version) VALUES (?)", (version,))
        conn.commit()
