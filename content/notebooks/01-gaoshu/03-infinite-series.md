# 第三章：无穷级数

## 学习目标

- 直观理解数列与级数的收敛性
- 掌握各类审敛法及其几何含义
- 理解幂级数的收敛半径
- 深刻理解泰勒级数作为函数逼近
- 感受傅里叶级数如何用正弦波叠加构造任意周期函数

## 预备知识

- 数列极限的定义
- 等比级数（几何级数）的求和公式
- 导数的基本概念

> 💡 **提示**：本页面由 Jupyter Notebook 自动转换而来。
> 运行 `jupyter lab` 启动本地环境，可体验完整的**交互式可视化**（拖动滑块、3D旋转、动画播放）。
> 下方代码块仅供参考，静态页面无法执行 Python。

---

# 第三章：无穷级数

## 学习目标

- 直观理解数列与级数的收敛性
- 掌握各类审敛法及其几何含义
- 理解幂级数的收敛半径
- 深刻理解泰勒级数作为函数逼近
- 感受傅里叶级数如何用正弦波叠加构造任意周期函数

## 预备知识

- 数列极限的定义
- 等比级数（几何级数）的求和公式
- 导数的基本概念

```python
%matplotlib widget

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sympy as sp
from ipywidgets import interact, FloatSlider, IntSlider, Play, jslink, VBox, HBox
from IPython.display import display, HTML, clear_output
import sys
sys.path.insert(0, '..')

from utils.plot_config import set_style, COLORS

set_style()
sp.init_printing()

x, n, k = sp.symbols('x n k', real=True)

print("✅ 环境就绪！")
```

---
## 3.1 数列与级数的收敛

> **数列收敛**：$\lim_{n\to\infty}a_n = L$，即对任意 ε > 0，存在 N，当 n > N 时，$|a_n - L| < ε$
> **级数收敛**：部分和 $S_N = \sum_{n=1}^N a_n$ 的极限存在

级数收敛 ⇔ 部分和数列收敛。用动画感受 ε-N 的几何意义：

```python
# 符号计算：几个经典级数的收敛性
n = sp.symbols('n', integer=True, positive=True)

print("经典级数求和:")
print("-" * 45)

# 几何级数
print(f"∑_{n=0}^∞ 1/2^n  = {float(sp.summation(1/2**n, (n, 0, sp.oo))):.6f}  (= 2)")

# p-级数 (需要特殊函数)
# ∑ 1/n² = π²/6
p2 = float(sp.zeta(2))
print(f"∑_{n=1}^∞ 1/n²  = {p2:.6f}  (= π²/6)")

# 调和级数发散
print(f"∑_{n=1}^∞ 1/n  = ∞  (调和级数发散)")

# 交错调和级数
print(f"∑_{n=1}^∞ (-1)^{n+1}/n  = ln(2) ≈ {np.log(2):.6f}")
```

```python
# === 数列收敛与 ε-N 可视化 ===

def plot_sequence_epsilon_N(epsilon=0.1):
    """展示数列 a_n = n/(n+1) → 1 (n→∞)，用 ε-N 语言可视化"""
    
    ns = np.arange(1, 80)
    a_n = ns / (ns + 1)  # 趋向 1
    L = 1.0
    
    # 找到 N: 使得 n > N 时 |a_n - L| < ε
    # |n/(n+1) - 1| = 1/(n+1) < ε ⇒ n > 1/ε - 1
    N = int(np.ceil(1/epsilon - 1))
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # 序列点
    ax.scatter(ns, a_n, s=25, c='steelblue', alpha=0.7, zorder=3)
    
    # ε 带
    ax.axhspan(L - epsilon, L + epsilon, alpha=0.15, color='green', label=f'ε-带: L ± {epsilon:.2f}')
    ax.axhline(y=L + epsilon, color='green', ls='--', lw=1, alpha=0.6)
    ax.axhline(y=L - epsilon, color='green', ls='--', lw=1, alpha=0.6)
    ax.axhline(y=L, color='red', lw=1.5, alpha=0.6, label=f'极限 L = {L}')
    
    # 标注 N
    ax.axvline(x=N, color='orange', ls=':', lw=1.5, alpha=0.8, label=f'N = {N}')
    
    # 强调 n > N 的点
    ax.scatter(ns[ns > N], a_n[ns > N], s=35, c='green', alpha=0.8, zorder=4,
              label=f'n > {N}: 项进入 ε-带')
    
    ax.set_xlabel('n')
    ax.set_ylabel('a_n')
    ax.set_title(f'ε-N 定义: a_n = n/(n+1) → 1\n'
                 f'当 n > N={N} 时, |a_n - 1| < {epsilon}')
    ax.legend(loc='lower right')
    ax.set_xlim(0, 80)
    
    plt.tight_layout()
    plt.show()

interact(plot_sequence_epsilon_N,
         epsilon=FloatSlider(min=0.01, max=0.3, step=0.005, value=0.1,
                            description='ε', continuous_update=False));
```

