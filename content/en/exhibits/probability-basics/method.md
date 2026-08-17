## The Strategist's Playbook: Problem-Solving with Probability Spaces

### 1. Draw the Sample Space First

The first step in almost every probability problem is to **clarify the sample space**: what are all the possible outcomes? Are they equally likely?

- Classical probability: finitely many equally likely outcomes → $P = \frac{|A|}{|\Omega|}$
- Geometric probability: continuous outcomes → $P = \frac{\text{area}}{\text{total area}}$
- Don't miss outcomes, and don't count the same outcome twice

### 2. Check for Independence

Are the two events independent? **Only independent events may be multiplied:**

$$P(A\cap B) = P(A)P(B) \quad (\text{only if } A, B \text{ are independent})$$

When they are not independent, use conditional probability: $P(A\cap B) = P(A)P(B|A)$.

### 3. Reach for the Definition of Conditional Probability First

$$P(A|B) = \frac{P(A\cap B)}{P(B)}$$

Find the intersection first, then divide by the probability of the conditioning event. **Don't estimate conditional probabilities by intuition** — many counterintuitive problems are born right there.

### 4. Random Variables: Find the Distribution Before Computing

For problems involving random variables, first determine the type of distribution:

| Type | Key formula |
|------|------------|
| Binomial $B(n,p)$ | $P(X=k) = \binom{n}{k}p^k(1-p)^{n-k}$, $E=np$ |
| Poisson | $P(X=k)=\frac{\lambda^k e^{-\lambda}}{k!}$ |
| Uniform | $E=\frac{a+b}{2}$ |
| Normal | Standardize $Z=\frac{X-\mu}{\sigma}$ |

### 5. Computing Expectation and Variance

Expectation is a weighted average, and it is linear: $E[aX+b] = aE[X]+b$; variance: $Var(X) = E[X^2] - (E[X])^2$.

### Common Pitfalls

1. **Multiplying without checking for independence**
2. **Confusing $P(A|B)$ with $P(B|A)$** (the classic medical-test trap)
3. **An unclear sample space** leading to counting errors
4. **Expectation is not "the most likely value"** — expectation is a weighted average
