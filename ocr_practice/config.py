"""
Configuration for the OCR practice Streamlit app.
"""

# ── Claude API ──
MODEL_ID = "claude-sonnet-4-20250514"
MAX_GRADING_TOKENS = 2000
MAX_PROBLEM_GENERATION_TOKENS = 8000

# ── Image ──
MAX_IMAGE_BYTES = 5 * 1024 * 1024  # 5 MB before compression
IMAGE_QUALITY = 85  # JPEG quality when compressing

# ── Topics ──
TOPICS = {
    "limits": {
        "zh": "极限与连续",
        "icon": "📈",
        "json": "limits.json",
        "description": "极限定义、左右极限、连续性、间断点",
    },
    "derivatives": {
        "zh": "微分学",
        "icon": "📉",
        "json": "derivatives.json",
        "description": "导数定义、求导法则、中值定理、泰勒公式",
    },
    "integrals": {
        "zh": "积分学",
        "icon": "∫",
        "json": "integrals.json",
        "description": "不定积分、定积分、换元法、分部积分、应用",
    },
    "series": {
        "zh": "无穷级数",
        "icon": "Σ",
        "json": "series.json",
        "description": "数项级数审敛、幂级数、傅里叶级数",
    },
    "multivariable": {
        "zh": "多元微积分",
        "icon": "🌐",
        "json": "multivariable.json",
        "description": "偏导数、梯度、二重积分、线面积分",
    },
}

# ── Difficulty ──
DIFFICULTY = {
    "easy": {"zh": "简单", "stars": "⭐", "color": "green"},
    "medium": {"zh": "中等", "stars": "⭐⭐", "color": "orange"},
    "hard": {"zh": "困难", "stars": "⭐⭐⭐", "color": "red"},
}
