## Integrals — The Limit of Sums

How do you find the area of an irregular shape? Archimedes' answer: fill it with ever-thinner rectangles. **The integral is the exact area obtained by adding infinitely many infinitely thin rectangles** — not an approximation, but a precise limit.

### Riemann Sums: Area as a Limit

$$\int_a^b f(x)\,dx = \lim_{n\to\infty}\sum_{i=1}^{n} f(x_i^*)\Delta x, \qquad \Delta x = \frac{b-a}{n}$$

Split $[a,b]$ into $n$ pieces, let a small rectangle represent the function on each, and add the areas. The finer the partition, the closer the sum to the true area; as $n \to \infty$, the limit of these sums is the definite integral.

### The Fundamental Theorem: A Shortcut to Summing

$$\frac{d}{dx}\int_a^x f(t)\,dt = f(x)$$

One of the deepest discoveries in mathematics: **differentiation and integration are inverse operations.** To compute an area you need not count infinitely many rectangles — just find a function whose derivative is $f$ (an antiderivative) and subtract its values at the endpoints. The Newton–Leibniz formula made calculus genuinely practical.

### Substitution and Integration by Parts: The Two Great Tools

**Substitution** — a change of variables that simplifies an integral, geometrically stretching the coordinate axis while preserving area:

$$\int_a^b f(g(x))\,g'(x)\,dx = \int_{g(a)}^{g(b)} f(u)\,du$$

**Integration by parts** — the product rule read backwards:

$$\int u\,dv = uv - \int v\,du$$

### Beyond Area

- **Volumes of revolution**: disk method $V = \pi\int_a^b [f(x)]^2\,dx$; shell method $V = 2\pi\int_a^b x\,f(x)\,dx$
- **Improper integrals**: $\int_a^{\infty}f(x)\,dx = \lim_{b\to\infty}\int_a^b f(x)\,dx$ — the core question is whether they converge
- **The p-test**: $\int_1^\infty \frac{1}{x^p}\,dx$ converges $\iff p>1$; $\int_0^1 \frac{1}{x^p}\,dx$ converges $\iff p<1$

---

**From here:** see [Applications](#applications) computing probabilities, signal energies, and work in physics; in [Interactive](#explore), drag the rectangle-count slider and watch the Riemann sum close in on the true area.

→ [Continue reading: Infinite Series — The Puzzle of Infinity](/exhibit/series)
