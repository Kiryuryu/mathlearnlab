## Explore Series

### Try It 1: The Power of 1

1 - 1 + 1 - 1 + 1 - 1 + ... = ?

<details>
<summary>Answer</summary>
This series does not converge. Stop after an odd number of terms: sum = 1. After an even number: sum = 0. No limit. Euler "proved" it equals 1/2 (by substituting x = 1 into 1/(1+x) = 1 - x + x² - ...). This shows that infinite series aren't always well-behaved.
</details>

### Try It 2: Convergence Speed

Compare: Σ 1/n² and Σ 1/n. Which converges? How fast?

<details>
<summary>Answer</summary>
Σ 1/n² converges (to π²/6 ≈ 1.645), Σ 1/n diverges.
Σ 1/n²: first 10 terms = 1.55 (close to limit 1.645), first 100 terms = 1.635.
Σ 1/n: first 10 terms = 2.93, first 100 = 5.19, first 1000 = 7.49... climbing forever.
</details>

### Try It 3: Polynomial Approximations

Approximate sin(0.5) using the first 3 terms of its Taylor series. How accurate is it?

<details>
<summary>Answer</summary>
sin(0.5) ≈ 0.5 - 0.5³/6 + 0.5⁵/120 = 0.5 - 0.020833 + 0.002604 = 0.4793.
True value sin(0.5) = 0.4794... error is only 0.0001!
</details>

### Try It 4: π by Series

Leibniz series π/4 = 1 - 1/3 + 1/5 - 1/7 + ... How many terms to get π ≈ 3.14?

<details>
<summary>Answer</summary>
About 600 terms. After 600 terms, π ≈ 3.14... barely there. This series converges extremely slowly — which is why π isn't computed this way. Instead, super-fast Ramanujan or Chudnovsky series are used.
</details>
