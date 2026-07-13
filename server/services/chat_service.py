"""
Chat service — SSE streaming chat via DeepSeek API.
Ported from the Cloudflare Worker handleChat function.
"""

import json
import anthropic
from server.config import settings


SYSTEM_PROMPT_TEMPLATE = """你是数学博物馆的 AI 导览员。{context_info}

你的使命：
- 帮助访客发现数学之美，理解概念的直观含义，而非应试技巧
- 用中文回答，语言优雅、引人入胜，像一位博学的导览员在讲解展品
- 数学公式用 LaTeX 格式（$...$ 行内，$$...$$ 块级）
- 回答要有层次：先给直观直觉，再展开严格解释
- 讲述概念背后的故事——谁发现的、为什么这样定义、美在哪里
- 主动指出概念之间的深层联系
- 举例说明抽象概念在现实世界中的应用
- 保持热情和好奇心，激发访客对数学的热爱"""


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
