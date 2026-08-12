## 探索导数

### 试试看 1：爬山问题

你在山上，高度函数 h(x) = -x² + 4x（x 是水平位置）。你在 x=1 的位置。应该往哪个方向走才能最快上升？

<svg width="240" height="200" viewBox="0 0 240 200" role="img" aria-label="抛物线 h=-x²+4x，在 x=1 处有斜率为正的切线，指向上升方向" style="margin:12px 0;display:block;">
  <g transform="translate(20,15)">
    <line x1="0" y1="150" x2="210" y2="150" stroke="var(--border)" stroke-width="1.5" />
    <line x1="60" y1="0" x2="60" y2="170" stroke="var(--border)" stroke-width="1.5" />
    <!-- h=-x²+4x on x 0..4: x scaled *45, y = (4x-x²) scaled *18 (max 4 -> 72) -->
    <path d="M 0,78 C 15,88 30,108 45,138 M 60,150 L 65,142 L 75,122 C 90,92 105,72 120,58 C 135,48 150,42 165,38 L 180,35" fill="none" stroke="var(--accent)" stroke-width="2.5" />
    <!-- tangent at x=1 (point 45,138), slope 2 -> rise 90 over run 45 -->
    <line x1="0" y1="48" x2="90" y2="228" stroke="var(--accent-error)" stroke-width="2" stroke-dasharray="0" />
    <circle cx="45" cy="138" r="4.5" fill="var(--accent-error)" />
    <text x="38" y="128" font-size="11" fill="var(--accent-error)">x=1</text>
    <text x="96" y="180" font-size="11" fill="var(--accent-error)">往右走上坡 ↑</text>
    <text x="120" y="24" font-size="11" fill="var(--accent)">h(x)=-x²+4x</text>
  </g>
</svg>

<details>
<summary>答案</summary>
h'(x) = -2x + 4。在 x=1 处，h'(1) = 2 > 0，所以往正方向走（x 增大）会上坡。导数为正 → 函数在增加。导数是正的 → 往上走。
</details>

### 试试看 2：速度极限

一辆车的位移 s(t) = t³ - 6t² + 9t。它什么时候停下来（速度为 0）？

<svg width="240" height="200" viewBox="0 0 240 200" role="img" aria-label="三次曲线 s=t³-6t²+9t，在 t=1 和 t=3 处有水平切线（速度为零）" style="margin:12px 0;display:block;">
  <g transform="translate(20,15)">
    <line x1="0" y1="150" x2="210" y2="150" stroke="var(--border)" stroke-width="1.5" />
    <line x1="60" y1="0" x2="60" y2="170" stroke="var(--border)" stroke-width="1.5" />
    <!-- s=t³-6t²+9t on t 0..3.5, x=t*50, y=150 - s*16 -->
    <path d="M 0,150 C 25,140 50,100 62,96 C 75,92 90,120 105,130 C 120,138 140,145 165,152 L 175,154" fill="none" stroke="var(--accent)" stroke-width="2.5" />
    <line x1="40" y1="96" x2="85" y2="96" stroke="var(--accent-error)" stroke-width="2" />
    <line x1="90" y1="130" x2="120" y2="130" stroke="var(--accent-error)" stroke-width="2" />
    <circle cx="62" cy="96" r="4.5" fill="var(--accent-error)" />
    <circle cx="105" cy="130" r="4.5" fill="var(--accent-error)" />
    <text x="55" y="86" font-size="11" fill="var(--accent-error)">t=1</text>
    <text x="108" y="122" font-size="11" fill="var(--accent-error)">t=3</text>
    <text x="140" y="30" font-size="11" fill="var(--accent)">s(t)=t³-6t²+9t</text>
  </g>
</svg>

<details>
<summary>答案</summary>
v(t) = s'(t) = 3t² - 12t + 9 = 3(t² - 4t + 3) = 3(t-1)(t-3)。t=1 和 t=3 时速度为 0。
注意 t=1 前后速度从正到正（拐了一下），t=3 前后速度从负到正（掉头）。
</details>

### 试试看 3：猜变化率

f(x) = x³ 在 x=2 处的导数是多少？（不用公式，先用直觉猜）

<details>
<summary>答案</summary>
f'(x) = 3x²，f'(2) = 12。
直觉：函数值 f(2)=8，f(2.01)≈(2.01)³≈8.1206，增长了约 0.1206。变化率≈0.1206/0.01=12.06≈12。
</details>

### 试试看 4：中值定理

你开车从 A 地到 B 地，路程 120 公里，用时 1 小时。是否在某个时刻你的瞬时速度恰好是 120 km/h？

<details>
<summary>答案</summary>
是的！中值定理：如果位移函数 s(t) 连续可导，那么存在某个时刻 c，s'(c) = (s(1)-s(0))/(1-0) = 120/1 = 120。
至少有一个瞬间，速度恰好等于平均速度。这是超速罚单的数学原理。
</details>
