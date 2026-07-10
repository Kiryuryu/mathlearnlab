"""
Problem bank loader for OCR practice app.

Loads problems from JSON files, supports filtering and random selection.
"""

import json
import random
from pathlib import Path

PROBLEM_BANK_DIR = Path(__file__).parent.parent / "problem_bank"


def _load_json(filename: str) -> dict:
    """Load a problem bank JSON file."""
    filepath = PROBLEM_BANK_DIR / filename
    if not filepath.exists():
        return {"problems": []}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(filename: str, data: dict):
    """Save a problem bank JSON file."""
    filepath = PROBLEM_BANK_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_problems(topic_key: str) -> list[dict]:
    """Load all problems for a topic."""
    from ocr_practice.config import TOPICS
    topic = TOPICS.get(topic_key, {})
    filename = topic.get("json", f"{topic_key}.json")
    data = _load_json(filename)
    return data.get("problems", [])


def get_problem(topic_key: str, problem_id: str) -> dict | None:
    """Get a specific problem by ID."""
    problems = load_problems(topic_key)
    for p in problems:
        if p.get("id") == problem_id:
            return p
    return None


def get_random_problem(topic_key: str, difficulty: str = None) -> dict | None:
    """Get a random problem, optionally filtered by difficulty."""
    problems = load_problems(topic_key)
    if not problems:
        return None
    if difficulty:
        problems = [p for p in problems if p.get("difficulty") == difficulty]
        if not problems:
            return None
    return random.choice(problems)


def list_problem_summaries(topic_key: str) -> list[dict]:
    """Return a summary list for the problem picker."""
    problems = load_problems(topic_key)
    return [
        {
            "id": p.get("id", "?"),
            "difficulty": p.get("difficulty_label_zh", ""),
            "knowledge_points": p.get("knowledge_points", []),
            "preview": (p.get("problem_statement", "") or "")[:80] + "...",
        }
        for p in problems
    ]


def save_problems(topic_key: str, new_problems: list[dict], append: bool = True):
    """Save problems to a topic JSON file.

    Parameters
    ----------
    topic_key : str
    new_problems : list[dict]
    append : bool
        If True, append to existing. If False, replace.
    """
    from ocr_practice.config import TOPICS
    topic = TOPICS.get(topic_key, {})
    filename = topic.get("json", f"{topic_key}.json")

    if append:
        data = _load_json(filename)
        existing_ids = {p["id"] for p in data.get("problems", [])}
        for p in new_problems:
            if p.get("id") not in existing_ids:
                data.setdefault("problems", []).append(p)
                existing_ids.add(p["id"])
    else:
        data = {"problems": new_problems}

    _save_json(filename, data)


def count_problems(topic_key: str) -> int:
    """Return the number of problems for a topic."""
    return len(load_problems(topic_key))
