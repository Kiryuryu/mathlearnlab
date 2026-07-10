"""
Matplotlib plotting configuration for MathLearnLab.

Applies consistent styling across all notebooks:
  - Chinese font support (SimHei / Noto Sans SC)
  - LaTeX rendering for math expressions
  - Consistent color palette and figure defaults
  - Seaborn style base
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np


# ── Color palette ──────────────────────────────────────────────────
# Accessible, colorblind-friendly palette
COLORS = {
    "blue":   "#1f77b4",
    "orange": "#ff7f0e",
    "green":  "#2ca02c",
    "red":    "#d62728",
    "purple": "#9467bd",
    "brown":  "#8c564b",
    "pink":   "#e377c2",
    "gray":   "#7f7f7f",
    "olive":  "#bcbd22",
    "cyan":   "#17becf",
}

COLOR_CYCLE = list(COLORS.values())


def _detect_chinese_font():
    """Find an available Chinese-capable font on the system."""
    candidates = [
        "PingFang SC",        # macOS (preferred — clean and always available)
        "Heiti SC",           # macOS fallback
        "STHeiti",            # macOS older
        "Noto Sans SC",       # cross-platform
        "Noto Sans CJK SC",   # cross-platform
        "WenQuanYi Micro Hei",# Linux
        "SimHei",             # Windows
        "Microsoft YaHei",    # Windows
        "Arial Unicode MS",   # macOS
    ]
    available = {f.name for f in mpl.font_manager.fontManager.ttflist}
    for font in candidates:
        if font in available:
            return font
    return "sans-serif"


def set_style():
    """Apply the MathLearnLab plotting style.

    Call this once at the top of every notebook after importing matplotlib.
    """
    # Base style
    plt.style.use("seaborn-v0_8-whitegrid")

    chinese_font = _detect_chinese_font()

    mpl.rcParams.update({
        # ── Font ──
        "font.family":      "sans-serif",
        "font.sans-serif":  [chinese_font, "DejaVu Sans", "Arial", "Helvetica"],
        "font.size":        12,
        "axes.titlesize":   15,
        "axes.labelsize":   13,
        "xtick.labelsize":  11,
        "ytick.labelsize":  11,
        "legend.fontsize":  11,

        # ── LaTeX for math ──
        "text.usetex":          False,   # keep False for simplicity; use mathtext
        "mathtext.fontset":     "dejavusans",

        # ── Figure ──
        "figure.figsize":       (10, 6),
        "figure.dpi":           100,
        "figure.facecolor":     "white",
        "axes.facecolor":       "#f8f9fa",
        "axes.edgecolor":       "#333333",
        "axes.grid":            True,
        "grid.alpha":           0.3,
        "grid.linestyle":       "--",
        "axes.prop_cycle":      mpl.cycler(color=COLOR_CYCLE),

        # ── Lines ──
        "lines.linewidth":      2.0,
        "lines.markersize":     6,

        # ── Legend ──
        "legend.frameon":       True,
        "legend.framealpha":    0.9,
        "legend.edgecolor":     "#cccccc",

        # ── Save ──
        "savefig.bbox":         "tight",
        "savefig.dpi":          150,
        "savefig.facecolor":    "white",
    })


def annotate_point(ax, x, y, text, offset=(10, 10), **kwargs):
    """Add a text annotation pointing to a specific (x, y) coordinate.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
    x, y : float
        Coordinate of the point to annotate.
    text : str
        Annotation text.
    offset : tuple
        (dx, dy) in points from the point.
    """
    defaults = dict(
        xytext=offset,
        textcoords="offset points",
        arrowprops=dict(arrowstyle="->", color="gray", lw=1.2),
        fontsize=11,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.85, edgecolor="gray"),
    )
    defaults.update(kwargs)
    ax.annotate(text, (x, y), **defaults)


def set_3d_style(ax):
    """Apply clean styling to a 3D matplotlib axis."""
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor('white')
    ax.yaxis.pane.set_edgecolor('white')
    ax.zaxis.pane.set_edgecolor('white')
    ax.grid(True, alpha=0.3)
