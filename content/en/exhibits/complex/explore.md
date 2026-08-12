## Interactive: The Intuition Lab of Complex Analysis

### Try It 1: The Cycle of Powers of i

Compute $i^0, i^1, i^2, i^3, i^4$. What pattern do you see?

<svg width="220" height="220" viewBox="0 0 220 220" role="img" aria-label="Unit circle in the complex plane with 1, i, -1, -i marked; multiplying by i rotates 90° counterclockwise" style="margin:12px 0;display:block;">
  <g transform="translate(110,110)">
    <circle cx="0" cy="0" r="80" fill="none" stroke="var(--border)" stroke-width="1.5" />
    <line x1="-110" y1="0" x2="110" y2="0" stroke="var(--border)" stroke-width="1" />
    <line x1="0" y1="-110" x2="0" y2="110" stroke="var(--border)" stroke-width="1" />
    <text x="-108" y="-6" font-size="11" fill="var(--text-muted)">Re</text>
    <text x="6" y="-104" font-size="11" fill="var(--text-muted)">Im</text>
    <circle cx="80" cy="0" r="4" fill="var(--accent)" /><text x="88" y="6" font-size="12" fill="var(--text-primary)">1</text>
    <circle cx="0" cy="-80" r="4" fill="var(--accent)" /><text x="8" y="-84" font-size="12" fill="var(--text-primary)">i</text>
    <circle cx="-80" cy="0" r="4" fill="var(--accent)" /><text x="-104" y="6" font-size="12" fill="var(--text-primary)">-1</text>
    <circle cx="0" cy="80" r="4" fill="var(--accent)" /><text x="8" y="92" font-size="12" fill="var(--text-primary)">-i</text>
    <path d="M 80,0 A 80,80 0 0 1 0,-80" fill="none" stroke="var(--accent-warm)" stroke-width="2" stroke-dasharray="5 4" marker-end="url(#arrC1)" />
    <text x="44" y="-44" font-size="11" fill="var(--accent-warm)">×i</text>
  </g>
  <defs>
    <marker id="arrC1" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="var(--accent-warm)" /></marker>
  </defs>
</svg>

<details>
<summary>Answer</summary>
$i^0 = 1$, $i^1 = i$, $i^2 = -1$, $i^3 = -i$, $i^4 = 1$. Then the cycle repeats every 4: $1, i, -1, -i$. Geometrically, multiplying by $i$ is a 90° counterclockwise rotation — you circle the unit circle in the complex plane. That is why "multiplication by $i$ is rotation."
</details>

### Try It 2: Evaluating Euler's Formula

Use $e^{i\theta} = \cos\theta + i\sin\theta$ to compute $e^{i\pi/2}$ and $e^{i\pi}$, then verify $e^{i\pi} + 1 = 0$.

<svg width="220" height="220" viewBox="0 0 220 220" role="img" aria-label="Unit circle in the complex plane with e^{iπ/2}=i and e^{iπ}=-1 marked; rotation angles 90° and 180°" style="margin:12px 0;display:block;">
  <g transform="translate(110,110)">
    <circle cx="0" cy="0" r="80" fill="none" stroke="var(--border)" stroke-width="1.5" />
    <line x1="-110" y1="0" x2="110" y2="0" stroke="var(--border)" stroke-width="1" />
    <line x1="0" y1="-110" x2="0" y2="110" stroke="var(--border)" stroke-width="1" />
    <text x="-108" y="-6" font-size="11" fill="var(--text-muted)">Re</text>
    <text x="6" y="-104" font-size="11" fill="var(--text-muted)">Im</text>
    <circle cx="-80" cy="0" r="4" fill="var(--accent)" />
    <circle cx="0" cy="-80" r="4" fill="var(--accent-warm)" /><text x="-62" y="-88" font-size="12" fill="var(--accent-warm)">e^{iπ/2}=i</text>
    <text x="6" y="8" font-size="12" fill="var(--text-primary)">e^{iπ}=-1</text>
    <path d="M 80,0 A 80,80 0 0 1 0,-80" fill="none" stroke="var(--accent-warm)" stroke-width="2" stroke-dasharray="5 4" />
    <path d="M 0,-80 A 80,80 0 0 1 -80,0" fill="none" stroke="var(--accent)" stroke-width="2" stroke-dasharray="5 4" />
    <text x="50" y="-52" font-size="11" fill="var(--accent-warm)">90°</text>
    <text x="-56" y="-40" font-size="11" fill="var(--accent)">180°</text>
  </g>
