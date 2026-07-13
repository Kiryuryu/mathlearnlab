"""
Chat API — SSE streaming chat with Claude.
API key now comes from backend config, not user header.
"""

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from server.services import chat_service

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

    return StreamingResponse(
        chat_service.stream_chat(
            messages=messages,
            system=system,
            model=model,
            max_tokens=max_tokens,
            api_key=None,  # use server-side API key from config
            context_route=context_route,
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
