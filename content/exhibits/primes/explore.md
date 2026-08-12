## 探索：数论的直觉实验室

### 试试看 1：埃拉托斯特尼筛法

列出 1 到 50 的所有整数。先划掉 1，然后从 2 开始：**每次取第一个未划掉的数（它是素数），划掉它的所有倍数**。哪些数是小于 50 的素数？

<svg width="360" height="210" viewBox="0 0 360 210" role="img" aria-label="1 到 50 的网格：1 被划掉，合数灰显，素数高亮（埃拉托斯特尼筛法结果）" style="margin:12px 0;display:block;">
  <g font-size="12" text-anchor="middle" font-family="var(--font-mono)">
    <!-- 10 cols x 5 rows, cell 32x38, origin (10,10) -->
    <text x="26" y="34" font-size="12" fill="var(--text-muted)" text-decoration="line-through">1</text>
    <text x="58" y="34" font-weight="700" fill="var(--accent)">2</text><text x="90" y="34" font-weight="700" fill="var(--accent)">3</text>
    <text x="122" y="34" fill="var(--text-muted)">4</text><text x="154" y="34" font-weight="700" fill="var(--accent)">5</text>
    <text x="186" y="34" fill="var(--text-muted)">6</text><text x="218" y="34" font-weight="700" fill="var(--accent)">7</text>
    <text x="250" y="34" fill="var(--text-muted)">8</text><text x="282" y="34" fill="var(--text-muted)">9</text><text x="314" y="34" fill="var(--text-muted)">10</text>
    <text x="26" y="72" fill="var(--text-muted)">11</text><text x="58" y="72" fill="var(--text-muted)">12</text><text x="90" y="72" font-weight="700" fill="var(--accent)">13</text>
    <text x="122" y="72" fill="var(--text-muted)">14</text><text x="154" y="72" fill="var(--text-muted)">15</text><text x="186" y="72" fill="var(--text-muted)">16</text>
    <text x="218" y="72" font-weight="700" fill="var(--accent)">17</text><text x="250" y="72" fill="var(--text-muted)">18</text><text x="282" y="72" font-weight="700" fill="var(--accent)">19</text>
    <text x="314" y="72" fill="var(--text-muted)">20</text>
    <text x="26" y="110" fill="var(--text-muted)">21</text><text x="58" y="110" fill="var(--text-muted)">22</text><text x="90" y="110" font-weight="700" fill="var(--accent)">23</text>
    <text x="122" y="110" fill="var(--text-muted)">24</text><text x="154" y="110" fill="var(--text-muted)">25</text><text x="186" y="110" fill="var(--text-muted)">26</text>
    <text x="218" y="110" fill="var(--text-muted)">27</text><text x="250" y="110" fill="var(--text-muted)">28</text><text x="282" y="110" font-weight="700" fill="var(--accent)">29</text>
    <text x="314" y="110" fill="var(--text-muted)">30</text>
    <text x="26" y="148" fill="var(--text-muted)">31</text><text x="58" y="148" fill="var(--text-muted)">32</text><text x="90" y="148" fill="var(--text-muted)">33</text>
    <text x="122" y="148" fill="var(--text-muted)">34</text><text x="154" y="148" fill="var(--text-muted)">35</text><text x="186" y="148" fill="var(--text-muted)">36</text>
    <text x="218" y="148" font-weight="700" fill="var(--accent)">37</text><text x="250" y="148" fill="var(--text-muted)">38</text><text x="282" y="148" fill="var(--text-muted)">39</text>
    <text x="314" y="148" fill="var(--text-muted)">40</text>
    <text x="26" y="186" font-weight="700" fill="var(--accent)">41</text><text x="58" y="186" fill="var(--text-muted)">42</text><text x="90" y="186" font-weight="700" fill="var(--accent)">43</text>
    <text x="122" y="186" fill="var(--text-muted)">44</text><text x="154" y="186" fill="var(--text-muted)">45</text><text x="186" y="186" fill="var(--text-muted)">46</text>
    <text x="218" y="186" font-weight="700" fill="var(--accent)">47</text><text x="250" y="186" fill="var(--text-muted)">48</text><text x="282" y="186" fill="var(--text-muted)">49</text>
    <text x="314" y="186" fill="var(--text-muted)">50</text>
  </g>
  <text x="180" y="204" text-anchor="middle" font-size="11" fill="var(--text-muted)">高亮 = 素数（共 15 个）</text>
</svg>

<details>
<summary>答案</summary>
2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47——共 15 个。注意：筛到 $\sqrt{50} \approx 7$ 就够了，因为任何合数必有一个不超过其平方根的因子。这个"划掉倍数"的过程就是最古老的素数筛法。
</details>

### 试试看 2：用费马小定理求逆元

费马小定理说：$p$ 为素数且 $p \nmid a$ 时，$a^{p-1} \equiv 1 \pmod p$，于是 $a \cdot a^{p-2} \equiv 1 \pmod p$，即 $a^{-1} \equiv a^{p-2} \pmod p$。

**用这个公式求 $3$ 在模 $7$ 下的逆元。**

<details>
<summary>答案</summary>
$3^{-1} \equiv 3^{7-2} = 3^5 = 243 \equiv 243 - 34\times 7 = 243 - 238 = 5 \pmod 7$。验证：$3 \times 5 = 15 \equiv 1 \pmod 7$ ✓。所以 $3$ 在模 $7$ 下的逆元是 $5$——这正是 RSA 解密需要的运算。
</details>

### 试试看 3：估算素数的个数

不用数，用素数定理估计：小于 $10^6$ 的素数大约有多少个？

<details>
<summary>答案</summary>
$\pi(10^6) \approx \frac{10^6}{\ln 10^6} = \frac{10^6}{6\ln 10} \approx \frac{10^6}{13.82} \approx 72{,}382$。真实值是 78,498——误差约 8%。这个"不太准但量级正确"的估计，正是素数定理作为渐近公式的含义：$x$ 越大，相对误差越小。
</details>

### 试试看 4：找一个大合数的因子

$n = 143$。用试除法：检查 $2, 3, 5, 7, 11$…… 它是不是合数？最小素因子是多少？

<details>
<summary>答案</summary>
试除到 $\sqrt{143} \approx 11.9$：143 不被 2、3、5 整除，但 $143 = 11 \times 13$。所以它是合数，最小素因子是 11。试除法的关键是只试到 $\sqrt{n}$——这保证了效率，也解释了为什么大合数难分解：因子可能分散在巨大的数轴上。
</details>
