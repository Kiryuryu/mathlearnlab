## Multivariable Calculus — From Plane to Space

Single-variable calculus studies change along a curve. But the real world is three-dimensional: weather, currents, stock prices, temperature fields in a chip. When variables go from one to two or three, problems jump from "on a line" to "on a surface" — yet the ideas are still the same four: **change, extrema, and flow.**

### Surfaces and Partial Derivatives

$z = f(x, y)$ defines a **surface** in three-dimensional space. Peaks, valleys, saddles — the shape of the surface is the starting point for every multivariable concept.

A partial derivative differentiates in one direction while holding the others fixed:

$$f_x(x_0,y_0) = \lim_{h\to0}\frac{f(x_0+h,y_0)-f(x_0,y_0)}{h}$$

Geometrically, $f_x$ is the slope of the tangent line along the $x$-axis, and $f_y$ along the $y$-axis. When both exist, the surface gains a **tangent plane** at that point: $z = f(x_0,y_0) + f_x(x_0,y_0)(x-x_0) + f_y(x_0,y_0)(y-y_0)$.

### The Gradient: The Steepest Direction

> **Directional derivative**: $D_{\mathbf{u}}f = \nabla f \cdot \mathbf{u}$ ($\|\mathbf{u}\|=1$); **gradient**: $\nabla f = (f_x, f_y)$

The gradient vector has two key properties:

- **Direction**: the direction of **fastest increase** of the function
- **Magnitude**: the maximum rate of change in that direction

More importantly, the gradient is always **perpendicular to the level curves**. Standing on a hillside, the gradient points where your step takes the most effort; walking along a level curve keeps your altitude constant.

### Gradient Descent: The Engine of AI

> Start at some point, take a small step in the **negative gradient direction** (steepest descent), and iterate — this finds a minimum.

Finding the minimum of a function is the core of almost every optimization problem. Gradient descent does not need a perfect answer on the first try; it only needs to "keep walking downhill": a learning rate too large causes oscillation or divergence, too small converges slowly. Training a neural network today is essentially this loop run millions of times.

### From Volumes to Flow

- **Double integrals**: $\iint_D f(x,y)\,dx\,dy$ — the volume under a surface, computed as iterated integrals
- **Lagrange multipliers**: at a constrained extremum, $\nabla f = \lambda \nabla g$ — the gradients of the objective and the constraint are parallel
- **Line integrals**: $\int_C \mathbf{F}\cdot d\mathbf{r}$ — the work done by a force field along a path; path-independent for conservative fields, with the three great formulas of Green, Stokes, and Gauss linking line, surface, and volume integrals

---

**From here:** visit **Applications** to see gradient descent drive AlphaFold and weather models solve partial differential equations; in **Interactive**, watch gradient descent zigzag its way down the valley in full animation.
