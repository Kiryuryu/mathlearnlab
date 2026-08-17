"""
MathLearnLab FastAPI application.

Run:
    uvicorn server.main:app --reload
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from server.config import settings, CONTENT_DIR, DATA_DIR, STATIC_DIR, STATIC_SPA_DIR
from server.models.database import init_db
from server.middleware import RequestLogMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, version="4.0.0", lifespan=lifespan)

# ── Request logging ──
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
app.add_middleware(RequestLogMiddleware)

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
        "subjects": settings.subjects,
        "exhibits": settings.exhibits,
        "nav_tree": settings.nav_tree,
        "mathematicians": settings.mathematicians,
    }

# Import and include routers
from server.routers import content, practice, grade, chat, stats, auth, admin, workshop, blog, bookmarks, daily, graph

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(content.router)
app.include_router(practice.router)
app.include_router(grade.router)
app.include_router(chat.router)
app.include_router(stats.router)
app.include_router(workshop.router)
app.include_router(blog.router)
app.include_router(bookmarks.router)
app.include_router(daily.router)
app.include_router(graph.router)

# ── SPA fallback (registered last, so specific routes win) ──
# The Vue build (server/static-spa) is served for any unmatched GET route,
# with history-mode deep links falling back to index.html.
# Note: /static, /api, /data, /content are handled by the routes/mounts above;
# a truly unknown API path still returns JSON 404 instead of the SPA shell.


@app.get("/{full_path:path}", include_in_schema=False)
async def spa_fallback(full_path: str):
    if full_path.startswith(("api/", "static/", "data/", "content/", "docs")):
        return JSONResponse(status_code=404, content={"detail": "Not found"})
    index = STATIC_SPA_DIR / "index.html"
    if full_path:
        candidate = STATIC_SPA_DIR / full_path
        if candidate.is_file():
            return FileResponse(candidate)
    if index.exists():
        return FileResponse(index)
    return JSONResponse(status_code=404, content={"detail": "Not found"})
