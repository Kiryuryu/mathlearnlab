"""
Daily Problem API — one AI-generated problem per calendar day (cached on disk).
Uses the server's DeepSeek key, so no user login/API key required.
"""

import json
import random
import string
from datetime import date
from pathlib import Path
from fastapi import APIRouter
from server.config import DATA_DIR, settings
from server.services.deepseek import chat_completion
from server.services.practice_service import build_generate_prompt, extract_json

router = APIRouter()

DAILY_DIR = DATA_DIR / "daily"
DAILY_DIR.mkdir(parents=True, exist_ok=True)

_DAILY_PROMPT = """请出一道适合大学生/数学爱好者的题目，难度为四星或以上（满分五星）。
要求：有相当的思考深度，需要综合运用概念或巧妙的数学技巧，不要出 1-2 步就能解出的简单题。
从以下主题中选一个：极限、导数、积分、无穷级数、多元微积分。

请用 JSON 格式输出：
{{
  "topic": "主题名（中文）",
  "knowledge_points": ["知识点1", "知识点2"],
  "problem_statement": "完整的题目描述，用 LaTeX 语法写数学公式",
  "preview": "题目简短预览（80字以内）",
  "solution": {{
    "method": "解题思路概述",
    "steps": ["步骤1的详细描述", "步骤2的详细描述", "步骤3的详细描述"],
    "final_answer": "最终答案，LaTeX 格式"
  }}
}}

只输出 JSON，不要其他内容。确保 problem_statement 使用正确的 LaTeX 语法（$...$ 或 $$...$$）。"""


def _daily_path(d: str) -> Path:
    return DAILY_DIR / f"{d}.json"


def _load_cached(d: str) -> dict | None:
    p = _daily_path(d)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def _save(d: str, data: dict):
    _daily_path(d).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


@router.get("/api/daily/problem")
async def daily_problem():
    """Return today's AI-generated problem (cached per day)."""
    today = date.today().isoformat()  # server-local date

    cached = _load_cached(today)
    if cached and not cached.get("_error"):
        return {"problem": cached, "generated": False, "date": today}

    key = settings.deepseek_api_key
    if not key:
        # Graceful fallback if no API key configured
        return {"error": "AI not configured", "date": today}

    gen_id = "DAILY-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    prompt = _DAILY_PROMPT

    try:
        response = await chat_completion(
            [{"role": "user", "content": prompt}],
            api_key=key,
            max_tokens=1500,
            json_mode=True,
        )
        problem = extract_json(response.choices[0].message.content)
        problem["id"] = gen_id
        _save(today, problem)
        return {"problem": problem, "generated": True, "date": today}
    except Exception as e:
        # Cache the error briefly so we don't hammer the AI API on every refresh.
        _save(today, {"_error": True, "_msg": str(e)[:200]})
        return {"error": "AI generation failed, will retry tomorrow", "date": today}
