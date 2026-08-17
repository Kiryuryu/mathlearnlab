"""
Database models and connection for MathLearnLab.
Supports SQLite (default) and MySQL via DATABASE_URL env var.

Conventions
-----------
- `get_db()` returns a thread-cached connection (one per thread, reused).
  Callers MUST NOT call `conn.close()` on it — that poisons the cached
  connection for every later request on the same thread. Use `db_session()`
  for a safe transactional context instead.
- All queries are parameterized; never interpolate user input into SQL.
"""

import os
import sqlite3
import threading
from pathlib import Path
from contextlib import contextmanager
from server.models.migrations import apply_pending

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "mathlearnlab.db"

# MySQL config (set DATABASE_URL to use MySQL)
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Thread-local connection reuse: one connection per thread (a minimal pool).
_mysql_local = threading.local()


def _get_mysql_conn():
    import pymysql
    url = DATABASE_URL.replace("mysql://", "")
    user_pass, host_db = url.split("@")
    user, password = user_pass.split(":")
    host, db = host_db.split("/")
    raw = pymysql.connect(host=host, user=user, password=password,
                           database=db, charset="utf8mb4",
                           cursorclass=pymysql.cursors.DictCursor)
    # Wrap to provide a SQLite-compatible .execute() / fetchone() / fetchall()
    # interface. Queries are executed lazily (no eager fetchall).
    return _MySQLWrapper(raw)


def _mysql_conn():
    """Get a cached MySQL connection for the current thread, or create one."""
    conn = getattr(_mysql_local, "conn", None)
    if conn is None:
        conn = _get_mysql_conn()
        _mysql_local.conn = conn
    return conn


class _MySQLWrapper:
    def __init__(self, conn):
        self._conn = conn
        self._cursor = None

    def execute(self, sql, params=None):
        # SQLite uses ? placeholders; MySQL uses %s. Only translate the
        # parameter markers, never the SQL structure.
        translated = _translate_placeholders(sql)
        if self._cursor is not None:
            self._cursor.close()
        self._cursor = self._conn.cursor()
        self._cursor.execute(translated, params or ())
        return self

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()

    def commit(self):
        self._conn.commit()

    def close(self):
        if self._cursor is not None:
            self._cursor.close()
        self._conn.close()


def _translate_placeholders(sql: str) -> str:
    """Replace ? placeholders with %s outside of quoted string literals."""
    out = []
    in_single = in_double = False
    i = 0
    while i < len(sql):
        ch = sql[i]
        if ch == "'" and not in_double:
            in_single = not in_single
            out.append(ch)
        elif ch == '"' and not in_single:
            in_double = not in_double
            out.append(ch)
        elif ch == "?" and not in_single and not in_double:
            out.append("%s")
        elif ch == "\\" and (in_single or in_double) and i + 1 < len(sql):
            # escaped char inside a literal — copy both characters verbatim
            out.append(ch)
            out.append(sql[i + 1])
            i += 1
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def get_db():
    """Get a (thread-cached) database connection: MySQL if configured, else SQLite."""
    if DATABASE_URL:
        return _mysql_conn()
    conn = getattr(_mysql_local, "sqlite", None)
    if conn is None:
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        # Avoid immediate "database is locked" errors under concurrent writes.
        conn.execute("PRAGMA busy_timeout=5000")
        _mysql_local.sqlite = conn
    return conn


@contextmanager
def db_session():
    """Transactional context. Commits on success; rolls back on exception.

    The underlying connection is thread-cached and reused — never closed here.
    """
    conn = get_db()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise


def init_db():
    """Create tables and apply pending schema migrations (idempotent)."""
    if DATABASE_URL:
        # MySQL: tables already created via schema.sql; migrations are manual.
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
            -- AI-generated practice problems (replaces JSON files; race-safe).
            CREATE TABLE IF NOT EXISTS generated_problems (
                id            TEXT PRIMARY KEY,
                topic_key     TEXT NOT NULL,
                difficulty    TEXT NOT NULL DEFAULT '',
                problem_json  TEXT NOT NULL,
                created_at    TEXT NOT NULL DEFAULT (datetime('now'))
            );
            CREATE INDEX IF NOT EXISTS idx_gp_topic ON generated_problems(topic_key);
            -- Recent-generation history (used for de-duplication).
            CREATE TABLE IF NOT EXISTS problem_gen_history (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                gen_id     TEXT NOT NULL,
                preview    TEXT NOT NULL DEFAULT '',
                topic_key  TEXT NOT NULL,
                difficulty TEXT NOT NULL DEFAULT '',
                ts         REAL NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_pgh_topic ON problem_gen_history(topic_key, ts);
            -- Per-user daily AI call quota (persistent across restarts).
            CREATE TABLE IF NOT EXISTS ai_usage (
                user_id TEXT NOT NULL,
                day     TEXT NOT NULL,
                calls   INTEGER NOT NULL DEFAULT 0,
                PRIMARY KEY (user_id, day)
            );
            -- Password-reset tokens (one-time, expiring).
            CREATE TABLE IF NOT EXISTS password_reset_tokens (
                token_hash TEXT PRIMARY KEY,
                user_id    TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                expires_at TEXT NOT NULL,
                used       INTEGER NOT NULL DEFAULT 0
            );
            CREATE INDEX IF NOT EXISTS idx_prt_user ON password_reset_tokens(user_id);
        """)
        conn.commit()
        apply_pending(conn)
    finally:
        pass  # Connection is thread-cached and reused.
