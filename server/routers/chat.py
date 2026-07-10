"""
Chat API — SSE streaming chat with Claude.
API key now comes from backend config, not user header.
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import StreamingResponse
from server.routers.auth import require_user
from server.services import chat_service

router = APIRouter()


@router.post("/api/chat/stream")
async def chat_stream(request: Request, user: dict = Depends(require_user)):
    """Stream a chat conversation with Claude via SSE.

    Request body (JSON):
        messages: list[{"role": "user"|"assistant", "content": "..."}]
        system: str (optional system prompt)
        model: str (optional model override)
        context_route: str (current page route for context awareness)
    """
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
