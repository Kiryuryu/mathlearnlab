## Probability Spaces — The Mathematical Framework of Randomness

Will it rain tomorrow? What number will a die show? A single random event cannot be predicted, yet we still need a rigorous language to describe "randomness." A **probability space** is that language: it breaks "random" into three workable parts and turns uncertainty into computable mathematics.

### The Three Ingredients of a Probability Space

> A probability space consists of three things: the **sample space Ω** (the set of all possible outcomes), **events** (subsets of Ω), and **probabilities** (a number between 0 and 1 assigned to each event).

- Rolling a die: Ω = {1,2,3,4,5,6}, the event "the number is greater than 4" = {5,6}
- Flipping a coin: Ω = {heads, tails}, the event "heads" = {heads}
- Probabilities must satisfy: $P(\Omega)=1$, $P(\text{event}) \ge 0$, and additivity for mutually exclusive events

### Conditional Probability: How Information Changes Probability

Knowing new information changes probability. **Conditional probability** $P(A|B)$ answers "given that $B$ happens, what is the probability of $A$?":

$$P(A|B) = \frac{P(A \cap B)}{P(B)}$$

- Given that an even number was rolled ({2,4,6}), the probability of a 2 → $\frac{1/6}{3/6} = \frac{1}{3}$
- Conditional probability embeds "background knowledge" into the calculation of probability

### Independence: When Information Changes Nothing

Two events are independent when **knowing one tells you nothing about the other**:

$$P(A \cap B) = P(A) \cdot P(B)$$

Note: independence ⟺ $P(A|B) = P(A)$. Flipping a coin twice, drawing twice with replacement — both are independent; drawing without replacement is not.

### Random Variables: Turning Randomness into Numbers

A **random variable** is a function mapping the sample space to the real numbers: the number on a die, tomorrow's rainfall, the length of a queue. Once you have a random variable, you can speak of its **distribution** (the probability of each value), its **expectation** (a weighted average), and its **variance** (how much it fluctuates):

$$E[X] = \sum x \cdot P(X=x), \qquad \text{Var}(X) = E[(X-\mu)^2]$$

The random variable is the bridge that carries probability theory from "events" to "data analysis."

---

**From here:** see [Applications](#applications) supporting actuarial science and financial pricing; in [Interactive](#explore), compute conditional probabilities and expectations by hand.

→ [Continue reading: Limit Theorems — Certainty Within Randomness](/exhibit/limit-theorems)
