"""
Workshop API — AI-assisted function plotting via DeepSeek.
"""
import asyncio
from fastapi import APIRouter, Request, HTTPException
import json, re
from server.config import settings

router = APIRouter()


@router.post("/api/workshop/plot")
async def workshop_plot(request: Request):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    description = body.get("description", "").strip()
    if not description:
        raise HTTPException(status_code=400, detail="Missing description")

    key = request.headers.get("X-API-Key") or settings.anthropic_api_key
    if not key:
        return {"code": None, "explanation": None, "message": "请先配置 API Key"}

    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=key, base_url="https://api.deepseek.com")

    code_prompt = f"""根据描述生成 Plotly.js 代码。只输出代码。

描述: {description}

要求:
1. 只输出 JavaScript 代码
2. x 范围默认 -6 到 6
3. 绘制在 document.getElementById('wsPlotArea') 上
4. paper_bgcolor: 'rgba(0,0,0,0)', plot_bgcolor: 'rgba(0,0,0,0)'
5. Plotly.newPlot(document.getElementById('wsPlotArea'), traces, layout, {{ responsive: true }})

只输出代码。"""

    explain_prompt = f"""用中文简要解释以下函数（面向学习微积分的学生，2-4段）：{description}
包含函数性质、关键特征、数学意义。只输出 HTML 段落。"""

    try:
        code_resp, explain_resp = await asyncio.gather(
            client.chat.completions.create(
                model="deepseek-chat", max_tokens=1000,
                messages=[{"role": "user", "content": code_prompt}],
            ),
            client.chat.completions.create(
                model="deepseek-chat", max_tokens=600,
                messages=[{"role": "user", "content": explain_prompt}],
            ),
            return_exceptions=True
        )

        code = None
        if not isinstance(code_resp, Exception) and code_resp.choices:
            code = code_resp.choices[0].message.content.strip()
            code = re.sub(r'^```(?:javascript|js)?\s*\n', '', code)
            code = re.sub(r'\n```\s*$', '', code)

        explanation = None
        if not isinstance(explain_resp, Exception) and explain_resp.choices:
            explanation = explain_resp.choices[0].message.content.strip()

        return {"code": code, "explanation": explanation, "description": description}
    except Exception as e:
        return {"code": None, "explanation": None, "description": description, "error": str(e)[:200]}
