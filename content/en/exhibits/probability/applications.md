## Applications of Probability

### 1. The "60%" in Weather Forecasts

"60% chance of rain" does not mean 60% of the area will get rain. It means: given the observed historical data, in similar weather states, rain actually fell on 60% of such days.

This is the **frequentist** interpretation: probability = the limit of long-run frequency.

### 2. Medical Testing and Bayes

A rare disease affects 1% of people; the test is 99% accurate. If the test is positive, what is the real probability of disease?

Using Bayes' formula:

$$P(\text{sick}|\text{positive}) = \frac{0.99 \times 0.01}{0.99 \times 0.01 + 0.01 \times 0.99} \approx 0.5$$

The surprising conclusion: **even a very accurate test gives only a 50% chance of disease on a positive result** — because the disease rate is so low. This is the counterintuitive heart of Bayesian reasoning.

### 3. Insurance Actuarial Science

Insurance pricing rests on **expected loss**: premium = probability of accident × average loss + operating cost.

$$E[\text{loss}] = \sum \text{loss}_i \times P(\text{loss}_i)$$

The law of large numbers guarantees: with enough policyholders, actual payouts approach the expected value and the company profits steadily.

### 4. The Central Limit Theorem and Quality Control

Screw diameters from a factory ideally follow some distribution. But the **average diameter** of many screws is approximately normal — the central limit theorem at work.

Quality engineers use control charts to monitor the mean: as long as it stays within $\mu \pm 3\sigma$, the process is considered in control. This is the mathematical basis of statistical process control.

### 5. Probability in Machine Learning

A classifier outputting "0.87 probability of cat" is essentially:

$$P(y=\text{cat} | \text{image features})$$

- **Bayesian classifiers**: classify directly with Bayes' formula
- **Softmax regression**: turn linear outputs into a probability distribution
- **Confidence intervals**: quantify the uncertainty alongside the answer

### 6. Pricing Financial Derivatives

The Black–Scholes option-pricing formula rests on **random walks** (Brownian motion): stock prices follow geometric Brownian motion, and option prices are a discounted expectation. Probability is the foundation of quantitative finance.
