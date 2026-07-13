"""
Workshop API — AI-assisted function plotting.
"""

from fastapi import APIRouter, Request, HTTPException
import json, re
from server.config import settings

router = APIRouter()


@router.post("/api/workshop/plot")
async def workshop_plot(request: Request):
    """Generate Plotly visualization code from a natural language description."""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    description = body.get("description", "").strip()
    if not description:
        raise HTTPException(status_code=400, detail="Missing description")

    key = settings.anthropic_api_key
    if not key:
        # Fallback: return null code, client can try math.js
        return {"code": None, "message": "No API key configured — using client-side parser"}

    import anthropic

    prompt = f"""你是一位数据可视化专家。根据以下描述，生成 Plotly.js + JavaScript 代码来绘制图像。
只输出可执行的 JavaScript 代码，使用 Plotly.newPlot() 或 Plotly.react() 函数。
变量 document 引用到当前文档，请在 id="plotArea" 的 DOM 元素上绘制。

描述: {description}

要求:
1. 只输出 JavaScript 代码，不要 markdown 代码块标记
2. 如果有 x 范围，用 x 从 -6 到 6（除非特别指定）
3. 曲面图用 Plotly surface trace
4. 绘制在 document.getElementById('plotArea') 上
5. layout 中 paper_bgcolor 设为 'rgba(0,0,0,0)', plot_bgcolor 设为 'rgba(0,0,0,0)'
6. responsive: true
7. 代码直接用 Plotly.newPlot(document.getElementById('plotArea'), traces, layout, {{ responsive: true }})

只输出代码。"""

    client = anthropic.AsyncAnthropic(api_key=key)
    response = await client.messages.create(
        model=settings.default_model,
        max_tokens=1000,
        system="你是一个 JavaScript + Plotly 代码生成器。只输出代码，不要解释。",
        messages=[{"role": "user", "content": prompt}],
    )

    code = response.content[0].text.strip()
    # Strip markdown code fences
    code = re.sub(r'^```(?:javascript|js)?\s*\n', '', code)
    code = re.sub(r'\n```\s*$', '', code)

    return {"code": code, "description": description}
