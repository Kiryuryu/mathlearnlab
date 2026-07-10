# 第一章：极限、连续与微分

## 学习目标

- 理解 ε-δ 极限定义的几何含义
- 掌握左右极限与极限存在性的判断
- 直观理解连续性与可导性的关系
- 几何理解三大微分中值定理
- 掌握泰勒展开的逼近思想
- 理解洛必达法则的使用条件

## 预备知识

- 函数的基本概念（定义域、值域、单调性、奇偶性）
- 导数定义：$f'(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$
- 基本初等函数的导数公式

> 💡 **提示**：本页面由 Jupyter Notebook 自动转换而来。
> 运行 `jupyter lab` 启动本地环境，可体验完整的**交互式可视化**（拖动滑块、3D旋转、动画播放）。
> 下方代码块仅供参考，静态页面无法执行 Python。

---

# 第一章：极限、连续与微分

## 学习目标

- 理解 ε-δ 极限定义的几何含义
- 掌握左右极限与极限存在性的判断
- 直观理解连续性与可导性的关系
- 几何理解三大微分中值定理
- 掌握泰勒展开的逼近思想
- 理解洛必达法则的使用条件

## 预备知识

- 函数的基本概念（定义域、值域、单调性、奇偶性）
- 导数定义：$f'(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$
- 基本初等函数的导数公式

```python
%matplotlib widget

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sympy as sp
from ipywidgets import interact, FloatSlider, IntSlider, Play, jslink, VBox, HBox, Output
from IPython.display import display, HTML, clear_output
import sys
sys.path.insert(0, '..')

from utils.plot_config import set_style, COLORS, annotate_point

set_style()
sp.init_printing()

# SymPy symbols
x, n = sp.symbols('x n', real=True)

print("✅ 环境就绪！")
```


---
## 1.1 ε-δ 极限定义

> 设函数 $f(x)$ 在点 $x_0$ 的某去心邻域内有定义。若 $\forall \varepsilon > 0$，$\exists \delta > 0$，使得当 $0 < |x - x_0| < \delta$ 时，恒有 $|f(x) - L| < \varepsilon$，则称 $\lim_{x\to x_0}f(x) = L$。

这个定义是微积分严密化的基石，但很多同学觉得抽象。**几何上**：
- ε 是你允许的「函数值的误差」
- δ 是你需要找到的「自变量的控制范围」
- 对于任意小的 ε，你都能找到 δ，使得 x 进入 (x₀-δ, x₀+δ) 后，f(x) 一定在 (L-ε, L+ε) 内

### 拖动滑块感受 ε-δ 的关系 👇

```python
# 符号验证：先确认极限存在
f_expr = (x**2 - 1) / (x - 1)
print("f(x) =", f_expr)
print("lim_{x→1} f(x) =", sp.limit(f_expr, x, 1))
print("说明：虽然 f(1) 无定义，但极限存在且等于 2")
print("实际上 f(x) = x + 1 (x ≠ 1)，是去掉了一个可去间断点")
```


