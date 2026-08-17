## Explore: The Bayesian Intuition Lab

### Try It 1: The Medical Test

A rare disease affects 1% of the population, and the test is 99% accurate. If the test comes back positive, what is the probability that you are actually sick?

<details>
<summary>Answer</summary>
Using Bayes' formula: $P(\text{sick}|\text{pos}) = \frac{0.99 \times 0.01}{0.99 \times 0.01 + 0.01 \times 0.99} \approx 0.5$. **Even a highly accurate test leaves only a 50% chance of disease after a positive result** — because the disease is so rare, a flood of false positives drowns out the true positives.
</details>

### Try It 2: Bayesian Updating

A box has a 70% chance of being "mostly red" (7 red, 3 blue) and a 30% chance of being "mostly blue" (3 red, 7 blue). After drawing one red ball, what is the probability that the box is "mostly red"?

<details>
<summary>Answer</summary>
Prior $P(\text{red box}) = 0.7$. Likelihoods: drawing red from a red box $P(\text{red}|\text{red box}) = 0.7$; drawing red from a blue box $P(\text{red}|\text{blue box}) = 0.3$. Posterior $P(\text{red box}|\text{red}) = \frac{0.7\times0.7}{0.7\times0.7 + 0.3\times0.3} = \frac{0.49}{0.58} \approx 0.845$. **One red ball lifts your belief from 70% to 84.5%** — evidence is updating belief.
</details>

### Try It 3: Spam Filtering

An email contains the word "free." It is known that 20% of spam messages contain "free," while only 1% of normal messages do. If 30% of all emails are spam, what is the probability that an email containing "free" is spam?

<details>
<summary>Answer</summary>
$P(\text{spam}|\text{free}) = \frac{0.2\times0.3}{0.2\times0.3 + 0.01\times0.7} = \frac{0.06}{0.067} \approx 0.896$. About 90% — "free" is a very strong spam signal. This is exactly how a naive Bayes classifier works.
</details>

### Try It 4: The Power of the Prior

With the same 99%-accurate test, if the prevalence is 10% (not 1%), what is the probability of disease after a positive result?

<details>
<summary>Answer</summary>
$P(\text{sick}|\text{pos}) = \frac{0.99\times0.1}{0.99\times0.1 + 0.01\times0.9} = \frac{0.099}{0.108} \approx 0.917$. When prevalence rises from 1% to 10%, the probability of disease after a positive result soars from 50% to 92%. **The prior (prevalence) sets the foundation for the posterior** — in Bayes' formula, the prior is anything but optional.
</details>
