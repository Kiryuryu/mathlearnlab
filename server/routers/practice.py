"""
Practice API — problem bank queries.
"""

from fastapi import APIRouter, HTTPException, Query
from server.services import problem_bank

router = APIRouter()


@router.get("/api/practice/{topic}/problems")
async def list_problems(topic: str, difficulty: str = Query(default="all")):
    summaries = problem_bank.list_problem_summaries(topic, difficulty=None if difficulty == "all" else difficulty)
    return {"topic": topic, "problems": summaries, "count": len(summaries)}


@router.get("/api/practice/{topic}/problems/random")
async def random_problem(topic: str, difficulty: str = Query(default="all")):
    """Return a random problem with full details (including solution)."""
    p = problem_bank.get_random_problem(topic, difficulty=None if difficulty == "all" else difficulty)
    if not p:
        raise HTTPException(status_code=404, detail="No problems found")
    return {"problem": p}


@router.get("/api/practice/{topic}/problems/{problem_id}")
async def get_problem(topic: str, problem_id: str):
    """Return a specific problem with full details."""
    p = problem_bank.get_problem(topic, problem_id)
    if not p:
        raise HTTPException(status_code=404, detail=f"Problem {problem_id} not found")
    return {"problem": p}
