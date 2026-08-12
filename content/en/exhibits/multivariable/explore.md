## Explore Multivariable Calculus

### Try It 1: Where Does the Gradient Point?

f(x, y) = x² + y². At (2, 1), which direction descends fastest?

<svg width="240" height="240" viewBox="0 0 240 240" role="img" aria-label="Level curves of f=x²+y² (concentric circles); at (2,1), the gradient (4,2) points to steepest ascent, the opposite direction to fastest descent" style="margin:12px 0;display:block;">
  <g transform="translate(120,120)">
    <circle cx="0" cy="0" r="30" fill="none" stroke="var(--border)" stroke-width="1.2" />
    <circle cx="0" cy="0" r="60" fill="none" stroke="var(--border)" stroke-width="1.2" />
    <circle cx="0" cy="0" r="90" fill="none" stroke="var(--border)" stroke-width="1.2" />
    <line x1="-120" y1="0" x2="120" y2="0" stroke="var(--border)" stroke-width="1" />
    <line x1="0" y1="-120" x2="0" y2="120" stroke="var(--border)" stroke-width="1" />
    <circle cx="40" cy="20" r="4" fill="var(--accent-error)" />
    <text x="48" y="14" font-size="11" fill="var(--text-primary)">(2,1)</text>
    <line x1="40" y1="20" x2="120" y2="60" stroke="var(--accent)" stroke-width="2.5" marker-end="url(#arrG)" />
    <line x1="40" y1="20" x2="-40" y2="-20" stroke="var(--accent-warm)" stroke-width="2.5" stroke-dasharray="5 4" marker-end="url(#arrD)" />
    <text x="122" y="64" font-size="11" fill="var(--accent)">∇f=(4,2)</text>
    <text x="-78" y="-14" font-size="11" fill="var(--accent-warm)">downhill</text>
  </g>
  <defs>
    <marker id="arrG" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="var(--accent)" /></marker>
    <marker id="arrD" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="var(--accent-warm)" /></marker>
  </defs>
</svg>

<details>
<summary>Answer</summary>
∇f = (2x, 2y). At (2, 1), gradient = (4, 2). Fastest increase is along (4, 2); fastest decrease (downhill) is (-4, -2).
The gradient always points in the direction of steepest ascent — it's the math of "water flows downhill."
</details>

### Try It 2: Identify the Saddle

z = x² - y². Is the origin a maximum, minimum, or neither?

<svg width="240" height="240" viewBox="0 0 240 240" role="img" aria-label="Level curves of z=x²-y² (hyperbolas); the origin is a saddle: a valley along x, a ridge along y" style="margin:12px 0;display:block;">
  <g transform="translate(120,120)">
    <path d="M -30,-18 C -10,-30 10,-30 30,-18 M -30,18 C -10,30 10,30 30,18" fill="none" stroke="var(--accent-correct)" stroke-width="1.6" />
    <path d="M -60,-60 C -30,-90 30,-90 60,-60 M -60,60 C -30,90 30,90 60,60" fill="none" stroke="var(--accent-correct)" stroke-width="1.2" />
    <path d="M -18,-30 C -30,-10 -30,10 -18,30 M 18,-30 C 30,-10 30,10 18,30" fill="none" stroke="var(--accent-error)" stroke-width="1.6" />
    <path d="M -60,-60 C -90,-30 -90,30 -60,60 M 60,-60 C 90,-30 90,30 60,60" fill="none" stroke="var(--accent-error)" stroke-width="1.2" />
    <line x1="-120" y1="0" x2="120" y2="0" stroke="var(--border)" stroke-width="1" />
    <line x1="0" y1="-120" x2="0" y2="120" stroke="var(--border)" stroke-width="1" />
    <circle cx="0" cy="0" r="4.5" fill="var(--accent-warm)" />
    <text x="10" y="10" font-size="11" fill="var(--accent-warm)">saddle</text>
    <text x="75" y="-66" font-size="11" fill="var(--accent-correct)">along x: valley (min)</text>
    <text x="-118" y="40" font-size="11" fill="var(--accent-error)">along y: ridge (max)</text>
  </g>
</svg>

<details>
<summary>Answer</summary>
Neither — it's a saddle point! Along the x-axis (y fixed at 0), z = x² is an upward-opening parabola (minimum at origin). Along the y-axis (x fixed at 0), z = -y² is a downward-opening parabola (maximum at origin). Second derivative test: fxx·fyy - fxy² = 2·(-2) - 0 = -4 < 0 → saddle.
</details>

### Try It 3: Constrained Optimization

You have 10 meters of fence for a rectangular garden. What length and width maximize the area?

<details>
<summary>Answer</summary>
Constraint: 2x + 2y = 10 (perimeter).
Area A = xy.
Use Lagrange multipliers: let L = xy - λ(2x + 2y - 10). ∂L/∂x = y - 2λ = 0, ∂L/∂y = x - 2λ = 0 → x = y.
Substitute into constraint: 4x = 10, x = y = 2.5. A square gives maximum area (6.25 m²).
</details>

### Try It 4: 3D Visualization Challenge

Without plotting, describe the shape of f(x, y) = sin(√(x² + y²)).

<details>
<summary>Answer</summary>
Circular ripples! The function depends only on distance from the origin r = √(x² + y²). Along any ray from the origin, the value is sin(r) — oscillating forever. The overall shape looks like ripples spreading from a stone thrown into a pond — concentric circular peaks and troughs.
Try plotting z = sin(sqrt(x^2+y^2)) in the function lab!
</details>
