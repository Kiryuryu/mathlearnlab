"""
MathLearnLab FastAPI application.

Run:
    uvicorn server.main:app --reload
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from server.config import settings, CONTENT_DIR, DATA_DIR, STATIC_DIR
from server.models.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, version="4.0.0", lifespan=lifespan)

# ── CORS ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Mount static files ──
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

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
        "mathematicians": settings.mathematicians,
    }

# Import and include routers
from server.routers import content, practice, grade, chat, stats, auth, workshop, blog, bookmarks

app.include_router(auth.router)
app.include_router(content.router)
app.include_router(practice.router)
app.include_router(grade.router)
app.include_router(chat.router)
app.include_router(stats.router)
app.include_router(workshop.router)
app.include_router(blog.router)
app.include_router(bookmarks.router)
