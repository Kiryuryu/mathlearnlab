## 探索：复分析的直觉实验室

### 试试看 1：i 的幂循环

计算 $i^0, i^1, i^2, i^3, i^4$，你发现了什么规律？

<svg width="220" height="220" viewBox="0 0 220 220" role="img" aria-label="复平面单位圆上标出 1、i、-1、-i 四点，乘以 i 就是逆时针旋转 90°" style="margin:12px 0;display:block;">
  <g transform="translate(110,110)">
    <circle cx="0" cy="0" r="80" fill="none" stroke="var(--border)" stroke-width="1.5" />
    <line x1="-110" y1="0" x2="110" y2="0" stroke="var(--border)" stroke-width="1" />
    <line x1="0" y1="-110" x2="0" y2="110" stroke="var(--border)" stroke-width="1" />
    <text x="-108" y="-6" font-size="11" fill="var(--text-muted)">Re</text>
    <text x="6" y="-104" font-size="11" fill="var(--text-muted)">Im</text>
    <circle cx="80" cy="0" r="4" fill="var(--accent)" /><text x="88" y="6" font-size="12" fill="var(--text-primary)">1</text>
    <circle cx="0" cy="-80" r="4" fill="var(--accent)" /><text x="8" y="-84" font-size="12" fill="var(--text-primary)">i</text>
    <circle cx="-80" cy="0" r="4" fill="var(--accent)" /><text x="-104" y="6" font-size="12" fill="var(--text-primary)">-1</text>
    <circle cx="0" cy="80" r="4" fill="var(--accent)" /><text x="8" y="92" font-size="12" fill="var(--text-primary)">-i</text>
    <path d="M 80,0 A 80,80 0 0 1 0,-80" fill="none" stroke="var(--accent-warm)" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#arrC1)" />
    <text x="44" y="-44" font-size="11" fill="var(--accent-warm)">×i</text>
  </g>
  <defs>
    <marker id="arrC1" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="var(--accent-warm)" /></marker>
  </defs>
</svg>

<details>
<summary>答案</summary>
$i^0 = 1$，$i^1 = i$，$i^2 = -1$，$i^3 = -i$，$i^4 = 1$。之后每 4 次循环一次：$1, i, -1, -i$。几何上，每次乘以 $i$ 就是逆时针旋转 90°——在复平面上绕单位圆转圈。这就是为什么 $i$ 的乘法"就是旋转"。
</details>

### 试试看 2：欧拉公式的取值

用 $e^{i\theta} = \cos\theta + i\sin\theta$ 计算 $e^{i\pi/2}$ 和 $e^{i\pi}$，然后验证 $e^{i\pi} + 1 = 0$。

<svg width="220" height="220" viewBox="0 0 220 220" role="img" aria-label="复平面单位圆上标出 e^{iπ/2}=i 和 e^{iπ}=-1，旋转角分别为 90° 和 180°" style="margin:12px 0;display:block;">
  <g transform="translate(110,110)">
    <circle cx="0" cy="0" r="80" fill="none" stroke="var(--border)" stroke-width="1.5" />
    <line x1="-110" y1="0" x2="110" y2="0" stroke="var(--border)" stroke-width="1" />
    <line x1="0" y1="-110" x2="0" y2="110" stroke="var(--border)" stroke-width="1" />
    <text x="-108" y="-6" font-size="11" fill="var(--text-muted)">Re</text>
    <text x="6" y="-104" font-size="11" fill="var(--text-muted)">Im</text>
    <circle cx="80" cy="0" r="4" fill="var(--accent)" /><text x="88" y="6" font-size="12" fill="var(--text-primary)">e^{iπ}=-1</text>
    <circle cx="-80" cy="0" r="4" fill="var(--accent)" />
    <circle cx="0" cy="-80" r="4" fill="var(--accent-warm)" /><text x="-46" y="-88" font-size="12" fill="var(--accent-warm)">e^{iπ/2}=i</text>
    <path d="M 80,0 A 80,80 0 0 1 0,-80" fill="none" stroke="var(--accent-warm)" stroke-width="2" stroke-dasharray="5 4" />
    <path d="M 0,-80 A 80,80 0 0 1 -80,0" fill="none" stroke="var(--accent)" stroke-width="2" stroke-dasharray="5 4" />
    <text x="50" y="-52" font-size="11" fill="var(--accent-warm)">90°</text>
    <text x="-56" y="-40" font-size="11" fill="var(--accent)">180°</text>
  </g>
