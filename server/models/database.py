"""
Database models and connection for MathLearnLab.
Supports SQLite (default) and MySQL via DATABASE_URL env var.
"""

import os
import sqlite3
from pathlib import Path
from contextlib import contextmanager

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "mathlearnlab.db"

# MySQL config (set DATABASE_URL to use MySQL)
DATABASE_URL = os.getenv("DATABASE_URL", "")


def _get_mysql_conn():
    import pymysql
    url = DATABASE_URL.replace("mysql://", "")
    user_pass, host_db = url.split("@")
    user, password = user_pass.split(":")
    host, db = host_db.split("/")
    raw = pymysql.connect(host=host, user=user, password=password,
                           database=db, charset="utf8mb4",
                           cursorclass=pymysql.cursors.DictCursor)
    # Wrap to provide SQLite-compatible .execute() and .commit() interface
    return _MySQLWrapper(raw)


class _MySQLWrapper:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = conn.cursor()
        self.row_factory = None  # dummy for compat

    def execute(self, sql, params=None):
        self._cursor.execute(sql.replace("?", "%s"), params or ())
        self._cursor._rows = list(self._cursor.fetchall())
        return self

    def fetchone(self):
        return self._cursor._rows[0] if self._cursor._rows else None

    def fetchall(self):
        return self._cursor._rows

    def commit(self):
        self._conn.commit()

    def close(self):
        self._cursor.close()
        self._conn.close()


def get_db():
    """Get a database connection (MySQL if configured, else SQLite)."""
    if DATABASE_URL:
        return _get_mysql_conn()
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


@contextmanager
def db_session():
    conn = get_db()
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Create tables if they don't exist."""
    if DATABASE_URL:
        # MySQL: tables already created via schema.sql
        return
    conn = get_db()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id          TEXT PRIMARY KEY,
                username    TEXT NOT NULL UNIQUE,
                email       TEXT NOT NULL DEFAULT '',
                password_hash TEXT NOT NULL,
                status      TEXT NOT NULL DEFAULT 'pending',
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
        # Migration: add status column if missing (for existing DBs)
        try:
            conn.execute("ALTER TABLE users ADD COLUMN status TEXT NOT NULL DEFAULT 'pending'")
            conn.commit()
        except Exception:
            pass  # column already exists
    finally:
        conn.close()
