## Laws of Large Numbers — Certainty Within Randomness

Flip a coin and the probability of heads is $0.5$, but 10 flips need not give exactly 5 heads. Flip it 10,000 times, though, and the proportion of heads will land remarkably close to $0.5$. **Randomness contains certainty** — the average of many independent random events always converges toward its expected value. The laws of large numbers capture precisely this passage "from chaos to order."

### The Law of Large Numbers: Frequency Approaching Probability

> $$\lim_{n\to\infty}\frac{X_1+X_2+\cdots+X_n}{n} = \mu$$

The more trials you run, the closer the sample average presses toward the expectation $\mu$. This is the **law of large numbers**:

- Flip a coin 10 times and the proportion of heads may drift far from 0.5
- Flip it 10,000 times and the proportion is almost exactly 0.5
- The profit logic of insurance, statistics, and casinos alike rests on this law

### The Central Limit Theorem: The Normal Distribution Is Everywhere

> Whatever the distribution of the original data, the **sum** of many independent random variables is always approximately normal.

One of the deepest theorems in probability:

- A single die is uniform, yet the sum of 10 dice is nearly a bell curve
- Height, weight, and measurement error are each the accumulation of countless tiny factors — hence their normality
- It tells us: the shape of the **sum** has nothing to do with the distribution of any single variable

$$\bar{X} \approx N\left(\mu, \frac{\sigma^2}{n}\right)$$

### The Scale of Convergence: 1/√n

The law of large numbers says the average converges to the expectation — but **how fast**? The central limit theorem gives the precise answer:

$$\text{deviation} \sim \frac{\sigma}{\sqrt{n}}$$

- Flip 100 times and the deviation is about $\frac{1}{\sqrt{100}} = 0.1$
- Flip 10,000 times and the deviation is about $\frac{1}{\sqrt{10000}} = 0.01$

**To halve the error, you need 4 times the sample** — the fundamental price of statistical inference.

### From Laws to Statistical Inference

The law of large numbers and the central limit theorem are the foundations of statistics: the confidence intervals of opinion polls, the p-values of hypothesis tests, the $\pm 3\sigma$ limits of quality-control charts — all stand on these two laws.

---

**From here:** see [Applications](#applications) for how these laws underpin weather forecasting and quality control; in [Explore](#explore), flip a coin endlessly and watch the frequency march toward the probability.

→ [Continue reading: Bayes — Updating Beliefs with Evidence](/exhibit/bayes)
