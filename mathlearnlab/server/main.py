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

# ── Import and include routers ──
# (imported after app creation to avoid circular imports)
from server.routers import pages, content, practice, grade, chat, stats

app.include_router(pages.router)          # GET /, /notebooks/*, /notes/*, /problems/*, /error-log, /practice/*
app.include_router(content.router)        # GET  /api/content/*
app.include_router(practice.router)       # GET  /api/practice/*
app.include_router(grade.router)           # POST /api/grade
app.include_router(chat.router)            # POST /api/chat/stream
app.include_router(stats.router)           # GET  /api/stats


# ── Health check ──
@app.get("/api/health")
async def health():
    return {"status": "ok", "app": settings.app_name}