```python
# === 交互式 ε-δ 可视化 ===

def plot_epsilon_delta(epsilon=0.3):
    """
    对 f(x) = (x^2-1)/(x-1) = x+1 (x≠1)，验证 lim_{x→1} f(x) = 2
    因为 f(x) = x+1（线性），所以 δ = ε 即可满足定义。
    """
    a, L = 1.0, 2.0      # x₀ 和极限值
    delta = epsilon       # 对线性函数 f(x)=x+1, |f(x)-L| = |x-a|, 所以 δ=ε
    
    # x 轴采样范围：x₀ 附近
    margin = max(3 * delta, 1.5)
    xs = np.linspace(a - margin, a + margin, 1000)
    ys = xs + 1  # 简化后的 f(x)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # 函数曲线
    ax.plot(xs, ys, 'b-', lw=2, label='f(x) = (x²−1)/(x−1) = x+1 (x≠1)')
    
    # 标注间断点
    ax.plot(a, L, 'wo', markersize=10, markeredgecolor='blue', markeredgewidth=2, zorder=5)
    ax.plot(a, L, 'bx', markersize=8, zorder=6)
    
    # ε-带（水平方向）：L ± ε
    ax.axhspan(L - epsilon, L + epsilon, alpha=0.2, color='green', label=f'ε-带: L ± ε = {L} ± {epsilon:.2f}')
    ax.axhline(y=L + epsilon, color='green', ls='--', lw=1, alpha=0.7)
    ax.axhline(y=L - epsilon, color='green', ls='--', lw=1, alpha=0.7)
    
    # δ-带（竖直方向）：x₀ ± δ
    ax.axvspan(a - delta, a + delta, alpha=0.15, color='orange', label=f'δ-带: x₀ ± δ = {a} ± {delta:.2f}')
    ax.axvline(x=a - delta, color='orange', ls='--', lw=1, alpha=0.7)
    ax.axvline(x=a + delta, color='orange', ls='--', lw=1, alpha=0.7)
    ax.axvline(x=a, color='gray', ls=':', lw=1, alpha=0.5)
    
    # 标注
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.set_title(f'ε-δ 定义可视化  (ε = {epsilon:.2f}, δ = {delta:.2f})\n'
                 f'当 x ∈ ({a-delta:.2f}, {a+delta:.2f}) 时，f(x) 一定在绿色带内')
    ax.legend(loc='upper left')
    
    # 自动缩放显示全貌
    ax.set_xlim(a - margin, a + margin)
    ax.set_ylim(L - max(3*epsilon, 1.0), L + max(3*epsilon, 1.0))
    
    plt.show()

interact(plot_epsilon_delta,
         epsilon=FloatSlider(min=0.05, max=0.8, step=0.01, value=0.3,
                            description='ε', continuous_update=False));
```


**💡 关键观察**：无论你把 ε 调到多小，对应的 δ 都会使函数值落在 ε-带内。这就是极限存在的几何意义。

> 🔑 **考研要点**：ε-δ 定义主要在数学一中考察证明题。数学二/三理解含义即可，重点是用极限运算法则和两个重要极限求极限。

---
## 1.2 左右极限与极限存在性

> $\lim_{x\to x_0}f(x) = L$ 存在的**充要条件**：$\lim_{x\to x_0^-}f(x) = \lim_{x\to x_0^+}f(x) = L$

分段函数是考察左右极限的经典载体。来看一个典型例子：

```python
# 符号计算：验证左右极限
x = sp.symbols('x', real=True)

# 分段函数 f(x) = { sin(x)/x,  x ≠ 0
#                  { 1,         x = 0

expr1 = sp.sin(x) / x

print("f(x) = sin(x)/x (x≠0), f(0)=1")
print(f"左极限 lim_{x→0⁻} sin(x)/x = {sp.limit(expr1, x, 0, dir='-')}")
print(f"右极限 lim_{x→0⁺} sin(x)/x = {sp.limit(expr1, x, 0, dir='+')}")
print(f"→ 左右极限相等，所以极限存在且等于 1")
print(f"→ 且 f(0)=1 = 极限值，所以函数在 x=0 连续 ✓")
```


