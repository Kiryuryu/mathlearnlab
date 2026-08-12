## Complex Analysis — The Kingdom of Imaginary Numbers

Does $x^2 = -1$ have a solution? In the real world, no. But if we **allow** an "imaginary number" $i$ with $i^2 = -1$, algebra becomes complete — every polynomial has a root. Complex analysis studies how functions behave on the **complex plane**, built from real and imaginary parts. And the rewards reach far beyond algebra.

### The Complex Plane: Unifying Number and Rotation

A complex number $z = x + iy$ is drawn on a plane: horizontal axis for the real part $x$, vertical for the imaginary part $y$. The key insight is — **multiplying by $i$ rotates 90°**:

$$i \cdot 1 = i, \quad i \cdot i = -1$$

So multiplication by $i$ corresponds to counterclockwise rotation. Complex multiplication is therefore both "scaling" and "rotation": in $z = re^{i\theta}$, $r$ is length and $\theta$ is angle. **A single complex number encodes both distance and direction** — this is why complex analysis unifies algebra and geometry.

### Euler's Formula: Five Constants Meet

$$e^{i\theta} = \cos\theta + i\sin\theta$$

One of the most famous formulas in mathematics. When $\theta = \pi$:

$$e^{i\pi} + 1 = 0$$

It binds the five most important constants — $e$, $i$, $\pi$, $1$, $0$ — into a single equation. It shows that exponential and trigonometric functions are two faces of the same object on the complex plane.

### Analytic Functions: The Magic of Complex Differentiability

A complex function $f(z)$ being "differentiable" (analytic) requires complex differentiability — an extraordinarily strong condition. **Analytic functions have astonishing properties**:

- Once differentiable at a point, they are differentiable everywhere (infinitely many times)
- The mean value property, the maximum modulus principle
- **Cauchy's integral theorem**: the integral around a closed path is zero (when the function is analytic)

These properties make complex integrals a powerful tool for computing real integrals — many real integrals untouchable by elementary methods are solved easily via contour integration on the complex plane.

### The Residue Theorem: The Integral Calculator

Near a singularity, an analytic function expands into a Laurent series; the coefficient of $1/(z-z_0)$ is the **residue**. The residue theorem says:

> A closed-path integral = $2\pi i$ × the sum of residues at all singularities inside the path

This greatly simplifies real integrals and series computations — one of the most practical results of complex analysis.

---

**From here:** see [Applications](#applications) on how complex analysis computes real integrals, understands fluids and electromagnetic fields, and designs filters; in [Interactive](#explore), watch functions like $z^2$ and $e^z$ stretch and rotate the complex plane.

→ [Continue reading: Graph Theory — Networks of Relations](/exhibit/discrete)
