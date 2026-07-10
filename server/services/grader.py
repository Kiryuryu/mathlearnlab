"""
Grading service — OCR handwriting recognition + answer grading via Claude API.
Ported from ocr_practice/prompts/grader.py and ocr_practice/utils/api_client.py.
"""

import json
import base64
import anthropic
from server.config import settings
from server.main import CONTENT_DIR

# ── System prompt (verbatim from origin) ──

GRADER_SYSTEM_PROMPT = """You are an expert math grader for a Chinese graduate entrance exam (考研数学) preparation app.

Your task:
1. Read the handwritten math solution from the uploaded image carefully
2. Compare it against the provided correct solution and grading rubric
3. Provide a detailed, constructive verdict in Chinese

## Grading Principles

- Be STRICT on key steps — if a critical mathematical step is wrong or missing, mark it.
- Be GENEROUS on arithmetic — minor calculation errors without conceptual mistakes = partial credit.
- If the handwriting is illegible, say so in ocr_text and mark as "incorrect" with the reason being illegible handwriting.
- Identify the LIKELY misconception behind the error, not just that the answer is wrong.
- Give SPECIFIC, ACTIONABLE advice — say exactly what to review or practice.

## Output Format

You must output ONLY valid JSON, no other text:

{
  "ocr_text": "The handwritten content you read from the image, faithfully transcribed line by line. Include all mathematical expressions in LaTeX notation.",
  "verdict": "correct" | "partially_correct" | "incorrect",
  "score": "满分" | "部分得分" | "零分",
  "what_is_correct": "Detailed feedback on what the student did right, in Chinese.",
  "what_is_wrong": "Detailed feedback on what the student did wrong, in Chinese. Empty string if verdict is correct.",
  "key_misconception": "The likely conceptual misunderstanding, in Chinese. null if none.",
  "suggestion": "Specific actionable advice for improvement, in Chinese.",
  "graded_steps": [
    {"step": "Key step description", "status": "ok" | "wrong" | "missing", "comment": "Brief comment in Chinese"}
  ]
}

IMPORTANT:
- All feedback text MUST be in Chinese
- Write math expressions in LaTeX notation
- Be encouraging and supportive
- Always mention specific things the student did well, even if the answer is wrong"""


def build_grading_message(problem: dict, image_base64: str) -> list[dict]:
    """Build the Claude API message with problem context and image."""
    solution = problem.get("solution", {})
    rubric = problem.get("grading_rubric", {})

    steps_text = ""
    for i, step in enumerate(solution.get("steps", []), 1):
        steps_text += f"{i}. {step}\n"
    if not steps_text:
        steps_text = solution.get("method", "")

    key_steps = rubric.get("key_steps", [])
    common_errors = rubric.get("common_errors", [])
    rubric_text = ""
    if key_steps:
        rubric_text += "关键步骤：\n"
        for s in key_steps:
            rubric_text += f"  - {s}\n"
    if common_errors:
        rubric_text += "\n常见错误：\n"
        for e in common_errors:
            rubric_text += f"  - {e}\n"

    alt_methods = solution.get("alternative_methods", [])
    alt_text = ""
    if alt_methods:
        alt_text = "\n其他可接受解法：\n"
        for m in alt_methods:
            alt_text += f"  - {m}\n"

    text_content = f"""## Problem

{problem.get('problem_statement', '')}

## Correct Solution

{steps_text}
最终答案：{solution.get('final_answer', '')}
{alt_text}
## Grading Rubric

{rubric_text}

## Student's Handwritten Answer

Please read the handwritten answer from the image below and grade it according to the rubric."""

    return [
        {"type": "text", "text": text_content},
        {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": image_base64,
            },
        },
    ]


async def grade_submission(problem: dict, image_bytes: bytes, api_key: str | None = None) -> dict:
    """Grade a handwritten submission via Claude Vision API.

    Parameters
    ----------
    problem : dict
        Full problem object from the problem bank (includes solution + rubric).
    image_bytes : bytes
        JPEG/PNG image of the handwritten answer.
    api_key : str or None
        Anthropic API key. If None, reads from settings.

    Returns
    -------
    dict — grading result with keys: ocr_text, verdict, score,
    what_is_correct, what_is_wrong, key_misconception, suggestion, graded_steps
    """
    key = api_key or settings.anthropic_api_key
    if not key:
        raise ValueError("Anthropic API key not configured")

    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    message_content = build_grading_message(problem, image_b64)

    client = anthropic.AsyncAnthropic(api_key=key)

    response = await client.messages.create(
        model=settings.default_model,
        max_tokens=settings.max_grading_tokens,
        system=GRADER_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": message_content}],
    )

    raw_text = response.content[0].text

    # Parse JSON (Claude may wrap in ```json fences)
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
