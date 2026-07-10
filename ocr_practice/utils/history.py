"""
Grading history for OCR practice app.

Tracks each submission and provides statistics.
"""

import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

HISTORY_DIR = Path(__file__).parent.parent / "grade_history"
HISTORY_FILE = HISTORY_DIR / "history.json"

# Beijing timezone offset (UTC+8)
CST = timezone(timedelta(hours=8))


def _ensure_history_file():
    """Create history file if it doesn't exist."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    if not HISTORY_FILE.exists():
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def _load_history() -> list[dict]:
    """Load all history entries."""
    _ensure_history_file()
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_grade(topic_key: str, problem_id: str, problem_statement: str,
               solution_steps: list[str], final_answer: str,
               grading_result: dict, image_bytes: bytes | None = None):
    """Append a grading result to the history.

    Parameters
    ----------
    topic_key : str
    problem_id : str
    problem_statement : str
    solution_steps : list[str]
    final_answer : str
    grading_result : dict
        Result from grade_submission().
    image_bytes : bytes or None
        Optionally save a copy of the submitted image.
    """
    _ensure_history_file()
    history = _load_history()

    entry = {
        "timestamp": datetime.now(CST).isoformat(),
        "topic_key": topic_key,
        "problem_id": problem_id,
        "problem_statement": problem_statement,
        "solution_steps": solution_steps,
        "final_answer": final_answer,
        "verdict": grading_result.get("verdict", "unknown"),
        "score": grading_result.get("score", ""),
        "ocr_text": grading_result.get("ocr_text", ""),
        "what_is_correct": grading_result.get("what_is_correct", ""),
        "what_is_wrong": grading_result.get("what_is_wrong", ""),
        "suggestion": grading_result.get("suggestion", ""),
    }

    history.append(entry)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def get_stats() -> dict:
    """Compute overall and per-topic statistics."""
    history = _load_history()
    total = len(history)
    if total == 0:
        return {
            "total": 0,
            "correct": 0,
            "partial": 0,
            "incorrect": 0,
            "accuracy": 0.0,
            "by_topic": {},
        }

    correct = sum(1 for h in history if h.get("verdict") == "correct")
    partial = sum(1 for h in history if h.get("verdict") == "partially_correct")
    incorrect = sum(1 for h in history if h.get("verdict") == "incorrect")

    # By topic
    by_topic = {}
    for h in history:
        tk = h.get("topic_key", "unknown")
        if tk not in by_topic:
            by_topic[tk] = {"total": 0, "correct": 0}
        by_topic[tk]["total"] += 1
        if h.get("verdict") == "correct":
            by_topic[tk]["correct"] += 1

    return {
        "total": total,
        "correct": correct,
        "partial": partial,
        "incorrect": incorrect,
        "accuracy": round(correct / total * 100, 1) if total > 0 else 0.0,
        "by_topic": by_topic,
    }


def get_error_problems() -> list[dict]:
    """Return problems graded as incorrect or partially correct."""
    history = _load_history()
    return [
        h for h in history
        if h.get("verdict") in ("incorrect", "partially_correct")
    ]


def get_recent_attempts(n: int = 10) -> list[dict]:
    """Return the n most recent attempts."""
    history = _load_history()
    return history[-n:][::-1]
