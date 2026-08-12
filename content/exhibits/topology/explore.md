## 探索：拓扑的直觉实验室

### 试试看 1：判断一笔画

下面每个图中，奇度（连接奇数条边）的顶点有几个？能不能一笔画？

<div style="display:flex;flex-wrap:wrap;gap:18px;margin:12px 0;">
  <figure style="margin:0;text-align:center;">
    <svg width="110" height="110" viewBox="0 0 100 100" role="img" aria-label="图 A：正方形，四个顶点度 2">
      <rect x="20" y="20" width="60" height="60" fill="none" stroke="var(--border-focus)" stroke-width="2.5" />
      <circle cx="20" cy="20" r="4" fill="var(--accent)" /><circle cx="80" cy="20" r="4" fill="var(--accent)" /><circle cx="80" cy="80" r="4" fill="var(--accent)" /><circle cx="20" cy="80" r="4" fill="var(--accent)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">图 A · 正方形</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;">
    <svg width="110" height="110" viewBox="0 0 100 100" role="img" aria-label="图 B：一条直线，两端度 1，中间度 2">
      <line x1="15" y1="50" x2="50" y2="50" stroke="var(--border-focus)" stroke-width="2.5" />
      <line x1="50" y1="50" x2="85" y2="50" stroke="var(--border-focus)" stroke-width="2.5" />
      <circle cx="15" cy="50" r="4" fill="var(--accent)" /><circle cx="50" cy="50" r="4" fill="var(--accent)" /><circle cx="85" cy="50" r="4" fill="var(--accent)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">图 B · 直线</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;">
    <svg width="110" height="110" viewBox="0 0 100 100" role="img" aria-label="图 C：五角星，五个顶点度 2">
      <polygon points="50,10 62,36 90,37 68,55 76,84 50,67 24,84 32,55 10,37 38,36" fill="none" stroke="var(--border-focus)" stroke-width="2.5" stroke-linejoin="round" />
      <circle cx="50" cy="10" r="4" fill="var(--accent)" /><circle cx="62" cy="36" r="4" fill="var(--accent)" /><circle cx="90" cy="37" r="4" fill="var(--accent)" /><circle cx="68" cy="55" r="4" fill="var(--accent)" /><circle cx="76" cy="84" r="4" fill="var(--accent)" />
      <circle cx="50" cy="67" r="4" fill="var(--accent)" /><circle cx="24" cy="84" r="4" fill="var(--accent)" /><circle cx="32" cy="55" r="4" fill="var(--accent)" /><circle cx="10" cy="37" r="4" fill="var(--accent)" /><circle cx="38" cy="36" r="4" fill="var(--accent)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">图 C · 五角星</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;">
    <svg width="110" height="110" viewBox="0 0 100 100" role="img" aria-label="图 D：X 形，交叉点度 4，四端度 1">
      <line x1="18" y1="18" x2="82" y2="82" stroke="var(--border-focus)" stroke-width="2.5" />
      <line x1="82" y1="18" x2="18" y2="82" stroke="var(--border-focus)" stroke-width="2.5" />
      <circle cx="18" cy="18" r="4" fill="var(--accent)" /><circle cx="82" cy="18" r="4" fill="var(--accent)" /><circle cx="82" cy="82" r="4" fill="var(--accent)" /><circle cx="18" cy="82" r="4" fill="var(--accent)" />
      <circle cx="50" cy="50" r="4" fill="var(--accent-warm)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">图 D · X 形</figcaption>
  </figure>
</div>

- 图 A：一个正方形（每条边连 2 个顶点，每个顶点度 2）
- 图 B：一条直线（两端顶点度 1，中间度 2）
- 图 C：五角星（每个顶点度 2）
- 图 D：一个"X"（交叉点度 4，四个端点度 1）

<details>
<summary>答案</summary>
- 图 A：4 个顶点全度 2，奇度 0 → 有欧拉回路 ✓
- 图 B：2 个奇度顶点 → 有欧拉路径 ✓
- 图 C：5 个顶点全度 2，奇度 0 → 有欧拉回路 ✓
- 图 D：4 个奇度端点（交叉点度 4 是偶的）→ 有欧拉路径 ✓
</details>

### 试试看 2：欧拉示性数

对一个立方体数一数：$V$（顶点）、$E$（棱）、$F$（面），然后算 $V-E+F$。

