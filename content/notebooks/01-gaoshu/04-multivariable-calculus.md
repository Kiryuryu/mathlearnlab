# 第四章：多元微积分

## 学习目标

- 直观理解二元函数的曲面与等高线
- 理解偏导数、方向导数、梯度的几何意义
- 感受梯度下降的寻路过程
- 理解拉格朗日乘数法的几何本质
- 掌握二重积分的累次积分思想
- 理解线积分与向量场的关系

## 预备知识

- 一元微积分的基本概念（导数、积分）
- 向量与空间解析几何基础
- 偏导数的定义与计算

> 💡 **提示**：本页面由 Jupyter Notebook 自动转换而来。
> 运行 `jupyter lab` 启动本地环境，可体验完整的**交互式可视化**（拖动滑块、3D旋转、动画播放）。
> 下方代码块仅供参考，静态页面无法执行 Python。

---

# 第四章：多元微积分

## 学习目标

- 直观理解二元函数的曲面与等高线
- 理解偏导数、方向导数、梯度的几何意义
- 感受梯度下降的寻路过程
- 理解拉格朗日乘数法的几何本质
- 掌握二重积分的累次积分思想
- 理解线积分与向量场的关系

## 预备知识

- 一元微积分的基本概念（导数、积分）
- 向量与空间解析几何基础
- 偏导数的定义与计算

```python
%matplotlib widget

import numpy as np
import matplotlib.pyplot as plt
import sympy as sp
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from ipywidgets import interact, FloatSlider, IntSlider, Dropdown, VBox, HBox
from IPython.display import display, HTML, clear_output
from scipy.optimize import minimize
import sys
sys.path.insert(0, '..')

from utils.plot_config import set_style, COLORS

set_style()
sp.init_printing()

x, y, z, t = sp.symbols('x y z t', real=True)

print("✅ 环境就绪！")
```

---
## 4.1 多元函数与曲面

> $z = f(x, y)$ 在三维空间中定义了一个**曲面**。

曲面的形状——山峰、山谷、鞍部——是理解多元微积分所有概念的出发点。

### 交互探索不同曲面 👇

```python
# === 4.1a Plotly 交互式 3D 曲面 ===

def plot_3d_surface(func_name='抛物面: z = x² + y²'):
    """用 Plotly 创建可旋转/缩放的 3D 曲面"""
    
    x_range = np.linspace(-3, 3, 80)
    y_range = np.linspace(-3, 3, 80)
    X, Y = np.meshgrid(x_range, y_range)
    
    if func_name == '抛物面: z = x² + y²':
        Z = X**2 + Y**2
        colorscale = 'Reds'
    elif func_name == '马鞍面: z = x² − y²':
        Z = X**2 - Y**2
        colorscale = 'RdBu'
    elif func_name == 'sin 波: z = sin(√(x²+y²))':
        R = np.sqrt(X**2 + Y**2)
        Z = np.sin(R)
        colorscale = 'Viridis'
    elif func_name == '山峰: z = x·exp(−x²−y²)':
        Z = X * np.exp(-X**2 - Y**2)
        colorscale = 'Earth'
    elif func_name == '墨西哥帽: z = (1−x²−y²)·exp(−(x²+y²)/2)':
        R2 = X**2 + Y**2
        Z = (1 - R2) * np.exp(-R2 / 2)
        colorscale = 'RdYlBu'
    else:
        Z = np.cos(X) * np.sin(Y)
        colorscale = 'Plasma'
    
    fig = go.Figure(data=[
        go.Surface(z=Z, x=x_range, y=y_range, colorscale=colorscale,
                   contours={"z": {"show": True, "usecolormap": True, "project": {"z": True}}},
                   opacity=0.9)
    ])
    
    fig.update_layout(
        title=func_name,
        scene=dict(
            xaxis_title='x',
            yaxis_title='y',
            zaxis_title='z',
        ),
        width=850, height=700,
    )
    
    fig.show()

surfaces = [
    '抛物面: z = x² + y²',
    '马鞍面: z = x² − y²',
    'sin 波: z = sin(√(x²+y²))',
    '山峰: z = x·exp(−x²−y²)',
    '墨西哥帽: z = (1−x²−y²)·exp(−(x²+y²)/2)',
    '网格波: z = cos(x)·sin(y)',
]

interact(plot_3d_surface,
         func_name=Dropdown(options=surfaces, value='马鞍面: z = x² − y²',
                           description='曲面'));
```

