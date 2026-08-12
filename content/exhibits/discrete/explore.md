## 探索：图论的直觉实验室

### 试试看 1：判断一笔画

下面的图形能不能一笔画？欧拉判定法告诉你答案。

<div style="display:flex;flex-wrap:wrap;gap:20px;margin:12px 0;">
  <figure style="margin:0;text-align:center;">
    <svg width="140" height="140" viewBox="0 0 100 100" role="img" aria-label="图 A：田字网格">
      <line x1="25" y1="25" x2="50" y2="25" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="50" y1="25" x2="75" y2="25" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="25" y1="50" x2="50" y2="50" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="50" y1="50" x2="75" y2="50" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="25" y1="75" x2="50" y2="75" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="50" y1="75" x2="75" y2="75" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="25" y1="25" x2="25" y2="50" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="25" y1="50" x2="25" y2="75" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="50" y1="25" x2="50" y2="50" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="50" y1="50" x2="50" y2="75" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="75" y1="25" x2="75" y2="50" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="75" y1="50" x2="75" y2="75" stroke="var(--border-focus)" stroke-width="2" />
      <circle cx="25" cy="25" r="4" fill="var(--accent)" /><circle cx="50" cy="25" r="4" fill="var(--accent)" /><circle cx="75" cy="25" r="4" fill="var(--accent)" />
      <circle cx="25" cy="50" r="4" fill="var(--accent)" /><circle cx="50" cy="50" r="4" fill="var(--accent)" /><circle cx="75" cy="50" r="4" fill="var(--accent)" />
      <circle cx="25" cy="75" r="4" fill="var(--accent)" /><circle cx="50" cy="75" r="4" fill="var(--accent)" /><circle cx="75" cy="75" r="4" fill="var(--accent)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">图 A · 田字</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;">
    <svg width="140" height="140" viewBox="0 0 100 100" role="img" aria-label="图 B：五角星">
      <polygon points="50,8 63,36 93,38 71,58 78,88 50,72 22,88 29,58 7,38 37,36" fill="none" stroke="var(--border-focus)" stroke-width="2" stroke-linejoin="round" />
      <circle cx="50" cy="8" r="4" fill="var(--accent)" /><circle cx="63" cy="36" r="4" fill="var(--accent)" /><circle cx="93" cy="38" r="4" fill="var(--accent)" /><circle cx="71" cy="58" r="4" fill="var(--accent)" /><circle cx="78" cy="88" r="4" fill="var(--accent)" />
      <circle cx="50" cy="72" r="4" fill="var(--accent)" /><circle cx="22" cy="88" r="4" fill="var(--accent)" /><circle cx="29" cy="58" r="4" fill="var(--accent)" /><circle cx="7" cy="38" r="4" fill="var(--accent)" /><circle cx="37" cy="36" r="4" fill="var(--accent)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">图 B · 五角星</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;">
    <svg width="140" height="140" viewBox="0 0 100 100" role="img" aria-label="图 C：品字">
      <polygon points="30,10 70,10 70,50 30,50" fill="none" stroke="var(--border-focus)" stroke-width="2" />
      <polygon points="10,50 50,50 50,90 10,90" fill="none" stroke="var(--border-focus)" stroke-width="2" />
      <polygon points="50,50 90,50 90,90 50,90" fill="none" stroke="var(--border-focus)" stroke-width="2" />
      <circle cx="30" cy="10" r="4" fill="var(--accent)" /><circle cx="70" cy="10" r="4" fill="var(--accent)" /><circle cx="30" cy="50" r="4" fill="var(--accent)" /><circle cx="70" cy="50" r="4" fill="var(--accent)" />
      <circle cx="10" cy="50" r="4" fill="var(--accent)" /><circle cx="10" cy="90" r="4" fill="var(--accent)" /><circle cx="50" cy="90" r="4" fill="var(--accent)" />
      <circle cx="90" cy="50" r="4" fill="var(--accent)" /><circle cx="90" cy="90" r="4" fill="var(--accent)" />
      <circle cx="50" cy="50" r="5" fill="var(--accent-warm)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">图 C · 品字</figcaption>
  </figure>
</div>

