"""
Grade API — OCR handwriting grading endpoint.
"""

import base64
import logging
from fastapi import APIRouter, Request, HTTPException, Depends
from server.config import settings
from server.routers.auth import require_user
from server.services import grader, history as history_svc
from server.services.deepseek import resolve_api_key
from server.services.ratelimit import use_ai_quota
from server.models.problems import load_problem

logger = logging.getLogger(__name__)

router = APIRouter()

# Magic bytes for supported image formats.
_IMAGE_SIGNATURES = {
    b"\xff\xd8\xff": "JPEG",
    b"\x89PNG\r\n\x1a\n": "PNG",
    b"GIF87a": "GIF",
    b"GIF89a": "GIF",
    b"RIFF": "WEBP",  # verified further below
}


def _validate_image(image_bytes: bytes) -> None:
    """Reject oversized or unsupported images before they hit the AI API."""
    if len(image_bytes) > settings.max_image_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"图片过大：最大 {settings.max_image_bytes // (1024 * 1024)}MB",
        )
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Empty image data")
    for magic, fmt in _IMAGE_SIGNATURES.items():
        if image_bytes.startswith(magic):
            if fmt == "WEBP" and not (image_bytes[8:12] in (b"WEBP", b"VP8 ")):
                break  # RIFF but not WebP — treat as unsupported
            return
    raise HTTPException(status_code=415, detail="仅支持 JPEG / PNG / WebP / GIF 图片")


@router.post("/api/grade")
async def grade_submission(request: Request, user: dict = Depends(require_user)):
    """Grade a handwritten answer."""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    topic_key = body.get("topic_key")
    problem_id = body.get("problem_id")
    image_b64 = body.get("image_base64")

    if not all([topic_key, problem_id, image_b64]):
        raise HTTPException(status_code=400, detail="Missing required fields: topic_key, problem_id, image_base64")

    # Load problem from the DB (race-safe, indexed by topic + id).
    problem = load_problem(topic_key, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail=f"Problem {problem_id} not found in {topic_key}")

    # Decode + validate image before spending AI quota.
    try:
        image_bytes = base64.b64decode(image_b64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 image data")
    _validate_image(image_bytes)

    api_key = resolve_api_key(request.headers.get("X-API-Key"))
    if not api_key:
        raise HTTPException(status_code=401, detail="请先配置 DeepSeek API Key（右上角设置）")

    if not use_ai_quota(user["user_id"]):
        raise HTTPException(
            status_code=429,
            detail=f"今日 AI 调用额度已用完（每日 {settings.ai_daily_limit} 次），请明天再来",
        )

    # Grade
    try:
        result = await grader.grade_submission(problem, image_bytes, api_key=api_key)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Grading failed: {str(e)}")

    # Save to history
    try:
        history_svc.save_grade(
            user_id=user["user_id"],
            topic_key=topic_key,
            problem_id=problem_id,
            problem_statement=problem.get("problem_statement", ""),
            solution_steps=problem.get("solution", {}).get("steps", []),
            final_answer=problem.get("solution", {}).get("final_answer", ""),
            grading_result=result,
        )
    except Exception:
        logger.exception("Failed to save grade history for user %s", user["user_id"])

    return result
