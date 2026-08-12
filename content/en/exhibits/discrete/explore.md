## Interactive: The Intuition Lab of Graph Theory

### Try It 1: Can It Be Drawn in One Stroke?

Can the following figures be drawn without lifting the pen? Euler's rule decides.

<div style="display:flex;flex-wrap:wrap;gap:20px;margin:12px 0;">
  <figure style="margin:0;text-align:center;">
    <svg width="140" height="140" viewBox="0 0 100 100" role="img" aria-label="Figure A: tian grid">
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
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">Figure A · tian grid</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;">
    <svg width="140" height="140" viewBox="0 0 100 100" role="img" aria-label="Figure B: five-pointed star">
      <polygon points="50,8 63,36 93,38 71,58 78,88 50,72 22,88 29,58 7,38 37,36" fill="none" stroke="var(--border-focus)" stroke-width="2" stroke-linejoin="round" />
      <circle cx="50" cy="8" r="4" fill="var(--accent)" /><circle cx="63" cy="36" r="4" fill="var(--accent)" /><circle cx="93" cy="38" r="4" fill="var(--accent)" /><circle cx="71" cy="58" r="4" fill="var(--accent)" /><circle cx="78" cy="88" r="4" fill="var(--accent)" />
      <circle cx="50" cy="72" r="4" fill="var(--accent)" /><circle cx="22" cy="88" r="4" fill="var(--accent)" /><circle cx="29" cy="58" r="4" fill="var(--accent)" /><circle cx="7" cy="38" r="4" fill="var(--accent)" /><circle cx="37" cy="36" r="4" fill="var(--accent)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">Figure B · star</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;">
    <svg width="140" height="140" viewBox="0 0 100 100" role="img" aria-label="Figure C: pin shape, three squares sharing a corner">
      <polygon points="30,10 70,10 70,50 30,50" fill="none" stroke="var(--border-focus)" stroke-width="2" />
      <polygon points="10,50 50,50 50,90 10,90" fill="none" stroke="var(--border-focus)" stroke-width="2" />
      <polygon points="50,50 90,50 90,90 50,90" fill="none" stroke="var(--border-focus)" stroke-width="2" />
      <circle cx="30" cy="10" r="4" fill="var(--accent)" /><circle cx="70" cy="10" r="4" fill="var(--accent)" /><circle cx="30" cy="50" r="4" fill="var(--accent)" /><circle cx="70" cy="50" r="4" fill="var(--accent)" />
      <circle cx="10" cy="50" r="4" fill="var(--accent)" /><circle cx="10" cy="90" r="4" fill="var(--accent)" /><circle cx="50" cy="90" r="4" fill="var(--accent)" />
      <circle cx="90" cy="50" r="4" fill="var(--accent)" /><circle cx="90" cy="90" r="4" fill="var(--accent)" />
      <circle cx="50" cy="50" r="5" fill="var(--accent-warm)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">Figure C · pin shape</figcaption>
  </figure>
</div>

- Figure A: a "tian" grid (3×3 lattice — boundary and internal cross)
- Figure B: a five-pointed star
- Figure C: three squares sharing one corner, forming no closed loop

<details>
<summary>Answer</summary>
- Figure A (3×3 lattice): four corners have degree 2, four edge-midpoints degree 3 (the internal cross passes through), center degree 4. Odd-degree count = 4 → **cannot**.
- Figure B (star): 5 vertices of degree 2 → odd count 0 → **can** (Euler circuit).
- Figure C (three squares sharing a corner): each square's corners share edges — all degrees are even → **can**.
</details>

### Try It 2: Verify the Tree Properties

Which of the following are trees?

