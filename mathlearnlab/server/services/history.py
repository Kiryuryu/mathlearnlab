"""
Grade history service — save and query grading results.
Ported from ocr_practice/utils/history.py.
"""

import json
from pathlib import Path
from datetime import datetime, timezone, timedelta
from server.main import DATA_DIR

HISTORY_FILE = DATA_DIR / "grade_history" / "history.json"
CST = timezone(timedelta(hours=8))


def _ensure_file():
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not HISTORY_FILE.exists():
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def _load() -> list[dict]:
    _ensure_file()
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_grade(topic_key: str, problem_id: str, problem_statement: str,
               solution_steps: list[str], final_answer: str,
               grading_result: dict):
    """Append a grading result to history."""
    _ensure_file()
    history = _load()

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
    # Keep last 500 entries
    if len(history) > 500:
        history = history[-500:]

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def get_stats() -> dict:
    """Compute overall stats."""
    history = _load()
    total = len(history)
    if total == 0:
        return {"total": 0, "correct": 0, "partial": 0, "incorrect": 0, "accuracy": 0.0, "by_topic": {}}

    correct = sum(1 for h in history if h.get("verdict") == "correct")
    partial = sum(1 for h in history if h.get("verdict") == "partially_correct")
    incorrect = sum(1 for h in history if h.get("verdict") == "incorrect")

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


def get_recent(n: int = 10) -> list[dict]:
    history = _load()
    return history[-n:][::-1]
