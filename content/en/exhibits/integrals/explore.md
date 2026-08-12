## Explore Integrals

### Try It 1: Odd Function Integral

Without computing, what's ∫[-1,1] x³ dx?

<svg width="220" height="200" viewBox="0 0 220 200" role="img" aria-label="Graph of x³ on [-1,1]: the negative area on the left and positive area on the right cancel" style="margin:12px 0;display:block;">
  <g transform="translate(110,100)">
    <line x1="-100" y1="0" x2="100" y2="0" stroke="var(--border)" stroke-width="1.5" />
    <line x1="0" y1="-85" x2="0" y2="85" stroke="var(--border)" stroke-width="1.5" />
    <path d="M -100,-85 C -70,-20 -55,-8 -30,-3 L -10,0 L 10,0 L 30,3 C 55,8 70,20 100,85" fill="none" stroke="var(--accent)" stroke-width="2.5" />
    <path d="M -30,-3 C -55,-8 -70,-20 -100,-85 L -100,0 L -30,0 Z" fill="color-mix(in srgb, var(--accent-error) 25%, transparent)" />
    <path d="M 30,3 C 55,8 70,20 100,85 L 100,0 L 30,0 Z" fill="color-mix(in srgb, var(--accent-correct) 25%, transparent)" />
    <text x="-52" y="40" text-anchor="middle" font-size="11" fill="var(--accent-error)">−area</text>
    <text x="52" y="40" text-anchor="middle" font-size="11" fill="var(--accent-correct)">+area</text>
    <text x="-40" y="18" font-size="11" fill="var(--text-muted)">-1</text>
    <text x="34" y="18" font-size="11" fill="var(--text-muted)">1</text>
  </g>
</svg>

<details>
<summary>Answer</summary>
0! x³ is an odd function, so its integral over a symmetric interval is always 0. Geometrically: the negative area on the left and positive area on the right exactly cancel. One second to answer.
</details>

### Try It 2: Physics Intuition

An object moves at velocity v(t) = t² for 3 seconds. How far does it travel?

<svg width="240" height="200" viewBox="0 0 240 200" role="img" aria-label="The area under the velocity curve v=t² from 0 to 3 equals the displacement" style="margin:12px 0;display:block;">
  <g transform="translate(40,20)">
    <line x1="0" y1="150" x2="200" y2="150" stroke="var(--border)" stroke-width="1.5" />
    <line x1="0" y1="10" x2="0" y2="150" stroke="var(--border)" stroke-width="1.5" />
    <path d="M 0,150 L 0,150 C 30,145 60,133 90,112 C 120,80 150,42 180,0 L 180,150 Z" fill="color-mix(in srgb, var(--accent) 20%, transparent)" />
    <path d="M 0,150 C 30,145 60,133 90,112 C 120,80 150,42 180,0" fill="none" stroke="var(--accent)" stroke-width="2.5" />
    <line x1="180" y1="150" x2="180" y2="0" stroke="var(--border-focus)" stroke-width="1" stroke-dasharray="4 4" />
    <text x="185" y="158" font-size="11" fill="var(--text-muted)">t=3</text>
    <text x="90" y="130" text-anchor="middle" font-size="12" fill="var(--text-primary)">area = displacement = 9 m</text>
    <text x="120" y="-4" font-size="11" fill="var(--text-muted)">v(t)=t²</text>
  </g>
</svg>

<details>
<summary>Answer</summary>
Displacement = ∫[0,3] t² dt = [t³/3]₀³ = 27/3 = 9 meters.
Physical meaning: the area under the velocity curve equals displacement.
</details>

### Try It 3: The Ungettable Antiderivative

Can you write an antiderivative for e^(-x²)?

<details>
<summary>Answer</summary>
No! e^(-x²) has no elementary antiderivative. But this doesn't stop us from computing the definite integral — ∫[-∞,∞] e^(-x²) dx = √π. Some integrals can only be evaluated numerically, but the results can be extremely precise.
</details>

### Try It 4: Archimedes' Insight

Approximate the area under y = x² from x = 0 to x = 1 using 10 rectangles. Which is more accurate: left endpoints, right endpoints, or midpoints?

<svg width="240" height="200" viewBox="0 0 240 200" role="img" aria-label="Area under y=x² on [0,1] approximated with left-endpoint rectangles" style="margin:12px 0;display:block;">
  <g transform="translate(15,15)">
    <line x1="0" y1="150" x2="210" y2="150" stroke="var(--border)" stroke-width="1.5" />
    <line x1="0" y1="10" x2="0" y2="150" stroke="var(--border)" stroke-width="1.5" />
    <path d="M 0,150 C 30,149 60,145 90,137 C 120,124 150,105 180,75" fill="none" stroke="var(--accent)" stroke-width="2.5" />
    <g fill="color-mix(in srgb, var(--accent) 12%, transparent)" stroke="var(--accent)" stroke-width="1">
      <rect x="0" y="149" width="18" height="1" /><rect x="18" y="148.5" width="18" height="1.5" /><rect x="36" y="147" width="18" height="3" />
      <rect x="54" y="145" width="18" height="5" /><rect x="72" y="142" width="18" height="8" /><rect x="90" y="138" width="18" height="12" />
      <rect x="108" y="133" width="18" height="17" /><rect x="126" y="126" width="18" height="24" /><rect x="144" y="117" width="18" height="33" /><rect x="162" y="106" width="18" height="44" />
    </g>
    <text x="105" y="185" text-anchor="middle" font-size="11" fill="var(--text-muted)">left endpoints</text>
  </g>
</svg>

<details>
<summary>Answer</summary>
Midpoints are typically far more accurate than left or right endpoints. With 10 midpoint rectangles approximating ∫[0,1] x² dx = 1/3, the midpoint sum gives 0.3325 (error 0.0008), while the right-endpoint sum gives 0.385 (error 0.052).
Try dragging the Riemann sum slider and watch!
</details>
