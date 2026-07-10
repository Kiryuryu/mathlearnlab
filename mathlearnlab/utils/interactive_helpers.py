"""
Interactive visualization helpers for MathLearnLab.

Wraps common ipywidgets + matplotlib/plotly patterns into reusable components
so notebooks don't repeat boilerplate.
"""

import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, IntSlider, Play, jslink, VBox, HBox, Output
import plotly.graph_objects as go


# ── General-purpose interact wrappers ───────────────────────────────

def function_slider(f, param_name, param_range, x_range=(-3, 3), n_points=400,
                    fixed_params=None, title=None):
    """Create an interactive plot of f(x; param) with a slider for one parameter.

    Parameters
    ----------
    f : callable
        Function with signature f(x, **params) -> y.
    param_name : str
        Name of the parameter to vary.
    param_range : tuple (min, max, step)
    x_range : tuple (xmin, xmax)
    n_points : int
        Number of sample points.
    fixed_params : dict or None
        Other keyword arguments passed to f.
    title : str or None
        Plot title.

    Example
    -------
    >>> function_slider(lambda x, a: np.sin(a * x), "a", (0.5, 3, 0.1))
    """
    if fixed_params is None:
        fixed_params = {}

    x = np.linspace(x_range[0], x_range[1], n_points)

    def plot_func(param_val):
        y = f(x, **{param_name: param_val}, **fixed_params)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, y, lw=2)
        ax.axhline(y=0, color='gray', lw=0.5)
        ax.axvline(x=0, color='gray', lw=0.5)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        if title:
            ax.set_title(f"{title}  ({param_name} = {param_val:.2f})")
        ax.set_ylim(np.min(y) - 0.5, np.max(y) + 0.5)
        plt.show()

    pmin, pmax, pstep = param_range
    interact(plot_func, param_val=FloatSlider(min=pmin, max=pmax, step=pstep, value=pmin))


def two_param_slider_plot(f, param1, param2, x_range=(-3, 3), n_points=400,
                          fixed_params=None, title=None):
    """Interactive plot with two sliders.

    Parameters
    ----------
    f : callable
        f(x, p1, p2, **fixed) -> y
    param1 : dict with keys name, range (min, max, step), start
    param2 : dict
    """
    if fixed_params is None:
        fixed_params = {}

    x = np.linspace(x_range[0], x_range[1], n_points)

    def plot_func(val1, val2):
        y = f(x, **{param1["name"]: val1, param2["name"]: val2}, **fixed_params)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, y, lw=2)
        ax.axhline(y=0, color='gray', lw=0.5)
        ax.axvline(x=0, color='gray', lw=0.5)
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        t = f"{title}  " if title else ""
        ax.set_title(f"{t}({param1['name']} = {val1:.2f}, {param2['name']} = {val2:.2f})")
        plt.show()

    interact(
        plot_func,
        val1=FloatSlider(min=param1["range"][0], max=param1["range"][1],
                         step=param1["range"][2], value=param1.get("start", param1["range"][0]),
                         description=param1["name"]),
        val2=FloatSlider(min=param2["range"][0], max=param2["range"][1],
                         step=param2["range"][2], value=param2.get("start", param2["range"][0]),
                         description=param2["name"]),
    )


# ── Sequence / Series helpers ───────────────────────────────────────

def plot_sequence_terms(seq_func, n_max=50, title="数列项"):
    """Plot the terms of a sequence a_n as a scatter plot with connecting line.

    Parameters
    ----------
    seq_func : callable
        a_n = seq_func(n), n >= 1.
    n_max : int
        Number of terms to compute.
    title : str
    """
    n = np.arange(1, n_max + 1)
    a = np.array([seq_func(i) for i in n])

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.scatter(n, a, s=30, zorder=3)
    ax.plot(n, a, lw=1, alpha=0.5, zorder=2)
    ax.axhline(y=np.array(a[-10:]).mean(), color='red', ls='--', lw=1,
               label=f'最后10项均值 = {np.mean(a[-10:]):.4f}')
    ax.set_xlabel("n")
    ax.set_ylabel("a_n")
    ax.set_title(title)
    ax.legend()
    plt.show()


