"""
Anthropic API client wrapper for OCR practice app.
"""

import json
import base64
import anthropic
from ocr_practice.config import MODEL_ID, MAX_GRADING_TOKENS


def get_client(api_key: str) -> anthropic.Anthropic:
    """Create an Anthropic client with the given API key."""
    return anthropic.Anthropic(api_key=api_key)


def grade_submission(problem: dict, image_bytes: bytes, api_key: str) -> dict:
    """Send problem + handwritten answer image to Claude for OCR + grading.

    Parameters
    ----------
    problem : dict
        Problem JSON with statement, solution, grading_rubric.
    image_bytes : bytes
        JPEG/PNG image of the handwritten answer.
    api_key : str
        Anthropic API key.

    Returns
    -------
    dict with keys: ocr_text, verdict, score, what_is_correct,
    what_is_wrong, key_misconception, suggestion, graded_steps
    """
    from ocr_practice.prompts.grader import SYSTEM_PROMPT, build_grading_message

    client = get_client(api_key)
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=MAX_GRADING_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": build_grading_message(problem, image_b64),
        }],
    )

    # Parse JSON from response
    raw_text = response.content[0].text

    # Claude might wrap JSON in ```json ... ``` fences
    if "```json" in raw_text:
        raw_text = raw_text.split("```json")[1].split("```")[0]
    elif "```" in raw_text:
        raw_text = raw_text.split("```")[1].split("```")[0]

    try:
        result = json.loads(raw_text.strip())
    except json.JSONDecodeError:
        # Fallback: return raw text as feedback
        result = {
            "ocr_text": "",
            "verdict": "unknown",
            "score": "无法判定",
            "what_is_correct": "",
            "what_is_wrong": "",
            "key_misconception": None,
            "suggestion": raw_text.strip(),
            "graded_steps": [],
        }

    return result


def generate_problems(topic_zh: str, knowledge_area: str, count: int,
                      difficulty: str, api_key: str) -> list[dict]:
    """Ask Claude to generate new practice problems for a topic.

    Parameters
    ----------
    topic_zh : str
        Topic name in Chinese, e.g. "积分学".
    knowledge_area : str
        Specific area, e.g. "定积分换元法".
    count : int
        Number of problems to generate.
    difficulty : str
        "easy", "medium", "hard".
    api_key : str
        Anthropic API key.

    Returns
    -------
    list[dict] — list of problem dicts matching the problem bank schema.
    """
    from ocr_practice.prompts.problem_generator import (
        SYSTEM_PROMPT, build_generation_message,
    )
    from ocr_practice.config import MAX_PROBLEM_GENERATION_TOKENS

    client = get_client(api_key)

    response = client.messages.create(
        model=MODEL_ID,
        max_tokens=MAX_PROBLEM_GENERATION_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": build_generation_message(topic_zh, knowledge_area, count, difficulty),
        }],
    )

    raw_text = response.content[0].text

    # Parse JSON array
    if "```json" in raw_text:
        raw_text = raw_text.split("```json")[1].split("```")[0]
    elif "```" in raw_text:
        raw_text = raw_text.split("```")[1].split("```")[0]

    try:
        problems = json.loads(raw_text.strip())
        if isinstance(problems, dict):
            problems = problems.get("problems", [])
    except json.JSONDecodeError:
        problems = []

    return problems
