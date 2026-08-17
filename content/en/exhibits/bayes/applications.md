## Bayes' Theorem in Action

### 1. Medical Testing and Bayes

A rare disease affects 1% of the population, and the test is 99% accurate. If the test comes back positive, what is the probability that you are actually sick?

Using Bayes' formula:

$$P(\text{sick}|\text{positive}) = \frac{0.99 \times 0.01}{0.99 \times 0.01 + 0.01 \times 0.99} \approx 0.5$$

A surprising conclusion: **even a highly accurate test leaves only a 50% chance of disease after a positive result** — because the disease is so rare. This is the counterintuitive heart of Bayesian thinking.

### 2. Spam Filtering

The naive Bayes classifier: given the features of an email (its word frequencies), compute the posterior probability that it is spam. Each word contributes a piece of "evidence," and Bayes' formula combines them — the filter in your inbox runs this calculation every single day.

### 3. Bayes in Machine Learning

- **Naive Bayes**: classifies directly with Bayes' formula
- **Bayesian inference**: treats parameters as random variables and updates their posterior distributions with data
- **Confidence intervals**: the model quantifies its uncertainty alongside its answer

### 4. Sensor Fusion in Self-Driving Cars

LiDAR, cameras, and millimeter-wave radar each report something different; Bayesian updating fuses them into a single unified estimate — the posterior judgment behind "the sensor says there is an obstacle."

### 5. A/B Testing and Decision-Making

After a product redesign, use Bayesian methods to ask "is the new version really better?": treat the size of the improvement as a random variable, update the posterior with observed data, and judge the confidence.

---

**Behind all these applications:** Bayes' theorem turns "learning" into mathematics — prior + evidence = posterior — and this is exactly how intelligent systems work.
