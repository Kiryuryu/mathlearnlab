## Limit Solving Strategies: From Blind Calculation to Structural Analysis

When facing a tricky limit, don't jump straight to L'Hôpital. Build a three-step process.

### Step 1: Classify (Identify the Conflict)

Determine the indeterminate form — a tug-of-war between two forces:

| Type | Strategy |
|------|----------|
| 0/0 | Cancel zero factors, equivalent infinitesimals, Taylor expansion |
| ∞/∞ | Divide numerator and denominator by highest-order term |
| 0·∞ | "Move down" — flip the simple factor to the denominator |
| ∞−∞ | Common denominator (rational) or rationalize (radicals); Taylor as fallback |
| 1^∞ | Formula e^{lim(f-1)g} |

> **Mindset**: Don't look at the numbers first. Ask "where are the two forces canceling each other?"

### Step 2: Simplify (Aggressive Reduction)

#### x→∞: Leading term dominance
Keep only the highest-order term in sums. ln(1+e^x) ~ x (x→∞).

#### x→0: Extract then replace
- **Extract**: factors with non-zero limits — compute and remove them. E.g., (1+cosx) → 2, remove immediately.
- **Replace**: product-form factors with equivalent infinitesimals. sinx~x, tanx~x, 1-cosx~x²/2, ln(1+x)~x, e^x-1~x.

### Step 3: The Heavy Artillery

#### Taylor Expansion (preferred)
For combinations of sin, cos, e^x, ln(1+x) **in addition/subtraction**, expand each to the same order as the denominator.

> "Match orders": if the denominator is x^k, expand the numerator to x^k.

#### L'Hôpital's Rule (use cautiously)
- **Good for**: variable-limit integrals, or functions that simplify on differentiation (arctanx, lnx)
- **Avoid when**: differentiation makes things messier (endless sec²x chains) — switch to Taylor

### Example

lim(x→0) (tanx - sinx)/x³

1. **Classify**: 0/0
2. **Simplify**: factor out sinx → sinx(1/cosx - 1)
3. **Replace**: sinx~x, combine the bracket to (1-cosx)/cosx
4. **Extract & replace**: cosx→1, extract; 1-cosx~x²/2
5. **Result**: x·(x²/2)/x³ = 1/2

### Quick Mnemonic

> Classify the form, extract constants first;
> Replace products with equivalents, Taylor for sums.