```python
# === 左右极限可视化：对比左右趋近过程 ===

def plot_left_right_limits(target=0):
    """展示函数在 target 附近的左右极限行为"""
    
    # 两个典型函数：一个极限存在，一个不存在
    def f1(x):  # sin(x)/x — 极限存在
        with np.errstate(divide='ignore', invalid='ignore'):
            result = np.where(x != 0, np.sin(x) / x, np.nan)
        return result
    
    def f2(x):  # |x|/x — sign 函数是经典极限不存在例子...但这里改为 1/(1+e^{-1/x})
        # 这不如展示 sign 函数简单
        with np.errstate(divide='ignore', invalid='ignore'):
            return np.where(x > 0, 1.0, np.where(x < 0, -1.0, 0.0))
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # ── 左图：极限存在的例子 sin(x)/x ──
    ax = axes[0]
    xs = np.linspace(-3, 3, 600)
    ys = f1(xs)
    ax.plot(xs, ys, 'b-', lw=1.5, label='sin(x)/x')
    ax.axhline(y=1, color='green', ls='--', lw=1.5, label='极限 L = 1')
    ax.axvline(x=0, color='gray', ls=':', lw=1)
    
    # 标注左右趋近
    x_left = np.linspace(-0.8, -0.01, 50)
    ax.scatter(x_left, f1(x_left), c='red', s=15, alpha=0.6, zorder=5, label='左趋近')
    x_right = np.linspace(0.01, 0.8, 50)
    ax.scatter(x_right, f1(x_right), c='darkorange', s=15, alpha=0.6, zorder=5, label='右趋近')
    
    ax.set_xlim(-3, 3)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title('✅ 极限存在：sin(x)/x → 1 (x→0)')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()
    
    # ── 右图：极限不存在的例子 sign 函数 ──
    ax = axes[1]
    xs = np.linspace(-2, 2, 600)
    ys = f2(xs)
    ax.plot(xs[xs < 0], ys[xs < 0], 'b-', lw=1.5, label='x<0: f(x) = -1')
    ax.plot(xs[xs > 0], ys[xs > 0], 'r-', lw=1.5, label='x>0: f(x) = +1')
    ax.axvline(x=0, color='gray', ls=':', lw=1)
    
    x_left = np.linspace(-1, -0.01, 30)
    ax.scatter(x_left, f2(x_left), c='blue', s=20, alpha=0.7, zorder=5, label=f'左极限 → -1')
    x_right = np.linspace(0.01, 1, 30)
    ax.scatter(x_right, f2(x_right), c='red', s=20, alpha=0.7, zorder=5, label=f'右极限 → +1')
    
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_title('❌ 极限不存在：sgn(x) 左右极限不等')
    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')
    ax.legend()
    
    plt.tight_layout()
    plt.show()

plot_left_right_limits()
```


> 🔑 **考研要点**：
> - 含绝对值的分段函数、含 $[x]$（取整）的函数，务必检查左右极限
> - $x\to \infty$ 时也要区分 $+\infty$ 和 $-\infty$（如 $\arctan x$）

---
## 1.3 连续与可导的关系

> **可导 ⇒ 连续**，但**连续 ⇏ 可导**

经典反例：$f(x) = |x|$ 在 $x = 0$ 连续但不可导。导数不存在的角点（corner）是微积分中重要的「不可导点」。

下面用交互动画展示切线在角点处的行为：

```python
# 符号计算：验证 |x| 在 x=0 的左右导数
x = sp.symbols('x', real=True)
f = sp.Abs(x)

print("f(x) = |x|")
print(f"左导数 lim_{h→0⁻} (|0+h| - 0)/h  = {sp.limit(f.subs(x, x) / x, x, 0, dir='-')}")
print(f"右导数 lim_{h→0⁺} (|0+h| - 0)/h  = {sp.limit(f.subs(x, x) / x, x, 0, dir='+')}")
print("→ 左右导数不相等 ⇒ f'(0) 不存在")
print("→ 但 lim_{x→0} |x| = 0 = f(0)，所以连续 ✓")

# 求导
fp = sp.diff(f, x)
print(f"\nf'(x) = {fp}  (sign 函数在 x=0 无定义)")
```


