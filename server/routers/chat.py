"""
Chat API — SSE streaming chat with Claude.
API key comes from client (X-API-Key header), not server config.
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import StreamingResponse
from server.services import chat_service
from server.config import settings
from server.routers.auth import require_user

router = APIRouter()


@router.post("/api/chat/stream")
async def chat_stream(request: Request, user: dict = Depends(require_user)):
    """Stream a chat conversation with Claude via SSE."""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    messages = body.get("messages", [])
    if not messages:
        raise HTTPException(status_code=400, detail="Missing messages array")

    system = body.get("system")
    model = body.get("model")
    max_tokens = body.get("max_tokens")
    context_route = body.get("context_route", "")
    lang = body.get("lang", "zh")

    api_key = request.headers.get("X-API-Key") or settings.deepseek_api_key
    if not api_key:
        err = "请先配置 API Key（点击右上角圆点按钮）" if lang == "zh" else "Please configure your API Key first"
        raise HTTPException(status_code=401, detail=err)

    return StreamingResponse(
        chat_service.stream_chat(
            messages=messages, system=system, model=model,
            max_tokens=max_tokens, api_key=api_key, context_route=context_route,
            lang=lang,
        ),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
    )
