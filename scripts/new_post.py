#!/usr/bin/env python3
"""
Create a new news post with proper frontmatter, then optionally deploy to ECS.

Usage:
    python scripts/new_post.py                     # interactive: prompts for fields
    python scripts/new_post.py --title "标题" --date 2026-07-23 --category 数学 --deploy
    python scripts/new_post.py --slug my-post --deploy   # only write body manually

Frontmatter written:
    ---
    title: <title>
    date: <YYYY-MM-DD>
    category: <category>
    author: 数学博物馆
    ---
"""

import argparse
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

NEWS_DIR = Path(__file__).resolve().parent.parent / "content" / "news"
DEPLOY_USER = "root"
DEPLOY_HOST = "8.137.78.250"
DEPLOY_DIR = "/opt/apps/mathlearnlab/content/news/"


def slugify(title: str) -> str:
    """ASCII-safe slug for URLs. Chinese titles fall back to post-YYYYMMDD."""
    s = title.strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    if s:
        return s
    return f"post-{date.today().strftime('%Y%m%d')}"


def validate_date(d: str) -> str:
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", d):
        raise SystemExit(f"Invalid date '{d}'. Use YYYY-MM-DD, e.g. 2026-07-23")
    return d


def build_frontmatter(title: str, d: str, category: str, author: str) -> str:
    return (
        "---\n"
        f"title: {title}\n"
        f"date: {d}\n"
        f"category: {category}\n"
        f"author: {author}\n"
        "---\n"
    )


def deploy_file(path: Path) -> bool:
    user_host = f"{DEPLOY_USER}@{DEPLOY_HOST}"
    cmd = [
        "scp", "-o", "StrictHostKeyChecking=no",
        str(path), f"{user_host}:{DEPLOY_DIR}",
    ]
    try:
        print(f"Deploying to {user_host}:{DEPLOY_DIR} ...")
        subprocess.run(cmd, check=True)
        print("Deployed. (Note: server reads files live; no restart needed.)")
        return True
    except FileNotFoundError:
        print("scp not found; deploy skipped. Upload manually.")
        return False
    except subprocess.CalledProcessError:
        print("scp failed; deploy skipped. Upload manually.")
        return False


def main():
    parser = argparse.ArgumentParser(description="Create a news post markdown file.")
    parser.add_argument("--title", help="Post title")
    parser.add_argument("--date", help="Post date YYYY-MM-DD (default: today)")
    parser.add_argument("--category", default="数学", help="Category (default: 数学)")
    parser.add_argument("--author", default="数学博物馆", help="Author (default: 数学博物馆)")
    parser.add_argument("--slug", help="Slug / filename stem (default: derived from title)")
    parser.add_argument("--deploy", action="store_true", help="scp to ECS after writing")
    args = parser.parse_args()

    title = args.title or input("标题 (title): ").strip() or "未命名"
    d = validate_date(args.date or input(f"日期 (date, 默认 {date.today()}): ").strip() or str(date.today()))
    slug = args.slug or slugify(title)

    category = args.category
    if not category:
        category = input("分类 (category, 默认 数学): ").strip() or "数学"

    news_dir = NEWS_DIR
    news_dir.mkdir(parents=True, exist_ok=True)
    path = news_dir / f"{slug}.md"
    if path.exists():
        print(f"⚠️  {path} 已存在，将追加内容（不覆盖 frontmatter）")

    front = build_frontmatter(title, d, category, args.author)

    if not path.exists():
        path.write_text(front + "\n", encoding="utf-8")
        print(f"✅ 已创建: {path}")
    else:
        print(f"📄 文件已存在: {path}")

    print("\n--- frontmatter ---")
    print(front)
    print("--- 正文写在这个文件里（支持 LaTeX $...$ / $$...$$ 和 Markdown） ---")

    if args.deploy:
        deploy_file(path)


if __name__ == "__main__":
    main()