</svg>

<details>
<summary>Answer</summary>
$e^{i\pi/2} = \cos(\pi/2) + i\sin(\pi/2) = 0 + i\cdot 1 = i$. So $e^{i\pi/2} = i$ — multiplying by $i$ and by $e^{i\pi/2}$ are the same act (a 90° rotation). $e^{i\pi} = \cos\pi + i\sin\pi = -1 + 0i = -1$, hence $e^{i\pi} + 1 = 0$ ✓. On the complex plane, the exponential "spirals forward"; at $\theta=\pi$ it lands exactly on $-1$.
</details>

### Try It 3: The Singularity of 1/(z−1)

At which point is $f(z) = \frac{1}{z-1}$ not analytic? What kind of singularity is it?

<details>
<summary>Answer</summary>
At $z=1$ the denominator vanishes and $f$ is not analytic. It is a **simple pole** (order 1): the Laurent expansion $f(z) = \frac{1}{z-1}$ has a single negative power, with residue $\mathrm{Res}(f, 1) = \lim_{z\to 1}(z-1)\cdot\frac{1}{z-1} = 1$. So $\oint_{|z-1|=r}\frac{dz}{z-1} = 2\pi i \cdot 1 = 2\pi i$ — the integral around a pole always equals $2\pi i$ times the residue.
</details>

### Try It 4: The Residue Theorem Computes a Real Integral

Use the residue theorem to compute $\int_{-\infty}^{\infty} \frac{dx}{1+x^2}$.

<svg width="260" height="180" viewBox="0 0 260 180" role="img" aria-label="Upper-half-plane contour: real-axis segment from -R to R plus upper semicircle; the pole z=i lies inside" style="margin:12px 0;display:block;">
  <line x1="20" y1="140" x2="240" y2="140" stroke="var(--border)" stroke-width="1.5" />
  <path d="M 20,140 L 240,140 A 110,110 0 0 1 20,140 Z" fill="none" stroke="var(--accent)" stroke-width="2" />
  <circle cx="130" cy="62" r="4.5" fill="var(--accent-error)" />
  <text x="138" y="58" font-size="12" fill="var(--accent-error)">z=i (pole)</text>
  <text x="230" y="132" font-size="11" fill="var(--text-muted)">R → ∞</text>
  <text x="20" y="162" font-size="11" fill="var(--text-muted)">-R</text>
  <text x="236" y="162" font-size="11" fill="var(--text-muted)">R</text>
  <text x="130" y="26" text-anchor="middle" font-size="11" fill="var(--accent)">upper semicircle</text>
</svg>

<details>
<summary>Answer</summary>
Consider the upper-half-plane contour (real axis $[-R,R]$ + upper semicircle). The function $f(z)=\frac{1}{1+z^2}=\frac{1}{(z+i)(z-i)}$ has only the pole $z=i$ (a simple pole) in the upper half-plane. Residue: $\mathrm{Res}(f,i) = \lim_{z\to i}(z-i)\frac{1}{(z-i)(z+i)} = \frac{1}{2i}$. By the residue theorem, $\oint f = 2\pi i \cdot \frac{1}{2i} = \pi$. Letting $R\to\infty$, the arc contribution vanishes, so $\int_{-\infty}^{\infty}\frac{dx}{1+x^2} = \pi$ ✓. An "infinite-interval" real integral, obtained from a single point ($z=i$) on the complex plane.
</details>
