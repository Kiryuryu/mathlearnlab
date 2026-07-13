# 第二章：积分学

## 学习目标

- 理解定积分作为黎曼和极限的几何含义
- 直观感受换元积分法的变量变换
- 理解分部积分法的几何本质
- 掌握定积分求面积、体积的应用
- 判断反常积分的收敛性

## 预备知识

- 不定积分与定积分的关系（Newton-Leibniz 公式）
- 基本积分公式
- 微积分基本定理：$\frac{d}{dx}\int_a^x f(t)dt = f(x)$

> 💡 **提示**：本页面由 Jupyter Notebook 自动转换而来。
> 运行 `jupyter lab` 启动本地环境，可体验完整的**交互式可视化**（拖动滑块、3D旋转、动画播放）。
> 下方代码块仅供参考，静态页面无法执行 Python。

---

# 第二章：积分学

## 学习目标

- 理解定积分作为黎曼和极限的几何含义
- 直观感受换元积分法的变量变换
- 理解分部积分法的几何本质
- 掌握定积分求面积、体积的应用
- 判断反常积分的收敛性

## 预备知识

- 不定积分与定积分的关系（Newton-Leibniz 公式）
- 基本积分公式
- 微积分基本定理：$\frac{d}{dx}\int_a^x f(t)dt = f(x)$

```python
%matplotlib widget

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from matplotlib.animation import FuncAnimation
import sympy as sp
from ipywidgets import interact, FloatSlider, IntSlider, Play, VBox, HBox
from IPython.display import display, HTML, clear_output
import sys
sys.path.insert(0, '..')

from utils.plot_config import set_style, COLORS

set_style()
sp.init_printing()

x, t, u = sp.symbols('x t u', real=True)

print("✅ 环境就绪！")
```

---
## 2.1 定积分作为黎曼和的极限

> $\int_a^b f(x)\,dx = \lim_{n\to\infty}\sum_{i=1}^{n} f(x_i^*)\Delta x$，其中 $\Delta x = \frac{b-a}{n}$

定积分的本质是**无穷多个无穷小的矩形面积之和**。分割越细，近似越精确。

### 拖动滑块，看矩形如何逼近曲线下的面积 👇

```python
# 符号计算：验证定积分
x = sp.symbols('x', real=True)

examples = [
    ("∫₀¹ x² dx", x**2, (x, 0, 1)),
    ("∫₀^π sin(x) dx", sp.sin(x), (x, 0, sp.pi)),
    ("∫₁^e (1/x) dx", 1/x, (x, 1, sp.E)),
]

for name, integrand, limits in examples:
    result = sp.integrate(integrand, limits)
    print(f"{name} = {result} = {float(result):.6f}")
```

```python
# === 黎曼和动画：矩形细分收敛 ===

def plot_riemann_sum(n=8, method='midpoint'):
    """
    用矩形近似 ∫₀² x*sin(x) dx
    method: 'left', 'right', 'midpoint'
    """
    def f(x):
        return x * np.sin(x) + 0.5
    
    a, b = 0.0, 4.0
    xs = np.linspace(a, b, 500)
    ys = f(xs)
    
    dx = (b - a) / n
    
    if method == 'left':
        xi = np.linspace(a, b - dx, n)
    elif method == 'right':
        xi = np.linspace(a + dx, b, n)
    else:  # midpoint
        xi = np.linspace(a + dx/2, b - dx/2, n)
    
    yi = f(xi)

    # 数值积分用于比较
    xs_fine = np.linspace(a, b, 10000)
    exact_area = np.trapz(f(xs_fine), xs_fine)
    riemann_area = np.sum(yi * dx)
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    # 曲线
    ax.plot(xs, ys, 'b-', lw=2.5, label=f'f(x) = x·sin(x) + 0.5')
    
    # 填色曲线下面积
    ax.fill_between(xs, 0, ys, alpha=0.1, color='blue')
    
    # 矩形
    for i in range(n):
        x_left = a + i * dx
        rect = Rectangle((x_left, 0), dx, yi[i],
                         facecolor='orange', edgecolor='darkorange',
                         alpha=0.6, lw=0.8)
        ax.add_patch(rect)
    
    # 标记
    ax.set_xlim(a - 0.2, b + 0.2)
    ax.set_ylim(-0.1, np.max(ys) + 1.0)
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title(f'黎曼和近似 (n={n}, {method}): 矩形面积 ≈ {riemann_area:.4f}\n'
                 f'精确值 ≈ {exact_area:.4f}，误差 ≈ {abs(riemann_area - exact_area):.4f}')
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()

# 交互控件：n 和 method
from ipywidgets import Dropdown

def riemann_interact(n, method):
    plot_riemann_sum(n=n, method=method)

interact(riemann_interact,
         n=IntSlider(min=2, max=60, step=1, value=8, description='分割数 n',
                    continuous_update=False),
         method=Dropdown(options=['midpoint', 'left', 'right'], value='midpoint',
                        description='取样方式'));
```

