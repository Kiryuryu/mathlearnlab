"""
Chat service — SSE streaming chat via DeepSeek (OpenAI-compatible) API.
"""

from server.services.deepseek import stream_chat as deepseek_stream
from server.content_data import subjects, exhibits

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

ZH_GUIDE_PROMPT = """你是数学博物馆「{exhibit_name}」展区的专职讲解员。

{exhibit_info}

请围绕这个展品为访客讲解：
- 先用一两句话点出这个展品的核心思想，让访客立刻抓住要点
- 用直觉和画面感解释核心概念，再补充严格定义
- 介绍与这个展品相关的关键人物（历史学家）及其贡献
- 指出这个展品「美在哪里」，以及它在现实中的应用
- 如果访客问到其他展品，可以自然地与当前展品联系起来
- 数学公式用 LaTeX 格式（$...$ 行内，$$...$$ 块级）
- 语言优雅、引人入胜，像一位热情而博学的讲解员"""

EN_GUIDE_PROMPT = """You are the dedicated tour guide of the "{exhibit_name}" exhibit at the Math Museum.

{exhibit_info}

Please guide visitors through this exhibit:
- Open with one or two sentences capturing the core idea of this exhibit
- Explain the central concepts with intuition and vivid imagery, then add the rigorous definitions
- Introduce the key figures (historians) associated with this exhibit and their contributions
- Point out what makes it beautiful, and its real-world applications
- If visitors ask about other exhibits, naturally connect them to the current one
- Use LaTeX for math formulas ($...$ inline, $$...$$ display)
- Be elegant and engaging, like a passionate and knowledgeable guide"""


def exhibit_context(exhibit_key: str) -> dict | None:
    """Return a structured summary of an exhibit for the guide prompt."""
    ex = exhibits.get(exhibit_key)
    if not ex:
        return None
    related = []
    for rk in ex.get("related", []) or []:
        rel = exhibits.get(rk)
        if rel:
            related.append(rel.get("zh", rk))
    return {
        "name_zh": ex.get("zh", exhibit_key),
        "name_en": ex.get("en", exhibit_key),
        "big_question": ex.get("big_question", ""),
        "big_question_en": ex.get("big_question_en", ""),
        "beauty": ex.get("beauty", ""),
        "beauty_en": ex.get("beauty_en", ""),
        "historian": ex.get("historian", ""),
        "related": related,
    }


def _format_exhibit_info(info: dict, lang: str) -> str:
    """Format the exhibit context dict into a prompt paragraph."""
    name = info["name_zh"] if lang == "zh" else info["name_en"]
    q = info["big_question"] if lang == "zh" else info["big_question_en"]
    beauty = info["beauty"] if lang == "zh" else info["beauty_en"]
    related = "、".join(info["related"]) if info["related"] else "（暂无关联展品）"
    if lang == "zh":
        return (
            f"本展品：{name}\n"
            f"核心问题：{q}\n"
            f"关键人物：{info['historian']}\n"
            f"数学之美：{beauty}\n"
            f"馆内相关展品：{related}"
        )
    return (
        f"This exhibit: {name}\n"
        f"Core question: {q}\n"
        f"Key figures: {info['historian']}\n"
        f"Why it's beautiful: {beauty}\n"
        f"Related exhibits in the museum: {related}"
    )


def build_system_prompt(lang: str, context_route: str = "", guide: dict | None = None,
                        exhibit_info: dict | None = None) -> str:
    """Construct the system prompt. Guide mode uses the dedicated tour-guide prompt."""
    if guide and exhibit_info:
        prompt = ZH_GUIDE_PROMPT if lang == "zh" else EN_GUIDE_PROMPT
        return prompt.format(
            exhibit_name=guide.get("name", exhibit_info["name_zh"]),
            exhibit_info=_format_exhibit_info(exhibit_info, lang),
        )
    prompt = ZH_SYSTEM_PROMPT if lang == "zh" else EN_SYSTEM_PROMPT
    context_info = f"当前访客在浏览: {context_route}" if context_route else ""
    return prompt.format(context_info=context_info)


async def stream_chat(messages: list[dict], system: str | None = None,
                      model: str | None = None, max_tokens: int | None = None,
                      api_key: str | None = None, context_route: str = "",
                      lang: str = "zh", guide: dict | None = None):
    """Async generator yielding SSE-formatted chat chunks via DeepSeek."""
    if not api_key:
        err = "请先登录并配置 DeepSeek API Key" if lang == "zh" else "Please log in and configure your DeepSeek API Key"
        yield f"data: {{\"error\":\"{err}\"}}\n\n"
        yield "data: [DONE]\n\n"
        return

    model = model or "deepseek-chat"
    guide_key = guide.get("key") if guide else None
    exhibit_info = exhibit_context(guide_key) if guide_key else None
    system_msg = system or build_system_prompt(lang, context_route, guide, exhibit_info)

    chat_messages = [{"role": "system", "content": system_msg}]
    for m in messages[-30:]:
        role = m.get("role", "user")
        if role in ("user", "assistant"):
            chat_messages.append({"role": role, "content": m.get("content", "")})

    try:
        stream = await deepseek_stream(
            chat_messages,
            api_key=api_key,
            model=model,
            max_tokens=max_tokens or 2048,
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
