"""
MathLearnLab FastAPI application.

Run:
    uvicorn server.main:app --reload
"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from server.config import settings

# Resolve absolute paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / settings.content_dir
DATA_DIR = BASE_DIR / settings.data_dir
STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(title=settings.app_name, version="2.0.0")

# ── Mount static files ──
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/data", StaticFiles(directory=str(DATA_DIR)), name="data")

# ── Health check ──
@app.get("/api/health")
async def health():
    return {"status": "ok", "app": settings.app_name}

# ── Import and include routers ──
# Remove CONTENT_DIR from pages.py import to avoid circular deps
from server.routers import content, practice, grade, chat, stats

app.include_router(content.router)
app.include_router(practice.router)
app.include_router(grade.router)
app.include_router(chat.router)
app.include_router(stats.router)

# Pages router last (imports CONTENT_DIR from this module)
from server.routers import pages
app.include_router(pages.router)