```python
# === 4.1b 等高线图 ===

def plot_contour(func_name='马鞍面: z = x² − y²'):
    """等高线是理解梯度和优化的重要工具"""
    
    x_range = np.linspace(-3, 3, 200)
    y_range = np.linspace(-3, 3, 200)
    X, Y = np.meshgrid(x_range, y_range)
    
    if func_name == '马鞍面: z = x² − y²':
        Z = X**2 - Y**2
        levels = np.arange(-8, 9, 1)
    elif func_name == '抛物面: z = x² + y²':
        Z = X**2 + Y**2
        levels = np.arange(0, 18, 1)
    elif func_name == '山峰: z = x·exp(−x²−y²)':
        Z = X * np.exp(-X**2 - Y**2)
        levels = np.linspace(-0.4, 0.4, 15)
    else:
        R2 = X**2 + Y**2
        Z = (1 - R2) * np.exp(-R2 / 2)
        levels = np.linspace(-0.3, 1.0, 15)
    
    fig, ax = plt.subplots(figsize=(9, 8))
    
    cs = ax.contour(X, Y, Z, levels=levels, cmap='RdYlBu_r', linewidths=1.5)
    ax.clabel(cs, inline=True, fontsize=9, fmt='%.1f')
    
    # 填充等高线
    ax.contourf(X, Y, Z, levels=50, cmap='RdYlBu_r', alpha=0.3)
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'等高线: {func_name}')
    ax.set_aspect('equal')
    ax.axhline(y=0, color='gray', lw=0.5, alpha=0.4)
    ax.axvline(x=0, color='gray', lw=0.5, alpha=0.4)
    
    plt.tight_layout()
    plt.show()

interact(plot_contour,
         func_name=Dropdown(options=['马鞍面: z = x² − y²', '抛物面: z = x² + y²',
                                     '山峰: z = x·exp(−x²−y²)',
                                     '墨西哥帽: z = (1−x²−y²)·exp(−(x²+y²)/2)'],
                           value='马鞍面: z = x² − y²',
                           description='曲面'));
```

**💡 关键观察**：
- 抛物面 $z=x^2+y^2$：等高线是同心圆，中心是最低点（极小值）
- 马鞍面 $z=x^2-y^2$：等高线是双曲线，中心是鞍点——x 方向是极小，y 方向是极大
- 等高线密集处 ⇒ 曲面陡峭；等高线稀疏处 ⇒ 曲面平缓

---
## 4.2 偏导数与切平面

> $f_x(x_0, y_0) = \lim_{h\to 0}\frac{f(x_0+h, y_0) - f(x_0, y_0)}{h}$（固定 $y$，对 $x$ 求导）
> $f_y(x_0, y_0) = \lim_{h\to 0}\frac{f(x_0, y_0+h) - f(x_0, y_0)}{h}$（固定 $x$，对 $y$ 求导）

偏导数的几何意义：**曲面在坐标轴方向的切线斜率**。

切平面方程：$z = f(x_0,y_0) + f_x(x_0,y_0)(x-x_0) + f_y(x_0,y_0)(y-y_0)$

```python
# 符号计算：偏导数与切平面
x_s, y_s = sp.symbols('x_s y_s', real=True)

# 示例：f(x,y) = x² + xy + y²
f = x_s**2 + x_s*y_s + y_s**2
print(f"f(x,y) = {f}")
print()

fx = sp.diff(f, x_s)
fy = sp.diff(f, y_s)
print(f"∂f/∂x = {fx}")
print(f"∂f/∂y = {fy}")
print()

# 在点 (1, 2) 处的切平面
x0, y0 = 1, 2
f0 = float(f.subs({x_s: x0, y_s: y0}))
fx0 = float(fx.subs({x_s: x0, y_s: y0}))
fy0 = float(fy.subs({x_s: x0, y_s: y0}))

print(f"在点 ({x0}, {y0}) 处:")
print(f"  f({x0},{y0}) = {f0}")
print(f"  f_x = {fx0},  f_y = {fy0}")
print(f"  切平面: z = {f0} + {fx0}(x - {x0}) + {fy0}(y - {y0})")
print(f"  即: z = {f0} + {fx0}x - {fx0*x0} + {fy0}y - {fy0*y0}")
print(f"  即: z = {fx0}x + {fy0}y + {f0 - fx0*x0 - fy0*y0}")
```

