"""
Chat API — SSE streaming chat with Claude.
API key comes from client (X-API-Key header), not server config.
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from server.services import chat_service
from server.config import settings

router = APIRouter()


@router.post("/api/chat/stream")
async def chat_stream(request: Request):
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

    # Use client-provided key, or server default if none
    api_key = request.headers.get("X-API-Key") or settings.anthropic_api_key
    if not api_key:
        raise HTTPException(status_code=401, detail="请先配置 API Key（点击右上角圆点按钮）")

    return StreamingResponse(
        chat_service.stream_chat(
            messages=messages, system=system, model=model,
            max_tokens=max_tokens, api_key=api_key, context_route=context_route,
        ),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive", "X-Accel-Buffering": "no"},
    )