<svg width="220" height="200" viewBox="0 0 220 200" role="img" aria-label="立方体线框：8 个顶点、12 条棱、6 个面" style="margin:12px 0;display:block;">
  <polygon points="60,40 140,40 160,110 80,110" fill="color-mix(in srgb, var(--accent) 8%, transparent)" stroke="var(--border-focus)" stroke-width="2" />
  <polygon points="40,90 80,110 160,110 120,90" fill="color-mix(in srgb, var(--accent-warm) 10%, transparent)" stroke="var(--border-focus)" stroke-width="2" />
  <line x1="60" y1="40" x2="40" y2="90" stroke="var(--border-focus)" stroke-width="2" />
  <line x1="140" y1="40" x2="120" y2="90" stroke="var(--border-focus)" stroke-width="2" />
  <line x1="80" y1="110" x2="160" y2="110" stroke="var(--border-focus)" stroke-width="2" />
  <line x1="40" y1="90" x2="120" y2="90" stroke="var(--border-focus)" stroke-width="2" />
  <circle cx="60" cy="40" r="3.5" fill="var(--accent)" /><circle cx="140" cy="40" r="3.5" fill="var(--accent)" />
  <circle cx="80" cy="110" r="3.5" fill="var(--accent)" /><circle cx="160" cy="110" r="3.5" fill="var(--accent)" />
  <circle cx="40" cy="90" r="3.5" fill="var(--accent)" /><circle cx="120" cy="90" r="3.5" fill="var(--accent)" />
  <text x="25" y="35" font-size="12" fill="var(--text-secondary)">V=8</text>
  <text x="25" y="185" font-size="12" fill="var(--text-secondary)">E=12</text>
  <text x="165" y="185" font-size="12" fill="var(--text-secondary)">F=6</text>
</svg>

<details>
<summary>答案</summary>
立方体：$V=8$，$E=12$，$F=6$ → $8-12+6=2$ ✓。现在想象把立方体压扁成一个球——再三角剖分后数，仍然是 2。这就是欧拉示性数的不变性：$V-E+F$ 与形状无关，只与"洞的个数"有关。
</details>

### 试试看 3：莫比乌斯带的秘密

拿一张长纸条，扭转 180°（半圈）后把两端粘起来。现在沿带子正中线剪开，会得到几条带子？

<svg width="260" height="120" viewBox="0 0 260 120" role="img" aria-label="莫比乌斯带示意：一条带子扭转半圈后粘合，虚线表示沿中线剪开的路径" style="margin:12px 0;display:block;">
  <path d="M 20,60 C 40,20 80,20 100,60 C 120,100 160,100 180,60 C 200,20 235,15 245,50 C 255,80 235,100 210,95 C 185,90 175,70 180,50" fill="none" stroke="var(--border-focus)" stroke-width="3" />
  <path d="M 20,60 C 40,20 80,20 100,60 C 120,100 160,100 180,60 C 200,20 235,15 245,50 C 255,80 235,100 210,95 C 185,90 175,70 180,50" fill="none" stroke="var(--accent-warm)" stroke-width="1.5" stroke-dasharray="6 5" transform="translate(0,8)" />
  <text x="130" y="112" text-anchor="middle" font-size="12" fill="var(--text-secondary)">沿中线剪开 → 一条更长的带子</text>
</svg>

<details>
<summary>答案</summary>
得到**一条**更长的带子，而不是两条！因为莫比乌斯带只有一个边，沿中线剪开相当于把这条"单边"放平展开，得到的是扭转了 4 个半圈的更长的带子。如果你再沿这条新带子的中线剪开，才会得到两条互相缠绕的带子——这条纸带藏着拓扑学最著名的反直觉。
</details>

### 试试看 4：布劳威尔不动点

拿一杯水，轻轻搅动，然后观察。物理上保证：**至少有一个水分子在搅动前后位于几乎相同的位置**。

<details>
<summary>答案</summary>
这正是布劳威尔不动点定理：连续映射（搅动产生的位移场）作用在圆盘形的水面上，必有一个点回到原处附近（严格地说，存在不动点）。数学上它保证任何"把圆盘连续地映到自身"的映射都有不动点——搅拌、地图折叠、纸张揉皱后叠回，都逃不开这个定理。
</details>
