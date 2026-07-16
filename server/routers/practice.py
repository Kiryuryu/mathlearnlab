"""
Practice API — AI-only problem generation with deduplication.
"""

import json
import random
import string
import time
from pathlib import Path
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from server.config import settings
from server.routers.auth import require_user
from openai import AsyncOpenAI

router = APIRouter()

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
GENERATED_DIR = DATA_DIR / "generated_problems"
GENERATED_DIR.mkdir(parents=True, exist_ok=True)


class GenerateRequest(BaseModel):
    topic_key: str
    difficulty: str = "medium"


def _history_path(topic: str) -> Path:
    return GENERATED_DIR / f"{topic}.json"


def _load_history(topic: str) -> list[dict]:
    p = _history_path(topic)
    if not p.exists():
        return []
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return []


def _save_history(topic: str, entries: list[dict]):
    _history_path(topic).write_text(
        json.dumps(entries[-200:], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


@router.post("/api/practice/generate")
async def generate_problem(request: Request, user: dict = Depends(require_user)):
    """Generate a new practice problem via DeepSeek, avoiding recent duplicates."""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    topic_key = body.get("topic_key", "limits")
    difficulty = body.get("difficulty", "exam")

    exhibit = settings.exhibits.get(topic_key, {})
    exhibit_name = exhibit.get("zh", topic_key)
    knowledge_points = exhibit.get("big_question", "")

    diff_guide = {
        "basic": "基础入门题，考察核心概念的直观理解，适合刚学完概念的学生",
        "advanced": "进阶提高题，需要综合运用多个知识点，有适度的技巧性",
        "exam": "考研难度，综合性强，需要灵活运用概念和技巧，对应数学一/二/三难度",
        "graduate": "研究生水平，需要深刻理解概念本质，可能涉及证明或构造性思维",
        "phd": "博士级难度，需要高度创造性的数学思维，可能是开放性问题或需要构造反例",
    }

    key = request.headers.get("X-API-Key")
    if not key:
        raise HTTPException(status_code=401, detail="请先在登录时配置 DeepSeek API Key")

    gen_id = "GEN-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))

    history = _load_history(topic_key)
    recent = [h.get("preview", "") for h in history[-10:] if h.get("preview")]
    avoid_text = ""
    if recent:
        avoid_text = (
            "\n\n以下是最近生成过的题目，请勿重复或高度相似，换一个角度或知识点：\n"
            + "\n".join(f"- {r}" for r in recent)
        )

    prompt = f"""你是一位数学命题专家。请为"{exhibit_name}"主题生成一道练习题。

难度级别：{difficulty}
难度要求：{diff_guide.get(difficulty, "中等难度")}
相关知识点：{knowledge_points}
{avoid_text}

请用 JSON 格式输出：
{{
  "id": "{gen_id}",
  "difficulty": "{difficulty}",
  "knowledge_points": ["知识点1", "知识点2"],
  "problem_statement": "完整的题目描述，用 LaTeX 语法写数学公式",
  "preview": "题目简短预览（120字以内）",
  "solution": {{
    "method": "解题思路概述",
    "steps": ["步骤1的详细描述", "步骤2的详细描述", "步骤3的详细描述"],
    "final_answer": "最终答案，LaTeX 格式"
  }},
  "grading_rubric": {{
    "key_steps": ["关键得分步骤1", "关键得分步骤2"],
    "common_errors": ["常见错误1", "常见错误2"]
  }},
  "metadata": {{"problem_type": "计算题"}}
}}

只输出 JSON，不要其他内容。确保 problem_statement 使用正确的 LaTeX 语法（$...$ 或 $$...$$）。"""

    client = AsyncOpenAI(api_key=key, base_url="https://api.deepseek.com")
    try:
        response = await client.chat.completions.create(
            model="deepseek-chat",
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.choices[0].message.content
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0]
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0]

        problem = json.loads(raw.strip())

        history.append({
            "id": problem.get("id", gen_id),
            "preview": problem.get("preview", "")[:120],
            "topic": topic_key,
            "difficulty": difficulty,
            "ts": time.time(),
        })
        _save_history(topic_key, history)

        problem_path = GENERATED_DIR / f"{topic_key}_problems.json"
        existing = []
        if problem_path.exists():
            try:
                existing = json.loads(problem_path.read_text(encoding="utf-8"))
            except Exception:
                existing = []
        existing.append(problem)
        problem_path.write_text(
            json.dumps(existing[-500:], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

        return {"problem": problem, "generated": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)[:200]}")
