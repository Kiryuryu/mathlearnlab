## Derivative Strategies: From Formulas to Geometric Intuition

### Core Idea: The Derivative Is the Rate of Change

f'(x) answers three questions:
1. Is the function rising or falling at x? (sign)
2. How fast is it rising or falling? (magnitude)
3. Is the rate itself accelerating or decelerating? (second derivative)

### Three-Step Framework

#### Step 1: Identify the Derivative Form

| Structure | Strategy |
|-----------|----------|
| Polynomial/power | Power rule: d/dx x^n = n x^(n-1) |
| Product f(x)·g(x) | Product rule: (fg)' = f'g + fg' |
| Quotient f(x)/g(x) | Quotient rule: (f/g)' = (f'g - fg')/g² |
| Composition f(g(x)) | Chain rule: f'(g(x))·g'(x), peel layer by layer |
| Implicit function | Differentiate both sides, solve for dy/dx |
| Parametric | dy/dx = (dy/dt)/(dx/dt) |

#### Step 2: The "Language" of Derivatives

**Slope of the tangent**: f'(a) is the slope of the line that best hugs the curve at x = a. The linear approximation f(x) ≈ f(a) + f'(a)(x-a) is calculus's most basic tool.

**Related rates**: when one quantity changes, how does another follow? All chain rule.

#### Step 3: The Mean Value Theorem Family

| Theorem | Meaning |
|---------|---------|
| Rolle | If f(a) = f(b), there's a point where f' = 0 |
| Lagrange (MVT) | Some point has derivative = average rate of change |
| Cauchy | Two functions' rates are proportional at some point |

> **Insight**: The MVT family is about "existence" — it guarantees some point satisfies a condition without telling you which point. If a problem asks "prove there exists a point where...", think MVT.

### Monotonicity and Extrema

f'(x) > 0 → increasing, f'(x) < 0 → decreasing.

**Finding extrema in three steps**:
1. Differentiate, solve f'(x) = 0 for critical points
2. Use second derivative: f'' > 0 minimum, f'' < 0 maximum, f'' = 0 needs more checking
3. Check boundaries and non-differentiable points

### Concavity and Inflection Points

f'' > 0 is concave up (bowl-shaped), f'' < 0 is concave down (arch-shaped). Points where f'' changes sign = inflection points.

### Quick Mnemonic

> First derivative tells rise or fall, second derivative concave or convex;
> Chain rule peels like an onion, product rule keeps each term;
> Extrema at critical points, inflection where concavity flips.