**💡 关键观察**：无论 ε 多小，总能找到对应的 N，使得 N 之后的所有项都落在 ε-带内。

---
## 3.2 审敛法可视化

判断正项级数 $\sum a_n$ 收敛性的主要工具：

| 方法 | 思路 | 关键词 |
|------|------|--------|
| **比较判别法** | 与已知级数比较 | $a_n \leq C b_n$ |
| **比值判别法** | $\lim \|a_{n+1}/a_n\| = \rho$ | $\rho < 1$ 收敛 |
| **根值判别法** | $\lim \sqrt[n]{\|a_n\|} = \rho$ | $\rho < 1$ 收敛 |
| **积分判别法** | 与反常积分比较 | $\int_1^\infty f(x)dx$ |

### 比较判别法的几何直觉

```python
# === 比较判别法可视化 ===

def plot_comparison_test():
    """比较 ∑ 1/n²（收敛）和 ∑ 1/n（发散）"""
    
    ns = np.arange(1, 30)
    a_n = 1 / ns**2   # p-级数 p=2：收敛
    b_n = 1 / ns      # 调和级数：发散
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # ── 左：项的比较 ──
    ax1.bar(ns - 0.15, a_n, width=0.3, color='green', alpha=0.7, label='a_n = 1/n² (收敛)')
    ax1.bar(ns + 0.15, b_n, width=0.3, color='red', alpha=0.7, label='b_n = 1/n (发散)')
    ax1.set_xlabel('n')
    ax1.set_ylabel('项的值')
    ax1.set_title('通项比较: 1/n² 远小于 1/n')
    ax1.legend()
    ax1.set_xlim(0, 30)
    
    # ── 右：部分和的比较 ──
    S_a = np.cumsum(a_n)
    S_b = np.cumsum(b_n)
    
    ax2.plot(ns, S_a, 'o-', color='green', lw=2, markersize=4, label=f'S_N(1/n²) → {np.sum(a_n[:1000]):.4f}')
    ax2.plot(ns, S_b, 'o-', color='red', lw=2, markersize=4, label='S_N(1/n) → ∞')
    ax2.set_xlabel('N')
    ax2.set_ylabel('部分和 S_N')
    ax2.set_title('部分和: 一个趋近极限, 一个无限增长')
    ax2.legend()
    
    plt.suptitle('比较判别法: 1/n² ≤ 1/n (n≥1), 小级数收敛 ⇒ 大级数不一定发散', fontsize=13, y=1.02)
    plt.tight_layout()
    plt.show()

plot_comparison_test()
```

```python
# === 比值判别法可视化 ===

def plot_ratio_test(rho=0.5):
    """
    几何级数 a_n = rho^n 是理解比值判别法的关键。
    ρ = lim |a_{n+1}/a_n| < 1 时，级数被几何级数控制，从而收敛。
    """
    ns = np.arange(1, 21)
    a_n = rho**ns
    S_N = np.cumsum(a_n)
    limit = 1/(1 - rho) - 1  # 首项为 rho^1，所以和 = rho/(1-rho)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))
    
    ax1.bar(ns, a_n, color='steelblue', alpha=0.7)
    ax1.set_xlabel('n')
    ax1.set_ylabel('a_n')
    ax1.set_title(f'几何级数通项: a_n = {rho}ⁿ (ρ={rho})')
    
    ax2.plot(ns, S_N, 'o-', color='darkorange', lw=2, markersize=5)
    ax2.axhline(y=limit, color='green', ls='--', lw=1.5, label=f'极限 = {limit:.4f}')
    ax2.set_xlabel('N')
    ax2.set_ylabel('部分和 S_N')
    ax2.set_title(f'部分和收敛至 {limit:.4f}')
    ax2.legend()
    
    plt.suptitle(f'比值判别法: ρ = {rho} < 1 ⇒ 级数收敛', fontsize=13, y=1.02)
    plt.tight_layout()
    plt.show()

interact(plot_ratio_test,
         rho=FloatSlider(min=0.1, max=0.95, step=0.05, value=0.5,
                        description='ρ', continuous_update=False));
```

