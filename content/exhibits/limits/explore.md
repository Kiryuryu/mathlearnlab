## 探索极限

### 试试看 1：你能找到 δ 吗？

对于函数 f(x) = 2x + 1，我们要证明 lim(x→3) f(x) = 7。

如果取 ε = 0.1，你需要取 δ = ______？
<details>
<summary>提示</summary>
|f(x) - 7| = |2x+1-7| = |2x-6| = 2|x-3|。所以要 |f(x)-7| < 0.1，只需 2|x-3| < 0.1，即 |x-3| < 0.05。δ = 0.05。
</details>

### 试试看 2：这个极限存在吗？

f(x) = |x|/x。当 x→0 时，极限存在吗？

<svg width="220" height="200" viewBox="0 0 220 200" role="img" aria-label="f=|x|/x 的图像：x>0 恒为 1，x<0 恒为 -1，在 x=0 处断点，左右极限不相等" style="margin:12px 0;display:block;">
  <g transform="translate(110,100)">
    <line x1="-100" y1="0" x2="100" y2="0" stroke="var(--border)" stroke-width="1.5" />
    <line x1="0" y1="-85" x2="0" y2="85" stroke="var(--border)" stroke-width="1.5" />
    <!-- y=1 for x>0 (right side), y=-1 for x<0 (left side) -->
    <line x1="0" y1="-65" x2="90" y2="-65" stroke="var(--accent)" stroke-width="3" />
    <line x1="-90" y1="65" x2="0" y2="65" stroke="var(--accent)" stroke-width="3" />
    <circle cx="0" cy="-65" r="4.5" fill="var(--bg-page)" stroke="var(--accent)" stroke-width="2" />
    <circle cx="0" cy="65" r="4.5" fill="var(--bg-page)" stroke="var(--accent)" stroke-width="2" />
    <text x="30" y="-78" font-size="12" fill="var(--accent)">+1（右极限）</text>
    <text x="-30" y="86" text-anchor="end" font-size="12" fill="var(--accent)">−1（左极限）</text>
    <text x="40" y="40" font-size="11" fill="var(--accent-error)">x=0 处断开</text>
  </g>
</svg>

<details>
<summary>思考</summary>
从右边逼近：x>0 时，f(x)=1。
从左边逼近：x<0 时，f(x)=-1。
左右极限不相等——极限不存在！
这就是为什么我们需要左右极限的概念。
</details>

### 试试看 3：猜猜看

sin(0.01) ≈ ?  (不需要计算器)

<details>
<summary>答案</summary>
当 x 很小时，sin(x) ≈ x。实际上 sin(0.01) ≈ 0.0099998... 非常接近 0.01！
这是微积分中最重要的近似之一，背后是极限 lim(x→0) sin(x)/x = 1。
</details>

### 试试看 4：调和级数的惊人性质

1 + 1/2 + 1/3 + 1/4 + ... 是收敛还是发散？猜一猜。

<details>
<summary>答案</summary>
发散！虽然每一项都趋近于 0，但加起来是无穷大。不过它的增长极慢——前 10^43 项的和才刚超过 100。

对比：1 + 1/4 + 1/9 + 1/16 + ... = π²/6 ≈ 1.645（收敛！）
</details>
