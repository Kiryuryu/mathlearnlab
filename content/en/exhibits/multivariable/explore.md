## Explore Multivariable Calculus

### Try It 1: Where Does the Gradient Point?

f(x, y) = x² + y². At (2, 1), which direction descends fastest?

<details>
<summary>Answer</summary>
∇f = (2x, 2y). At (2, 1), gradient = (4, 2). Fastest increase is along (4, 2); fastest decrease (downhill) is (-4, -2).
The gradient always points in the direction of steepest ascent — it's the math of "water flows downhill."
</details>

### Try It 2: Identify the Saddle

z = x² - y². Is the origin a maximum, minimum, or neither?

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
