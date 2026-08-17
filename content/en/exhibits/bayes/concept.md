## Bayes' Theorem — Updating Beliefs with Evidence

A positive test result — are you really sick? Is this email spam? When new evidence arrives, how should our beliefs change? **Bayes' theorem** gives the precise answer: combine the "prior belief" with the "new evidence" to obtain the "posterior belief."

### Bayes' Theorem

$$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$$

One formula answers a core question of epistemology: **after learning the new evidence $B$, how should our belief in $A$ be updated?**

- $P(A)$: the **prior** — your belief before seeing the evidence
- $P(B|A)$: the **likelihood** — how likely $B$ is when $A$ holds
- $P(A|B)$: the **posterior** — your updated belief after seeing the evidence

### The Counterintuitive Medical Test

A rare disease affects 1% of the population, and the test is 99% accurate. If the test comes back positive, what is the probability that you are actually sick?

Using Bayes' formula:

$$P(\text{sick}|\text{positive}) = \frac{0.99 \times 0.01}{0.99 \times 0.01 + 0.01 \times 0.99} \approx 0.5$$

**Even a highly accurate test leaves only a 50% chance of disease after a positive result** — because the disease is so rare, a flood of false positives drowns out the true positives. This is the most counterintuitive — and most practical — insight of Bayesian thinking.

### Bayesian Updating: Continuous Learning

Bayes' theorem can be applied again and again: today's posterior is tomorrow's prior.

$$\text{posterior} \to \text{new prior} \to \text{more evidence} \to \text{updated posterior}$$

This is precisely the method of science: constantly revising old beliefs with new evidence. Naive Bayes and Bayesian inference in machine learning turn this updating process into algorithms.

### Bayesians vs. Frequentists

- **Frequentists**: probability is long-run frequency — an objective property
- **Bayesians**: probability is the strength of a belief, and it can be updated with evidence

Weather forecasts ("60% chance of rain"), medical tests, spam filters, sensor fusion in self-driving cars — much of the core of modern AI rests on Bayesian updating.

---

**From here:** see [Applications](#applications) driving medical testing, spam filtering, and machine learning; in [Interactive](#explore), perform a Bayesian update by hand and feel how evidence revises the prior.

→ [Continue reading: Back to the probability overview](/exhibit/probability)
