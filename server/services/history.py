"""
Grade history service — save and query grading results (SQLite-backed, per-user).
"""

import json
from server.models.database import get_db, db_session


def save_grade(user_id: str, topic_key: str, problem_id: str,
               problem_statement: str, solution_steps: list[str], final_answer: str,
               grading_result: dict):
    """Append a grading result to history for a specific user."""
    conn = get_db()
    conn.execute(
        """INSERT INTO grade_records
           (user_id, topic_key, problem_id, problem_statement, solution_steps,
            final_answer, verdict, score, ocr_text, what_is_correct, what_is_wrong, suggestion)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            user_id,
            topic_key,
            problem_id,
            problem_statement,
            json.dumps(solution_steps, ensure_ascii=False),
            final_answer,
            grading_result.get("verdict", "unknown"),
            grading_result.get("score", ""),
            grading_result.get("ocr_text", ""),
            grading_result.get("what_is_correct", ""),
            grading_result.get("what_is_wrong", ""),
            grading_result.get("suggestion", ""),
        ),
    )
    conn.commit()
    conn.close()


def get_stats(user_id: str) -> dict:
    """Compute overall stats for a user."""
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) as c FROM grade_records WHERE user_id = ?", (user_id,)).fetchone()["c"]
    if total == 0:
        conn.close()
        return {"total": 0, "correct": 0, "partial": 0, "incorrect": 0, "accuracy": 0.0, "by_topic": {}}

    correct = conn.execute(
        "SELECT COUNT(*) as c FROM grade_records WHERE user_id = ? AND verdict = 'correct'", (user_id,)
    ).fetchone()["c"]
    partial = conn.execute(
        "SELECT COUNT(*) as c FROM grade_records WHERE user_id = ? AND verdict = 'partially_correct'", (user_id,)
    ).fetchone()["c"]
    incorrect = conn.execute(
        "SELECT COUNT(*) as c FROM grade_records WHERE user_id = ? AND verdict = 'incorrect'", (user_id,)
    ).fetchone()["c"]

    rows = conn.execute(
        "SELECT topic_key, COUNT(*) as total, SUM(CASE WHEN verdict='correct' THEN 1 ELSE 0 END) as correct "
        "FROM grade_records WHERE user_id = ? GROUP BY topic_key", (user_id,)
    ).fetchall()
    by_topic = {r["topic_key"]: {"total": r["total"], "correct": r["correct"]} for r in rows}

    conn.close()
    return {
        "total": total,
        "correct": correct,
        "partial": partial,
        "incorrect": incorrect,
        "accuracy": round(correct / total * 100, 1) if total > 0 else 0.0,
        "by_topic": by_topic,
    }


def get_recent(user_id: str, n: int = 10) -> list[dict]:
    """Get recent grade records for a user."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM grade_records WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?",
        (user_id, n),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_errors(user_id: str) -> list[dict]:
    """Return problems with incorrect or partial verdicts."""
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM grade_records WHERE user_id = ? AND verdict IN ('incorrect', 'partially_correct') "
        "ORDER BY timestamp DESC LIMIT 200",
        (user_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