```python
# === 切线程动画：展示在角点附近切线的行为 ===

def plot_tangent_at_corner(h=0.5):
    """
    对 f(x) = |x|，计算 x=h 处的导数和切线。
    当 h→0 时，切线在左右两侧给出不同的极限斜率。
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    xs_full = np.linspace(-2, 2, 500)
    ys_full = np.abs(xs_full)
    
    for ax, side, h_val in [(ax1, '左 (h<0)', -abs(h)), (ax2, '右 (h>0)', abs(h))]:
        # f(x) = |x|
        ax.plot(xs_full, ys_full, 'b-', lw=2, label='f(x) = |x|')
        
        # 切点
        x0 = h_val
        y0 = np.abs(x0)
        slope = 1 if x0 > 0 else -1  # |x| 的导数
        
        # 切线
        xs_tan = np.linspace(x0 - 0.8, x0 + 0.8, 100)
        ys_tan = slope * (xs_tan - x0) + y0
        ax.plot(xs_tan, ys_tan, 'r--', lw=2, label=f'切线: 斜率 = {slope}')
        ax.plot(x0, y0, 'ro', markersize=10, zorder=5, label=f'切点 x={x0:.2f}')
        
        # 导数差商线（从切点画一个小的差商三角形）
        dx = 0.3
        ax.plot([x0, x0+dx], [y0, y0], 'gray', lw=1, alpha=0.5)
        ax.plot([x0+dx, x0+dx], [y0, y0+slope*dx], 'gray', lw=1, alpha=0.5)
        
        ax.set_xlim(-2, 2)
        ax.set_ylim(-0.3, 2.5)
        ax.set_title(f'{side} 导数 = {slope}')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.legend()
        ax.axhline(y=0, color='gray', lw=0.5)
        ax.axvline(x=0, color='gray', lw=0.5)
    
    plt.suptitle(f'当 h→0 时，左右切线斜率分别为 −1 和 +1，不相等 ⇒ f\'(0) 不存在',
                 fontsize=14, y=1.02)
    plt.tight_layout()
    plt.show()

interact(plot_tangent_at_corner,
         h=FloatSlider(min=0.05, max=1.5, step=0.01, value=0.5,
                       description='|h|', continuous_update=False));
```


> 🔑 **考研要点**：
> - 选择题常考「$f(x)$ 在 $x_0$ 可导的充要条件是左右导数存在且相等」
> - 常见不可导点：角点（|x|）、尖点（$x^{2/3}$ 在 0）、垂直切线（$\sqrt[3]{x}$ 在 0）、间断点

---
## 1.4 微分中值定理

三大中值定理是微分学的核心，它们都是 **Rolle 定理**的推广：

| 定理 | 条件 | 结论 |
|------|------|------|
| **Rolle** | f 在 [a,b] 连续、(a,b) 可导、f(a)=f(b) | ∃ ξ∈(a,b)，f'(ξ)=0 |
| **Lagrange** | f 在 [a,b] 连续、(a,b) 可导 | ∃ ξ∈(a,b)，f'(ξ) = (f(b)−f(a))/(b−a) |
| **Cauchy** | f,g 在 [a,b] 连续、(a,b) 可导、g'(x)≠0 | ∃ ξ∈(a,b)，f'(ξ)/g'(ξ) = (f(b)−f(a))/(g(b)−g(a)) |

### Lagrange 中值定理的几何可视化

定理告诉我们：曲线上至少存在一点，该点的切线平行于连接两端点的弦。