```python
# === 3D 切平面可视化 (Plotly) ===

def plot_tangent_plane(x0=0.5, y0=0.5):
    """展示曲面 z = x² + xy + y² 在 (x0, y0) 处的切平面"""
    
    f = lambda x, y: x**2 + x*y + y**2
    fx = lambda x, y: 2*x + y
    fy = lambda x, y: x + 2*y
    
    z0 = f(x0, y0)
    fx0 = fx(x0, y0)
    fy0 = fy(x0, y0)
    
    # 曲面
    xr = np.linspace(-2, 2, 60)
    yr = np.linspace(-2, 2, 60)
    X, Y = np.meshgrid(xr, yr)
    Z = f(X, Y)
    
    # 切平面
    Z_plane = z0 + fx0 * (X - x0) + fy0 * (Y - y0)
    
    # x 方向的切线 (固定 y=y0)
    xs_xdir = np.linspace(x0 - 1, x0 + 1, 30)
    ys_xdir = np.full_like(xs_xdir, y0)
    zs_xdir = z0 + fx0 * (xs_xdir - x0)
    
    # y 方向的切线 (固定 x=x0)
    ys_ydir = np.linspace(y0 - 1, y0 + 1, 30)
    xs_ydir = np.full_like(ys_ydir, x0)
    zs_ydir = z0 + fy0 * (ys_ydir - y0)
    
    fig = go.Figure()
    
    # 曲面
    fig.add_trace(go.Surface(z=Z, x=xr, y=yr, colorscale='Blues', opacity=0.6,
                             name='z = f(x,y)', showscale=False))
    
    # 切平面 (半透明)
    fig.add_trace(go.Surface(z=Z_plane, x=xr, y=yr, colorscale=[[0, 'orange'], [1, 'orange']],
                             opacity=0.5, name='切平面', showscale=False))
    
    # 切点
    fig.add_trace(go.Scatter3d(x=[x0], y=[y0], z=[z0], mode='markers',
                               marker=dict(size=8, color='red'), name='切点'))
    
    # x 方向切线
    fig.add_trace(go.Scatter3d(x=xs_xdir, y=ys_xdir, z=zs_xdir, mode='lines',
                               line=dict(color='green', width=5), name=f'x-方向切线 (斜率={fx0:.2f})'))
    
    # y 方向切线
    fig.add_trace(go.Scatter3d(x=xs_ydir, y=ys_ydir, z=zs_ydir, mode='lines',
                               line=dict(color='purple', width=5), name=f'y-方向切线 (斜率={fy0:.2f})'))
    
    fig.update_layout(
        title=f'切平面与偏导数 (x₀={x0}, y₀={y0})<br>'
              f'f_x = {fx0:.2f}, f_y = {fy0:.2f}',
        scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='z'),
        width=850, height=700,
    )
    
    fig.show()

interact(plot_tangent_plane,
         x0=FloatSlider(min=-1.5, max=1.5, step=0.1, value=0.5, description='x₀',
                        continuous_update=False),
         y0=FloatSlider(min=-1.5, max=1.5, step=0.1, value=0.5, description='y₀',
                        continuous_update=False));
```

---
## 4.3 方向导数与梯度

> **方向导数**：$D_{\mathbf{u}}f = \nabla f \cdot \mathbf{u}$（$\|\mathbf{u}\| = 1$）
> **梯度**：$\nabla f = (f_x, f_y)$

梯度的几何意义：
- 方向：函数**增长最快**的方向
- 模：该方向上的最大方向导数值
- 梯度垂直于等高线（等高线的法向量）

这是理解多元函数优化的核心概念！