def plot_partial_sums(seq_func, n_max=30, title="部分和序列"):
    """Plot the sequence of partial sums S_N = sum_{n=1}^N a_n.

    Parameters
    ----------
    seq_func : callable
        a_n = seq_func(n)
    n_max : int
    title : str
    """
    n = np.arange(1, n_max + 1)
    a = np.array([seq_func(i) for i in n])
    S = np.cumsum(a)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Terms
    ax1.bar(n, a, color='steelblue', alpha=0.7)
    ax1.axhline(y=0, color='gray', lw=0.5)
    ax1.set_xlabel("n")
    ax1.set_ylabel("a_n")
    ax1.set_title(f"{title} — 通项")

    # Partial sums
    ax2.plot(n, S, 'o-', lw=1.5, markersize=3, color='darkorange')
    ax2.axhline(y=S[-1], color='red', ls='--', lw=1, label=f'S∞ ≈ {S[-1]:.4f}')
    ax2.set_xlabel("N")
    ax2.set_ylabel("S_N")
    ax2.set_title(f"{title} — 部分和")
    ax2.legend()

    plt.tight_layout()
    plt.show()


# ── Plotly 3D helpers ───────────────────────────────────────────────

def surface_3d(f, x_range=(-3, 3), y_range=(-3, 3), n=80,
               title="z = f(x, y)", colorscale="Viridis"):
    """Create an interactive 3D surface plot with Plotly.

    Parameters
    ----------
    f : callable
        z = f(x, y) — must accept meshgrid arrays.
    x_range, y_range : tuple
    n : int
        Grid resolution.
    title : str
    colorscale : str

    Returns
    -------
    plotly.graph_objects.Figure
    """
    x = np.linspace(x_range[0], x_range[1], n)
    y = np.linspace(y_range[0], y_range[1], n)
    X, Y = np.meshgrid(x, y)
    Z = f(X, Y)

    fig = go.Figure(data=[
        go.Surface(z=Z, x=x, y=y, colorscale=colorscale,
                   contours={"z": {"show": True, "usecolormap": True, "project": {"z": True}}})
    ])
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="x",
            yaxis_title="y",
            zaxis_title="z",
        ),
        width=800, height=700,
    )
    return fig


def vector_field_3d(Fx, Fy, Fz, x_range=(-3, 3), y_range=(-3, 3), z_range=(-3, 3),
                    n=10, title="3D Vector Field"):
    """Plot a 3D vector field using Plotly cones.

    Parameters
    ----------
    Fx, Fy, Fz : callable
        Components F(x, y, z).
    x_range, y_range, z_range : tuple
    n : int
        Number of cones per dimension.
    title : str
    """
    x = np.linspace(x_range[0], x_range[1], n)
    y = np.linspace(y_range[0], y_range[1], n)
    z = np.linspace(z_range[0], z_range[1], n)
    X, Y, Z = np.meshgrid(x, y, z)

    U = Fx(X, Y, Z)
    V = Fy(X, Y, Z)
    W = Fz(X, Y, Z)

    fig = go.Figure(data=[
        go.Cone(x=X.flatten(), y=Y.flatten(), z=Z.flatten(),
                u=U.flatten(), v=V.flatten(), w=W.flatten(),
                sizemode="absolute", sizeref=2,
                colorscale="Viridis")
    ])
    fig.update_layout(
        title=title,
        scene=dict(xaxis_title="x", yaxis_title="y", zaxis_title="z"),
        width=800, height=700,
    )
    return fig


# ── Animation helpers ───────────────────────────────────────────────

def animate_sequence_frames(frame_generator, n_frames=50, interval=100):
    """Create a matplotlib animation from a frame generator.

    Parameters
    ----------
    frame_generator : callable
        A function that takes frame index i (0..n_frames-1) and returns
        a dict of {artist: new_data} or calls plotting code on an axis.
    n_frames : int
    interval : int
        Milliseconds between frames.

    Returns
    -------
    matplotlib.animation.FuncAnimation

    Note: For actual use in a notebook, see the animation patterns in
    notebooks; this is a thin wrapper.
    """
    from matplotlib.animation import FuncAnimation

    fig, ax = plt.subplots()

    def init():
        # Initial empty plot — frame 0 will set up artists
        pass

    def update(frame):
        ax.clear()
        frame_generator(ax, frame)

    ani = FuncAnimation(fig, update, frames=n_frames, init_func=init,
                        interval=interval, blit=False)
    plt.close()  # prevent duplicate display
    return ani
