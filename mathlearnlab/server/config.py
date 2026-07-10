"""
MathLearnLab server configuration via pydantic-settings.
Reads from environment variables or .env file.
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── Server ──
    app_name: str = "MathLearnLab"
    debug: bool = False
    host: str = "127.0.0.1"
    port: int = 8000

    # ── Paths ──
    content_dir: str = "content"
    data_dir: str = "data"

    # ── Anthropic API ──
    anthropic_api_key: str = ""
    default_model: str = "claude-sonnet-4-20250514"
    fast_model: str = "claude-haiku-4-5-20251001"
    max_grading_tokens: int = 2000
    max_chat_tokens: int = 4096

    # ── Topics ──
    topics: dict = {
        "limits":        {"zh": "极限与连续", "icon": "§", "json": "limits.json", "desc": "极限定义、左右极限、连续性、间断点"},
        "derivatives":   {"zh": "微分学",     "icon": "¶", "json": "derivatives.json", "desc": "导数定义、求导法则、中值定理、泰勒公式"},
        "integrals":     {"zh": "积分学",     "icon": "∫", "json": "integrals.json", "desc": "不定积分、定积分、换元法、分部积分、应用"},
        "series":        {"zh": "无穷级数",   "icon": "∑", "json": "series.json", "desc": "数项级数审敛、幂级数、傅里叶级数"},
        "multivariable": {"zh": "多元微积分", "icon": "∂", "json": "multivariable.json", "desc": "偏导数、梯度、二重积分、线面积分"},
    }

    difficulty: dict = {
        "easy":   {"zh": "简单", "stars": "★"},
        "medium": {"zh": "中等", "stars": "★★"},
        "hard":   {"zh": "困难", "stars": "★★★"},
    }

    # ── Navigation tree ──
    nav_tree: list[dict] = [
        {
            "section": "高等数学",
            "entries": [
                {"label": "极限、连续与微分", "route": "/notebooks/01-gaoshu/01-limits-continuity-differentiation"},
                {"label": "积分学",            "route": "/notebooks/01-gaoshu/02-integration"},
                {"label": "无穷级数",          "route": "/notebooks/01-gaoshu/03-infinite-series"},
                {"label": "多元微积分",         "route": "/notebooks/01-gaoshu/04-multivariable-calculus"},
            ],
        },
        {
            "section": "知识笔记",
            "entries": [
                {"label": "高等数学", "route": "/notes/01-gaoshu/README"},
                {"label": "线性代数", "route": "/notes/02-xiandai/README"},
                {"label": "概率论",   "route": "/notes/03-gailvlun/README"},
            ],
        },
        {
            "section": "解题集",
            "entries": [
                {"label": "极限与连续", "route": "/problems/01-gaoshu/limits-problems"},
                {"label": "积分学",    "route": "/problems/01-gaoshu/integration-problems"},
                {"label": "无穷级数",  "route": "/problems/01-gaoshu/series-problems"},
                {"label": "多元微积分", "route": "/problems/01-gaoshu/multivariable-problems"},
            ],
        },
        {
            "section": "错题本",
            "entries": [
                {"label": "高等数学", "route": "/error-log"},
            ],
        },
        {
            "section": "OCR 刷题",
            "entries": [
                {"label": "极限与连续", "route": "/practice/limits"},
                {"label": "微分学",     "route": "/practice/derivatives"},
                {"label": "积分学",     "route": "/practice/integrals"},
                {"label": "无穷级数",   "route": "/practice/series"},
                {"label": "多元微积分", "route": "/practice/multivariable"},
            ],
        },
    ]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