**💡 关键观察**：当 n 增大时，矩形面积的和趋近于曲线下的真实面积。这就是定积分定义的核心。

---
## 2.2 换元积分法

> $\int_a^b f(g(x))\,g'(x)\,dx = \int_{g(a)}^{g(b)} f(u)\,du$

换元法的核心思想：**通过变量代换，将一个复杂的积分转化为简单积分**。几何上，你是在拉伸或压缩坐标轴，但面积保持不变。

```python
# 符号计算：换元积分示例
x, u = sp.symbols('x u', real=True)

print("=".center(60, "="))
print("示例 1: ∫ 2x·cos(x²) dx  令 u = x²")
print("=".center(60, "="))

integrand = 2*x*sp.cos(x**2)
print(f"原积分: ∫ {integrand} dx")

# 不定积分
result = sp.integrate(integrand, x)
print(f"直接积分: {result}")

# 换元验证：设 u = x², 则 du = 2x dx
# 积分变为 ∫ cos(u) du = sin(u) + C = sin(x²) + C
print(f"换元验证: 令 u=x², du=2xdx, 积分变为 ∫cos(u)du = sin(u)+C = sin(x²)+C")
print()

print("=".center(60, "="))
print("示例 2: ∫₀¹ x/(1+x²) dx  令 u = 1+x²")
print("=".center(60, "="))

integrand2 = x / (1 + x**2)
result2 = sp.integrate(integrand2, (x, 0, 1))
print(f"原积分: ∫₀¹ {integrand2} dx")
print(f"定积分值: {result2} = {float(result2):.6f}")
print(f"换元验证: 令 u=1+x², x=0→u=1, x=1→u=2, du=2xdx")
print(f"积分变为 (1/2)∫₁² du/u = (1/2)[ln|u|]₁² = (1/2)ln2 ≈ {0.5*np.log(2):.6f}")
```

```python
# === 换元法的几何可视化 ===

def plot_substitution_visual():
    """
    演示 ∫₀¹ 2x·cos(x²) dx 的换元过程。
    换元前：x 轴上是 [0,1]，被积函数 2x·cos(x²)
    换元后：u 轴上是 [0,1]，被积函数 cos(u)（因为 u=x², du=2xdx）
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # ── 左图：换元前 ──
    xs = np.linspace(0.01, 1.5, 500)
    f_original = lambda x: 2 * x * np.cos(x**2)
    ys1 = f_original(xs)
    
    ax1.plot(xs, ys1, 'b-', lw=2.5, label='2x·cos(x²)')
    ax1.fill_between(xs, 0, ys1, where=(xs <= 1), alpha=0.2, color='blue')
    ax1.axvline(x=0, color='gray', lw=0.5)
    ax1.axvline(x=1, color='red', ls='--', lw=1.5, alpha=0.7, label='x=1')
    ax1.set_xlim(0, 1.5)
    ax1.set_ylim(-0.5, 2.2)
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.set_title('换元前: ∫₀¹ 2x·cos(x²) dx')
    ax1.legend()
    
    # 标注：x 的划分
    for xi in np.linspace(0.2, 1.0, 5):
        ax1.axvline(x=xi, color='gray', ls=':', lw=0.5, alpha=0.4)
    
    # ── 右图：换元后 ──
    us = np.linspace(0.01, 2.5, 500)
    f_transformed = lambda u: np.cos(u)
    ys2 = f_transformed(us)
    
    ax2.plot(us, ys2, 'green', lw=2.5, label='cos(u)')
    ax2.fill_between(us, 0, ys2, where=(us <= 1), alpha=0.2, color='green')
    ax2.axvline(x=0, color='gray', lw=0.5)
    ax2.axvline(x=1, color='red', ls='--', lw=1.5, alpha=0.7, label='u=1  (x=1)')
    ax2.set_xlim(0, 2.5)
    ax2.set_ylim(-1.2, 1.5)
    ax2.set_xlabel('u = x²')
    ax2.set_ylabel('f(u) = cos(u)')
    ax2.set_title('换元后: ∫₀¹ cos(u) du = sin(1)')
    ax2.legend()
    
    plt.suptitle('换元积分法: 面积保持不变, 但被积函数简化了', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.show()
    
    print(f"换元前积分值: ∫₀¹ 2x·cos(x²)dx = sin(1) ≈ {np.sin(1):.6f}")
    print(f"换元后积分值: ∫₀¹ cos(u)du = sin(1) ≈ {np.sin(1):.6f}")
    print(f"✅ 两者相等，验证了换元法的正确性")

plot_substitution_visual()
```

