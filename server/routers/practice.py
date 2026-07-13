"""
Practice API — problem bank queries + AI generation.
"""

from fastapi import APIRouter, HTTPException, Query, Request
from pydantic import BaseModel
from server.services import problem_bank

router = APIRouter()


class GenerateRequest(BaseModel):
    topic_key: str
    difficulty: str = "medium"


@router.get("/api/practice/{topic}/problems")
async def list_problems(topic: str, difficulty: str = Query(default="all")):
    summaries = problem_bank.list_problem_summaries(topic, difficulty=None if difficulty == "all" else difficulty)
    return {"topic": topic, "problems": summaries, "count": len(summaries)}


@router.get("/api/practice/{topic}/problems/random")
async def random_problem(topic: str, difficulty: str = Query(default="all")):
    """Return a random problem with full details (including solution)."""
    p = problem_bank.get_random_problem(topic, difficulty=None if difficulty == "all" else difficulty)
    if not p:
        raise HTTPException(status_code=404, detail="No problems found")
    return {"problem": p}


@router.get("/api/practice/{topic}/problems/{problem_id}")
async def get_problem(topic: str, problem_id: str):
    """Return a specific problem with full details."""
    p = problem_bank.get_problem(topic, problem_id)
    if not p:
        raise HTTPException(status_code=404, detail=f"Problem {problem_id} not found")
    return {"problem": p}


@router.post("/api/practice/generate")
async def generate_problem(request: Request):
    """Use Claude to generate a new practice problem on the fly."""
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

    import anthropic, json, random, string
    key = settings.anthropic_api_key
    if not key:
        p = problem_bank.get_random_problem(topic_key, None)
        if p:
            return {"problem": p, "generated": False}
        raise HTTPException(status_code=500, detail="未配置 API Key，且题库无可用题目")

    prompt = f"""你是一位数学命题专家。请为"{exhibit_name}"主题生成一道练习题。

难度级别：{difficulty}
难度要求：{diff_guide.get(difficulty, '中等难度')}
相关知识点：{knowledge_points}

请用 JSON 格式输出：
{{
  "id": "GEN-{''.join(random.choices(string.ascii_uppercase + string.digits, k=5))}",
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

    client = anthropic.AsyncAnthropic(api_key=key)
    try:
        response = await client.messages.create(
            model=settings.default_model,
            max_tokens=1500,
            system="你是一位数学命题专家。只输出有效 JSON，不要其他内容。",
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text
        if "```json" in raw:
            raw = raw.split("```json")[1].split("```")[0]
        elif "```" in raw:
            raw = raw.split("```")[1].split("```")[0]

        problem = json.loads(raw.strip())
        return {"problem": problem, "generated": True}
    except Exception as e:
        p = problem_bank.get_random_problem(topic_key, None)
        if p:
            return {"problem": p, "generated": False, "fallback_reason": str(e)[:100]}
        raise HTTPException(status_code=500, detail=f"生成失败: {str(e)[:200]}")
