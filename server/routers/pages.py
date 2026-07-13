"""
Page router — serves Jinja2 templates for all frontend routes.
"""

from pathlib import Path
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from server.config import settings
from server.main import CONTENT_DIR
from server.services import problem_bank

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))

router = APIRouter()


def _ctx(request: Request, **extra):
    return {"request": request, "settings": settings, **extra}


async def _read_md(filepath: str) -> str:
    """Read and render a markdown file to HTML. Strips Python code blocks."""
    full_path = CONTENT_DIR / filepath
    if not full_path.exists():
        return f'<p class="content-error">内容未找到: {filepath}</p>'
    md_text = full_path.read_text(encoding="utf-8")

    # Strip fenced code blocks: they're Jupyter notebook artifacts
    import re
    md_text = re.sub(r'```python[\s\S]*?```', '', md_text)
    md_text = re.sub(r'```\s*\{.*?\}[\s\S]*?```', '', md_text)

    try:
        import markdown as md
        html = md.markdown(md_text, extensions=["fenced_code", "tables", "nl2br"])
    except ImportError:
        html = f"<pre>{md_text}</pre>"
    return html


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("pages/home.html", _ctx(request))


@router.get("/gaoshu", response_class=HTMLResponse)
async def gaoshu_page(request: Request):
    gaoshu_subtopics = sorted(
        [(k, v) for k, v in settings.exhibits.items() if k != "gaoshu"],
        key=lambda kv: kv[1].get("order", 99)
    )
    return templates.TemplateResponse("pages/gaoshu.html", _ctx(request, gaoshu_subtopics=gaoshu_subtopics))


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


@router.get("/exhibit/{topic}", response_class=HTMLResponse)
async def exhibit_page(request: Request, topic: str, tab: str = "concept"):
    exhibit_info = settings.exhibits.get(topic, {})
    if not exhibit_info:
        return templates.TemplateResponse("pages/content.html", _ctx(request,
            content_html=f"<p class=\"content-error\">展厅未找到: {topic}</p>", title="未知展厅"))

    # Load main content
    filepath = f"notebooks/{exhibit_info['notebook']}.md" if 'notebook' in exhibit_info else None
    content_html = await _read_md(filepath) if filepath else ""

    # Load tabbed content
    tab_content = {}
    tab_dir = CONTENT_DIR / "exhibits" / topic
    for tab_name in ["applications", "history", "beauty", "explore"]:
        tab_file = tab_dir / f"{tab_name}.md"
        if tab_file.exists():
            tab_content[tab_name] = await _read_md(str(tab_file.relative_to(CONTENT_DIR)))

    return templates.TemplateResponse("pages/exhibit.html", _ctx(request,
        content_html=content_html, title=exhibit_info.get("zh", topic),
        exhibit=exhibit_info, topic_key=topic, tab=tab, tab_content=tab_content))


@router.get("/mathematicians", response_class=HTMLResponse)
async def mathematicians_list(request: Request):
    return templates.TemplateResponse("pages/mathematicians.html", _ctx(request))


@router.get("/mathematicians/{key}", response_class=HTMLResponse)
async def mathematician_detail(request: Request, key: str):
    m = settings.mathematicians.get(key, {})
    if not m:
        return templates.TemplateResponse("pages/content.html", _ctx(request,
            content_html="<p class=\"content-error\">数学家未找到</p>", title="未知"))
    return templates.TemplateResponse("pages/mathematician.html", _ctx(request, m=m, key=key))


@router.get("/workshop", response_class=HTMLResponse)
async def workshop_page(request: Request):
    return templates.TemplateResponse("pages/workshop.html", _ctx(request))


@router.get("/gallery", response_class=HTMLResponse)
async def gallery_page(request: Request):
    return templates.TemplateResponse("pages/gallery.html", _ctx(request))


@router.get("/fractal", response_class=HTMLResponse)
async def fractal_page(request: Request):
    return templates.TemplateResponse("pages/fractal.html", _ctx(request))


@router.get("/practice", response_class=HTMLResponse)
@router.get("/practice/{topic}", response_class=HTMLResponse)
async def practice_page(request: Request, topic: str = "limits"):
    exhibit_info = settings.exhibits.get(topic, {})
    summaries = problem_bank.list_problem_summaries(topic)
    gaoshu_subtopics = sorted(
        [(k, v) for k, v in settings.exhibits.items() if k != "gaoshu" and v.get("parent") == "gaoshu"],
        key=lambda kv: kv[1].get("order", 99)
    )
    return templates.TemplateResponse("pages/practice.html", _ctx(request,
        topic_key=topic, topic=exhibit_info or {"zh": topic}, problems=summaries, count=len(summaries), gaoshu_subtopics=gaoshu_subtopics))
