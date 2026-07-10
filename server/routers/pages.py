"""
Page router — serves Jinja2 templates for all frontend routes.
"""

from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from server.config import settings
from server.main import CONTENT_DIR
from server.services import problem_bank, history as history_svc

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

router = APIRouter()

def _ctx(request: Request, **extra):
    """Build template context with settings as plain dict."""
    return {"request": request, "settings": settings.model_dump(), **extra}


async def _read_md(filepath: str) -> str:
    """Read and render a markdown file to HTML."""
    full_path = CONTENT_DIR / filepath
    if not full_path.exists():
        return f'<p class="content-error">内容未找到: {filepath}</p>'
    md_text = full_path.read_text(encoding="utf-8")
    try:
        import markdown as md
        html = md.markdown(md_text, extensions=["fenced_code", "tables", "codehilite"])
    except ImportError:
        html = f"<pre>{md_text}</pre>"
    return html


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    stats = history_svc.get_stats()
    return templates.TemplateResponse("pages/home.html", _ctx(request, stats=stats))


@router.get("/notebooks/{chapter}/{filename}", response_class=HTMLResponse)
async def notebook_page(request: Request, chapter: str, filename: str):
    filepath = f"notebooks/{chapter}/{filename}.md"
    content_html = await _read_md(filepath)
    return templates.TemplateResponse("pages/content.html", _ctx(request,
        content_html=content_html, title=filename.replace("-", " ").title()))


@router.get("/notes/{path:path}", response_class=HTMLResponse)
async def notes_page(request: Request, path: str):
    filepath = f"notes/{path}.md"
    content_html = await _read_md(filepath)
    return templates.TemplateResponse("pages/content.html", _ctx(request,
        content_html=content_html, title=path))


@router.get("/problems/{path:path}", response_class=HTMLResponse)
async def problems_page(request: Request, path: str):
    filepath = f"problems/{path}.md"
    content_html = await _read_md(filepath)
    return templates.TemplateResponse("pages/content.html", _ctx(request,
        content_html=content_html, title=path))


@router.get("/error-log", response_class=HTMLResponse)
async def error_log_page(request: Request):
    filepath = "error-log/01-gaoshu-errors.md"
    content_html = await _read_md(filepath)
    return templates.TemplateResponse("pages/content.html", _ctx(request,
        content_html=content_html, title="错题本"))


@router.get("/practice/{topic}", response_class=HTMLResponse)
async def practice_page(request: Request, topic: str):
    topic_info = settings.topics.get(topic, {})
    summaries = problem_bank.list_problem_summaries(topic)
    return templates.TemplateResponse("pages/practice.html", _ctx(request,
        topic_key=topic, topic=topic_info, problems=summaries, count=len(summaries)))