- 图 A：一个"田"字（9 个交点，边界的度与内部十字交叉的度）
- 图 B：一个五角星
- 图 C：一个"品"字（三个正方形共享一角，没有闭环）

<details>
<summary>答案</summary>
- 图 A（田字）：四个角点度 2，四条边中点度 3（内部十字穿过），中心点度 4。奇度顶点数 = 4 → **不能一笔画**。
- 图 B（五角星）：5 个顶点度 2 → 奇度 0 → **能一笔画**（欧拉回路）。
- 图 C（品字）：8 个顶点全是偶度？仔细数——每个"口"的角共享边，有的度 2 有的度 4，奇度 0 → **能一笔画**。
</details>

### 试试看 2：验证树的性质

下面哪些是树？

<div style="display:flex;flex-wrap:wrap;gap:20px;margin:12px 0;">
  <figure style="margin:0;text-align:center;">
    <svg width="150" height="80" viewBox="0 0 150 60" role="img" aria-label="图 A：直链三顶点两边的树">
      <line x1="20" y1="30" x2="75" y2="30" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="75" y1="30" x2="130" y2="30" stroke="var(--border-focus)" stroke-width="2" />
      <circle cx="20" cy="30" r="4" fill="var(--accent)" /><circle cx="75" cy="30" r="4" fill="var(--accent)" /><circle cx="130" cy="30" r="4" fill="var(--accent)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">图 A · 直链（树）</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;">
    <svg width="150" height="80" viewBox="0 0 150 60" role="img" aria-label="图 B：L 形四顶点三边的树">
      <line x1="20" y1="50" x2="70" y2="50" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="70" y1="50" x2="70" y2="12" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="70" y1="12" x2="115" y2="12" stroke="var(--border-focus)" stroke-width="2" />
      <circle cx="20" cy="50" r="4" fill="var(--accent)" /><circle cx="70" cy="50" r="4" fill="var(--accent)" /><circle cx="70" cy="12" r="4" fill="var(--accent)" /><circle cx="115" cy="12" r="4" fill="var(--accent)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">图 B · L 形（树）</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;">
    <svg width="150" height="80" viewBox="0 0 150 60" role="img" aria-label="图 C：断开的两组，不是树">
      <line x1="20" y1="15" x2="60" y2="15" stroke="var(--border-focus)" stroke-width="2" />
      <circle cx="20" cy="15" r="4" fill="var(--accent)" /><circle cx="60" cy="15" r="4" fill="var(--accent)" />
      <circle cx="110" cy="45" r="4" fill="var(--text-muted)" /><circle cx="135" cy="45" r="4" fill="var(--text-muted)" />
      <text x="110" y="60" text-anchor="middle" font-size="10" fill="var(--text-muted)">断开</text>
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">图 C · 断开两组（非树）</figcaption>
  </figure>
</div>

- 图 A：三个顶点、两条边、一条直链
- 图 B：四个顶点、三条边、一个"L"形
- 图 C：四个顶点、三条边、但分成两组（两个孤立顶点 + 一条边）

<details>
<summary>答案</summary>
- 图 A：连通 + 3 顶点 2 边 → **是树** ✓
- 图 B：连通 + 4 顶点 3 边 → **是树** ✓
- 图 C：有 4 顶点 3 边但不连通 → **不是树**（$n-1$ 条边还不够，连通性也必要）

关键：树 = 连通 + 边数 = 顶点数 − 1，两个条件缺一不可。
</details>

### 试试看 3：地图染色

下面这张"地图"有 4 个区域，相邻区域不能同色。最少需要几种颜色？

<svg width="220" height="180" viewBox="0 0 220 180" role="img" aria-label="四区域地图：A 与 B、C 相邻，B 与 A、C、D 相邻，C 与 A、B、D 相邻，D 与 B、C 相邻" style="margin:12px 0;display:block;">
  <polygon points="110,10 210,10 210,85 110,85" fill="color-mix(in srgb, var(--accent) 18%, var(--bg-card))" stroke="var(--border-focus)" stroke-width="2" />
  <polygon points="10,95 105,95 105,170 10,170" fill="color-mix(in srgb, var(--accent-warm) 18%, var(--bg-card))" stroke="var(--border-focus)" stroke-width="2" />
  <polygon points="110,95 210,95 210,170 110,170" fill="color-mix(in srgb, var(--accent-correct) 16%, var(--bg-card))" stroke="var(--border-focus)" stroke-width="2" />
  <polygon points="105,10 110,10 110,90 105,90" fill="color-mix(in srgb, var(--accent-error) 16%, var(--bg-card))" stroke="var(--border-focus)" stroke-width="2" />
  <text x="160" y="52" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-primary)">A</text>
  <text x="57" y="138" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-primary)">B</text>
  <text x="160" y="138" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-primary)">C</text>
  <text x="107" y="52" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-primary)">D</text>
