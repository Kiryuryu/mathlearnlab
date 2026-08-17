"""
Problem storage — SQLite-backed generated problems + generation history.

Replaces the previous JSON-file based storage (data/generated_problems/*.json),
which was vulnerable to read-modify-write races under concurrent requests.
Legacy JSON data is imported into the DB automatically once, idempotently.
"""

import json
import time
from pathlib import Path
from server.models.database import db_session

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
GENERATED_DIR = DATA_DIR / "generated_problems"

# Keep the same retention as the legacy JSON files.
HISTORY_KEEP = 200
PROBLEMS_KEEP = 500

_legacy_import_done = False


def _prune(conn):
    """Trim per-topic history/problems to the retention limits."""
    for row in conn.execute("SELECT DISTINCT topic_key FROM problem_gen_history").fetchall():
        topic = row["topic_key"]
        conn.execute(
            "DELETE FROM problem_gen_history WHERE topic_key = ? AND id NOT IN "
            "(SELECT id FROM problem_gen_history WHERE topic_key = ? ORDER BY ts DESC, id DESC LIMIT ?)",
            (topic, topic, HISTORY_KEEP),
        )
    for row in conn.execute("SELECT DISTINCT topic_key FROM generated_problems").fetchall():
        topic = row["topic_key"]
        conn.execute(
            "DELETE FROM generated_problems WHERE topic_key = ? AND id NOT IN "
            "(SELECT id FROM generated_problems WHERE topic_key = ? ORDER BY created_at DESC, id DESC LIMIT ?)",
            (topic, topic, PROBLEMS_KEEP),
        )


def ensure_legacy_import():
    """One-time import of legacy JSON files into the DB (idempotent)."""
    global _legacy_import_done
    if _legacy_import_done:
        return
    with db_session() as conn:
        count = conn.execute("SELECT COUNT(*) AS c FROM generated_problems").fetchone()["c"]
        if count == 0:
            for topic_file in sorted(GENERATED_DIR.glob("*_problems.json")):
                topic = topic_file.name[: -len("_problems.json")]
                try:
                    problems = json.loads(topic_file.read_text(encoding="utf-8"))
                except Exception:
                    continue
                for p in problems:
                    pid = p.get("id", "")
                    if not pid:
                        continue
                    conn.execute(
                        "INSERT OR IGNORE INTO generated_problems (id, topic_key, difficulty, problem_json) "
                        "VALUES (?, ?, ?, ?)",
                        (pid, topic, p.get("difficulty", ""), json.dumps(p, ensure_ascii=False)),
                    )
            for hist_file in sorted(GENERATED_DIR.glob("*.json")):
                if hist_file.name.endswith("_problems.json"):
                    continue
                topic = hist_file.stem
                try:
                    entries = json.loads(hist_file.read_text(encoding="utf-8"))
                except Exception:
                    continue
                for h in entries:
                    conn.execute(
                        "INSERT OR IGNORE INTO problem_gen_history (gen_id, preview, topic_key, difficulty, ts) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (h.get("id", ""), h.get("preview", "")[:120], topic,
                         h.get("difficulty", ""), h.get("ts", 0.0)),
                    )
    _legacy_import_done = True


def persist_problem(problem: dict, topic_key: str):
    """Insert or update a generated problem in the DB."""
    pid = problem.get("id", "")
    if not pid:
        return
    ensure_legacy_import()
    with db_session() as conn:
        conn.execute(
            """INSERT INTO generated_problems (id, topic_key, difficulty, problem_json)
               VALUES (?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                   difficulty = excluded.difficulty,
                   problem_json = excluded.problem_json""",
            (pid, topic_key, problem.get("difficulty", ""), json.dumps(problem, ensure_ascii=False)),
        )
        _prune(conn)


def record_generated(problem: dict, gen_id: str, topic_key: str, difficulty: str):
    """Record a generation event (for de-duplication)."""
    ensure_legacy_import()
    with db_session() as conn:
        conn.execute(
            "INSERT INTO problem_gen_history (gen_id, preview, topic_key, difficulty, ts) VALUES (?, ?, ?, ?, ?)",
            (problem.get("id", gen_id), problem.get("preview", "")[:120], topic_key, difficulty, time.time()),
        )
        _prune(conn)


def load_recent_history(topic_key: str, n: int = 10) -> list[dict]:
    """Most recent generated previews for a topic (oldest-first, newest-last)."""
    ensure_legacy_import()
    with db_session() as conn:
        rows = conn.execute(
            "SELECT gen_id AS id, preview, topic_key, difficulty, ts FROM problem_gen_history "
            "WHERE topic_key = ? ORDER BY ts DESC, id DESC LIMIT ?",
            (topic_key, n),
        ).fetchall()
    return list(reversed([dict(r) for r in rows]))


def load_problem(topic_key: str, problem_id: str) -> dict | None:
    """Load a single generated problem by topic + id."""
    ensure_legacy_import()
    with db_session() as conn:
        row = conn.execute(
            "SELECT problem_json FROM generated_problems WHERE topic_key = ? AND id = ?",
            (topic_key, problem_id),
        ).fetchone()
    if row is None:
        return None
    try:
        return json.loads(row["problem_json"])
    except Exception:
        return None
