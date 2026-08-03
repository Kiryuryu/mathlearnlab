"""
Grading service — OCR handwriting recognition + answer grading via DeepSeek API.
Ported from ocr_practice/prompts/grader.py and ocr_practice/utils/api_client.py.
"""

import json
import base64
from server.config import settings
from server.services.deepseek import chat_completion
from server.services.prompts import GRADER_SYSTEM_PROMPT, build_grading_message


async def grade_submission(problem: dict, image_bytes: bytes, api_key: str | None = None) -> dict:
    """Grade a handwritten submission via Claude Vision API.

    Parameters
    ----------
    problem : dict
        Full problem object from the problem bank (includes solution + rubric).
    image_bytes : bytes
        JPEG/PNG image of the handwritten answer.
    api_key : str or None
        DeepSeek API key. If None, reads from settings.

    Returns
    -------
    GradingResult — dict with keys: ocr_text, verdict, score,
    what_is_correct, what_is_wrong, key_misconception, suggestion, graded_steps
    """
    key = api_key or settings.deepseek_api_key
    if not key:
        raise ValueError("API key not configured")

    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    message_content = build_grading_message(problem, image_b64)

    response = await chat_completion(
        [{"role": "system", "content": GRADER_SYSTEM_PROMPT}, {"role": "user", "content": message_content}],
        api_key=api_key,
        max_tokens=settings.max_grading_tokens,
    )

    raw_text = response.choices[0].message.content

    # Parse JSON (may wrap in ```json fences)
    if "```json" in raw_text:
        raw_text = raw_text.split("```json")[1].split("```")[0]
    elif "```" in raw_text:
        raw_text = raw_text.split("```")[1].split("```")[0]

    try:
        result = json.loads(raw_text.strip())
    except json.JSONDecodeError:
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