```python
# === 梯度向量场 + 等高线 ===

def plot_gradient_field(func_name='马鞍面: z = x² − y²'):
    """在等高线图上叠加梯度向量场"""
    
    xr = np.linspace(-3, 3, 30)
    yr = np.linspace(-3, 3, 30)
    X, Y = np.meshgrid(xr, yr)
    
    if func_name == '马鞍面: z = x² − y²':
        Z = X**2 - Y**2
        dZ_dX = 2 * X
        dZ_dY = -2 * Y
        levels = np.arange(-8, 9, 1)
    elif func_name == '抛物面: z = x² + y²':
        Z = X**2 + Y**2
        dZ_dX = 2 * X
        dZ_dY = 2 * Y
        levels = np.arange(0, 18, 1)
    else:
        Z = X * np.exp(-X**2 - Y**2)
        dZ_dX = np.exp(-X**2 - Y**2) * (1 - 2*X**2)
        dZ_dY = -2 * X * Y * np.exp(-X**2 - Y**2)
        levels = np.linspace(-0.4, 0.4, 15)
    
    fig, ax = plt.subplots(figsize=(10, 9))
    
    # 等高线填充
    ax.contourf(X, Y, Z, levels=50, cmap='RdYlBu_r', alpha=0.25)
    # 等高线
    cs = ax.contour(X, Y, Z, levels=levels, cmap='RdYlBu_r', linewidths=1.2)
    ax.clabel(cs, inline=True, fontsize=8, fmt='%.1f')
    
    # 梯度向量场
    ax.quiver(X, Y, dZ_dX, dZ_dY, color='black', alpha=0.7,
              scale=40, width=0.003, headwidth=6)
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'梯度向量场: ∇f = (∂f/∂x, ∂f/∂y)\n{func_name}\n'
                 f'梯度方向 ⊥ 等高线，指向增长最快的方向')
    ax.set_aspect('equal')
    ax.axhline(y=0, color='gray', lw=0.5, alpha=0.4)
    ax.axvline(x=0, color='gray', lw=0.5, alpha=0.4)
    
    plt.tight_layout()
    plt.show()

interact(plot_gradient_field,
         func_name=Dropdown(options=['马鞍面: z = x² − y²',
                                     '抛物面: z = x² + y²',
                                     '山峰: z = x·exp(−x²−y²)'],
                           value='马鞍面: z = x² − y²',
                           description='曲面'));
```

**💡 关键观察**：
- 梯度向量始终**垂直于**等高线
- 对于抛物面 $z=x^2+y^2$，梯度指向外（离开原点），因为值在增大
- 对于马鞍面，梯度在 x 方向指向外、y 方向指向内

---
## 4.4 ⭐ 梯度下降可视化

> 从初始点出发，沿**负梯度方向**（最陡下降方向）走一小步，反复迭代 → 找到极小值。

梯度下降是机器学习的核心算法。理解它的几何过程对学习优化和深度学习至关重要。

