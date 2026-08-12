## 探索积分

### 试试看 1：奇函数的积分

不用计算，∫[-1,1] x³ dx = ？

<svg width="220" height="200" viewBox="0 0 220 200" role="img" aria-label="x³ 曲线在 [-1,1] 上的图形：左侧负面积和右侧正面积相互抵消" style="margin:12px 0;display:block;">
  <g transform="translate(110,100)">
    <line x1="-100" y1="0" x2="100" y2="0" stroke="var(--border)" stroke-width="1.5" />
    <line x1="0" y1="-85" x2="0" y2="85" stroke="var(--border)" stroke-width="1.5" />
    <!-- x³ curve -->
    <path d="M -100,-85 C -70,-20 -55,-8 -30,-3 L -10,0 L 10,0 L 30,3 C 55,8 70,20 100,85" fill="none" stroke="var(--accent)" stroke-width="2.5" />
    <!-- filled areas -->
    <path d="M -30,-3 C -55,-8 -70,-20 -100,-85 L -100,0 L -30,0 Z" fill="color-mix(in srgb, var(--accent-error) 25%, transparent)" />
    <path d="M 30,3 C 55,8 70,20 100,85 L 100,0 L 30,0 Z" fill="color-mix(in srgb, var(--accent-correct) 25%, transparent)" />
    <text x="-52" y="40" text-anchor="middle" font-size="11" fill="var(--accent-error)">−面积</text>
    <text x="52" y="40" text-anchor="middle" font-size="11" fill="var(--accent-correct)">+面积</text>
    <text x="-40" y="18" font-size="11" fill="var(--text-muted)">-1</text>
    <text x="34" y="18" font-size="11" fill="var(--text-muted)">1</text>
  </g>
</svg>

<details>
<summary>答案</summary>
0！x³ 是奇函数，在对称区间上的积分恒为 0。几何上：左边的负面积和右边的正面积恰好抵消。花 1 秒钟就能得到答案。
</details>

### 试试看 2：物理直觉

一个物体以 v(t)=t² 的速度运动了 3 秒。它走了多远？

<svg width="240" height="200" viewBox="0 0 240 200" role="img" aria-label="v=t² 速度曲线在 [0,3] 下方的面积即位移" style="margin:12px 0;display:block;">
  <g transform="translate(40,20)">
    <line x1="0" y1="150" x2="200" y2="150" stroke="var(--border)" stroke-width="1.5" />
    <line x1="0" y1="10" x2="0" y2="150" stroke="var(--border)" stroke-width="1.5" />
    <!-- v=t² scaled: x: 0-3 -> 0-180, y: 0-9 -> 150-10 -->
    <path d="M 0,150 L 0,150 C 30,145 60,133 90,112 C 120,80 150,42 180,0 L 180,150 Z" fill="color-mix(in srgb, var(--accent) 20%, transparent)" />
    <path d="M 0,150 C 30,145 60,133 90,112 C 120,80 150,42 180,0" fill="none" stroke="var(--accent)" stroke-width="2.5" />
    <line x1="180" y1="150" x2="180" y2="0" stroke="var(--border-focus)" stroke-width="1" stroke-dasharray="4 4" />
    <text x="185" y="158" font-size="11" fill="var(--text-muted)">t=3</text>
    <text x="90" y="130" text-anchor="middle" font-size="12" fill="var(--text-primary)">面积 = 位移 = 9 m</text>
    <text x="120" y="-4" font-size="11" fill="var(--text-muted)">v(t)=t²</text>
  </g>
</svg>

<details>
<summary>答案</summary>
位移 = ∫[0,3] t² dt = [t³/3]₀³ = 27/3 = 9 米。
积分的物理含义：速度曲线下的面积 = 位移。
</details>

### 试试看 3：无法积分的函数

你能写出 e^(-x²) 的原函数吗？

<details>
<summary>答案</summary>
不能！e^(-x²) 没有初等原函数。但这不妨碍我们求定积分——∫[-∞,∞] e^(-x²) dx = √π。有些积分只能用数值方法，但结果可以非常精确。
</details>

### 试试看 4：阿基米德的洞察

抛物线 y = x² 下从 x=0 到 x=1 的面积，用 10 个矩形近似。左端点法、右端点法、中点法哪个更准？

<svg width="240" height="200" viewBox="0 0 240 200" role="img" aria-label="y=x² 在 [0,1] 下用矩形近似：左端点法示意" style="margin:12px 0;display:block;">
  <g transform="translate(15,15)">
    <line x1="0" y1="150" x2="210" y2="150" stroke="var(--border)" stroke-width="1.5" />
    <line x1="0" y1="10" x2="0" y2="150" stroke="var(--border)" stroke-width="1.5" />
    <path d="M 0,150 C 30,149 60,145 90,137 C 120,124 150,105 180,75" fill="none" stroke="var(--accent)" stroke-width="2.5" />
    <g fill="color-mix(in srgb, var(--accent) 12%, transparent)" stroke="var(--accent)" stroke-width="1">
      <rect x="0" y="149" width="18" height="1" /><rect x="18" y="148.5" width="18" height="1.5" /><rect x="36" y="147" width="18" height="3" />
      <rect x="54" y="145" width="18" height="5" /><rect x="72" y="142" width="18" height="8" /><rect x="90" y="138" width="18" height="12" />
      <rect x="108" y="133" width="18" height="17" /><rect x="126" y="126" width="18" height="24" /><rect x="144" y="117" width="18" height="33" /><rect x="162" y="106" width="18" height="44" />
    </g>
    <text x="105" y="185" text-anchor="middle" font-size="11" fill="var(--text-muted)">左端点法</text>
  </g>
</svg>

<details>
<summary>答案</summary>
中点法通常比左右端点法精确得多。用 10 个中点矩形近似 ∫[0,1] x² dx = 1/3，中点法得 0.3325（误差 0.0008），右端点法得 0.385（误差 0.052）。
拖动黎曼和的滑块试试看！
</details>