```python
# === Lagrange 中值定理的几何可视化 ===

def f_mvt(x):
    """示例函数：多项式，在 [-1, 1.5] 上连续可导"""
    return x**3 - 2*x**2 + 0.5*x + 1.5


def find_mvt_point(f, a, b):
    """用 SymPy 数值求解 f'(ξ) = (f(b)-f(a))/(b-a)"""
    x = sp.symbols('x', real=True)
    f_sym = x**3 - 2*x**2 + 0.5*x + 1.5
    fp_sym = sp.diff(f_sym, x)
    secant_slope = (f(b) - f(a)) / (b - a)
    eq = sp.Eq(fp_sym, secant_slope)
    solutions = sp.nsolve(eq, 0.5)  # 数值解
    return float(solutions), float(secant_slope)


def plot_lagrange_mvt():
    a, b = -1.0, 1.5
    f = f_mvt
    xi, slope = find_mvt_point(f, a, b)
    
    xs = np.linspace(a - 0.3, b + 0.3, 500)
    ys = f(xs)
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # 函数曲线
    ax.plot(xs, ys, 'b-', lw=2.5, label='f(x) = x³ − 2x² + 0.5x + 1.5')
    
    # 端点
    ax.plot(a, f(a), 'ro', markersize=12, zorder=5, label=f'端点 A({a}, {f(a):.2f})')
    ax.plot(b, f(b), 'ro', markersize=12, zorder=5, label=f'端点 B({b}, {f(b):.2f})')
    
    # 割线（弦）
    xs_secant = np.linspace(a, b, 100)
    ys_secant = slope * (xs_secant - a) + f(a)
    ax.plot(xs_secant, ys_secant, 'orange', ls='--', lw=2, alpha=0.8,
            label=f'割线: 斜率 = {slope:.3f}')
    
    # 中值点：切线平行于割线
    y_xi = f(xi)
    xs_tan = np.linspace(xi - 0.6, xi + 0.6, 100)
    ys_tan = slope * (xs_tan - xi) + y_xi
    ax.plot(xs_tan, ys_tan, 'green', lw=2.5, label=f'切线 (ξ={xi:.3f}): 斜率 = {slope:.3f}')
    ax.plot(xi, y_xi, 'go', markersize=12, zorder=6, markeredgecolor='darkgreen', markeredgewidth=2)
    
    # 垂直虚线连接端点与切线
    ax.axvline(x=a, color='gray', ls=':', lw=0.8, alpha=0.5)
    ax.axvline(x=b, color='gray', ls=':', lw=0.8, alpha=0.5)
    ax.axvline(x=xi, color='green', ls=':', lw=0.8, alpha=0.5)
    
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'Lagrange 中值定理\n存在 ξ ≈ {xi:.3f} ∈ ({a}, {b})，使得 f\'(ξ) = 割线斜率 = {slope:.3f}')
    ax.legend(loc='upper left')
    ax.set_xlim(a - 0.3, b + 0.3)
    
    plt.tight_layout()
    plt.show()
    
    print(f"✅ 找到 ξ ≈ {xi:.4f}，f'(ξ) = 割线斜率 = {slope:.4f}")

plot_lagrange_mvt()
```


> 🔑 **考研要点**：
> - 中值定理主要用于证明题（存在性证明、不等式证明）
> - Rolle 定理是证明中值定理相关题目的起点
> - 辅助函数构造法是关键技巧

---
## 1.5 泰勒展开

> $f(x) = f(x_0) + f'(x_0)(x-x_0) + \frac{f''(x_0)}{2!}(x-x_0)^2 + \cdots + \frac{f^{(n)}(x_0)}{n!}(x-x_0)^n + R_n(x)$

泰勒公式的思想：**用多项式逼近任意光滑函数**。每一项使用更高阶的导数信息来修正。

这是考研数学最重要的工具之一，用于求极限、证明不等式、近似计算。

```python
# SymPy 符号计算：泰勒展开
x = sp.symbols('x', real=True)

functions = {
    "sin(x)": sp.sin(x),
    "e^x": sp.exp(x),
    "ln(1+x)": sp.log(1 + x),
    "cos(x)": sp.cos(x),
}

for name, f_sym in functions.items():
    series = sp.series(f_sym, x, 0, 6).removeO()  # Maclaurin, 到 x^5
    print(f"{name} 的 Maclaurin 展开 (到 5 阶):")
    sp.pprint(series)
    print()
```