---
## 2.3 分部积分法

> $\int u\,dv = uv - \int v\,du$

分部积分来源于乘积的导数公式：$(uv)' = u'v + uv'$

几何意义：曲线 $y = f(x)$ 下的面积可以等价地用另一种方式计算。

```python
# 符号计算：分部积分示例
x = sp.symbols('x', real=True)

examples_ibp = [
    ("∫ x·eˣ dx", x*sp.exp(x)),
    ("∫ x·sin(x) dx", x*sp.sin(x)),
    ("∫ ln(x) dx", sp.log(x)),
    ("∫ x·arctan(x) dx", x*sp.atan(x)),
]

for name, integrand in examples_ibp:
    result = sp.integrate(integrand, x)
    print(f"{name} = {result}")
    print()
```

```python
# 也可以让 SymPy 展示分部积分的中间步骤
x = sp.symbols('x', real=True)
print("分部积分 ∫ x·eˣ dx 的推导:")
print("  令 u = x,  dv = eˣ dx")
print("  则 du = dx,  v = eˣ")
print("  ∫ x·eˣ dx = x·eˣ − ∫ eˣ dx")
print("             = x·eˣ − eˣ + C")
print()
print("验证:")
result = sp.integrate(x*sp.exp(x), x)
sp.pprint(result)
print()
print("分部积分 ∫ ln(x) dx 的推导:")
print("  令 u = ln(x),  dv = dx")
print("  则 du = (1/x)dx,  v = x")
print("  ∫ ln(x) dx = x·ln(x) − ∫ x·(1/x)dx")
print("             = x·ln(x) − x + C")
print()
print("验证:")
result2 = sp.integrate(sp.log(x), x)
sp.pprint(result2)
```

---
## 2.4 定积分的应用：面积

> 由曲线 $y = f(x)$、$y = g(x)$ 与直线 $x = a$、$x = b$ 围成的面积：$A = \int_a^b |f(x) - g(x)|\,dx$

### 交互选择曲线，看围成的面积 👇

```python
# === 曲线间面积的可视化 ===

def plot_area_between(f_upper_name='sin(x)+2', f_lower_name='cos(x)'):
    """展示两条曲线之间的面积"""
    
    funcs = {
        'sin(x)+2': lambda x: np.sin(x) + 2,
        'cos(x)': lambda x: np.cos(x),
        'x²': lambda x: x**2,
        'x': lambda x: x,
        '√x': lambda x: np.sqrt(np.maximum(x, 0)),
    }
    
    f_upper = funcs[f_upper_name]
    f_lower = funcs[f_lower_name]
    
    a, b = 0.0, np.pi/2
    xs = np.linspace(a, b, 500)
    ys_upper = f_upper(xs)
    ys_lower = f_lower(xs)
    
    # 确保 upper >= lower
    if np.any(ys_upper < ys_lower):
        print("⚠️ 在这个区间内上曲线在某些地方低于下曲线，面积计算时会取绝对值")
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    ax.plot(xs, ys_upper, 'b-', lw=2.5, label=f'上: y = {f_upper_name}')
    ax.plot(xs, ys_lower, 'r-', lw=2.5, label=f'下: y = {f_lower_name}')
    ax.fill_between(xs, ys_lower, ys_upper, alpha=0.3, color='purple', label='面积区域')
    
    # 边界
    ax.axvline(x=a, color='gray', ls='--', lw=1, alpha=0.7, label=f'x = {a}')
    ax.axvline(x=b, color='gray', ls='--', lw=1, alpha=0.7, label=f'x = {b}')
    
    # 数值积分求面积
    xs_fine = np.linspace(a, b, 5000)
    area = np.trapz(np.abs(f_upper(xs_fine) - f_lower(xs_fine)), xs_fine)
    
    ax.set_xlim(a - 0.2, b + 0.3)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'曲线间面积: ∫_{{{a}}}^{{{b}}} |{f_upper_name} − ({f_lower_name})| dx ≈ {area:.4f}')
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.show()

from ipywidgets import Dropdown

curve_names = ['sin(x)+2', 'cos(x)', 'x²', 'x', '√x']
interact(plot_area_between,
         f_upper_name=Dropdown(options=curve_names, value='sin(x)+2', description='上曲线'),
         f_lower_name=Dropdown(options=curve_names, value='cos(x)', description='下曲线'));
```

