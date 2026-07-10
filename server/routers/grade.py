"""
Grade API — OCR handwriting grading endpoint.
"""

import base64
from fastapi import APIRouter, Request, HTTPException
from server.services import grader, problem_bank, history as history_svc

router = APIRouter()


@router.post("/api/grade")
async def grade_submission(request: Request):
    """Grade a handwritten answer.

    Request body (JSON):
        topic_key: str
        problem_id: str
        image_base64: str

    Returns the grading result dict.
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON body")

    topic_key = body.get("topic_key")
    problem_id = body.get("problem_id")
    image_b64 = body.get("image_base64")

    if not all([topic_key, problem_id, image_b64]):
        raise HTTPException(status_code=400, detail="Missing required fields: topic_key, problem_id, image_base64")

    # Load problem
    problem = problem_bank.get_problem(topic_key, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail=f"Problem {problem_id} not found in {topic_key}")

    # Decode image
    try:
        image_bytes = base64.b64decode(image_b64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 image data")

    # Grade
    api_key = request.headers.get("X-API-Key")
    try:
        result = await grader.grade_submission(problem, image_bytes, api_key=api_key)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Grading failed: {str(e)}")

    # Save to history
    history_svc.save_grade(
        topic_key=topic_key,
        problem_id=problem_id,
        problem_statement=problem.get("problem_statement", ""),
        solution_steps=problem.get("solution", {}).get("steps", []),
        final_answer=problem.get("solution", {}).get("final_answer", ""),
        grading_result=result,
    )

    return result