```python
# === 泰勒逼近动画：逐项加项，看多项式如何逼近原函数 ===

# 预计算 sin(x) 的各阶 Taylor 多项式系数
# sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + x⁹/9! - ...

import math

def sin_taylor(x, order):
    """sin(x) 的 Maclaurin 多项式，保留到 order 阶"""
    result = np.zeros_like(x)
    for k in range(order + 1):
        n = 2 * k + 1  # 奇数阶
        coeff = 1.0 / math.factorial(n)
        if k % 2 == 1:
            coeff = -coeff
        result += coeff * x**n
    return result


def plot_taylor_sin(max_order=5):
    """展示不同阶数的泰勒多项式对 sin(x) 的逼近"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    xs = np.linspace(-2*np.pi, 2*np.pi, 1000)
    ys_true = np.sin(xs)
    
    # ── 左图：多项式 vs 原函数 ──
    ax1.plot(xs, ys_true, 'k-', lw=3, alpha=0.7, label='sin(x) (原函数)', zorder=10)
    
    colors = ['#e74c3c', '#e67e22', '#2ecc71', '#3498db', '#9b59b6', '#1abc9c']
    
    for order in range(1, max_order + 1):
        ys_approx = sin_taylor(xs, order)
        label = f'T_{{{2*order+1}}}(x) (到 x^{{{2*order+1}}})'
        ax1.plot(xs, ys_approx, '--', lw=1.5, color=colors[order-1], alpha=0.8, label=label)
    
    ax1.set_xlim(-2*np.pi, 2*np.pi)
    ax1.set_ylim(-2, 2)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title('Taylor 多项式逐阶逼近 sin(x)')
    ax1.legend(loc='upper right', fontsize=9)
    ax1.axhline(y=0, color='gray', lw=0.5)
    ax1.axvline(x=0, color='gray', lw=0.5)
    
    # ── 右图：误差 |f(x) - T_n(x)| ──
    for order in range(1, max_order + 1):
        error = np.abs(ys_true - sin_taylor(xs, order))
        label = f'|sin(x) − T_{{{2*order+1}}}(x)|'
        ax2.plot(xs, error, lw=1.5, color=colors[order-1], alpha=0.8, label=label)
    
    ax2.set_xlim(-2*np.pi, 2*np.pi)
    ax2.set_xlabel('x')
    ax2.set_ylabel('绝对误差')
    ax2.set_title('逼近误差：越远离 0，需要越高阶')
    ax2.legend(loc='upper left', fontsize=9)
    ax2.axhline(y=0, color='gray', lw=0.5)
    
    plt.tight_layout()
    plt.show()


interact(plot_taylor_sin,
         max_order=IntSlider(min=1, max=10, step=1, value=5,
                            description='最高阶数', continuous_update=False));
```


**💡 关键观察**：
- 在 $x=0$ 附近，低阶逼近就已经非常精确
- 远离展开点，需要更多项才能逼近好
- 高阶项的加入显著扩展了逼近的有效范围

> 🔑 **考研要点**：记住常见函数的 Maclaurin 展开式（$e^x$、$\sin x$、$\cos x$、$\ln(1+x)$、$(1+x)^\alpha$），
> 它们是求极限和证明题的重要工具。**展开到足够高阶**是解题成功的关键。

---
## 1.6 洛必达法则

> 若 $\lim \frac{f(x)}{g(x)}$ 为 $\frac{0}{0}$ 或 $\frac{\infty}{\infty}$ 型，且 $\lim \frac{f'(x)}{g'(x)}$ 存在（或为无穷），
> 则 $\lim \frac{f(x)}{g(x)} = \lim \frac{f'(x)}{g'(x)}$

**⚠️ 注意**：洛必达法则虽好用，但需要验证条件！不是所有 $0/0$ 都能用洛必达。

```python
# SymPy 验证洛必达法则
x = sp.symbols('x', real=True)

examples = [
    ("lim_{x→0} sin(x)/x", sp.sin(x), x, 0),
    ("lim_{x→0} (e^x - 1)/x", sp.exp(x) - 1, x, 0),
    ("lim_{x→0} (1 - cos(x))/x²", 1 - sp.cos(x), x**2, 0),
    ("lim_{x→∞} ln(x)/x", sp.log(x), x, sp.oo),
    ("lim_{x→0} (x - sin(x))/x³", x - sp.sin(x), x**3, 0),
]

for name, num, den, pt in examples:
    limit_val = sp.limit(num/den, x, pt)
    num_deriv = sp.diff(num, x)
    den_deriv = sp.diff(den, x)
    lhopital_val = sp.limit(num_deriv/den_deriv, x, pt)
    print(f"{name}")
    print(f"  直接求极限:    {limit_val}")
    print(f"  洛必达(一次):  lim f'/g' = {lhopital_val}")
    print(f"  一致: {limit_val == lhopital_val}")
    print()
```