---
## 2.5 旋转体体积（3D 可视化）

> **圆盘法 (Disk)**：$V = \pi\int_a^b [f(x)]^2\,dx$
> **柱壳法 (Shell)**：$V = 2\pi\int_a^b x\,f(x)\,dx$（绕 y 轴）

这是许多同学觉得难以想象的部分。用 3D 可视化一目了然！

```python
# 符号计算：旋转体体积
x = sp.symbols('x', real=True)

print("示例: y = sin(x), x ∈ [0, π], 绕 x 轴旋转")
f = sp.sin(x)
# 圆盘法
volume = sp.pi * sp.integrate(f**2, (x, 0, sp.pi))
print(f"V = π ∫₀^π sin²(x) dx = {volume} = {float(volume):.4f}")

print()
print("示例: y = √x, x ∈ [0, 4], 绕 x 轴旋转")
volume2 = sp.pi * sp.integrate(x, (x, 0, 4))
print(f"V = π ∫₀⁴ x dx = {volume2} = {float(volume2):.4f}")
print("（这是一个底面半径 2、高 4 的圆锥，体积 8π ≈ 25.13）")
```

```python
# === 3D 旋转体可视化 (Plotly) ===

import plotly.graph_objects as go

def plot_solid_of_revolution(f, a, b, n_theta=80, n_x=200, title="旋转体"):
    """
    将曲线 y=f(x) 绕 x 轴旋转，生成 3D 旋转体。
    
    Parameters
    ----------
    f : callable
        曲线函数 y = f(x)
    a, b : float
        区间
    n_theta : int
        圆周方向采样点数
    n_x : int
        x 方向采样点数
    title : str
    """
    theta = np.linspace(0, 2 * np.pi, n_theta)
    x_vals = np.linspace(a, b, n_x)
    
    Theta, X = np.meshgrid(theta, x_vals)
    R = f(X)
    
    Y = R * np.cos(Theta)
    Z = R * np.sin(Theta)
    
    fig = go.Figure(data=[
        go.Surface(
            x=X, y=Y, z=Z,
            colorscale='Blues',
            opacity=0.85,
            showscale=False,
            name='旋转体'
        )
    ])
    
    # 添加原始曲线（在 xy 平面上的投影）
    curve_x = np.linspace(a, b, 200)
    curve_y = f(curve_x)
    fig.add_trace(go.Scatter3d(
        x=curve_x, y=curve_y, z=np.zeros_like(curve_x),
        mode='lines', line=dict(color='red', width=6),
        name='原始曲线 y=f(x)'
    ))
    
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title='x',
            yaxis_title='y',
            zaxis_title='z',
            aspectmode='data',
        ),
        width=850, height=700,
    )
    
    return fig

# 示例 1: y = sin(x), x ∈ [0, π]
fig1 = plot_solid_of_revolution(
    lambda x: np.sin(x),
    0, np.pi,
    title="旋转体: y = sin(x), x ∈ [0, π], 绕 x 轴"
)
fig1.show()
print("💡 用鼠标拖动旋转 3D 图，从不同角度观察旋转体！")
print(f"体积 = π ∫₀^π sin²(x) dx = π²/2 ≈ {np.pi**2/2:.4f}")
```

```python
# 示例 2: y = √x, x ∈ [0, 4] — 形成圆锥
fig2 = plot_solid_of_revolution(
    lambda x: np.sqrt(x),
    0, 4,
    title="旋转体: y = √x, x ∈ [0, 4], 绕 x 轴 (圆锥)"
)
fig2.show()
print(f"体积 = π ∫₀⁴ x dx = 8π ≈ {8*np.pi:.4f}")
```

---
## 2.6 反常积分

> 无穷区间：$\int_a^{\infty}f(x)dx = \lim_{b\to\infty}\int_a^b f(x)dx$
> 无界函数：$\int_a^b f(x)dx = \lim_{t\to b^-}\int_a^t f(x)dx$（当 $x=b$ 是瑕点时）

反常积分的核心问题：**积分是否收敛（有限）？**

