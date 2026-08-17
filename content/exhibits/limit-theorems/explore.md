## 探索：极限定律的直觉实验室

### 试试看 1：大数定律

想象不断抛硬币。单次结果随机，但随着次数增加，正面比例越来越接近 0.5。**你觉得抛 10 次、100 次、10000 次，正面比例离 0.5 的差距分别会怎样变化？**

<svg width="300" height="180" viewBox="0 0 300 180" role="img" aria-label="正面比例随抛掷次数收敛到 0.5 的折线图，波动随次数增加而收窄" style="margin:12px 0;display:block;">
  <line x1="40" y1="150" x2="290" y2="150" stroke="var(--border)" stroke-width="1.5" />
  <line x1="40" y1="10" x2="40" y2="150" stroke="var(--border)" stroke-width="1.5" />
  <line x1="40" y1="85" x2="290" y2="85" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="6 5" />
  <text x="290" y="80" text-anchor="end" font-size="11" fill="var(--accent)">0.5</text>
  <polyline points="42,140 55,120 68,135 82,95 96,112 110,80 124,98 138,72 152,88 166,75 180,82 194,70 208,78 222,66 236,74 250,68 264,72 278,70 288,71" fill="none" stroke="var(--accent-warm)" stroke-width="2" />
  <path d="M 42,130 C 80,105 140,95 200,89 250,87 288,86 288,86 L 288,84 C 250,84 200,85 140,87 80,91 42,100 42,130" fill="none" stroke="var(--border-focus)" stroke-width="1" stroke-dasharray="4 4" />
  <text x="150" y="165" text-anchor="middle" font-size="11" fill="var(--text-muted)">抛掷次数 n →</text>
</svg>

<details>
<summary>答案</summary>
抛 10 次可能差 0.2 甚至更多；抛 100 次通常差 0.05 以内；抛 10000 次差距小于 0.01 的概率很大。注意：不是"次数越多越接近 0.5"（那没有随机性），而是**偏离的幅度在收缩**，这正是 $\frac{1}{\sqrt{n}}$ 量级的规律。
</details>

### 试试看 2：中心极限定理的魔力

无论单个随机变量是什么分布，**只要把它们加起来**，和就趋向正态分布：

<div style="display:flex;flex-wrap:wrap;gap:10px;margin:12px 0;">
  <figure style="margin:0;text-align:center;flex:1;min-width:120px;">
    <svg width="120" height="110" viewBox="0 0 120 110" role="img" aria-label="1 个骰子：均匀分布，6 根等高柱">
      <g transform="translate(8,15)">
        <rect x="10" y="0" width="12" height="70" fill="var(--accent)" /><rect x="24" y="0" width="12" height="70" fill="var(--accent)" /><rect x="38" y="0" width="12" height="70" fill="var(--accent)" />
        <rect x="52" y="0" width="12" height="70" fill="var(--accent)" /><rect x="66" y="0" width="12" height="70" fill="var(--accent)" /><rect x="80" y="0" width="12" height="70" fill="var(--accent)" />
        <line x1="0" y1="70" x2="105" y2="70" stroke="var(--border)" stroke-width="1" />
      </g>
    </svg>
    <figcaption style="font-size:11px;color:var(--text-muted);">1 个骰子 · 均匀</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;flex:1;min-width:120px;">
    <svg width="120" height="110" viewBox="0 0 120 110" role="img" aria-label="2 个骰子的和：三角形分布">
      <g transform="translate(5,15)">
        <rect x="6" y="58" width="11" height="12" fill="var(--accent)" /><rect x="18" y="44" width="11" height="26" fill="var(--accent)" /><rect x="30" y="28" width="11" height="42" fill="var(--accent)" />
        <rect x="42" y="12" width="11" height="58" fill="var(--accent)" /><rect x="54" y="0" width="11" height="70" fill="var(--accent)" /><rect x="66" y="12" width="11" height="58" fill="var(--accent)" />
        <rect x="78" y="28" width="11" height="42" fill="var(--accent)" /><rect x="90" y="44" width="11" height="26" fill="var(--accent)" /><rect x="102" y="58" width="11" height="12" fill="var(--accent)" />
        <line x1="0" y1="70" x2="115" y2="70" stroke="var(--border)" stroke-width="1" />
      </g>
    </svg>
    <figcaption style="font-size:11px;color:var(--text-muted);">2 个骰子 · 三角</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;flex:1;min-width:120px;">
    <svg width="120" height="110" viewBox="0 0 120 110" role="img" aria-label="10 个骰子的和：几乎正态分布">
      <g transform="translate(4,15)">
        <rect x="6" y="62" width="6" height="8" fill="var(--accent)" /><rect x="13" y="58" width="6" height="12" fill="var(--accent)" /><rect x="20" y="52" width="6" height="18" fill="var(--accent)" />
        <rect x="27" y="44" width="6" height="26" fill="var(--accent)" /><rect x="34" y="34" width="6" height="36" fill="var(--accent)" /><rect x="41" y="24" width="6" height="46" fill="var(--accent)" />
        <rect x="48" y="14" width="6" height="56" fill="var(--accent)" /><rect x="55" y="8" width="6" height="62" fill="var(--accent)" /><rect x="62" y="4" width="6" height="66" fill="var(--accent)" />
        <rect x="69" y="8" width="6" height="62" fill="var(--accent)" /><rect x="76" y="14" width="6" height="56" fill="var(--accent)" /><rect x="83" y="24" width="6" height="46" fill="var(--accent)" />
        <rect x="90" y="34" width="6" height="36" fill="var(--accent)" /><rect x="97" y="44" width="6" height="26" fill="var(--accent)" /><rect x="104" y="52" width="6" height="18" fill="var(--accent)" />
        <line x1="0" y1="70" x2="112" y2="70" stroke="var(--border)" stroke-width="1" />
      </g>
    </svg>
    <figcaption style="font-size:11px;color:var(--text-muted);">10 个骰子 · 近正态</figcaption>
  </figure>
</div>

<details>
<summary>答案</summary>
正是中心极限定理。身高、体重、测量误差都是无数微小、独立因素叠加的结果，所以都近似服从正态分布。关键在"和"而不在单个因素——**即使单个骰子的分布一点也不"钟形"，加起来也变钟形了。**
</details>

### 试试看 3：收敛速度

已知 $n=100$ 次试验的偏差约 0.1。要减半误差（0.05），需要多少次？

<details>
<summary>答案</summary>
偏差 $\sim \frac{\sigma}{\sqrt{n}}$，减半误差需 $\sqrt{n}$ 翻倍 → $n$ 变 4 倍，即 $n=400$。这就是"统计代价"：精度翻倍，样本量四倍。
</details>