```python
# === 梯度下降动画 ===

def plot_gradient_descent(start_x=-2.0, start_y=-1.5, learning_rate=0.15, n_steps=20):
    """
    对 f(x,y) = x² + 2y² (椭球抛物面) 执行梯度下降。
    同时显示在 3D 曲面和 2D 等高线上的路径。
    """
    
    # 目标函数和梯度
    f = lambda x, y: x**2 + 2 * y**2
    grad = lambda x, y: (2*x, 4*y)
    
    # 梯度下降迭代
    path_x, path_y = [start_x], [start_y]
    cx, cy = start_x, start_y
    for _ in range(n_steps):
        gx, gy = grad(cx, cy)
        cx -= learning_rate * gx
        cy -= learning_rate * gy
        path_x.append(cx)
        path_y.append(cy)
    
    path_x = np.array(path_x)
    path_y = np.array(path_y)
    path_z = f(path_x, path_y)
    
    # 曲面网格
    xr = np.linspace(-2.5, 2.5, 60)
    yr = np.linspace(-2, 2, 60)
    X, Y = np.meshgrid(xr, yr)
    Z = f(X, Y)
    
    # ── 图 1: 3D 曲面 + 下降路径 ──
    fig3d = go.Figure()
    
    fig3d.add_trace(go.Surface(z=Z, x=xr, y=yr, colorscale='Blues', opacity=0.7,
                               name='f(x,y)', showscale=False))
    
    fig3d.add_trace(go.Scatter3d(x=path_x, y=path_y, z=path_z,
                                 mode='lines+markers',
                                 line=dict(color='red', width=4),
                                 marker=dict(size=4, color='darkred'),
                                 name='下降路径'))
    
    fig3d.add_trace(go.Scatter3d(x=[path_x[0]], y=[path_y[0]], z=[path_z[0]],
                                 mode='markers',
                                 marker=dict(size=10, color='green', symbol='circle'),
                                 name='起点'))
    
    fig3d.add_trace(go.Scatter3d(x=[path_x[-1]], y=[path_y[-1]], z=[path_z[-1]],
                                 mode='markers',
                                 marker=dict(size=10, color='red', symbol='x'),
                                 name=f'终点 (z≈{path_z[-1]:.4f})'))
    
    fig3d.update_layout(
        title=f'梯度下降 3D: f(x,y) = x² + 2y², lr = {learning_rate}',
        scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='z'),
        width=800, height=650,
    )
    fig3d.show()
    
    # ── 图 2: 2D 等高线 + 下降路径 ──
    fig2d, ax = plt.subplots(figsize=(10, 8))
    
    ax.contourf(X, Y, Z, levels=50, cmap='Blues', alpha=0.4)
    cs = ax.contour(X, Y, Z, levels=np.arange(0, 15, 1), colors='steelblue', linewidths=0.8)
    ax.clabel(cs, inline=True, fontsize=8)
    
    ax.plot(path_x, path_y, 'r-o', lw=2, markersize=5, label='下降路径')
    ax.plot(path_x[0], path_y[0], 'go', markersize=12, label='起点')
    ax.plot(path_x[-1], path_y[-1], 'rx', markersize=14, markeredgewidth=2.5, label='终点')
    
    # 沿路径画出梯度方向（小箭头）
    for i in range(0, len(path_x) - 1, max(1, len(path_x)//10)):
        gx, gy = grad(path_x[i], path_y[i])
        g_norm = np.sqrt(gx**2 + gy**2)
        if g_norm > 0.001:
            ax.arrow(path_x[i], path_y[i],
                    -learning_rate * gx / g_norm * 0.3,
                    -learning_rate * gy / g_norm * 0.3,
                    head_width=0.08, head_length=0.1, fc='red', ec='red', alpha=0.6)
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'梯度下降 等高线: {n_steps} 步后 f = {path_z[-1]:.6f}')
    ax.set_aspect('equal')
    ax.legend()
    ax.axhline(y=0, color='gray', lw=0.5, alpha=0.4)
    ax.axvline(x=0, color='gray', lw=0.5, alpha=0.4)
    
    plt.tight_layout()
    plt.show()
    
    print(f"起点: ({start_x}, {start_y}), f = {f(start_x, start_y):.4f}")
    print(f"终点: ({path_x[-1]:.4f}, {path_y[-1]:.4f}), f = {path_z[-1]:.6f}")
    print(f"步数: {n_steps}, 学习率: {learning_rate}")

interact(plot_gradient_descent,
         start_x=FloatSlider(min=-2.5, max=2.5, step=0.1, value=-2.0, description='x₀',
                            continuous_update=False),
         start_y=FloatSlider(min=-2.0, max=2.0, step=0.1, value=-1.5, description='y₀',
                            continuous_update=False),
         learning_rate=FloatSlider(min=0.01, max=0.5, step=0.01, value=0.15, description='lr',
                                   continuous_update=False),
         n_steps=IntSlider(min=5, max=50, step=1, value=20, description='步数',
                           continuous_update=False));
```

**💡 关键观察**：
- 路径始终沿负梯度方向（最陡下降）
- 学习率太大 ⇒ 震荡甚至发散；太小 ⇒ 收敛慢
- 路径在 2D 等高线图上**垂直于等高线**

---
## 4.5 拉格朗日乘数法

> 求 $f(x,y)$ 在约束 $g(x,y)=0$ 下的极值：
> 解 $\nabla f = \lambda \nabla g$，即 $\nabla f \parallel \nabla g$

几何意义：**在约束曲线上，极值点处目标函数的梯度与约束函数的梯度平行**（都垂直于约束曲线）。

```python
# 符号计算：拉格朗日乘数法
x_s, y_s, lam = sp.symbols('x_s y_s lam', real=True)

print("=".center(50, "="))
print("示例: 求 f(x,y) = x² + y² 在约束 x + y = 1 下的最小值")
print("=".center(50, "="))

# f = x² + y², g(x,y) = x + y - 1 = 0
f_sym = x_s**2 + y_s**2
g_sym = x_s + y_s - 1

# Lagrange 方程组: ∇f = λ∇g  + 约束
# fx = λ·gx  →  2x = λ
# fy = λ·gy  →  2y = λ
# g = 0      →  x + y = 1

eq1 = sp.Eq(2*x_s, lam)
eq2 = sp.Eq(2*y_s, lam)
eq3 = sp.Eq(x_s + y_s, 1)

solution = sp.solve([eq1, eq2, eq3], [x_s, y_s, lam], dict=True)
print(f"解: {solution}")
print(f"→ 最小值点: x = y = 1/2, f = (1/2)² + (1/2)² = 0.5")
print(f"→ λ = 1")
print()
print("几何解释: 等高线 x²+y² = c 与直线 x+y=1 相切时取得极值")
print("         在切点处，圆的法向量 (2x,2y) 平行于直线的法向量 (1,1)")
```

