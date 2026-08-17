## Explore: The Probability Space Intuition Lab

### Try It 1: Conditional Probability with a Die

Roll a fair die. Given that the result is even, what is the probability that it is a 2?

<details>
<summary>Answer</summary>
The sample space shrinks to {2,4,6}, and $P(2|\text{even}) = \frac{P(2\cap\text{even})}{P(\text{even})} = \frac{1/6}{3/6} = \frac{1}{3}$. Conditional probability is just "renormalization" — rescaling the probabilities of the known cases so they sum to 1.
</details>

### Try It 2: Are They Independent?

Flip two coins at once. Event A: "the first coin is heads." Event B: "both coins show the same face." Are A and B independent?

<details>
<summary>Answer</summary>
$P(A) = \frac{1}{2}$, $P(B) = \frac{1}{2}$, $P(A\cap B)$ = "first is heads and both are the same" = "both are heads" = $\frac{1}{4}$. Since $\frac{1}{2}\times\frac{1}{2} = \frac{1}{4}$, they are independent ✓. Knowing the first coin is heads does not change the judgment that "both are the same" — in fact, the two pieces of information happen to complement each other.
</details>

### Try It 3: Drawing Without Replacement

A bag contains 3 red and 2 blue balls. Draw twice without replacement. What is the probability of drawing red both times?

<details>
<summary>Answer</summary>
$P = \frac{3}{5} \times \frac{2}{4} = \frac{3}{10}$. Notice that the second probability changes (3/5 → 2/4), because drawing without replacement changes the sample space — this is a case of dependence.
</details>

### Try It 4: Expected Value

A gamble: flip a fair coin — heads wins 100 yuan, tails loses 90 yuan. What is the expected value? Should you play?

<details>
<summary>Answer</summary>
$E[X] = 0.5 \times 100 + 0.5 \times (-90) = 5$ yuan > 0. The expectation is positive, so in the long run you average a profit of 5 yuan per game — **worth playing** (as long as you can stomach the swings). Expectation tells you "should I do it?"; variance tells you "how much will it swing?"
</details>
