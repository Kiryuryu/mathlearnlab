"""
Chat service — SSE streaming chat via DeepSeek (OpenAI-compatible) API.
"""

from openai import AsyncOpenAI

ZH_SYSTEM_PROMPT = """你是数学博物馆的 AI 导览员。{context_info}

你的使命：
- 帮助访客发现数学之美，理解概念的直观含义，而非应试技巧
- 用中文回答，语言优雅、引人入胜，像一位博学的导览员在讲解展品
- 数学公式用 LaTeX 格式（$...$ 行内，$$...$$ 块级）
- 回答要有层次：先给直观直觉，再展开严格解释
- 讲述概念背后的故事——谁发现的、为什么这样定义、美在哪里
- 主动指出概念之间的深层联系
- 举例说明抽象概念在现实世界中的应用
- 保持热情和好奇心，激发访客对数学的热爱"""

EN_SYSTEM_PROMPT = """You are the AI tour guide of the Math Museum. {context_info}

Your mission:
- Help visitors discover the beauty of mathematics and understand concepts intuitively
- Answer in English, with elegant and engaging language like a knowledgeable guide
- Use LaTeX for math formulas ($...$ inline, $$...$$ display)
- Structure answers: first give intuition, then rigorous explanation
- Tell the stories behind concepts — who discovered them, why they are defined that way, what makes them beautiful
- Point out deep connections between concepts
- Give real-world examples of abstract ideas
- Be passionate and curious, inspiring visitors' love for mathematics"""


async def stream_chat(messages: list[dict], system: str | None = None,
                      model: str | None = None, max_tokens: int | None = None,
                      api_key: str | None = None, context_route: str = "",
                      lang: str = "zh"):
    """Async generator yielding SSE-formatted chat chunks via DeepSeek."""
    if not api_key:
        err = "请先登录并配置 DeepSeek API Key" if lang == "zh" else "Please log in and configure your DeepSeek API Key"
        yield f"data: {{\"error\":\"{err}\"}}\n\n"
        yield "data: [DONE]\n\n"
        return

    model = model or "deepseek-chat"
    prompt = ZH_SYSTEM_PROMPT if lang == "zh" else EN_SYSTEM_PROMPT
    context_info = f"当前访客在浏览: {context_route}" if context_route else ""
    system_msg = system or prompt.format(context_info=context_info)

    chat_messages = [{"role": "system", "content": system_msg}]
    for m in messages[-30:]:
        role = m.get("role", "user")
        if role in ("user", "assistant"):
            chat_messages.append({"role": role, "content": m.get("content", "")})

    client = AsyncOpenAI(api_key=api_key, base_url="https://api.deepseek.com")

    try:
        stream = await client.chat.completions.create(
            model=model,
            messages=chat_messages,
            max_tokens=max_tokens or 2048,
            stream=True,
        )

        async for chunk in stream:
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta and delta.content:
                yield f"data: {delta.content}\n\n"

        yield "data: [DONE]\n\n"
    except Exception as e:
        err = str(e).replace("\n", " ")[:200]
        yield f"data: {{\"error\":\"{err}\"}}\n\n"
        yield "data: [DONE]\n\n"
