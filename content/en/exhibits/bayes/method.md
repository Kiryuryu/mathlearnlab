## The Strategist's Playbook: Problem-Solving with Bayes

### 1. Reach for the Definition of Conditional Probability First

$$P(A|B) = \frac{P(A\cap B)}{P(B)}$$

Find the intersection first, then divide by the probability of the conditioning event. **Don't estimate conditional probabilities by intuition** — many counterintuitive problems are born right there.

### 2. The Law of Total Probability: Split into Cases

When a problem has several "mutually exclusive and exhaustive" cases $B_1,\dots,B_n$:

$$P(A) = \sum_{i=1}^n P(A|B_i)P(B_i)$$

Classic applications: multiple factories supplying goods, repeated testing, multi-level decisions.

### 3. Bayes: Reasoning Backward to the Cause

Given the outcome A, ask which kind of cause B produced it:

$$P(B_j|A) = \frac{P(A|B_j)P(B_j)}{\sum_i P(A|B_i)P(B_i)}$$

The mnemonic: **the numerator is "this one path"; the denominator is "the sum of all paths."**

### 4. The Standard Medical-Test Procedure

Prevalence $P(\text{sick})$, sensitivity $P(\text{pos}|\text{sick})$, false-positive rate $P(\text{pos}|\text{healthy})$:

$$P(\text{sick}|\text{pos}) = \frac{P(\text{pos}|\text{sick})P(\text{sick})}{P(\text{pos}|\text{sick})P(\text{sick}) + P(\text{pos}|\text{healthy})P(\text{healthy})}$$

When the prior (prevalence) is extremely low, even the most accurate test gets drowned out by false positives.

### 5. Bayesian Updating: Apply It Again and Again

The posterior becomes the new prior; keep refining with more evidence — Bayesian inference in machine learning is exactly this loop.

### Common Pitfalls

1. **Confusing $P(A|B)$ with $P(B|A)$** (the classic medical-test trap)
2. **Forgetting that the denominator is "the sum of all paths"** — there is more than one path
3. **Ignoring the prior**: when prevalence is very low, test results deviate wildly from intuition
4. **Treating a conditional probability as a joint probability**: $P(A|B) \neq P(A\cap B)$