```python
# === 可视化：原函数比值 vs 导数比值的趋近过程 ===

def plot_lhopital_comparison():
    """对于 sin(x)/x，展示原比值和导数比值在 x→0 时的行为"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    xs = np.linspace(-2, 2, 500)
    # 避开 x=0 的奇点
    mask = xs != 0
    
    # ── 左图：sin(x)/x vs cos(x)/1 ──
    ax1.plot(xs[mask], np.sin(xs[mask]) / xs[mask], 'b-', lw=2.5, label='f/g = sin(x)/x')
    ax1.plot(xs, np.cos(xs), 'r--', lw=2, alpha=0.7, label="f'/g' = cos(x)/1")
    ax1.axhline(y=1, color='green', ls=':', lw=1.5, alpha=0.7, label='极限 = 1')
    ax1.axvline(x=0, color='gray', ls=':', lw=0.5)
    
    ax1.set_xlim(-2, 2)
    ax1.set_ylim(-1.5, 2)
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_title('sin(x)/x 与 cos(x) 的对比')
    ax1.legend()
    
    # ── 右图：放大 x→0 的区域 ──
    xs_zoom = np.linspace(-0.3, 0.3, 500)
    mask_z = xs_zoom != 0
    
    ax2.plot(xs_zoom[mask_z], np.sin(xs_zoom[mask_z]) / xs_zoom[mask_z], 'b-', lw=2.5, label='sin(x)/x')
    ax2.plot(xs_zoom, np.cos(xs_zoom), 'r--', lw=2, alpha=0.7, label='cos(x)')
    ax2.axhline(y=1, color='green', ls=':', lw=1.5, alpha=0.7)
    ax2.axvline(x=0, color='gray', ls=':', lw=0.5)
    
    ax2.set_xlim(-0.3, 0.3)
    ax2.set_ylim(0.95, 1.05)
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_title('放大 x→0：两者同时趋近 1')
    ax2.legend()
    
    plt.tight_layout()
    plt.show()

plot_lhopital_comparison()
```


> 🔑 **考研要点**：
> - 洛必达法则对 $0/0$ 和 $\infty/\infty$ 型有效
> - $0 \cdot \infty$、$\infty - \infty$、$1^\infty$、$0^0$、$\infty^0$ 型需要先转化为 $0/0$ 或 $\infty/\infty$
> - **并非所有情况都能用洛必达**（如 $\lim_{x\to\infty}\frac{x+\sin x}{x}$ 用洛必达会陷入循环）
> - 考研中，**泰勒展开往往比反复使用洛必达更高效**

---
## 📋 本章小结

| 概念 | 核心理解 |
|------|---------|
| ε-δ 定义 | 对于任意小的函数值误差，都能找到自变量的控制范围 |
| 极限存在 | 左右极限存在且相等 |
| 连续 vs 可导 | 可导 ⇒ 连续；连续 ⇏ 可导（如 \|x\| 在 0 处） |
| 中值定理 | 曲线上至少有一点切线平行于割线 |
| 泰勒展开 | 用多项式逐阶逼近函数，在展开点附近精度极高 |
| 洛必达法则 | 处理 0/0 或 ∞/∞ 型不定式，但务必先检查条件 |

### ⚠️ 常见错误

1. **忘记检查洛必达条件**：分子分母必须同时趋于 0 或 ∞，且导数比值极限需存在
2. **泰勒展开阶数不够**：求极限时必须展开到足够的阶数
3. **混淆连续与可导**：判断可导性必须检查左右导数
4. **忽视左右极限**：含绝对值、取整函数的极限题务必考虑左右

### 📝 自测题

1. 求 $\lim_{x\to 0}\frac{\tan x - \sin x}{x^3}$（提示：泰勒展开到 3 阶）
2. 证明 $f(x) = x^2\sin(1/x)$（$x\neq 0$），$f(0)=0$ 在 $x=0$ 可导
3. 用 Lagrange 中值定理证明：$x > 0$ 时，$\frac{x}{1+x} < \ln(1+x) < x$