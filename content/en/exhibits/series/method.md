## Series Strategies: From Rote Tests to Understanding "Speed"

### Core Idea: Convergence Means "Terms Approach 0 Fast Enough"

Each term approaching 0 is necessary but not sufficient. The harmonic series Σ 1/n has terms → 0 but diverges — because they don't approach 0 **fast enough**.

### Three-Step Framework

#### Step 1: Check the General Term

Given Σ aₙ, first check:
1. Does aₙ → 0? If not, it diverges immediately (necessary condition)
2. How fast does aₙ → 0? Compare to 1/n^p:
   - p > 1 → likely converges
   - p ≤ 1 → likely diverges

#### Step 2: Choose Your Test

| Test | Best For |
|------|----------|
| Ratio test | Factorials n! and exponentials aⁿ |
| Root test | (·)ⁿ structures, terms with nth powers |
| Comparison test | Can directly compare to a known series |
| Limit comparison | General term is asymptotically like 1/n^p |
| Integral test | Positive decreasing terms (maps to improper integral) |
| Alternating series | Alternating signs + decreasing terms → converges |

> **Insight**: The ratio test is a "magnifying glass" — the ratio of successive terms tells you the shrinking speed. Ratio < 1 → shrinking geometrically → converges. Ratio > 1 → growing → diverges.

#### Step 3: Power Series — Find the "Territory"

A power series Σ aₙ(x-c)ⁿ converges within its "radius of convergence."

Finding the radius R:
- Ratio method: R = lim |aₙ/aₙ₊₁|
- Root method: R = 1 / lim |aₙ|^{1/n}

Absolute convergence inside |x-c| < R, divergence outside |x-c| > R. Endpoints must be checked separately.

### Taylor Series: A Function's Polynomial Face

eˣ = 1 + x + x²/2! + x³/3! + ...
sinx = x - x³/3! + x⁵/5! - ...
cosx = 1 - x²/2! + x⁴/4! - ...
ln(1+x) = x - x²/2 + x³/3 - ...
(1+x)ᵅ = 1 + αx + α(α-1)x²/2! + ...

### Fourier Series: Periodic = Sine Wave Summation

a₀/2 + Σ(aₙ·cos(nx) + bₙ·sin(nx))

Coefficients: aₙ = (1/π)∫f(x)cos(nx)dx, bₙ = (1/π)∫f(x)sin(nx)dx

Odd extension → sine series (only sin terms), even extension → cosine series (only cos terms).

### Quick Mnemonic

> Check the term tends to zero, then compare to p-series;
> Factorials and exponentials use ratio test, nth powers use root test;
> Power series find radius, Taylor expansion matches orders.
