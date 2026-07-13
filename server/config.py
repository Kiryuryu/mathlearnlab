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
        "gaoshu":        {"zh": "微积分的世界", "icon": "📐",
                          "historian": "牛顿、莱布尼茨、柯西、欧拉…",
                          "big_question": "变化、累积、无穷——微积分如何改变了人类理解世界的方式？",
                          "beauty": "微积分是人类思想史上最伟大的成就之一。从芝诺的飞矢不动悖论，到牛顿和莱布尼茨的激烈争论，到柯西用ε-δ语言为它打下坚实根基——这是一个跨越两千年的故事。"},
        "limits":        {"zh": "极限 — 无限逼近的艺术", "icon": "∞", "json": "limits.json",
                          "parent": "gaoshu", "order": 1,
                          "historian": "柯西、魏尔斯特拉斯",
                          "big_question": "如何用数学语言精确描述'无限接近'？",
                          "beauty": "ε-δ 定义用有限的符号捕捉了无穷的直觉",
                          "notebook": "01-gaoshu/01-limits-continuity-differentiation"},
        "derivatives":   {"zh": "导数 — 瞬间的变化率",   "icon": "∆", "json": "derivatives.json",
                          "parent": "gaoshu", "order": 2,
                          "historian": "费马、牛顿、莱布尼茨",
                          "big_question": "如何在某一瞬间测量变化？",
                          "beauty": "泰勒展开：任何光滑函数都可以用多项式逼近",
                          "notebook": "01-gaoshu/01-limits-continuity-differentiation"},
        "integrals":     {"zh": "积分 — 和的极限",       "icon": "∫", "json": "integrals.json",
                          "parent": "gaoshu", "order": 3,
                          "historian": "阿基米德、黎曼、勒贝格",
                          "big_question": "如何求一个曲线下方不规则图形的面积？",
                          "beauty": "微积分基本定理：微分和积分是互逆运算——这是数学史上最伟大的发现之一",
                          "notebook": "01-gaoshu/02-integration"},
        "series":        {"zh": "无穷级数 — 无限的拼图",  "icon": "∑", "json": "series.json",
                          "parent": "gaoshu", "order": 4,
                          "historian": "欧拉、傅里叶",
                          "big_question": "无穷多个数加起来可以是有限的吗？",
                          "beauty": "巴塞尔问题：1+1/4+1/9+1/16+... = π²/6 —— 自然数的倒数平方和竟然与圆周率有关",
                          "notebook": "01-gaoshu/03-infinite-series"},
        "multivariable": {"zh": "多元微积分 — 从平面到空间","icon": "∂", "json": "multivariable.json",
                          "parent": "gaoshu", "order": 5,
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

    # ── Mathematicians ──
    mathematicians: dict = {
        "newton": {
            "name": "艾萨克·牛顿",
            "name_en": "Isaac Newton",
            "years": "1643–1727",
            "icon": "N",
            "contributions": "微积分、万有引力定律、光学",
            "story": "1665年，剑桥因瘟疫关闭，23岁的牛顿回到乡下。在18个月里，他发明了微积分（他称之为\"流数法\"）——这可以计算任意瞬间的变化率。他还发现了万有引力定律，并证明白光由多种颜色组成。这18个月被称为科学史上最富有成果的\"奇迹年\"。",
            "quote": "如果说我看得比别人更远，那是因为我站在巨人的肩膀上。",
            "exhibits": ["derivatives", "integrals"],
        },
        "leibniz": {
            "name": "戈特弗里德·莱布尼茨",
            "name_en": "Gottfried Leibniz",
            "years": "1646–1716",
            "icon": "L",
            "contributions": "微积分符号系统（∫, d/dx）、二进制、哲学",
            "story": "莱布尼茨独立于牛顿发明了微积分，但他设计的符号系统——∫ 表示积分、d/dx 表示微分——比牛顿的\"流数法\"符号优雅得多，至今仍在被全世界使用。这引发了一场关于\"谁先发明微积分\"的激烈争论，延续了数十年。历史对两个人的贡献都给予了高度认可。",
            "quote": "∫ 是一个最美的字母，它把无穷细小的部分加总成完整的整体。",
            "exhibits": ["derivatives", "integrals", "series"],
        },
        "euler": {
            "name": "莱昂哈德·欧拉",
            "name_en": "Leonhard Euler",
            "years": "1707–1783",
            "icon": "E",
            "contributions": "e^(iπ)+1=0、图论、流体力学、分析学",
            "story": "欧拉是历史上最高产的数学家——他发表了超过850篇论文和著作。即使在双目失明的最后17年，他依然以惊人的速度产出数学成果。他发现了最美公式 e^(iπ)+1=0，将五个最重要的数学常数统一在一个方程中。他还解决了著名的巴塞尔问题：1+1/4+1/9+1/16+... = π²/6。",
            "quote": "数学是真实世界的语言，上帝用它书写了宇宙。",
            "exhibits": ["series", "integrals", "multivariable"],
        },
        "gauss": {
            "name": "卡尔·弗里德里希·高斯",
            "name_en": "Carl Friedrich Gauss",
            "years": "1777–1855",
            "icon": "G",
            "contributions": "数论、正态分布、最小二乘法、曲面理论",
            "story": "高斯3岁时就能纠正父亲的算术错误；10岁时，老师让全班算1+2+...+100，他几秒内就发现了配对法(1+100)×50=5050。成年后，他几乎在所有数学分支都做出了深远贡献。他发明的\"最小二乘法\"至今是数据拟合的基石；他的曲面理论为后来的爱因斯坦广义相对论铺平了道路。",
            "quote": "数学是科学的皇后，数论是数学的皇后。",
            "exhibits": ["integrals", "multivariable", "series"],
        },
        "fourier": {
            "name": "约瑟夫·傅里叶",
            "name_en": "Joseph Fourier",
            "years": "1768–1830",
            "icon": "F",
            "contributions": "傅里叶级数、傅里叶变换、热传导方程",
            "story": "傅里叶在研究热传导时提出了一个疯狂的想法：任何周期函数都可以表示成正弦波和余弦波的无穷和。当时绝大多数数学家认为这不可能，但他坚持了自己的发现。今天，傅里叶变换是现代世界最重要的数学工具之一——MP3音频压缩、JPEG图片、5G通信、量子力学都依赖它。",
            "quote": "对自然的深入研究是数学发现最肥沃的土壤。",
            "exhibits": ["series", "derivatives"],
        },
        "ramanujan": {
            "name": "斯里尼瓦瑟·拉马努金",
            "name_en": "Srinivasa Ramanujan",
            "years": "1887–1920",
            "icon": "R",
            "contributions": "无穷级数、整数分拆、模形式、π的公式",
            "story": "拉马努金出身于印度贫困家庭，几乎完全靠自学。他用粉笔在石板上计算，在笔记本上记录了近4000个惊人的公式——没有任何证明，但他声称\"女神在梦中告诉他这些结果\"。1913年他写信给英国数学家哈代，哈代看后大惊失色，说\"这些公式一定是对的，因为没有人能编造出这么复杂的东西\"。他32岁英年早逝，但他的笔记至今仍然在被研究。",
            "quote": "一个方程对我没有意义，除非它表达的是上帝的思想。",
            "exhibits": ["series", "integrals"],
        },
        "cauchy_weierstrass": {
            "name": "柯西 & 魏尔斯特拉斯",
            "name_en": "Cauchy & Weierstrass",
            "years": "1789–1857 / 1815–1897",
            "icon": "C",
            "contributions": "ε-δ极限定义、分析严密化、复分析",
            "story": "牛顿和莱布尼茨发明微积分后，\"无穷小量\"到底是不是零这个问题困扰了数学家们近200年。柯西率先用不等式而非模糊的\"无穷小\"来定义极限。魏尔斯特拉斯进一步完善了这个方法，发明了著名的 ε-δ 定义。从此，微积分终于有了牢不可破的逻辑基础——数学分析诞生了。",
            "quote": "数学的本质不在于数字，而在于严密的逻辑推理。 — 魏尔斯特拉斯",
            "exhibits": ["limits"],
        },
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
            "section": "微积分",
            "entries": [
                {"label": "微积分的世界", "route": "/gaoshu"},
                {"label": "极限 — 无限逼近", "route": "/exhibit/limits"},
                {"label": "导数 — 瞬间变化率", "route": "/exhibit/derivatives"},
                {"label": "积分 — 和的极限", "route": "/exhibit/integrals"},
                {"label": "无穷级数 — 无限拼图", "route": "/exhibit/series"},
                {"label": "多元微积分 — 从平面到空间", "route": "/exhibit/multivariable"},
            ],
        },
        {
            "section": "数学家长廊",
            "entries": [
                {"label": "牛顿 & 莱布尼茨", "route": "/mathematicians/newton"},
                {"label": "欧拉", "route": "/mathematicians/euler"},
                {"label": "高斯", "route": "/mathematicians/gauss"},
                {"label": "傅里叶", "route": "/mathematicians/fourier"},
                {"label": "柯西 & 魏尔斯特拉斯", "route": "/mathematicians/cauchy_weierstrass"},
                {"label": "拉马努金", "route": "/mathematicians/ramanujan"},
            ],
        },
        {
            "section": "工具",
            "entries": [
                {"label": "🎨 函数工坊", "route": "/workshop"},
                {"label": "🧪 动手实验室", "route": "/practice/integrals"},
            ],
        },
    ]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}
    """pydantic model config"""


def get_settings_dict() -> dict:
    """Return settings as plain dict for Jinja2 template context.
    Must convert nested dicts and non-serializable values to plain types."""
    s = settings
    gaoshu_subtopics = sorted(
        [(k, v) for k, v in s.exhibits.items() if k != "gaoshu"],
        key=lambda kv: kv[1].get("order", 99)
    )
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
        "gaoshu_subtopics": gaoshu_subtopics,
    }


settings = Settings()
