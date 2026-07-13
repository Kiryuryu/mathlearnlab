"""
MathLearnLab FastAPI application.

Run:
    uvicorn server.main:app --reload
"""

from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from server.config import settings
from server.models.database import init_db

# Resolve absolute paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / settings.content_dir
DATA_DIR = BASE_DIR / settings.data_dir
STATIC_DIR = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, version="3.0.0", lifespan=lifespan)

# ── CORS ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Mount static files ──
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.mount("/data", StaticFiles(directory=str(DATA_DIR)), name="data")

# ── Health check ──
@app.get("/api/health")
async def health():
    return {"status": "ok", "app": settings.app_name, "version": "4.0.0"}

# ── Museum exhibit info ──
@app.get("/api/museum/exhibits")
async def museum_exhibits():
    return {
        "app_name": settings.app_name,
        "app_subtitle": settings.app_subtitle,
        "exhibits": settings.exhibits,
        "nav_tree": settings.nav_tree,
    }

# Import and include routers
from server.routers import content, practice, grade, chat, stats, auth, workshop

app.include_router(auth.router)
app.include_router(content.router)
app.include_router(practice.router)
app.include_router(grade.router)
app.include_router(chat.router)
app.include_router(stats.router)
app.include_router(workshop.router)

# Pages router — serves existing Jinja2 frontend until Flutter replaces it
from server.routers import pages
app.include_router(pages.router)
