"""
Problem bank service — load/save problems from JSON files.
Ported from ocr_practice/utils/problem_loader.py.
"""

import json
import random
from pathlib import Path
from server.config import settings

# Avoid circular import — resolve DATA_DIR directly
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
PROBLEM_BANK_DIR = DATA_DIR / "problem_bank"


DIFFICULTY_MAP = {
    "easy": "basic", "medium": "exam", "hard": "graduate",
    "basic": "basic", "advanced": "advanced", "exam": "exam",
    "graduate": "graduate", "phd": "phd",
}

def _normalize_difficulty(diff: str) -> str:
    return DIFFICULTY_MAP.get(diff, diff)


def _load_json(filename: str) -> dict:
    filepath = PROBLEM_BANK_DIR / filename
    if not filepath.exists():
        return {"problems": []}
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Normalize difficulty labels from old system (easy/medium/hard) to new
    for p in data.get("problems", []):
        if "difficulty" in p:
            p["difficulty"] = _normalize_difficulty(p["difficulty"])
    return data


def load_problems(topic_key: str) -> list[dict]:
    """Load all problems for a topic."""
    exhibit = settings.exhibits.get(topic_key, {})
    filename = exhibit.get("json", f"{topic_key}.json")
    return _load_json(filename).get("problems", [])


def get_problem(topic_key: str, problem_id: str) -> dict | None:
    """Get a specific problem by ID (full details including solution)."""
    for p in load_problems(topic_key):
        if p.get("id") == problem_id:
            return p
    return None


def get_random_problem(topic_key: str, difficulty: str | None = None) -> dict | None:
    """Get a random problem, optionally filtered by difficulty."""
    problems = load_problems(topic_key)
    if not problems:
        return None
    if difficulty and difficulty != "all":
        problems = [p for p in problems if p.get("difficulty") == difficulty]
        if not problems:
            return None
    return random.choice(problems)


def list_problem_summaries(topic_key: str, difficulty: str | None = None) -> list[dict]:
    """Return summary list (no solutions) for the problem picker."""
    problems = load_problems(topic_key)
    if difficulty and difficulty != "all":
        problems = [p for p in problems if p.get("difficulty") == difficulty]
    return [
        {
            "id": p.get("id", "?"),
            "difficulty": p.get("difficulty", "medium"),
            "difficulty_label_zh": p.get("difficulty_label_zh", ""),
            "knowledge_points": p.get("knowledge_points", []),
            "preview": (p.get("problem_statement", "") or "")[:120] + "...",
            "problem_type": (p.get("metadata") or {}).get("problem_type", "计算题"),
        }
        for p in problems
    ]


def count_problems(topic_key: str) -> int:
    return len(load_problems(topic_key))
