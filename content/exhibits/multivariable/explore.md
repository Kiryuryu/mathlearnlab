## 探索多元微积分

### 试试看 1：梯度指向哪里？

f(x,y) = x² + y²。在点 (2,1) 处，沿什么方向走能最快下山？

<svg width="240" height="240" viewBox="0 0 240 240" role="img" aria-label="f=x²+y² 的等高线（同心圆），在点 (2,1) 处标注梯度向量 (4,2) 指向最大增加方向，反方向 (4,2) 指向最快下山" style="margin:12px 0;display:block;">
  <g transform="translate(120,120)">
    <circle cx="0" cy="0" r="30" fill="none" stroke="var(--border)" stroke-width="1.2" />
    <circle cx="0" cy="0" r="60" fill="none" stroke="var(--border)" stroke-width="1.2" />
    <circle cx="0" cy="0" r="90" fill="none" stroke="var(--border)" stroke-width="1.2" />
    <line x1="-120" y1="0" x2="120" y2="0" stroke="var(--border)" stroke-width="1" />
    <line x1="0" y1="-120" x2="0" y2="120" stroke="var(--border)" stroke-width="1" />
    <!-- Point (2,1) mapped to ~(2/4.5)*90, (1/4.5)*90 => (40, 20) -->
    <circle cx="40" cy="20" r="4" fill="var(--accent-error)" />
    <text x="48" y="14" font-size="11" fill="var(--text-primary)">(2,1)</text>
    <!-- gradient (4,2) scaled to ~ (80, 40) -->
    <line x1="40" y1="20" x2="120" y2="60" stroke="var(--accent)" stroke-width="2.5" marker-end="url(#arrG)" />
    <line x1="40" y1="20" x2="-40" y2="-20" stroke="var(--accent-warm)" stroke-width="2.5" stroke-dasharray="5 4" marker-end="url(#arrD)" />
    <text x="122" y="64" font-size="11" fill="var(--accent)">∇f=(4,2)</text>
    <text x="-78" y="-14" font-size="11" fill="var(--accent-warm)">下山</text>
  </g>
  <defs>
    <marker id="arrG" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="var(--accent)" /></marker>
    <marker id="arrD" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="var(--accent-warm)" /></marker>
  </defs>
</svg>

<details>
<summary>答案</summary>
∇f = (2x, 2y)。在 (2,1) 处，梯度 = (4, 2)。最快增加的方向是 (4, 2)；最快减少的方向（下山）是 (-4, -2)。
梯度总是指向函数值增长最快的方向——就像水往低处流的数学描述。
</details>

### 试试看 2：鞍点识别

z = x² - y²。原点 (0,0) 是极大值点、极小值点、还是都不是？

<svg width="240" height="240" viewBox="0 0 240 240" role="img" aria-label="z=x²-y² 的等高线（双曲线族），原点为鞍点：沿 x 轴是谷、沿 y 轴是脊" style="margin:12px 0;display:block;">
  <g transform="translate(120,120)">
    <path d="M -30,-18 C -10,-30 10,-30 30,-18 M -30,18 C -10,30 10,30 30,18" fill="none" stroke="var(--accent-correct)" stroke-width="1.6" />
    <path d="M -60,-60 C -30,-90 30,-90 60,-60 M -60,60 C -30,90 30,90 60,60" fill="none" stroke="var(--accent-correct)" stroke-width="1.2" />
    <path d="M -18,-30 C -30,-10 -30,10 -18,30 M 18,-30 C 30,-10 30,10 18,30" fill="none" stroke="var(--accent-error)" stroke-width="1.6" />
    <path d="M -60,-60 C -90,-30 -90,30 -60,60 M 60,-60 C 90,-30 90,30 60,60" fill="none" stroke="var(--accent-error)" stroke-width="1.2" />
    <line x1="-120" y1="0" x2="120" y2="0" stroke="var(--border)" stroke-width="1" />
    <line x1="0" y1="-120" x2="0" y2="120" stroke="var(--border)" stroke-width="1" />
    <circle cx="0" cy="0" r="4.5" fill="var(--accent-warm)" />
    <text x="10" y="10" font-size="11" fill="var(--accent-warm)">鞍点</text>
    <text x="75" y="-66" font-size="11" fill="var(--accent-correct)">沿 x：谷（极小）</text>
    <text x="-108" y="40" font-size="11" fill="var(--accent-error)">沿 y：脊（极大）</text>
  </g>
</svg>

<details>
<summary>答案</summary>
都不是——是鞍点！沿 x 轴方向（固定 y=0），z=x² 是开口向上的抛物线（原点极小）；沿 y 轴方向（固定 x=0），z=-y² 是开口向下的抛物线（原点极大）。二阶判别：fxx·fyy - fxy² = 2·(-2) - 0 = -4 < 0 → 鞍点。
</details>

### 试试看 3：约束优化

用 10 米长的篱笆围一个长方形区域。长和宽各取多少，面积最大？

<details>
<summary>答案</summary>
约束：2x + 2y = 10（周长）。
面积 A = xy。
用 Lagrange 乘数法：设 L = xy - λ(2x+2y-10)。∂L/∂x = y - 2λ = 0, ∂L/∂y = x - 2λ = 0 → x = y。
代入约束：4x = 10, x = y = 2.5。正方形面积最大（6.25 m²）。
</details>

### 试试看 4：三维可视化挑战

不画图，描述 f(x,y) = sin(√(x²+y²)) 的形状。

<details>
<summary>答案</summary>
圆形波纹！函数只依赖于到原点的距离 r = √(x²+y²)。沿任意从原点出发的射线，函数值是 sin(r)——不停地振荡。整体看起来像一个池塘里投下石头后的涟漪——一圈圈同心圆波峰波谷。
去函数工坊画 z = sin(sqrt(x^2+y^2)) 看看！
</details>