```python
# === 拉格朗日乘数法 3D 可视化 ===

def plot_lagrange_multiplier():
    """展示 f(x,y)=x²+y² 在约束 x+y=1 下的极值"""
    
    # 曲面
    xr = np.linspace(-1.5, 1.5, 80)
    yr = np.linspace(-1.5, 1.5, 80)
    X, Y = np.meshgrid(xr, yr)
    Z = X**2 + Y**2
    
    # 约束曲线 x + y = 1 在曲面上的投影
    t_vals = np.linspace(-1.5, 2.5, 200)
    x_line = t_vals
    y_line = 1 - t_vals
    z_line = x_line**2 + y_line**2
    
    # 极值点
    opt_x, opt_y = 0.5, 0.5
    opt_z = opt_x**2 + opt_y**2
    
    fig = go.Figure()
    
    fig.add_trace(go.Surface(z=Z, x=xr, y=yr, colorscale='Blues', opacity=0.6,
                             name='f(x,y) = x² + y²', showscale=False))
    
    fig.add_trace(go.Scatter3d(x=x_line, y=y_line, z=z_line,
                               mode='lines',
                               line=dict(color='red', width=6),
                               name='约束: x + y = 1'))
    
    fig.add_trace(go.Scatter3d(x=[opt_x], y=[opt_y], z=[opt_z],
                               mode='markers',
                               marker=dict(size=12, color='gold', symbol='diamond',
                                          line=dict(color='black', width=2)),
                               name=f'极小值点 ({opt_x}, {opt_y}, {opt_z})'))
    
    fig.update_layout(
        title='拉格朗日乘数法: min x²+y² s.t. x+y=1<br>'
              f'极小值点: ({opt_x}, {opt_y})，f = {opt_z}',
        scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='z'),
        width=850, height=700,
    )
    fig.show()
    
    # ── 2D 等高线视角 ──
    fig2, ax = plt.subplots(figsize=(9, 8))
    
    ax.contourf(X, Y, Z, levels=40, cmap='Blues', alpha=0.3)
    cs = ax.contour(X, Y, Z, levels=np.arange(0, 4, 0.25), colors='steelblue', linewidths=0.8)
    ax.clabel(cs, inline=True, fontsize=8)
    
    ax.plot(x_line, y_line, 'r-', lw=3, label='约束: x + y = 1')
    ax.plot(opt_x, opt_y, 'o', color='gold', markersize=14,
            markeredgecolor='black', markeredgewidth=2, zorder=5, label='极值点')
    
    # 标注梯度平行
    grad_f = np.array([2*opt_x, 2*opt_y])
    grad_g = np.array([1.0, 1.0])
    
    ax.arrow(opt_x, opt_y, grad_f[0]*0.15, grad_f[1]*0.15,
             head_width=0.06, head_length=0.08, fc='blue', ec='blue', lw=2,
             label=f'∇f = ({grad_f[0]}, {grad_f[1]})')
    ax.arrow(opt_x, opt_y, grad_g[0]*0.15, grad_g[1]*0.15,
             head_width=0.06, head_length=0.08, fc='green', ec='green', lw=2,
             label=f'∇g = ({grad_g[0]}, {grad_g[1]})')
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('等高线视角: ∇f ∥ ∇g 在极值点处')
    ax.set_aspect('equal')
    ax.legend()
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    
    plt.tight_layout()
    plt.show()

plot_lagrange_multiplier()
```

---
## 4.6 二重积分

> $\iint_D f(x,y)\,dx\,dy$ — 曲面下体积的推广

二重积分的本质：**将区域 D 划分为小矩形，求 $f(x_i, y_i)\Delta A$ 的和的极限**。

计算时化为**累次积分**（先对 x 再对 y，或反过来，取决于区域形状）。

