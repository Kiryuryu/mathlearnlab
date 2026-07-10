"""
Grader prompt template for OCR + math answer grading.

This is the most quality-critical file. The system prompt sets the
grading persona, output format, and grading principles.
"""

SYSTEM_PROMPT = """You are an expert math grader for a Chinese graduate entrance exam (考研数学) preparation app.

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

```json
{
  "ocr_text": "The handwritten content you read from the image, faithfully transcribed line by line. Include all mathematical expressions in LaTeX notation.",
  "verdict": "correct" | "partially_correct" | "incorrect",
  "score": "满分" | "部分得分" | "零分",
  "what_is_correct": "Detailed feedback on what the student did right, in Chinese. Be specific about which steps are correct.",
  "what_is_wrong": "Detailed feedback on what the student did wrong, in Chinese. Quote specific parts of their work. Empty string if verdict is 'correct'.",
  "key_misconception": "The likely conceptual misunderstanding revealed by the error, in Chinese. Write null if there is no clear misconception.",
  "suggestion": "Specific actionable advice for improvement, in Chinese. Mention which concepts or problem types to practice.",
  "graded_steps": [
    {"step": "Description of key step 1", "status": "ok" | "wrong" | "missing", "comment": "Brief comment in Chinese"}
  ]
}
```

IMPORTANT:
- All feedback text MUST be in Chinese
- Write math expressions in LaTeX notation within the text (e.g., $\\int_0^\\pi \\sin x \\, dx$)
- Be encouraging and supportive in tone — the student is preparing for an important exam
- Always mention specific things the student did well, even if the answer is wrong
- If the answer uses a different valid method from the standard solution, still mark it correct
"""


def build_grading_message(problem: dict, image_base64: str) -> list[dict]:
    """Build the user message with problem context and image.

    Parameters
    ----------
    problem : dict
        Problem JSON with statement, solution, grading_rubric.
    image_base64 : str
        Base64-encoded image (without the data:image/... prefix).

    Returns
    -------
    list[dict] — Claude API content blocks.
    """
    # Format solution steps
    steps_text = ""
    for i, step in enumerate(problem.get("solution", {}).get("steps", []), 1):
        steps_text += f"{i}. {step}\n"
    if not steps_text:
        steps_text = problem.get("solution", {}).get("method", "无详细步骤")

    final_answer = problem.get("solution", {}).get("final_answer", "")

    # Format rubric
    rubric = problem.get("grading_rubric", {})
    key_steps = rubric.get("key_steps", [])
    common_errors = rubric.get("common_errors", [])

    rubric_text = ""
    if key_steps:
        rubric_text += "关键步骤：\n"
        for s in key_steps:
            rubric_text += f"  • {s}\n"
    if common_errors:
        rubric_text += "\n常见错误：\n"
        for e in common_errors:
            rubric_text += f"  • {e}\n"

    alt_methods = problem.get("solution", {}).get("alternative_methods", [])
    alt_text = ""
    if alt_methods:
        alt_text = "\n## Alternative Solutions (also acceptable)\n"
        for m in alt_methods:
            alt_text += f"  • {m}\n"

    text_content = f"""## Problem

{problem.get('problem_statement', '')}

## Correct Solution

{steps_text}
最终答案：{final_answer}
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