### 对比收敛与发散的积分

```python
# 符号计算：判断反常积分收敛性
x = sp.symbols('x', real=True)

# 关键比较：∫₁^∞ 1/x^p dx
print("=".center(50, "="))
print("p-积分: ∫₁^∞ 1/x^p dx")
print("=".center(50, "="))
print()

for p in [0.5, 1.0, 1.5, 2.0]:
    try:
        result = sp.integrate(1/x**p, (x, 1, sp.oo))
        print(f"p = {p}: 收敛 → {result}")
    except:
        print(f"p = {p}: 发散 (积分值为无穷大)")

print()
print("结论: ∫₁^∞ 1/x^p dx 收敛 ⇔ p > 1")
```

```python
# === 可视化：反常积分的收敛与发散 ===

def plot_improper_comparison(p=1.5):
    """展示 ∫₁^∞ 1/x^p dx 的尾部面积"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # ── 左图：被积函数 ──
    xs = np.linspace(0.1, 8, 500)
    for p_val, color, label in [(2.0, 'green', 'p=2 (收敛)'), (1.0, 'orange', 'p=1 (发散)'), (0.5, 'red', 'p=0.5 (发散)')]:
        ys = 1 / xs**p_val
        ax1.plot(xs, ys, lw=2, color=color, alpha=0.8, label=label)
    
    ax1.axhline(y=0, color='gray', lw=0.5)
    ax1.set_xlim(0, 8)
    ax1.set_ylim(0, 4)
    ax1.set_xlabel('x')
    ax1.set_ylabel('1/x^p')
    ax1.set_title('被积函数 1/x^p 的衰减速度')
    ax1.legend()
    
    # 标注 x=1
    ax1.axvline(x=1, color='gray', ls=':', lw=1, alpha=0.5)
    
    # ── 右图：尾部累积面积 (∫₁^b) ──
    bs = np.linspace(1, 50, 500)
    for p_val, color, label in [(2.0, 'green', 'p=2'), (1.5, 'blue', 'p=1.5'), (1.1, 'purple', 'p=1.1'), (1.0, 'orange', 'p=1')]:
        cum_area = np.array([np.trapz(1 / np.linspace(1, b, 5000)**p_val, np.linspace(1, b, 5000)) for b in bs])
        ax2.plot(bs, cum_area, lw=2, color=color, alpha=0.8, label=f'{label}: → {"∞" if p_val <= 1 else f"{1/(p_val-1):.2f}"}')
    
    ax2.axhline(y=0, color='gray', lw=0.5)
    ax2.set_xlabel('上限 b')
    ax2.set_ylabel('累积面积 ∫₁^b 1/x^p dx')
    ax2.set_title('尾部累积面积: 收敛 vs 发散')
    ax2.legend()
    
    plt.suptitle(f'反常积分收敛性判别: ∫₁^∞ 1/x^p dx 收敛 ⇔ p > 1', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.show()

plot_improper_comparison()
```

**💡 关键观察**：
- $p > 1$ 时，1/x^p 衰减得足够快，尾部面积有限（收敛）
- $p \leq 1$ 时，1/x^p 衰减不够快，尾部面积无限增长（发散）
- $p=1$ 的 $\int_1^\infty 1/x\,dx = \ln x|_1^\infty \to \infty$ 是临界情况

> - $\int_1^\infty 1/x^p\,dx$：收敛 $\iff p > 1$
> - $\int_0^1 1/x^p\,dx$：收敛 $\iff p < 1$

---
## 📋 本章小结

| 概念 | 核心理解 |
|------|---------|
| 定积分 | 黎曼和的极限，曲线下的面积 |
| 换元法 | 坐标轴伸缩，面积不变 |
| 分部积分 | 乘积求导公式的反向应用 |
| 几何应用 | 面积 = ∫(上−下)；体积 = 旋转+积分 |
| 反常积分 | 判断收敛性：p-积分、比较判别法 |

### ⚠️ 常见错误

1. **定积分换元忘记改上下限**
2. **面积忘记取绝对值**：曲线交叉时需要分段计算
3. **混淆绕 x 轴和绕 y 轴的旋转体公式**
4. **反常积分不判断收敛性就直接计算**

### 📝 自测题

1. 求 $\int_0^{\pi/2} x\sin x\,dx$（分部积分）
2. 求由 $y = x^2$ 和 $y = x$ 围成区域绕 x 轴的旋转体体积
3. 判断 $\int_1^\infty \frac{\ln x}{x^2}dx$ 是否收敛