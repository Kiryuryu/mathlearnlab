"""
Workshop API — AI-assisted function plotting.
"""

import asyncio
from fastapi import APIRouter, Request, HTTPException
import json, re
from server.config import settings

router = APIRouter()


@router.post("/api/workshop/plot")
async def workshop_plot(request: Request):
    """Generate Plotly visualization code from a natural language description.
    Returns both plot code and a math explanation."""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    description = body.get("description", "").strip()
    if not description:
        raise HTTPException(status_code=400, detail="Missing description")

    key = settings.anthropic_api_key
    if not key:
        return {"code": None, "explanation": None, "message": "No API key configured — using client-side parser"}

    import anthropic

    code_prompt = f"""你是一位数据可视化专家。根据以下描述，生成 Plotly.js + JavaScript 代码来绘制图像。
只输出可执行的 JavaScript 代码，使用 Plotly.newPlot() 或 Plotly.react() 函数。
变量 document 引用到当前文档，请在 id="wsPlotArea" 的 DOM 元素上绘制。

描述: {description}

要求:
1. 只输出 JavaScript 代码，不要 markdown 代码块标记
2. 如果有 x 范围，用 x 从 -6 到 6（除非特别指定）
3. 曲面图用 Plotly surface trace
4. 绘制在 document.getElementById('wsPlotArea') 上
5. layout 中 paper_bgcolor 设为 'rgba(0,0,0,0)', plot_bgcolor 设为 'rgba(0,0,0,0)'
6. responsive: true
7. 代码直接用 Plotly.newPlot(document.getElementById('wsPlotArea'), traces, layout, {{ responsive: true }})

只输出代码。"""

    explain_prompt = f"""你是一位数学教授，请用中文简要解释以下函数或表达式，面向学习高等数学的学生：

{description}

要求：
1. 2-4 个自然段，简洁明了
2. 包含：函数的基本性质（奇偶性、周期性等）、关键特征（极值点、渐近线等）、在高等数学中的意义
3. 用简洁的 HTML 标签（<p>, <strong>, <em>）格式化
4. 如果涉及特殊点或范围，明确指出
5. 保持教学语气，引人入胜

只输出 HTML 内容，不要 markdown。"""

    client = anthropic.AsyncAnthropic(api_key=key)

    # Get code first, then explanation in parallel
    code_resp, explain_resp = await asyncio.gather(
        client.messages.create(
            model=settings.default_model,
            max_tokens=1000,
            system="你是一个 JavaScript + Plotly 代码生成器。只输出代码，不要解释。",
            messages=[{"role": "user", "content": code_prompt}],
        ),
        client.messages.create(
            model=settings.fast_model,
            max_tokens=600,
            system="你是一位数学教授，用中文简洁解释函数。用HTML格式化输出。",
            messages=[{"role": "user", "content": explain_prompt}],
        ),
        return_exceptions=True
    )

    code = None
    if not isinstance(code_resp, Exception) and code_resp.content:
        code = code_resp.content[0].text.strip()
        code = re.sub(r'^```(?:javascript|js)?\s*\n', '', code)
        code = re.sub(r'\n```\s*$', '', code)

    explanation = None
    if not isinstance(explain_resp, Exception) and explain_resp.content:
        explanation = explain_resp.content[0].text.strip()
        explanation = re.sub(r'^```(?:html)?\s*\n', '', explanation)
        explanation = re.sub(r'\n```\s*$', '', explanation)

    return {"code": code, "explanation": explanation, "description": description}
