## Explore Series

### Try It 1: The Power of 1

1 - 1 + 1 - 1 + 1 - 1 + ... = ?

<details>
<summary>Answer</summary>
This series does not converge. Stop after an odd number of terms: sum = 1. After an even number: sum = 0. No limit. Euler "proved" it equals 1/2 (by substituting x = 1 into 1/(1+x) = 1 - x + x² - ...). This shows that infinite series aren't always well-behaved.
</details>

### Try It 2: Convergence Speed

Compare: Σ 1/n² and Σ 1/n. Which converges? How fast?

<svg width="300" height="190" viewBox="0 0 300 190" role="img" aria-label="Partial sums of Σ1/n² converge to π²/6≈1.645 while Σ1/n grows without bound" style="margin:12px 0;display:block;">
  <line x1="40" y1="160" x2="290" y2="160" stroke="var(--border)" stroke-width="1.5" />
  <line x1="40" y1="10" x2="40" y2="160" stroke="var(--border)" stroke-width="1.5" />
  <line x1="40" y1="111" x2="290" y2="111" stroke="var(--accent)" stroke-width="1.2" stroke-dasharray="6 5" />
  <text x="290" y="106" text-anchor="end" font-size="11" fill="var(--accent)">π²/6≈1.645</text>
  <polyline points="40,130 65,123 90,119 115,116 140,114 165,113 190,112 215,111.5 240,111.3 265,111.2 290,111.1" fill="none" stroke="var(--accent-correct)" stroke-width="2" />
  <text x="60" y="140" font-size="11" fill="var(--accent-correct)">Σ1/n² (converges)</text>
  <polyline points="40,160 55,152 70,145 85,139 100,134 115,130 130,127 145,124 160,122 175,120 190,118.5 205,117 220,116 235,115 250,114 265,113.5 280,113 290,112.8" fill="none" stroke="var(--accent-error)" stroke-width="2" />
  <text x="230" y="28" font-size="11" fill="var(--accent-error)">Σ1/n (diverges)</text>
</svg>

<details>
<summary>Answer</summary>
Σ 1/n² converges (to π²/6 ≈ 1.645), Σ 1/n diverges.
Σ 1/n²: first 10 terms = 1.55 (close to limit 1.645), first 100 terms = 1.635.
Σ 1/n: first 10 terms = 2.93, first 100 = 5.19, first 1000 = 7.49... climbing forever.
</details>

### Try It 3: Polynomial Approximations

Approximate sin(0.5) using the first 3 terms of its Taylor series. How accurate is it?

<svg width="260" height="200" viewBox="0 0 260 200" role="img" aria-label="sin(x) and its 3-term Taylor polynomial overlap near the origin; at x=0.5 they almost coincide" style="margin:12px 0;display:block;">
  <g transform="translate(20,100)">
    <line x1="0" y1="0" x2="225" y2="0" stroke="var(--border)" stroke-width="1.5" />
    <line x1="112" y1="-85" x2="112" y2="85" stroke="var(--border)" stroke-width="1.5" />
    <path d="M 0,-72 C 20,-70 40,-55 56,-40 C 72,-24 92,-8 112,0 C 132,8 152,24 168,40 C 184,55 204,70 224,72" fill="none" stroke="var(--accent)" stroke-width="2.5" />
    <path d="M 28,-40 C 45,-33 60,-22 72,-13 C 84,-6 98,-1 112,0 C 126,1 140,6 152,13 C 164,22 179,33 196,40" fill="none" stroke="var(--accent-error)" stroke-width="2" stroke-dasharray="6 4" />
    <line x1="140" y1="-28" x2="140" y2="28" stroke="var(--border-focus)" stroke-width="1" stroke-dasharray="3 3" />
    <circle cx="140" cy="-12" r="3.5" fill="var(--accent)" />
    <circle cx="140" cy="-12.06" r="3.5" fill="var(--accent-error)" opacity="0.7" />
    <text x="140" y="45" text-anchor="middle" font-size="11" fill="var(--text-muted)">x=0.5</text>
    <text x="196" y="-40" font-size="11" fill="var(--accent)">sin(x)</text>
    <text x="196" y="-26" font-size="11" fill="var(--accent-error)">Taylor (3 terms)</text>
  </g>
</svg>

<details>
<summary>Answer</summary>
sin(0.5) ≈ 0.5 - 0.5³/6 + 0.5⁵/120 = 0.5 - 0.020833 + 0.002604 = 0.4793.
True value sin(0.5) = 0.4794... error is only 0.0001!
</details>

### Try It 4: π by Series

Leibniz series π/4 = 1 - 1/3 + 1/5 - 1/7 + ... How many terms to get π ≈ 3.14?

<details>
<summary>Answer</summary>
About 600 terms. After 600 terms, π ≈ 3.14... barely there. This series converges extremely slowly — which is why π isn't computed this way. Instead, super-fast Ramanujan or Chudnovsky series are used.
</details>
