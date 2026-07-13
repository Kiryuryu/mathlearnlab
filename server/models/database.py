"""
Database models and connection for MathLearnLab.
Uses SQLite for simplicity — single-file, zero-config deployment.
"""

import sqlite3
from pathlib import Path

# Resolve DATA_DIR without importing main (avoid circular import)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "mathlearnlab.db"


def get_db() -> sqlite3.Connection:
    """Get a SQLite connection with row factory for dict-like access."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


from contextlib import contextmanager

@contextmanager
def db_session():
    conn = get_db()
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Create tables if they don't exist."""
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id          TEXT PRIMARY KEY,
            username    TEXT NOT NULL UNIQUE,
            email       TEXT NOT NULL DEFAULT '',
            password_hash TEXT NOT NULL,
            created_at  TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS grade_records (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       TEXT NOT NULL,
            timestamp     TEXT NOT NULL DEFAULT (datetime('now')),
            topic_key     TEXT NOT NULL,
            problem_id    TEXT NOT NULL,
            problem_statement TEXT NOT NULL DEFAULT '',
            solution_steps   TEXT NOT NULL DEFAULT '[]',
            final_answer     TEXT NOT NULL DEFAULT '',
            verdict       TEXT NOT NULL DEFAULT 'unknown',
            score         TEXT NOT NULL DEFAULT '',
            ocr_text      TEXT NOT NULL DEFAULT '',
            what_is_correct TEXT NOT NULL DEFAULT '',
            what_is_wrong  TEXT NOT NULL DEFAULT '',
            suggestion    TEXT NOT NULL DEFAULT '',
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE INDEX IF NOT EXISTS idx_grade_user ON grade_records(user_id);
        CREATE INDEX IF NOT EXISTS idx_grade_topic ON grade_records(user_id, topic_key);
    """)
    conn.commit()
    conn.close()