</svg>

- 区域 A 与 B、C 相邻
- 区域 B 与 A、C、D 相邻
- 区域 C 与 A、B、D 相邻
- 区域 D 与 B、C 相邻

<details>
<summary>答案</summary>
把区域画成顶点、相邻画成边，得到图：A–B、A–C、B–C、B–D、C–D（这是一个 4 环加对角线）。贪心染色：A 染 1，B 染 2，C 与 A、B 都相邻必须染 3，D 与 B、C 相邻但 A 可用 → D 染 1。**只需 3 种颜色**（A、D 同色）。注意这不是平面图最坏情形——有些地图需要 4 色，但四色定理保证永远不会超过 4。
</details>

### 试试看 4：最小生成树

四个城市之间的距离：AB=2, AC=5, AD=4, BC=3, BD=7, CD=6。要铺设管道连接所有城市且总长度最短，选哪几条路？

<svg width="240" height="200" viewBox="0 0 240 200" role="img" aria-label="四个城市的带权完全图，边标注距离" style="margin:12px 0;display:block;">
  <line x1="45" y1="40" x2="195" y2="40" stroke="var(--border)" stroke-width="1.5" />
  <line x1="45" y1="40" x2="70" y2="160" stroke="var(--border)" stroke-width="1.5" />
  <line x1="45" y1="40" x2="195" y2="160" stroke="var(--border)" stroke-width="1.5" />
  <line x1="195" y1="40" x2="70" y2="160" stroke="var(--border)" stroke-width="1.5" />
  <line x1="195" y1="40" x2="195" y2="160" stroke="var(--border)" stroke-width="1.5" />
  <line x1="70" y1="160" x2="195" y2="160" stroke="var(--border)" stroke-width="1.5" />
  <text x="120" y="30" text-anchor="middle" font-size="12" fill="var(--text-secondary)">2</text>
  <text x="42" y="105" text-anchor="middle" font-size="12" fill="var(--text-secondary)">4</text>
  <text x="118" y="112" text-anchor="middle" font-size="12" fill="var(--text-secondary)">7</text>
  <text x="128" y="90" text-anchor="middle" font-size="12" fill="var(--text-secondary)">3</text>
  <text x="205" y="105" text-anchor="middle" font-size="12" fill="var(--text-secondary)">6</text>
  <text x="128" y="180" text-anchor="middle" font-size="12" fill="var(--text-secondary)">5</text>
  <circle cx="45" cy="40" r="5" fill="var(--accent)" /><text x="38" y="30" font-size="13" font-weight="700" fill="var(--text-primary)">A</text>
  <circle cx="195" cy="40" r="5" fill="var(--accent)" /><text x="202" y="30" font-size="13" font-weight="700" fill="var(--text-primary)">B</text>
  <circle cx="70" cy="160" r="5" fill="var(--accent)" /><text x="60" y="185" font-size="13" font-weight="700" fill="var(--text-primary)">D</text>
  <circle cx="195" cy="160" r="5" fill="var(--accent)" /><text x="203" y="185" font-size="13" font-weight="700" fill="var(--text-primary)">C</text>
</svg>

<details>
<summary>答案</summary>
用 Kruskal 算法从小到大选边、避免成环：选 AB(2) → 选 BC(3) → 下一步 AD(4)（CD=5、AC=5 更大）→ 此时 4 个顶点已连通（AB、BC、AD 三条边，4 顶点 3 边 = 树）。总长 $2+3+4=9$。验证：这是最小生成树，任何其他三边组合总长都不小于 9。
</details>
