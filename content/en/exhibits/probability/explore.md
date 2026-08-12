## Interactive: The Intuition Lab of Probability

> Use the folded exercises below to feel the laws of probability — certainty within randomness, the shapes of distributions, and Bayesian updating.

### Try It 1: The Law of Large Numbers

Imagine flipping a coin forever. A single result is random, but as the count grows, the proportion of heads approaches 0.5. This is the **law of large numbers**:

$$\lim_{n\to\infty}\frac{\text{number of heads}}{n} = \frac{1}{2}$$

Feel it: randomness is "locally chaotic, globally ordered." **How do you think the gap from 0.5 changes after 10 flips, 100 flips, and 10,000 flips?**

<details>
<summary>Answer</summary>
After 10 flips you might be off by 0.2 or more; after 100 flips usually within 0.05; after 10,000 flips a gap under 0.01 is very likely. Note: it is not that "more flips get closer to 0.5" (that would remove randomness) — it is that **the size of the deviation shrinks**, on the order of $1/\sqrt{n}$. The precise version of the law of large numbers is the central limit theorem.
</details>

### Try It 2: The Magic of the Central Limit Theorem

Whatever the distribution of a single random variable (uniform, exponential, discrete…), **as soon as you add them up**, the sum approaches a normal distribution:

- One die: uniform (every face equally likely)
- Two dice: triangular distribution
- Three dice: already approaching a bell
- Ten dice: almost exactly normal

**Why do "sums of many tiny factors" in real life always form a bell curve? Guess which theorem is behind it.**

<details>
<summary>Answer</summary>
It is the central limit theorem. Height, weight, and measurement error are all sums of countless tiny, independent factors, so they are approximately normal. The key is the "sum," not the individual factors — **even if a single die's distribution is not bell-shaped at all, summing them turns it into one.**
</details>

### Try It 3: Bayesian Updating

Bayes' theorem tells us how to update beliefs with evidence:

$$P(A|B) = \frac{P(B|A)\,P(A)}{P(B)}$$

An example: with a 1% disease rate and a 99%-accurate test, a positive result updates the prior of 1% to about 50%.

**A test claims "99% accuracy," and you test positive. Is your probability of disease really close to 99%? Why?**

<details>
<summary>Answer</summary>
No. If 99% of the sick test positive and 1% of the healthy are falsely flagged, then out of 10,000 people about 100 are sick (99 test positive) and 9,900 are healthy (99 false positives) — among 198 positives, only about half are actually sick. **When the prior (disease rate) is extremely low, even a very accurate test is drowned by false positives.** This is the most counterintuitive — and most useful — lesson of Bayesian thinking.
</details>

### Try It 4: Expected Value

The expectation is the "long-run average":

$$E[X] = \sum x \cdot P(X=x)$$

A gamble: flip a fair coin — win 100 yuan on heads, lose 90 on tails. **Should you take this bet?**

<details>
<summary>Answer</summary>
$E[X] = 0.5 \times 100 + 0.5 \times (-90) = 5$ yuan > 0. The expectation is positive, so in the long run you average 5 yuan per game — **worth playing** (as long as you can tolerate the interim swings). Conversely, any bet with negative expectation loses in the long run. The expectation tells you what to do; the variance tells you how bumpy the ride is.
</details>
