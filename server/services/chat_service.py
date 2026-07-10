"""
Chat service — SSE streaming chat via Anthropic API.
Ported from the Cloudflare Worker handleChat function.
"""

import json
import anthropic
from server.config import settings


SYSTEM_PROMPT_TEMPLATE = """你是 MathLearnLab 的考研数学 AI 助手。{context_info}

你的角色：
- 用中文回答，语言通俗易懂，帮助考研学生理解数学概念
- 数学公式用 LaTeX 格式（$...$ 行内，$$...$$ 块级）
- 回答要有层次：先给简短结论，再展开详细解释
- 主动指出常见错误和易混淆的概念
- 举例说明抽象概念
- 如果学生问题目，先给思路引导，不要直接给完整答案
- 保持鼓励和支持的语气

考试范围：考研数学一/二/三（高等数学、线性代数、概率论与数理统计）"""


async def stream_chat(messages: list[dict], system: str | None = None,
                      model: str | None = None, max_tokens: int | None = None,
                      api_key: str | None = None, context_route: str = ""):
    """Async generator yielding SSE-formatted chat chunks.

    Parameters
    ----------
    messages : list[dict]
        Chat history as [{"role": "user"|"assistant", "content": "..."}, ...]
    system : str or None
        Custom system prompt. If None, uses the template with context.
    model : str or None
        Claude model ID. Defaults to settings.default_model.
    max_tokens : int or None
    api_key : str or None
    context_route : str
        Current page route, injected into system prompt context.

    Yields
    ------
    str — SSE-formatted data lines.
    """
    key = api_key or settings.anthropic_api_key
    if not key:
        yield f"data: {json.dumps({'error': 'API key not configured'})}\n\n"
        return

    # Build system prompt with context
    context_info = ""
    if context_route:
        # Extract topic from route
        topic_hints = {
            "limits": "极限与连续", "derivatives": "微分学",
            "integrals": "积分学", "series": "无穷级数", "multivariable": "多元微积分",
            "integration": "积分学",
        }
        for hint, name in topic_hints.items():
            if hint in context_route:
                context_info = f"学生当前正在浏览：{name}。"
                break

    system_prompt = system or SYSTEM_PROMPT_TEMPLATE.format(context_info=context_info)

    client = anthropic.AsyncAnthropic(api_key=key)

    try:
        async with client.messages.stream(
            model=model or settings.default_model,
            max_tokens=max_tokens or settings.max_chat_tokens,
            system=system_prompt,
            messages=messages,
        ) as stream:
            async for event in stream:
                if event.type == "content_block_delta":
                    text = event.delta.text
                    yield f"data: {json.dumps({'type': 'content_block_delta', 'delta': {'text': text}})}\n\n"
                elif event.type == "message_stop":
                    yield "data: [DONE]\n\n"
                    break
    except Exception as e:
        yield f"data: {json.dumps({'error': str(e)})}\n\n"
