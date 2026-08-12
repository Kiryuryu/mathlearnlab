## Interactive: The Intuition Lab of Topology

### Try It 1: Can It Be Drawn in One Stroke?

For each graph below, how many vertices have odd degree (an odd number of edges meeting)? Can it be drawn without lifting the pen?

<div style="display:flex;flex-wrap:wrap;gap:18px;margin:12px 0;">
  <figure style="margin:0;text-align:center;">
    <svg width="110" height="110" viewBox="0 0 100 100" role="img" aria-label="Graph A: a square, each vertex degree 2">
      <rect x="20" y="20" width="60" height="60" fill="none" stroke="var(--border-focus)" stroke-width="2.5" />
      <circle cx="20" cy="20" r="4" fill="var(--accent)" /><circle cx="80" cy="20" r="4" fill="var(--accent)" /><circle cx="80" cy="80" r="4" fill="var(--accent)" /><circle cx="20" cy="80" r="4" fill="var(--accent)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">Graph A · square</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;">
    <svg width="110" height="110" viewBox="0 0 100 100" role="img" aria-label="Graph B: a straight line, endpoints degree 1, middle degree 2">
      <line x1="15" y1="50" x2="50" y2="50" stroke="var(--border-focus)" stroke-width="2.5" />
      <line x1="50" y1="50" x2="85" y2="50" stroke="var(--border-focus)" stroke-width="2.5" />
      <circle cx="15" cy="50" r="4" fill="var(--accent)" /><circle cx="50" cy="50" r="4" fill="var(--accent)" /><circle cx="85" cy="50" r="4" fill="var(--accent)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">Graph B · line</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;">
    <svg width="110" height="110" viewBox="0 0 100 100" role="img" aria-label="Graph C: a five-pointed star, each vertex degree 2">
      <polygon points="50,10 62,36 90,37 68,55 76,84 50,67 24,84 32,55 10,37 38,36" fill="none" stroke="var(--border-focus)" stroke-width="2.5" stroke-linejoin="round" />
      <circle cx="50" cy="10" r="4" fill="var(--accent)" /><circle cx="62" cy="36" r="4" fill="var(--accent)" /><circle cx="90" cy="37" r="4" fill="var(--accent)" /><circle cx="68" cy="55" r="4" fill="var(--accent)" /><circle cx="76" cy="84" r="4" fill="var(--accent)" />
      <circle cx="50" cy="67" r="4" fill="var(--accent)" /><circle cx="24" cy="84" r="4" fill="var(--accent)" /><circle cx="32" cy="55" r="4" fill="var(--accent)" /><circle cx="10" cy="37" r="4" fill="var(--accent)" /><circle cx="38" cy="36" r="4" fill="var(--accent)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">Graph C · star</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;">
    <svg width="110" height="110" viewBox="0 0 100 100" role="img" aria-label="Graph D: an X, crossing degree 4, four endpoints degree 1">
      <line x1="18" y1="18" x2="82" y2="82" stroke="var(--border-focus)" stroke-width="2.5" />
      <line x1="82" y1="18" x2="18" y2="82" stroke="var(--border-focus)" stroke-width="2.5" />
      <circle cx="18" cy="18" r="4" fill="var(--accent)" /><circle cx="82" cy="18" r="4" fill="var(--accent)" /><circle cx="82" cy="82" r="4" fill="var(--accent)" /><circle cx="18" cy="82" r="4" fill="var(--accent)" />
      <circle cx="50" cy="50" r="4" fill="var(--accent-warm)" />
    </svg>
    <figcaption style="font-size:12px;color:var(--text-muted);margin-top:4px;">Graph D · X</figcaption>
  </figure>
</div>

- Graph A: a square (each vertex has degree 2)
- Graph B: a straight line (endpoints degree 1, middle degree 2)
- Graph C: a five-pointed star (each vertex degree 2)
- Graph D: an "X" (crossing degree 4, four endpoints degree 1)

<details>
<summary>Answer</summary>
- Graph A: all 4 vertices degree 2, odd count 0 → Euler circuit exists ✓
- Graph B: 2 odd vertices → Euler path exists ✓
- Graph C: all 5 vertices degree 2, odd count 0 → Euler circuit exists ✓
- Graph D: 4 odd endpoints (the crossing, degree 4, is even) → Euler path exists ✓
</details>

### Try It 2: The Euler Characteristic

For a cube, count $V$ (vertices), $E$ (edges), $F$ (faces), then compute $V-E+F$.

<svg width="220" height="200" viewBox="0 0 220 200" role="img" aria-label="Cube wireframe: 8 vertices, 12 edges, 6 faces" style="margin:12px 0;display:block;">
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
<summary>Answer</summary>
Cube: $V=8$, $E=12$, $F=6$ → $8-12+6=2$ ✓. Now imagine squashing the cube into a sphere — triangulate and count again; it is still 2. This is the invariance of the Euler characteristic: $V-E+F$ depends not on shape but only on the number of holes.
</details>

### Try It 3: The Secret of the Möbius Strip

Take a long strip of paper, twist it 180° (half a turn), and glue the ends. Now cut along the middle line. How many strips do you get?

<svg width="260" height="120" viewBox="0 0 260 120" role="img" aria-label="Möbius strip: a band twisted half a turn and glued; dashed line shows the cut along the middle" style="margin:12px 0;display:block;">
  <path d="M 20,60 C 40,20 80,20 100,60 C 120,100 160,100 180,60 C 200,20 235,15 245,50 C 255,80 235,100 210,95 C 185,90 175,70 180,50" fill="none" stroke="var(--border-focus)" stroke-width="3" />
  <path d="M 20,60 C 40,20 80,20 100,60 C 120,100 160,100 180,60 C 200,20 235,15 245,50 C 255,80 235,100 210,95 C 185,90 175,70 180,50" fill="none" stroke="var(--accent-warm)" stroke-width="1.5" stroke-dasharray="6 5" transform="translate(0,8)" />
  <text x="130" y="112" text-anchor="middle" font-size="12" fill="var(--text-secondary)">cut along the middle → one longer strip</text>
</svg>

<details>
<summary>Answer</summary>
You get **one longer strip**, not two! Because a Möbius strip has only one edge, cutting along the middle is like laying out that single edge flat — you get a longer strip with four half-twists. If you then cut that new strip down the middle, you finally get two strips linked together — the paper strip hides topology's most famous counterintuition.
</details>

### Try It 4: Brouwer's Fixed Point

Take a glass of water, stir it gently, then look. Physics guarantees: **at least one water molecule ends up almost exactly where it started.**

<details>
<summary>Answer</summary>
This is Brouwer's fixed-point theorem: a continuous map (the displacement field of stirring) acting on the disk-like water surface must have a point returning near its original position (strictly, a fixed point). Mathematically, any continuous map of a disk into itself has a fixed point — stirring, folding a map, crumpling a paper and stacking it back — none can escape this theorem.
</details>
