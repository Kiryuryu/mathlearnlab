## Key Insights: How to Solve Complex Analysis Problems

### 1. First Verify Analyticity: The Cauchy–Riemann Equations

A complex function $f = u + iv$ is analytic (at a point) if and only if the **Cauchy–Riemann equations** hold:

$$\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y}, \quad \frac{\partial u}{\partial y} = -\frac{\partial v}{\partial x}$$

Check whether the C-R equations hold before judging differentiability. If $u, v$ have continuous partial derivatives and satisfy C-R, then $f$ is analytic there.

### 2. Basic Facts About Analytic Functions

Splitting $z$ into real and imaginary parts is slow — remember a few direct results:

- Polynomials, $e^z$, $\sin z$, $\cos z$ are analytic on the whole plane
- $\log z$, $z^\alpha$ are analytic on regions (minus branch cuts)
- $1/z$ is analytic except at $z=0$ — that is its pole

### 3. The Residue Theorem: Three Steps

Compute the closed-path integral $\oint_C f(z)dz$:

1. Find all singularities inside $C$
2. Compute the residue $\mathrm{Res}(f, z_0)$ at each:
   - Simple pole: $\mathrm{Res} = \lim_{z\to z_0} (z-z_0)f(z)$
   - Pole of order $m$: $\mathrm{Res} = \frac{1}{(m-1)!}\lim_{z\to z_0}\frac{d^{m-1}}{dz^{m-1}}[(z-z_0)^m f(z)]$
3. Result: $\oint_C f(z)dz = 2\pi i \sum \mathrm{Res}$

### 4. Real Integrals → Contour Integrals

To compute $\int_{-\infty}^{\infty} f(x)dx$:

- Choose a suitable closed contour (upper semicircle/rectangle/wedge)
- Verify the arc contribution → 0 as radius → ∞ (usually via the ML inequality)
- Apply the residue theorem to the whole contour, take the real or imaginary part

Common trick: $\int_0^{2\pi}$ of trigonometric rational functions → set $z=e^{i\theta}$ and integrate over the unit circle.

### 5. Laurent Series: Behavior Near Singularities

Expand a Laurent series $\sum a_n(z-z_0)^n$ near a singularity:

- No negative powers → removable singularity
- Finitely many negative powers → pole (the order = the highest negative power's absolute value)
- Infinitely many negative powers → essential singularity ($e^{1/z}$ at 0)

**The coefficient of $1/(z-z_0)$ is the residue** — another route to computing residues.

### Common Pitfalls

1. **C-R equations are necessary and sufficient** — but only when $u,v$ have continuous partials; otherwise extra checks are needed
2. **Forgetting to check whether a singularity lies inside the contour**: $\oint_C f dz$ depends only on singularities inside $C$
3. **Treating essential singularities as poles**: $e^{1/z}$ at 0 has no finite principal part in its Laurent expansion
4. **Forgetting the unit when taking the real part of a real integral**: sometimes the answer is purely imaginary or a multiple of $\pi$
