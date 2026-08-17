## The Problem-Solver's Toolkit: Working with the Laws of Large Numbers

### 1. Choose the Right Law

- "What happens to the frequency after many trials?" → **Law of large numbers**
- "What is the distribution of the sum/average of many independent variables?" → **Central limit theorem**
- "How close will the average be to the expectation?" → estimate with $\frac{\sigma}{\sqrt{n}}$

### 2. Standardizing with the Central Limit Theorem

If $X_1,\dots,X_n$ are independent and identically distributed (mean $\mu$, variance $\sigma^2$), then:

$$\frac{\bar{X} - \mu}{\sigma/\sqrt{n}} \approx N(0,1)$$

Standardize the "sum/average" into a standard normal, and probability tables do the rest.

### 3. Weak Form vs. Strong Form of the Law of Large Numbers

- **Weak law**: $\bar{X}_n \to \mu$ converges in probability
- **Strong law**: $\bar{X}_n \to \mu$ converges almost surely

For most problems the weak form suffices — but it pays to know the difference.

### 4. Speed of Convergence: The 1/√n Rule

$$\text{deviation} \sim \frac{\sigma}{\sqrt{n}}$$

Halving the error takes 4 times the sample. Use this whenever you need to estimate "how many samples for this precision."

### 5. When the Normal Approximation Applies

The central limit theorem demands: independence, identical (or nearly identical) distributions, and a large enough sample (typically $n \ge 30$). When these conditions fail, the approximation fails with them.

### Common Pitfalls

1. **Reading the law of large numbers as "more trials means closer"**: it is "error shrinking," not "eventual equality"
2. **Forcing the normal approximation on small $n$**: be cautious when $n < 30$
3. **Forgetting to standardize**: working with $\bar{X}$ directly instead of $Z = \frac{\bar{X}-\mu}{\sigma/\sqrt{n}}$
4. **Confusing "distribution of the sum" with "distribution of the average"**: $\sum X_i \sim N(n\mu, n\sigma^2)$, while $\bar{X} \sim N(\mu, \sigma^2/n)$