---
## 3.3 幂级数与收敛半径

> $\sum_{n=0}^{\infty} c_n(x-a)^n$ 的收敛半径 $R$ 由 $\frac{1}{R} = \limsup \sqrt[n]{|c_n|}$ 或 $\frac{1}{R} = \lim \left|\frac{c_{n+1}}{c_n}\right|$ 确定

在 $|x-a| < R$ 内绝对收敛，$|x-a| > R$ 外发散，$|x-a| = R$ 处需要单独判断。

```python
# 符号计算：求幂级数的收敛半径
n = sp.symbols('n', integer=True, positive=True)

print("示例 1: ∑ xⁿ/n!  (即 eˣ 的展开式)")
# c_n = 1/n!, 收敛半径 R = lim |c_n/c_{n+1}| = lim (n+1)!/n! = lim (n+1) = ∞
print("  收敛半径 R = ∞ (对任意 x 都收敛)")
print()

print("示例 2: ∑ n·xⁿ")
# c_n = n, 收敛半径 R = lim n/(n+1) = 1
r = sp.limit(n / (n+1), n, sp.oo)
print(f"  收敛半径 R = lim n/(n+1) = {r}")
print("  在 |x| < 1 收敛，|x| > 1 发散")
print()

print("示例 3: ∑ xⁿ/n²")
# c_n = 1/n², 收敛半径 R = lim (n+1)²/n² = 1
r = sp.limit((n+1)**2 / n**2, n, sp.oo)
print(f"  收敛半径 R = {r}")
print("  在 x = ±1 处也收敛 (因为 ∑ 1/n² 收敛)")
```

```python
# === 收敛半径的几何可视化 ===

def plot_radius_of_convergence():
    """展示幂级数 ∑ xⁿ (几何级数) 在 |x|<1 收敛、|x|>1 发散"""
    
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # x 轴
    xs = np.linspace(-2.5, 2.5, 500)
    
    # 对于每个 x，用部分和的值来判断收敛性
    # 几何级数 ∑ xⁿ: |x| < 1 收敛于 1/(1-x)
    
    # 画收敛区间
    ax.axvspan(-1, 1, alpha=0.12, color='green', label='收敛区间 |x| < 1')
    ax.axvspan(-2.5, -1, alpha=0.08, color='red', label='发散区域')
    ax.axvspan(1, 2.5, alpha=0.08, color='red')
    
    # 标注收敛半径
    ax.axvline(x=-1, color='green', ls='--', lw=2, alpha=0.8)
    ax.axvline(x=1, color='green', ls='--', lw=2, alpha=0.8)
    ax.annotate('x = −1', (-1, 0.85), xytext=(-2.2, 1.3),
                arrowprops=dict(arrowstyle='->', color='gray'), fontsize=11,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    ax.annotate('x = +1 (R=1)', (1, 0.85), xytext=(1.4, 1.3),
                arrowprops=dict(arrowstyle='->', color='gray'), fontsize=11,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # 对于几个 x 值，计算部分和 S_20
    N_terms = 20
    x_test = np.array([-1.5, -0.8, -0.5, 0.0, 0.3, 0.6, 0.9, 1.2])
    for xv in x_test:
        ns = np.arange(N_terms)
        terms = xv**ns
        S = np.sum(terms)
        
        if abs(xv) < 1:
            true_sum = 1/(1 - xv)
            color = 'green'
            ax.plot(xv, true_sum, 'o', color=color, markersize=12, zorder=6)
            ax.annotate(f'S_∞ = {true_sum:.1f}', (xv, true_sum),
                        xytext=(5, 12), textcoords='offset points', fontsize=10,
                        color=color, fontweight='bold')
        else:
            color = 'red'
            ax.plot(xv, S, 'x', color=color, markersize=12, markeredgewidth=2, zorder=6)
            ax.annotate(f'S_20 = {S:.0f} (发散!)', (xv, S),
                        xytext=(5, -18), textcoords='offset points', fontsize=10,
                        color=color, fontweight='bold')
    
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-5, 8)
    ax.set_xlabel('x')
    ax.set_ylabel('级数和 (或部分和)')
    ax.set_title('几何级数 ∑ xⁿ: 收敛半径 R = 1')
    ax.legend(loc='upper center')
    ax.axhline(y=0, color='gray', lw=0.5)
    
    plt.tight_layout()
    plt.show()

plot_radius_of_convergence()
```

