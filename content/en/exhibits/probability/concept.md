## Probability — The Science of Uncertainty

Will it rain tomorrow? How many heads in ten coin flips? Does a positive test result mean you are sick? A single random event is unpredictable, but **large numbers of random events follow definite laws as a whole** — probability is the mathematical language built for randomness, and the science of finding order in chaos.

### How Randomness Is Measured

A probability space consists of three things: the **sample space** (all possible outcomes), **events** (subsets of outcomes), and **probabilities** (a number in $[0,1]$ for each event). Two events are independent when knowing one tells you nothing about the other:

$$P(A \cap B) = P(A) \cdot P(B)$$

### The Law of Large Numbers: Certainty Within Randomness

A coin has probability $0.5$ of heads, but 10 flips need not give exactly 5 heads. Yet 10,000 flips will bring the proportion of heads extremely close to $0.5$:

$$\lim_{n\to\infty}\frac{X_1+X_2+\cdots+X_n}{n} = \mu$$

**Randomness contains certainty** — the average of many independent trials always approaches the expected value. This is the foundation of insurance and statistics.

### The Central Limit Theorem: The Normal Distribution Is Everywhere

No matter the underlying distribution, the **sum** of many independent random variables is approximately normally distributed. That is why height, weight, and measurement error all form "bell curves" — they are the accumulation of countless tiny factors.

### Bayes' Theorem: Updating Beliefs with New Evidence

$$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$

This formula answers one question: **after learning new evidence $B$, how should our belief in $A$ be updated?**

- Medical diagnosis: given a positive test, what is the probability of disease?
- Spam filtering: given the message content, how likely is it spam?
- Self-driving cars: the sensor says there is an obstacle — is there really one?

The core of modern machine learning (naive Bayes, Bayesian inference) is repeatedly applying this update.

---

**From here:** see [Applications](#applications) at work in weather forecasting, medical testing, and financial pricing; in [Interactive](#explore), "flip" a coin millions of times and watch the frequency march toward the probability.

→ [Continue reading: Back to the exhibits](/gaoshu) to pick a new direction
