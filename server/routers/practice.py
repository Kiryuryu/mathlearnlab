"""
Practice API — AI-only problem generation with deduplication.
"""

import random
import string
from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel
from server.config import settings
from server.routers.auth import require_user
from server.services.deepseek import chat_completion
from server.services.practice_service import (
    build_generate_prompt,
    build_recent_avoidance,
    extract_json,
    persist_problem,
    record_generated,
)

router = APIRouter()


class GenerateRequest(BaseModel):
    topic_key: str
    difficulty: str = "medium"


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

    key = request.headers.get("X-API-Key")
    if not key:
        raise HTTPException(status_code=401, detail="请先在登录时配置 DeepSeek API Key")

    gen_id = "GEN-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    avoid_text = build_recent_avoidance(topic_key)
    prompt = build_generate_prompt(exhibit_name, difficulty, knowledge_points, gen_id, avoid_text)

    try:
        response = await chat_completion(
            [{"role": "user", "content": prompt}],
            api_key=key,
            max_tokens=1500,
        )
        problem = extract_json(response.choices[0].message.content)
        record_generated(problem, gen_id, topic_key, difficulty)
        persist_problem(problem, topic_key)
        return {"problem": problem, "generated": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)[:200]}")