---
## 3.4 泰勒级数 vs 原函数

> $f(x) = \sum_{n=0}^{\infty}\frac{f^{(n)}(a)}{n!}(x-a)^n$

泰勒级数是幂级数的特例。在第一章我们已经看了 sin(x) 的泰勒逼近。这里深入看一下误差分布。

```python
# === 泰勒级数逼近误差热力图 ===

def plot_taylor_error_heatmap(func_name='sin(x)'):
    """展示不同阶数和 x 位置处的逼近误差"""
    
    import math
    
    if func_name == 'sin(x)':
        def f(x): return np.sin(x)
        def taylor(x, order):
            result = np.zeros_like(x)
            for k in range(order + 1):
                m = 2 * k + 1
                coeff = 1.0 / math.factorial(m)
                if k % 2 == 1:
                    coeff = -coeff
                result += coeff * x**m
            return result
        x_range = np.linspace(-np.pi, np.pi, 200)
        x_label = 'x'
    elif func_name == 'e^x':
        def f(x): return np.exp(x)
        def taylor(x, order):
            result = np.zeros_like(x)
            for k in range(order + 1):
                result += x**k / math.factorial(k)
            return result
        x_range = np.linspace(-3, 3, 200)
        x_label = 'x'
    else:  # ln(1+x)
        def f(x): return np.log(1 + x)
        def taylor(x, order):
            result = np.zeros_like(x)
            for k in range(1, order + 1):
                coeff = 1.0 / k
                if k % 2 == 0:
                    coeff = -coeff
                result += coeff * x**k
            return result
        x_range = np.linspace(-0.9, 1.5, 200)
        x_label = 'x'
    
    max_order = 10
    errors = np.zeros((max_order, len(x_range)))
    
    for order in range(1, max_order + 1):
        errors[order - 1, :] = np.abs(f(x_range) - taylor(x_range, order))
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    im = ax.imshow(np.log10(errors + 1e-16), aspect='auto', origin='lower',
                   extent=[x_range[0], x_range[-1], 0.5, max_order + 0.5],
                   cmap='RdYlGn_r')
    
    ax.set_xlabel(x_label)
    ax.set_ylabel('泰勒多项式阶数')
    ax.set_title(f'{func_name} 的泰勒逼近误差分布 (log10|误差|)\n'
                 f'绿色 = 精确 (误差小), 红色 = 不精确 (误差大)')
    
    plt.colorbar(im, ax=ax, label='log₁₀(|误差|)')
    plt.tight_layout()
    plt.show()

from ipywidgets import Dropdown
interact(plot_taylor_error_heatmap,
         func_name=Dropdown(options=['sin(x)', 'e^x', 'ln(1+x)'], value='sin(x)',
                           description='函数'));
```

**💡 关键观察**：
- 热力图清楚地显示：在展开点 (x=0) 附近误差最小
- 阶数越高，低误差（绿色）区域越宽
- 这就是 Taylor 公式余项 $R_n(x)$ 的几何含义

---
## 3.5 ⭐ 傅里叶级数

> $f(x) = \frac{a_0}{2} + \sum_{n=1}^{\infty}\left[a_n\cos(nx) + b_n\sin(nx)\right]$
>
> 其中 $a_n = \frac{1}{\pi}\int_{-\pi}^{\pi}f(x)\cos(nx)dx$，$b_n = \frac{1}{\pi}\int_{-\pi}^{\pi}f(x)\sin(nx)dx$

傅里叶级数告诉我们：**任何周期函数都可以表示为正弦波和余弦波的叠加**。这是信号处理、图像压缩等领域的基础。

几何理解：你正在用越来越快的正弦波去「雕刻」出目标波形。