```python
# 符号计算：二重积分
x_s, y_s = sp.symbols('x_s y_s', real=True)

print("示例 1: 矩形区域 D = [0,1]×[0,2]")
f1 = x_s**2 * y_s
result1 = sp.integrate(sp.integrate(f1, (y_s, 0, 2)), (x_s, 0, 1))
print(f"  ∬_D x²y dxdy = ∫₀¹∫₀² x²y dy dx = {result1}")
print()

print("示例 2: 三角形区域 D: 0 ≤ x ≤ 1, 0 ≤ y ≤ x")
f2 = x_s + y_s
result2 = sp.integrate(sp.integrate(f2, (y_s, 0, x_s)), (x_s, 0, 1))
print(f"  ∬_D (x+y) dxdy = ∫₀¹∫₀ˣ (x+y) dy dx = {result2}")
print()

print("示例 3: 极坐标, 单位圆内的面积")
r, theta = sp.symbols('r theta', real=True, positive=True)
# 二重积分 ∬_D √(1-x²-y²) dxdy, D 是单位圆
# 换为极坐标: ∫₀^{2π}∫₀¹ √(1-r²)·r dr dθ
integrand = sp.sqrt(1 - r**2) * r
result3 = sp.integrate(sp.integrate(integrand, (r, 0, 1)), (theta, 0, 2*sp.pi))
print(f"  ∬_{x²+y²≤1} √(1−x²−y²) dxdy = {result3}")
print(f"  = 2π/3 ≈ {float(2*sp.pi/3):.6f}  (上半球的体积的一半)")
```

```python
# === 二重积分: 矩形棱柱逼近体积 (3D) ===

def plot_double_integral_approximation(nx=8, ny=8):
    """
    用矩形棱柱逼近曲面 z = f(x,y) 下区域 D = [0,1]×[0,1] 的体积。
    这类似于一维的黎曼和，但是二维版本。
    """
    
    f = lambda x, y: 2 - x**2 - y**2  # 在 [0,1]×[0,1] 上的曲面
    
    a, b = 0.0, 1.0
    dx = (b - a) / nx
    dy = (b - a) / ny
    
    xr = np.linspace(a, b, 60)
    yr = np.linspace(a, b, 60)
    X, Y = np.meshgrid(xr, yr)
    Z = f(X, Y)
    
    # 精确体积
    exact_volume = (2*xr[-1]*yr[-1] - xr[-1]**3*yr[-1]/3 - xr[-1]*yr[-1]**3/3)
    exact_volume = 2 - 1/3 - 1/3  # = 4/3 (解析解)
    
    # 矩形棱柱
    approx_volume = 0
    
    fig = go.Figure()
    
    # 曲面
    fig.add_trace(go.Surface(z=Z, x=xr, y=yr, colorscale='Blues', opacity=0.5,
                             name='曲面 z = 2−x²−y²', showscale=False))
    
    # 矩形棱柱
    for i in range(nx):
        for j in range(ny):
            xi = a + i * dx
            yj = a + j * dy
            # 用中点值
            x_mid = xi + dx / 2
            y_mid = yj + dy / 2
            f_mid = f(x_mid, y_mid)
            approx_volume += f_mid * dx * dy
            
            # 棱柱的 8 个顶点
            vx = [xi, xi+dx, xi+dx, xi,
                  xi, xi+dx, xi+dx, xi]
            vy = [yj, yj, yj+dy, yj+dy,
                  yj, yj, yj+dy, yj+dy]
            vz = [0, 0, 0, 0,
                  f_mid, f_mid, f_mid, f_mid]
            
            # 简化：只画棱柱的顶面
            fig.add_trace(go.Mesh3d(
                x=[xi, xi+dx, xi+dx, xi],
                y=[yj, yj, yj+dy, yj+dy],
                z=[f_mid, f_mid, f_mid, f_mid],
                color='orange', opacity=0.5, alphahull=0,
                showscale=False, name='' if (i+j > 0) else '棱柱顶面'
            ))
    
    fig.update_layout(
        title=f'二重积分的矩形棱柱近似 (nx={nx}, ny={ny})<br>'
              f'近似体积 ≈ {approx_volume:.4f} (精确值 = 4/3 ≈ {4/3:.4f})',
        scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='z'),
        width=850, height=700,
    )
    fig.show()

interact(plot_double_integral_approximation,
         nx=IntSlider(min=2, max=12, step=1, value=5, description='x 分割',
                     continuous_update=False),
         ny=IntSlider(min=2, max=12, step=1, value=5, description='y 分割',
                     continuous_update=False));
```

---
## 4.7 向量场与线积分

> $\int_C \mathbf{F}\cdot d\mathbf{r} = \int_a^b \mathbf{F}(\mathbf{r}(t))\cdot \mathbf{r}'(t)\,dt$

线积分的物理意义：力场 $\mathbf{F}$ 沿路径 $C$ 做的**功**。

如果 $\mathbf{F}$ 是保守场（$\nabla\times\mathbf{F}=0$），则线积分与路径无关。