</svg>

<details>
<summary>答案</summary>
$e^{i\pi/2} = \cos(\pi/2) + i\sin(\pi/2) = 0 + i\cdot 1 = i$。所以 $e^{i\pi/2} = i$——乘以 $i$ 和 $e^{i\pi/2}$ 是同一件事（旋转 90°）。$e^{i\pi} = \cos\pi + i\sin\pi = -1 + 0i = -1$，于是 $e^{i\pi} + 1 = 0$ ✓。指数函数在复平面上就是"螺旋前进"，在 $\theta=\pi$ 时正好落在 $-1$。
</details>

### 试试看 3：1/(z−1) 的奇点

函数 $f(z) = \frac{1}{z-1}$ 在哪个点不解析？它属于什么类型的奇点？

<details>
<summary>答案</summary>
在 $z=1$ 处分母为零，$f$ 不解析。这是**简单极点**（一阶极点）：洛朗展开 $f(z) = \frac{1}{z-1}$ 中只有一个负幂项，留数 $\mathrm{Res}(f, 1) = \lim_{z\to 1}(z-1)\cdot\frac{1}{z-1} = 1$。所以 $\oint_{|z-1|=r}\frac{dz}{z-1} = 2\pi i \cdot 1 = 2\pi i$——绕极点的积分永远等于 $2\pi i$ 倍留数。
</details>

### 试试看 4：留数定理算实积分

用留数定理求 $\int_{-\infty}^{\infty} \frac{dx}{1+x^2}$。

<svg width="260" height="180" viewBox="0 0 260 180" role="img" aria-label="上半平面围道：实轴线段从 -R 到 R 加上半圆弧，极点 z=i 在围道内" style="margin:12px 0;display:block;">
  <line x1="20" y1="140" x2="240" y2="140" stroke="var(--border)" stroke-width="1.5" />
  <path d="M 20,140 L 240,140 A 110,110 0 0 1 20,140 Z" fill="none" stroke="var(--accent)" stroke-width="2" stroke-dasharray="none" />
  <line x1="20" y1="140" x2="240" y2="140" stroke="var(--accent)" stroke-width="2" />
  <circle cx="130" cy="62" r="4.5" fill="var(--accent-error)" />
  <text x="138" y="58" font-size="12" fill="var(--accent-error)">z=i (极点)</text>
  <text x="230" y="132" font-size="11" fill="var(--text-muted)">R → ∞</text>
  <text x="20" y="162" font-size="11" fill="var(--text-muted)">-R</text>
  <text x="236" y="162" font-size="11" fill="var(--text-muted)">R</text>
  <text x="130" y="26" text-anchor="middle" font-size="11" fill="var(--accent)">上半圆弧</text>
</svg>

<details>
<summary>答案</summary>
考虑上半平面围道（实轴 $[-R,R]$ + 上半圆弧）。函数 $f(z)=\frac{1}{1+z^2}=\frac{1}{(z+i)(z-i)}$ 在上半平面只有极点 $z=i$（简单极点）。留数：$\mathrm{Res}(f,i) = \lim_{z\to i}(z-i)\frac{1}{(z-i)(z+i)} = \frac{1}{2i}$。由留数定理，$\oint f = 2\pi i \cdot \frac{1}{2i} = \pi$。令 $R\to\infty$，圆弧部分趋于 0，故 $\int_{-\infty}^{\infty}\frac{dx}{1+x^2} = \pi$ ✓。一个"无穷区间"的实积分，用复平面上的一点（$z=i$）就求出来了。
</details>