```python
# 符号计算：方波的傅里叶级数
x = sp.symbols('x', real=True)
n = sp.symbols('n', integer=True, positive=True)

print("方波 f(x) = { 1,  0 < x < π")
print("             { −1, −π < x < 0")
print()
print("傅里叶系数:")
print("  a₀ = 0 (奇函数)")
print("  a_n = 0 (奇函数)")
print("  b_n = (2/(nπ))(1 − cos(nπ)) = { 4/(nπ), n 为奇数")
print("                                  { 0,     n 为偶数")
print()

# 用 SymPy 验证
# b_n = (1/π) ∫_{-π}^{π} f(x) sin(nx) dx = (2/π) ∫_0^{π} sin(nx) dx
bn = (2/sp.pi) * sp.integrate(sp.sin(n*x), (x, 0, sp.pi))
print(f"b_n = {sp.simplify(bn)}")
print()

print("傅里叶级数:")
print("  f(x) = (4/π) [ sin(x) + sin(3x)/3 + sin(5x)/5 + sin(7x)/7 + ... ]")
print()
print("每个谐波都是奇频率的正弦波，振幅以 1/n 衰减。")
```

```python
# === ⭐ 傅里叶级数交互动画：方波的谐波叠加 ===

def plot_fourier_square_wave(n_terms=5):
    """
    用前 n_terms 个谐波叠加逼近方波。
    同时展示每个单独的谐波。
    """
    xs = np.linspace(-2*np.pi, 2*np.pi, 1000)
    
    # 方波目标（理想）
    square_wave = np.where(np.sin(xs) >= 0, 1.0, -1.0)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    
    # ── 上图：叠加结果 vs 理想方波 ──
    # 计算叠加
    fourier_sum = np.zeros_like(xs)
    colors_harmonic = plt.cm.viridis(np.linspace(0.1, 0.9, n_terms))
    
    for k in range(n_terms):
        m = 2 * k + 1  # 1, 3, 5, 7, ...
        amplitude = 4.0 / (np.pi * m)
        harmonic = amplitude * np.sin(m * xs)
        fourier_sum += harmonic
        # 画每个谐波（半透明）
        ax1.plot(xs, harmonic, lw=1, alpha=0.35, color=colors_harmonic[k],
                label=f'sin({m}x)/{m}' if k < 8 else '')
    
    ax1.plot(xs, square_wave, 'k-', lw=2.5, alpha=0.6, label='理想方波', zorder=10)
    ax1.plot(xs, fourier_sum, 'r-', lw=2.5, alpha=0.9, label=f'前 {n_terms} 项叠加', zorder=9)
    ax1.set_xlim(-2*np.pi, 2*np.pi)
    ax1.set_ylim(-1.8, 1.8)
    ax1.set_ylabel('f(x)')
    ax1.set_title(f'方波的傅里叶级数逼近 (N = {n_terms} 个谐波)')
    ax1.legend(loc='upper right', fontsize=9, ncol=2)
    ax1.axhline(y=0, color='gray', lw=0.5)
    ax1.grid(True, alpha=0.3)
    
    # ── 下图：各谐波的振幅（频谱）──
    harmonics_idx = [2*k+1 for k in range(n_terms)]
    amplitudes = [4.0/(np.pi*m) for m in harmonics_idx]
    
    ax2.stem(harmonics_idx, amplitudes, basefmt='gray', linefmt='steelblue', markerfmt='o')
    ax2.set_xlabel('谐波频率 (n)')
    ax2.set_ylabel('振幅')
    ax2.set_title('频谱: 振幅以 1/n 衰减')
    ax2.set_xlim(0, 2*n_terms + 2)
    ax2.grid(True, alpha=0.3)
    
    # 标注
    for m, amp in zip(harmonics_idx, amplitudes):
        ax2.annotate(f'{amp:.2f}', (m, amp), xytext=(5, 5),
                     textcoords='offset points', fontsize=9)
    
    plt.tight_layout()
    plt.show()

interact(plot_fourier_square_wave,
         n_terms=IntSlider(min=1, max=40, step=1, value=5,
                          description='谐波数', continuous_update=False));
```

**💡 拖动滑到 20+ 个谐波**，你会看到叠加结果越来越接近理想方波。但注意在跳变处仍然有过冲——这就是著名的**吉布斯现象**。

---
## 3.6 吉布斯现象

> 在间断点附近，傅里叶级数的部分和会出现约 **9%** 的过冲，且过冲不会因增加项数而消失。

这是一个反直觉的事实：即使取无限多项，过冲依然存在！

