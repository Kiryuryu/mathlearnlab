## Multivariable Strategies: From 1D Intuition to Multi-Dimensional Vision

### Core Idea: One More Variable, One More Dimension

Multivariable calculus is "upgraded" single-variable calculus. Most concepts map directly:

| Single-Variable | Multivariable |
|----------------|---------------|
| f'(x) | Partial derivatives ∂f/∂x, ∂f/∂y |
| Monotonicity | Gradient ∇f direction |
| Extrema f'(x) = 0 | ∇f = 0 |
| Integral ∫f dx | Double integral ∬f dxdy |
| Indeterminate forms | Approach along different paths |

### Three-Step Framework

#### Step 1: Partial Derivatives — One Direction at a Time

∂f/∂x: treat y as constant, differentiate with respect to x.
∂f/∂y: treat x as constant, differentiate with respect to y.

Higher-order: ∂²f/∂x², ∂²f/∂x∂y, ∂²f/∂y². **Mixed partials are equal regardless of order** (given continuity).

#### Step 2: Finding Extrema

1. Take partial derivatives, set ∇f = 0 for critical points
2. Compute discriminant D = fxx·fyy - (fxy)²

| D | fxx | Conclusion |
|---|-----|-----------|
| > 0 | > 0 | Local minimum |
| > 0 | < 0 | Local maximum |
| < 0 | any | Saddle point |
| = 0 | — | Inconclusive, need more analysis |

> Saddle points are unique to multivariable — a minimum in one direction, maximum in another. Like a horse's saddle: concave along one axis, convex along the other.

#### Step 3: Lagrange Multipliers

To find extrema of f(x,y) under constraint g(x,y) = 0:

Set L(x,y,λ) = f(x,y) - λ·g(x,y), then solve ∇L = 0.

Intuition: at the extremum on the constraint curve, f's gradient is parallel to g's gradient (both perpendicular to the constraint curve).

### Multiple Integrals: Two Single Integrals

A double integral = integrate over one variable (fixing the other), then the other.

**Switching integration order**: the result of the first integration becomes the integrand of the second. Draw the region first, then determine bounds.

**Polar coordinates**: x = r·cosθ, y = r·sinθ, dxdy = r·dr·dθ. Use when the region is a circle, sector, or annulus.

### Line Integrals and Green's Theorem

Type 1 (arc length): ∫_L f(x,y) ds
Type 2 (coordinate): ∫_L Pdx + Qdy

Green's theorem connects line integrals and area integrals:

∮_C Pdx + Qdy = ∬_D (∂Q/∂x - ∂P/∂y) dxdy

### Quick Mnemonic

> Partial locks one dimension at a time, D determines min/max/saddle;
> Lagrange handles constraints, double integrals draw region first;
> Closed curves use Green's theorem, path independence checks mixed partials.