<div style="display:flex;flex-wrap:wrap;gap:20px;margin:12px 0;">
  <figure style="margin:0;text-align:center;">
    <svg width="150" height="80" viewBox="0 0 150 60" role="img" aria-label="Graph A: a straight chain — a tree">
      <line x1="20" y1="30" x2="75" y2="30" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="75" y1="30" x2="130" y2="30" stroke="var(--border-focus)" stroke-width="2" />
      <circle cx="20" cy="30" r="4" fill="var(--accent)" /><circle cx="75" cy="30" r="4" fill="var(--accent)" /><circle cx="130" cy="30" r="4" fill="var(--accent)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">Graph A · chain (tree)</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;">
    <svg width="150" height="80" viewBox="0 0 150 60" role="img" aria-label="Graph B: an L shape — a tree">
      <line x1="20" y1="50" x2="70" y2="50" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="70" y1="50" x2="70" y2="12" stroke="var(--border-focus)" stroke-width="2" />
      <line x1="70" y1="12" x2="115" y2="12" stroke="var(--border-focus)" stroke-width="2" />
      <circle cx="20" cy="50" r="4" fill="var(--accent)" /><circle cx="70" cy="50" r="4" fill="var(--accent)" /><circle cx="70" cy="12" r="4" fill="var(--accent)" /><circle cx="115" cy="12" r="4" fill="var(--accent)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">Graph B · L shape (tree)</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;">
    <svg width="150" height="80" viewBox="0 0 150 60" role="img" aria-label="Graph C: disconnected, not a tree">
      <line x1="20" y1="15" x2="60" y2="15" stroke="var(--border-focus)" stroke-width="2" />
      <circle cx="20" cy="15" r="4" fill="var(--accent)" /><circle cx="60" cy="15" r="4" fill="var(--accent)" />
      <circle cx="110" cy="45" r="4" fill="var(--text-muted)" /><circle cx="135" cy="45" r="4" fill="var(--text-muted)" />
      <text x="110" y="60" text-anchor="middle" font-size="10" fill="var(--text-muted)">disconnected</text>
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">Graph C · disconnected (not a tree)</figcaption>
  </figure>
</div>

- Graph A: three vertices, two edges, a straight chain
- Graph B: four vertices, three edges, an "L" shape
- Graph C: four vertices, three edges, but split into two groups (two isolated vertices + one edge)

<details>
<summary>Answer</summary>
- Graph A: connected + 3 vertices 2 edges → **tree** ✓
- Graph B: connected + 4 vertices 3 edges → **tree** ✓
- Graph C: has 4 vertices 3 edges but is disconnected → **not a tree** ($n-1$ edges is not enough; connectivity is also required)

Key: tree = connected AND edges = vertices − 1; both conditions are necessary.
</details>

### Try It 3: Map Coloring

This "map" has 4 regions; adjacent regions cannot share a color. How few colors are needed?

<svg width="220" height="180" viewBox="0 0 220 180" role="img" aria-label="Four-region map: A borders B and C; B borders A, C, D; C borders A, B, D; D borders B and C" style="margin:12px 0;display:block;">
  <polygon points="110,10 210,10 210,85 110,85" fill="color-mix(in srgb, var(--accent) 18%, var(--bg-card))" stroke="var(--border-focus)" stroke-width="2" />
  <polygon points="10,95 105,95 105,170 10,170" fill="color-mix(in srgb, var(--accent-warm) 18%, var(--bg-card))" stroke="var(--border-focus)" stroke-width="2" />
  <polygon points="110,95 210,95 210,170 110,170" fill="color-mix(in srgb, var(--accent-correct) 16%, var(--bg-card))" stroke="var(--border-focus)" stroke-width="2" />
  <polygon points="105,10 110,10 110,90 105,90" fill="color-mix(in srgb, var(--accent-error) 16%, var(--bg-card))" stroke="var(--border-focus)" stroke-width="2" />
  <text x="160" y="52" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-primary)">A</text>
  <text x="57" y="138" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-primary)">B</text>
  <text x="160" y="138" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-primary)">C</text>
  <text x="107" y="52" text-anchor="middle" font-size="18" font-weight="700" fill="var(--text-primary)">D</text>
</svg>

- Region A borders B and C
- Region B borders A, C, D
- Region C borders A, B, D
- Region D borders B and C

<details>
<summary>Answer</summary>
Draw regions as vertices and borders as edges: you get A–B, A–C, B–C, B–D, C–D (a 4-cycle plus a diagonal). Greedy coloring: A=1, B=2, C must be 3 (borders both A and B), D borders B and C but A is free → D=1. **Only 3 colors** (A and D share). Note this is not the worst planar case — some maps need 4 colors, but the four color theorem guarantees never more than 4.
</details>

### Try It 4: Minimum Spanning Tree

Distances among four cities: AB=2, AC=5, AD=4, BC=3, BD=7, CD=6. To lay pipe connecting all cities with minimum total length, which roads do you choose?

<svg width="240" height="200" viewBox="0 0 240 200" role="img" aria-label="Complete weighted graph on four cities with edge distances" style="margin:12px 0;display:block;">
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
<summary>Answer</summary>
Use Kruskal's algorithm — pick edges smallest-first, avoiding cycles: pick AB(2) → pick BC(3) → next AD(4) (CD=5, AC=5 are larger) → now all 4 vertices are connected (AB, BC, AD = three edges, 4 vertices, 3 edges = a tree). Total $2+3+4=9$. Verify: this is a minimum spanning tree; any other combination of three edges has total length ≥ 9.
</details>
