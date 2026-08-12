## 探索级数

### 试试看 1：1 的威力

1 - 1 + 1 - 1 + 1 - 1 + ... = ？

<details>
<summary>答案</summary>
这个级数不收敛。如果我们在奇数项停止，和=1；在偶数项停止，和=0。它没有极限。但 Euler 曾"证明"它等于 1/2（通过代入 x=1 到 1/(1+x) = 1 - x + x² - ... 中）。这个级数启示我们：无穷级数不总是有意义的。
</details>

### 试试看 2：收敛速度

比较这两个级数：Σ 1/n² 和 Σ 1/n。哪个收敛？收敛的速度怎样？

<svg width="300" height="190" viewBox="0 0 300 190" role="img" aria-label="Σ1/n² 的部分和收敛到 π²/6≈1.645，而 Σ1/n 的部分和持续增长" style="margin:12px 0;display:block;">
  <line x1="40" y1="160" x2="290" y2="160" stroke="var(--border)" stroke-width="1.5" />
  <line x1="40" y1="10" x2="40" y2="160" stroke="var(--border)" stroke-width="1.5" />
  <!-- target pi²/6 ≈ 1.645 -> y = 160 - 1.645*30 = 111 -->
  <line x1="40" y1="111" x2="290" y2="111" stroke="var(--accent)" stroke-width="1.2" stroke-dasharray="6 5" />
  <text x="290" y="106" text-anchor="end" font-size="11" fill="var(--accent)">π²/6≈1.645</text>
  <!-- Σ1/n² partial sums: 1,1.25,1.361,1.424,1.464,1.491,1.512,... approaching 1.645 -->
  <polyline points="40,130 65,123 90,119 115,116 140,114 165,113 190,112 215,111.5 240,111.3 265,111.2 290,111.1" fill="none" stroke="var(--accent-correct)" stroke-width="2" />
  <text x="60" y="140" font-size="11" fill="var(--accent-correct)">Σ1/n²（收敛）</text>
  <!-- Σ1/n partial sums: diverging, accelerating upward -->
  <polyline points="40,160 55,152 70,145 85,139 100,134 115,130 130,127 145,124 160,122 175,120 190,118.5 205,117 220,116 235,115 250,114 265,113.5 280,113 290,112.8" fill="none" stroke="var(--accent-error)" stroke-width="2" />
  <text x="230" y="28" font-size="11" fill="var(--accent-error)">Σ1/n（发散）</text>
</svg>

<details>
<summary>答案</summary>
Σ 1/n² 收敛（到 π²/6≈1.645），Σ 1/n 发散。
Σ 1/n² 前 10 项和 = 1.55（已接近极限 1.645），前 100 项和 = 1.635。
Σ 1/n 前 10 项和 = 2.93，前 100 项和 = 5.19，前 1000 项和 = 7.49...永远在涨。
</details>

### 试试看 3：用多项式逼近函数

用前 3 项泰勒展开近似计算 sin(0.5)。误差有多大？

<svg width="260" height="200" viewBox="0 0 260 200" role="img" aria-label="sin(x) 曲线与泰勒展开前几项在原点附近重合，x=0.5 处两者几乎重合" style="margin:12px 0;display:block;">
  <g transform="translate(20,100)">
    <line x1="0" y1="0" x2="225" y2="0" stroke="var(--border)" stroke-width="1.5" />
    <line x1="112" y1="-85" x2="112" y2="85" stroke="var(--border)" stroke-width="1.5" />
    <!-- sin(x) on -2..2, x scaled 56/unit, y scaled 40 -->
    <path d="M 0,-72 C 20,-70 40,-55 56,-40 C 72,-24 92,-8 112,0 C 132,8 152,24 168,40 C 184,55 204,70 224,72" fill="none" stroke="var(--accent)" stroke-width="2.5" />
    <!-- Taylor x - x³/6 + x⁵/120 on -1.5..1.5 -->
    <path d="M 28,-40 C 45,-33 60,-22 72,-13 C 84,-6 98,-1 112,0 C 126,1 140,6 152,13 C 164,22 179,33 196,40" fill="none" stroke="var(--accent-error)" stroke-width="2" stroke-dasharray="6 4" />
    <!-- x=0.5 marker: at x=0.5*56+112=140 -->
    <line x1="140" y1="-28" x2="140" y2="28" stroke="var(--border-focus)" stroke-width="1" stroke-dasharray="3 3" />
    <circle cx="140" cy="-12" r="3.5" fill="var(--accent)" />
    <circle cx="140" cy="-12.06" r="3.5" fill="var(--accent-error)" opacity="0.7" />
    <text x="140" y="45" text-anchor="middle" font-size="11" fill="var(--text-muted)">x=0.5</text>
    <text x="196" y="-40" font-size="11" fill="var(--accent)">sin(x)</text>
    <text x="196" y="-26" font-size="11" fill="var(--accent-error)">泰勒前3项</text>
  </g>
</svg>

<details>
<summary>答案</summary>
sin(0.5) ≈ 0.5 - 0.5³/6 + 0.5⁵/120 = 0.5 - 0.020833 + 0.002604 = 0.4793。
真实值 sin(0.5) = 0.4794... 误差只有 0.0001！
</details>

### 试试看 4：π 的级数

莱布尼茨级数 π/4 = 1 - 1/3 + 1/5 - 1/7 + ... 需要多少项才能让 π 精确到 3.14？

<details>
<summary>答案</summary>
大约需要 600 项。取 600 项后 π≈3.140... 刚到目标。这个级数收敛极慢——这就是为什么计算 π 不用这个公式，而是用拉马努金或楚德诺夫斯基的超快收敛级数。
</details>
