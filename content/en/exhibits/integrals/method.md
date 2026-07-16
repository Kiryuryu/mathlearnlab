## Integration Strategies: From Memorization to Pattern Recognition

### Core Idea: Integration Is "Reverse Differentiation"

Every integration formula corresponds to a differentiation formula in reverse. Understanding "why this integrates that way" is a hundred times more important than memorizing.

### Three-Step Framework

#### Step 1: Recognize the Structure, Choose the Weapon

Scan the integrand:

| Structure | Method |
|-----------|--------|
| Clearly a derivative of something | Direct antiderivative (e.g., ∫e^x dx = e^x) |
| Polynomial × trig function | Integration by parts, polynomial as u |
| Composite f(g(x))·g'(x) | Substitution, let u = g(x) |
| Radical √(a²-x²) | Trig substitution x = a·sinθ |
| Radical √(x²+a²) | Trig substitution x = a·tanθ |
| Radical √(x²-a²) | Trig substitution x = a·secθ |
| Rational P(x)/Q(x) | Partial fractions |
| Messy trig combinations | Universal substitution t = tan(x/2) (last resort) |

#### Step 2: Integration by Parts

Formula: ∫u dv = uv - ∫v du

**LIATE rule**: choose u in this priority — Log > Inverse trig > Algebraic > Trig > Exponential. Earlier ones simplify when differentiated.

**Classic pairings**:
- ∫x·e^x dx → u=x, dv=e^x dx
- ∫x·sinx dx → u=x, dv=sinx dx
- ∫lnx dx → u=lnx, dv=dx
- ∫e^x·sinx dx → integrate by parts twice, solve the equation

#### Step 3: Definite Integral Tactics

**Symmetry**: odd functions integrate to 0 on [-a, a]; even functions can be halved.

**Change limits with substitution**: when substituting variables, update the integration bounds.

**Wallis formula**: ∫[0,π/2] sinⁿ x dx = ∫[0,π/2] cosⁿ x dx, with different formulas for odd/even n.

### Improper Integrals: Finite or Infinite?

To decide if ∫[a,∞) f(x)dx converges or diverges, the key is comparison.

**p-integrals**: ∫[1,∞) 1/x^p dx converges if p > 1, diverges if p ≤ 1. This is the benchmark.

**Comparison test**: compare against a known convergent/divergent integral.

### Quick Mnemonic

> Composite calls for substitution, products call for parts;
> Radicals with squares need trig substitution;
> Definite integrals use symmetry, improper tests compare to p-series.
