"""
MathLearnLab server configuration via pydantic-settings.
Reads from environment variables or .env file.
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── Server ──
    app_name: str = "数学博物馆"
    app_subtitle: str = "知其然，知其所以然"
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

    # ── Auth / JWT ──
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24  # 24 hours

    # ── Museum Exhibits ──
    exhibits: dict = {
        "limits":        {"zh": "极限 — 无限逼近的艺术", "icon": "∞", "json": "limits.json",
                          "historian": "柯西、魏尔斯特拉斯",
                          "big_question": "如何用数学语言精确描述'无限接近'？",
                          "beauty": "ε-δ 定义用有限的符号捕捉了无穷的直觉",
                          "notebook": "01-gaoshu/01-limits-continuity-differentiation"},
        "derivatives":   {"zh": "导数 — 瞬间的变化率",   "icon": "∆", "json": "derivatives.json",
                          "historian": "费马、牛顿、莱布尼茨",
                          "big_question": "如何在某一瞬间测量变化？",
                          "beauty": "泰勒展开：任何光滑函数都可以用多项式逼近",
                          "notebook": "01-gaoshu/01-limits-continuity-differentiation"},
        "integrals":     {"zh": "积分 — 和的极限",       "icon": "∫", "json": "integrals.json",
                          "historian": "阿基米德、黎曼、勒贝格",
                          "big_question": "如何求一个曲线下方不规则图形的面积？",
                          "beauty": "微积分基本定理：微分和积分是互逆运算——这是数学史上最伟大的发现之一",
                          "notebook": "01-gaoshu/02-integration"},
        "series":        {"zh": "无穷级数 — 无限的拼图",  "icon": "∑", "json": "series.json",
                          "historian": "欧拉、傅里叶",
                          "big_question": "无穷多个数加起来可以是有限的吗？",
                          "beauty": "巴塞尔问题：1+1/4+1/9+1/16+... = π²/6 —— 自然数的倒数平方和竟然与圆周率有关",
                          "notebook": "01-gaoshu/03-infinite-series"},
        "multivariable": {"zh": "多元微积分 — 从平面到空间","icon": "∂", "json": "multivariable.json",
                          "historian": "拉格朗日、高斯、格林",
                          "big_question": "如何在多维世界中理解变化、极值和流动？",
                          "beauty": "梯度下降：沿着最陡峭的方向下山——这个概念今天驱动着所有AI的学习",
                          "notebook": "01-gaoshu/04-multivariable-calculus"},
    }

    difficulty: dict = {
        "easy":   {"zh": "简单", "stars": "★"},
        "medium": {"zh": "中等", "stars": "★★"},
        "hard":   {"zh": "困难", "stars": "★★★"},
    }

    # ── Navigation tree — Museum floor plan ──
    nav_tree: list[dict] = [
        {
            "section": "序幕",
            "entries": [
                {"label": "序幕大厅", "route": "/"},
            ],
        },
        {
            "section": "展厅",
            "entries": [
                {"label": "第一展厅：极限", "route": "/exhibit/limits"},
                {"label": "第二展厅：导数", "route": "/exhibit/derivatives"},
                {"label": "第三展厅：积分", "route": "/exhibit/integrals"},
                {"label": "第四展厅：无穷级数", "route": "/exhibit/series"},
                {"label": "第五展厅：多元微积分", "route": "/exhibit/multivariable"},
            ],
        },
        {
            "section": "动手实验室",
            "entries": [
                {"label": "极限与连续", "route": "/practice/limits"},
                {"label": "微分学", "route": "/practice/derivatives"},
                {"label": "积分学", "route": "/practice/integrals"},
                {"label": "无穷级数", "route": "/practice/series"},
                {"label": "多元微积分", "route": "/practice/multivariable"},
            ],
        },
    ]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}
    """pydantic model config"""


def get_settings_dict() -> dict:
    """Return settings as plain dict for Jinja2 template context.
    Must convert nested dicts and non-serializable values to plain types."""
    s = settings
    return {
        "app_name": s.app_name,
        "app_subtitle": s.app_subtitle,
        "debug": s.debug,
        "content_dir": s.content_dir,
        "data_dir": s.data_dir,
        "default_model": s.default_model,
        "fast_model": s.fast_model,
        "exhibits": s.exhibits,
        "difficulty": s.difficulty,
        "nav_tree": s.nav_tree,
    }


settings = Settings()