```python
# === 吉布斯现象的放大观察 ===

def plot_gibbs_phenomenon(n_terms=10):
    """放大观察方波间断点 x=0 附近的逼近行为"""
    
    # 聚焦在间断点 x=0 附近
    xs = np.linspace(0, np.pi/2, 2000)
    
    # 方波（在 x=0 右侧应该是 1）
    true_val = 1.0
    
    # 傅里叶级数
    fourier = np.zeros_like(xs)
    for k in range(n_terms):
        m = 2 * k + 1
        fourier += (4.0 / (np.pi * m)) * np.sin(m * xs)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # ── 左：全貌 ──
    xs_full = np.linspace(-np.pi, np.pi, 1000)
    fourier_full = np.zeros_like(xs_full)
    for k in range(n_terms):
        m = 2 * k + 1
        fourier_full += (4.0 / (np.pi * m)) * np.sin(m * xs_full)
    
    square_full = np.where(np.sin(xs_full) >= 0, 1.0, -1.0)
    
    ax1.plot(xs_full, square_full, 'k-', lw=2, alpha=0.5, label='理想方波')
    ax1.plot(xs_full, fourier_full, 'r-', lw=1.5, label=f'前 {n_terms} 项')
    ax1.axvspan(-0.3, 0.3, alpha=0.15, color='yellow', label='放大区域')
    ax1.set_xlim(-np.pi, np.pi)
    ax1.set_ylim(-1.5, 1.5)
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.set_title('方波的傅里叶逼近 (全貌)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # ── 右：放大间断点附近 ──
    # 多取几项看吉布斯过冲
    fourier_zoom = np.zeros_like(xs)
    for k in range(max(n_terms, 20)):
        m = 2 * k + 1
        fourier_zoom += (4.0 / (np.pi * m)) * np.sin(m * xs)
    
    
    ax2.plot(xs, fourier_zoom, 'r-', lw=2, label=f'前 {max(n_terms, 20)} 项叠加')
    ax2.axhline(y=true_val, color='black', ls='--', lw=1.5, alpha=0.6, label=f'理想值 = {true_val}')
    
    # 标注过冲
    gibbs_overshoot = 1.08949  # 吉布斯常数
    ax2.axhline(y=gibbs_overshoot, color='red', ls=':', lw=1.5, alpha=0.7,
                label=f'吉布斯过冲 ≈ {gibbs_overshoot:.4f} (约 +9%)')
    
    # 找第一个峰值
    peak_idx = np.argmax(fourier_zoom[:len(fourier_zoom)//2])
    ax2.plot(xs[peak_idx], fourier_zoom[peak_idx], 'ro', markersize=8, zorder=5)
    ax2.annotate(f'({xs[peak_idx]:.4f}, {fourier_zoom[peak_idx]:.4f})',
                (xs[peak_idx], fourier_zoom[peak_idx]),
                xytext=(15, 15), textcoords='offset points', fontsize=11,
                arrowprops=dict(arrowstyle='->', color='gray'))
    
    ax2.set_xlim(0, np.pi/2)
    ax2.set_ylim(0.7, 1.3)
    ax2.set_xlabel('x')
    ax2.set_ylabel('f(x)')
    ax2.set_title('🌟 吉布斯现象: 即使增加无穷多项，过冲依然存在 (~9%)')
    ax2.legend(loc='lower right')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()

interact(plot_gibbs_phenomenon,
         n_terms=IntSlider(min=1, max=50, step=1, value=10,
                          description='谐波数', continuous_update=False));
```

---
## 📋 本章小结

| 概念 | 核心理解 |
|------|---------|
| 数列收敛 | 项最终全部进入 ε-带 |
| 级数审敛 | 比较、比值、根值、积分 — 四种武器 |
| 幂级数 | 在收敛半径内相当于一个函数 |
| 泰勒级数 | 用多项式逐点逼近，误差随阶数减小 |
| 傅里叶级数 | 用正弦波叠加构造周期函数，间断点处有吉布斯现象 |

### ⚠️ 常见错误

1. **混淆必要条件与充分条件**：$a_n \to 0$ 是收敛的必要条件，但不是充分的（调和级数反例）
2. **比值/根值判别法 ρ=1 时强行下结论**
3. **收敛半径端点处忘记单独判断**
4. **傅里叶级数忘记 $a_0/2$ 的写法**

### 📝 自测题

1. 判断 $\sum_{n=1}^{\infty} \frac{n!}{n^n}$ 的收敛性（比值判别法）
2. 求 $\sum_{n=1}^{\infty} \frac{x^n}{n}$ 的收敛域
3. 求 $f(x) = |x|$ ($-\pi < x < \pi$) 的傅里叶级数