```python
# === 3D 向量场 + 路径 ===

def plot_vector_field_line_integral():
    """展示 2D 向量场 F = (−y, x) 中沿路径的线积分"""
    
    # 向量场 F(x,y) = (-y, x)  (旋转场)
    xr = np.linspace(-3, 3, 15)
    yr = np.linspace(-3, 3, 15)
    X, Y = np.meshgrid(xr, yr)
    U = -Y
    V = X
    
    # 路径: 单位圆的上半部分
    t_path = np.linspace(0, np.pi, 200)
    path_x = np.cos(t_path)
    path_y = np.sin(t_path)
    
    fig, ax = plt.subplots(figsize=(10, 9))
    
    # 向量场
    ax.quiver(X, Y, U, V, color='steelblue', alpha=0.6, scale=25, width=0.003)
    
    # 路径
    ax.plot(path_x, path_y, 'r-', lw=3, label='路径 C (单位圆上半)')
    ax.scatter(path_x[0], path_y[0], color='green', s=100, zorder=5, label='起点 (−1,0)')
    ax.scatter(path_x[-1], path_y[-1], color='darkred', s=100, zorder=5, marker='s', label='终点 (1,0)')
    
    # 路径上的向量
    n_arrows = 12
    for i in range(n_arrows):
        idx = i * len(t_path) // n_arrows
        px, py = path_x[idx], path_y[idx]
        fx, fy = -py, px  # F(px, py)
        f_norm = np.sqrt(fx**2 + fy**2)
        if f_norm > 0:
            ax.arrow(px, py, fx*0.12, fy*0.12,
                    head_width=0.12, head_length=0.15, fc='red', ec='red', alpha=0.7)
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('向量场 F = (−y, x) 和路径 C\n'
                 '注意: 沿路径的线积分 = 向量场在路径切线方向的分量的累积')
    ax.set_aspect('equal')
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.legend()
    ax.axhline(y=0, color='gray', lw=0.5)
    ax.axvline(x=0, color='gray', lw=0.5)
    
    plt.tight_layout()
    plt.show()
    
    # 数值计算线积分
    # F(r(t)) · r'(t) = (−sin t, cos t) · (−sin t, cos t) = sin²t + cos²t = 1
    print("线积分数值验证:")
    print("  F = (−y, x),  路径 r(t) = (cos t, sin t), t ∈ [0, π]")
    print("  F(r(t)) = (−sin t, cos t)")
    print("  r'(t) = (−sin t, cos t)")
    print("  F·r' = sin²t + cos²t = 1")
    print(f"  ∫_C F·dr = ∫₀^π 1 dt = π ≈ {np.pi:.6f}")
```

```python
plot_vector_field_line_integral()
```

>
> - **Green 公式**：闭曲线上的线积分 = 区域上的二重积分：$\oint_C Pdx+Qdy = \iint_D (Q_x-P_y)dxdy$
> - **Stokes 公式**：空间闭曲线线积分 = 曲面积分
> - **Gauss 公式**：闭曲面积分 = 三重积分（散度定理）
> - 判断保守场：$\frac{\partial P}{\partial y} = \frac{\partial Q}{\partial x}$

---
## 📋 本章小结

| 概念 | 核心理解 |
|------|---------|
| 二元函数 | z = f(x,y) 是一个曲面 |
| 偏导数 | 沿坐标轴方向的切线斜率 |
| 梯度 ∇f | 增长最快的方向，⊥ 等高线 |
| 梯度下降 | 沿 −∇f 走 → 找极小值 |
| 拉格朗日乘数 | 极值点处 ∇f ∥ ∇g |
| 二重积分 | 曲面下的体积 = 累次积分 |
| 线积分 | 向量场沿路径做的功 |

### ⚠️ 常见错误

1. **偏导数存在 ⇏ 可微**：这是多元与一元最大的区别
2. **混淆梯度与方向导数**：方向导数是一个数，梯度是一个向量
3. **二重积分上下限写反**：积分次序需要根据区域形状确定
4. **Green/Stokes/Gauss 公式的方向和侧**：注意曲线的正方向和曲面的侧

### 📝 自测题

1. 求 $f(x,y) = x^3 + y^3 - 3xy$ 的极值点和鞍点
2. 用拉格朗日乘数法求椭圆 $x^2 + 4y^2 = 4$ 上点 $(x,y)$ 到原点的最大距离
3. 计算 $\iint_D xy\,dx\,dy$，其中 D 由 $y=x^2$ 和 $y=x$ 围成