## What is a Limit?

Intuitively, the limit of $f(x)$ as $x$ approaches $a$ is the value that $f(x)$ gets arbitrarily close to.

### Formal Definition (ε-δ)

$$\lim_{x \to a} f(x) = L$$

means: for every $\varepsilon > 0$, there exists $\delta > 0$ such that if $0 < |x - a| < \delta$, then $|f(x) - L| < \varepsilon$.

### Classic Examples

**1. A Simple Limit**

$$\lim_{x \to 3} (2x + 1) = 7$$

**2. The Derivative as a Limit**

$$\lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$$

This is the instantaneous rate of change — the foundation of differential calculus.

**3. A Special Limit**

$$\lim_{x \to 0} \frac{\sin x}{x} = 1$$

This limit is the key to computing derivatives of trigonometric functions.

### Why Limits Matter

Limits give us the ability to reason about:
- **Instantaneous change** (velocity at a single moment)
- **Infinite sums** (area under a curve)
- **Continuity** (no jumps or breaks)
- **Approximation** (getting as close as we want)
