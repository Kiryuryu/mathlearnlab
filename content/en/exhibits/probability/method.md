## Key Insights: How to Solve Probability Problems

### 1. First, Draw the Sample Space

Nearly every probability problem begins with **making the sample space explicit**: what are all possible outcomes, and are they equally likely?

- Classical: finitely many equally likely outcomes → $P = \frac{|A|}{|\Omega|}$
- Geometric: continuous outcomes → $P = \frac{\text{area}}{\text{total area}}$
- Do not omit outcomes; do not double-count

### 2. Check Independence

Are the two events independent? **Only independent events may be multiplied:**

$$P(A\cap B) = P(A)P(B) \quad (\text{only if } A, B \text{ are independent})$$

When not independent, use conditional probability: $P(A\cap B) = P(A)P(B|A)$.

### 3. Prefer the Definition for Conditional Probability

$$P(A|B) = \frac{P(A\cap B)}{P(B)}$$

Find the intersection first, then divide by the probability of the conditioning event. **Do not estimate conditional probabilities by intuition** — many counterintuitive problems come from here.

### 4. The Law of Total Probability: Split into Cases

When the problem has several "mutually exclusive and exhaustive" cases $B_1,\dots,B_n$:

$$P(A) = \sum_{i=1}^n P(A|B_i)P(B_i)$$

Classic applications: multiple suppliers, multiple tests, multi-level decisions.

### 5. Bayes: Working Backward from the Cause

Given an outcome A, ask which cause B produced it:

$$P(B_j|A) = \frac{P(A|B_j)P(B_j)}{\sum_i P(A|B_i)P(B_i)}$$

Mnemonic: **the numerator is "this path"; the denominator is "the sum of all paths."**

### 6. Random Variables: Distribution First, Then Compute

For problems involving a random variable, first identify the distribution type:

| Type | Key formula |
|------|-------------|
| Binomial $B(n,p)$ | $P(X=k) = \binom{n}{k}p^k(1-p)^{n-k}$, $E=np$ |
| Poisson | $P(X=k)=\frac{\lambda^k e^{-\lambda}}{k!}$ |
| Uniform | $E=\frac{a+b}{2}$ |
| Normal | standardize $Z=\frac{X-\mu}{\sigma}$ |

### 7. Large Numbers and Limits

For "frequency after many trials," use the law of large numbers; for "distribution of a sum of many independent variables," use the central limit theorem — get the normal approximation directly.

### Common Pitfalls

1. **Multiplying without checking independence**
2. **Confusing $P(A|B)$ with $P(B|A)$** (the classic medical-test trap)
3. **Unclear sample space** leading to counting errors
4. **The expectation is not the "most likely value"** — it is the weighted average
