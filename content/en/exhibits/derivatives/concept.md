## Derivatives — Instantaneous Rate of Change

A train flashes past you; your phone measures 3 meters in 0.1 seconds, and you call that "speed" — but it is really an average over a short interval. What if the interval shrank to zero? How much could anything move in a single instant? **The derivative is the rate of change you can still compute as the interval tends to zero.**

### From Average to Instantaneous Rate

$$f'(x) = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}$$

The quotient $\frac{f(x+h)-f(x)}{h}$ is the **average rate of change** over $[x, x+h]$ — the slope of a secant line. As $h \to 0$, the secant slides onto the tangent at $x$, and the slope settles to a definite value: the instantaneous rate of change $f'(x)$, the **slope of the tangent line**.

### Differentiable vs Continuous: One Direction Only

> **Differentiable ⇒ Continuous**, but **Continuous ⇏ Differentiable**

The classic counterexample is $f(x)=|x|$ at $x=0$: the curve is continuous, but the sharp corner has no tangent — the left and right derivatives differ. **Continuity** means the curve does not break; **differentiability** means it does not bend sharply. Smoothness is a stronger condition than continuity.

### The Mean Value Theorems: Levers of the Function World

| Theorem | Condition | Conclusion |
|---------|-----------|------------|
| **Rolle** | $f(a)=f(b)$ | $\exists \xi$ with $f'(\xi)=0$ |
| **Lagrange** | continuous, differentiable | $f'(\xi)=\frac{f(b)-f(a)}{b-a}$ |
| **Cauchy** | two functions | $\frac{f'(\xi)}{g'(\xi)}=\frac{f(b)-f(a)}{g(b)-g(a)}$ |

The geometric meaning of Lagrange's theorem is the most intuitive: **somewhere on the curve, the tangent is parallel to the chord joining the endpoints.** It ties global change to local derivatives — a universal tool for inequalities and error estimates.

### Two Powerful Tools Built on Derivatives

**Taylor expansion** approximates any smooth function by polynomials:

$$f(x) = f(x_0) + f'(x_0)(x-x_0) + \frac{f''(x_0)}{2!}(x-x_0)^2 + \cdots + \frac{f^{(n)}(x_0)}{n!}(x-x_0)^n + R_n(x)$$

Near the expansion point, even low-order approximations are remarkably accurate; more terms widen the range of good approximation.

**L'Hôpital's rule** resolves $\frac{0}{0}$ or $\frac{\infty}{\infty}$ indeterminate forms:

$$\lim \frac{f(x)}{g(x)} = \lim \frac{f'(x)}{g'(x)}$$

⚠️ Useful as it is, check the conditions first: both numerator and denominator must tend to $0$ or $\infty$, and the limit of the derivative ratio must exist.

---

**From here:** see [Applications](#applications) on gradient descent driving AI, Newton's method solving equations, and light finding its own path; in [Interactive](#explore), drag the tangent point and watch the line chase the curve.

→ [Continue reading: Integrals — The Limit of Sums](/exhibit/integrals)
