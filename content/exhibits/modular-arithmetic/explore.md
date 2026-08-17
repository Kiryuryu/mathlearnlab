## 探索：模运算的直觉实验室

### 试试看 1：时钟上的幂 — $a^k \bmod n$ 的循环

固定模 $n$ 和底数 $a$，依次计算 $a^1, a^2, a^3, \dots$ 对 $n$ 取余，观察序列何时开始循环。先看模 7 的世界里 3 的幂：

<svg width="320" height="240" viewBox="0 0 320 240" role="img" aria-label="3 的幂在模 7 下的循环：3→2→6→4→5→1→3" style="margin:12px 0;display:block;">
  <defs>
    <marker id="arrPow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><polygon points="0 0, 9 4.5, 0 9" fill="var(--accent)" /></marker>
  </defs>
  <g stroke="var(--accent)" stroke-width="2" fill="none" marker-end="url(#arrPow)">
    <line x1="177.3" y1="60.1" x2="202.7" y2="74.9" />
    <line x1="220" y1="105" x2="220" y2="135" />
    <line x1="202.7" y1="165.1" x2="177.3" y2="179.9" />
    <line x1="142.6" y1="180" x2="116.4" y2="165" />
    <line x1="99" y1="135" x2="99" y2="105" />
    <line x1="116.4" y1="75" x2="142.6" y2="60" />
  </g>
  <g font-size="11" fill="var(--text-muted)" text-anchor="middle">
    <text x="188" y="58">×3</text>
    <text x="230" y="116">×3</text>
    <text x="197" y="183">×3</text>
    <text x="122" y="183">×3</text>
    <text x="89" y="116">×3</text>
    <text x="122" y="58">×3</text>
  </g>
  <g font-family="var(--font-mono)" font-size="15" font-weight="700" text-anchor="middle">
    <circle cx="160" cy="50" r="20" fill="var(--bg-card)" stroke="var(--border-focus)" stroke-width="1.5" />
    <text x="160" y="55" fill="var(--text-primary)">3</text>
    <circle cx="220" cy="85" r="20" fill="var(--bg-card)" stroke="var(--border-focus)" stroke-width="1.5" />
    <text x="220" y="90" fill="var(--text-primary)">2</text>
    <circle cx="220" cy="155" r="20" fill="var(--bg-card)" stroke="var(--border-focus)" stroke-width="1.5" />
    <text x="220" y="160" fill="var(--text-primary)">6</text>
    <circle cx="160" cy="190" r="20" fill="var(--bg-card)" stroke="var(--border-focus)" stroke-width="1.5" />
    <text x="160" y="195" fill="var(--text-primary)">4</text>
    <circle cx="99" cy="155" r="20" fill="var(--bg-card)" stroke="var(--border-focus)" stroke-width="1.5" />
    <text x="99" y="160" fill="var(--text-primary)">5</text>
    <circle cx="99" cy="85" r="20" fill="var(--bg-card)" stroke="var(--border-focus)" stroke-width="1.5" />
    <text x="99" y="90" fill="var(--text-primary)">1</text>
  </g>
  <text x="160" y="228" text-anchor="middle" font-size="11" fill="var(--text-muted)">每一步 ×3（模 7）：3→2→6→4→5→1→3</text>
</svg>

序列是 $3, 2, 6, 4, 5, 1, 3, \dots$——**周期 6**：走遍所有非零剩余后回到起点。

**你来试试：**

1. $n = 5, a = 2$：序列是什么？周期多少？
2. $n = 8, a = 2$：序列会怎样？为什么？
3. 什么条件下序列能走遍所有非零剩余？

<details>
<summary>答案</summary>
1. $2, 4, 3, 1, 2, \dots$，周期 4——遍历了全部非零剩余，2 是模 5 的原根。<br>
2. $2, 4, 0, 0, 0, \dots$——一旦碰到 0 就永远停住。因为 $\gcd(2, 8) = 2 > 1$，2 的幂最终被 8 的因子"吞掉"：$2^k$ 一旦被 8 整除（$k \ge 3$），余数就永远是 0。<br>
3. 需要 $\gcd(a, n) = 1$（先保证不"塌陷"），且 $a$ 是 $n$ 的**原根**；对素数 $n$，原根一定存在。模 7 时 3 是原根，2 不是。
</details>

### 试试看 2：当一回"孙子"——物不知数

解同余方程组：$x \equiv 2 \pmod 3$，$x \equiv 3 \pmod 5$，$x \equiv 2 \pmod 7$。用中国剩余定理（见[破局心法](#method)）或耐心枚举，求最小正整数解。

<details>
<summary>答案</summary>
$x = 23$。验证：$23 \bmod 3 = 2$ ✓，$23 \bmod 5 = 3$ ✓，$23 \bmod 7 = 2$ ✓。这正是《孙子算经》"物不知数"的经典答案。用中国剩余定理：先合并前两个得 $x \equiv 8 \pmod{15}$，再与 $x \equiv 2 \pmod 7$ 合并，得 $x \equiv 23 \pmod{105}$——最小正整数解就是 23。
</details>

### 试试看 3：口算快速幂

用"平方-乘"或费马小定理心算：$2^{10} \bmod 13$ 和 $3^{1000} \bmod 7$。

<details>
<summary>答案</summary>
$2^{10} = 1024 = 78 \times 13 + 10$，所以 $2^{10} \equiv 10 \pmod{13}$。对 $3^{1000} \bmod 7$：费马小定理说 $3^6 \equiv 1 \pmod 7$，而 $1000 = 6 \times 166 + 4$，所以 $3^{1000} \equiv 3^4 = 81 \equiv 4 \pmod 7$——先让指数除以周期、再取余数，这就是同余的威力。
</details>

### 试试看 4：当一名校验码侦探

ISBN-13 的前 12 位是 `978-7-302-56645`，第 13 位校验码是多少？规则：前 12 位乘以交替权重 $1, 3, 1, 3, \dots$ 求和得 $S$，校验位 $= (10 - S \bmod 10) \bmod 10$。

<details>
<summary>答案</summary>
加权和 $S = 9+21+8+21+3+0+2+15+6+18+4+15 = 122$，$S \bmod 10 = 2$，校验位 $= 10 - 2 = 8$。完整书号是 978-7-302-56645-8。现在把其中任意一位改掉再重新计算——校验几乎必失败。一串数字的"余数指纹"，让抄写错误无处遁形。
</details>

### 延伸思考

- 生活中还有哪些"模"？星期是模 7，月份是模 12，生肖是模 12，秒表是模 60……试着找出你身边的一个循环，说出它的模数
- 把 $a^k \bmod n$ 的循环画成图：周期长的数与"塌陷到 0"的数，规律是什么？提示：看 $\gcd(a, n)$
- 为什么钟面是 12 小时？如果人类有 10 根手指，钟面会不会是 10 小时？试着设计你自己的"模 10 时钟"
