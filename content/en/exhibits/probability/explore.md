## Interactive: The Intuition Lab of Probability

> Use the folded exercises below to feel the laws of probability — certainty within randomness, the shapes of distributions, and Bayesian updating.

### Try It 1: The Law of Large Numbers

Imagine flipping a coin forever. A single result is random, but as the count grows, the proportion of heads approaches 0.5. This is the **law of large numbers**:

$$\lim_{n\to\infty}\frac{\text{number of heads}}{n} = \frac{1}{2}$$

Feel it: randomness is "locally chaotic, globally ordered." **How do you think the gap from 0.5 changes after 10 flips, 100 flips, and 10,000 flips?**

<svg width="300" height="180" viewBox="0 0 300 180" role="img" aria-label="Line chart of the proportion of heads converging to 0.5 as the number of flips grows; the wobble narrows with more flips" style="margin:12px 0;display:block;">
  <line x1="40" y1="150" x2="290" y2="150" stroke="var(--border)" stroke-width="1.5" />
  <line x1="40" y1="10" x2="40" y2="150" stroke="var(--border)" stroke-width="1.5" />
  <line x1="40" y1="85" x2="290" y2="85" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="6 5" />
  <text x="290" y="80" text-anchor="end" font-size="11" fill="var(--accent)">0.5</text>
  <polyline points="42,140 55,120 68,135 82,95 96,112 110,80 124,98 138,72 152,88 166,75 180,82 194,70 208,78 222,66 236,74 250,68 264,72 278,70 288,71" fill="none" stroke="var(--accent-warm)" stroke-width="2" />
  <path d="M 42,130 C 80,105 140,95 200,89 250,87 288,86 288,86 L 288,84 C 250,84 200,85 140,87 80,91 42,100 42,130" fill="none" stroke="var(--border-focus)" stroke-width="1" stroke-dasharray="4 4" />
  <text x="150" y="165" text-anchor="middle" font-size="11" fill="var(--text-muted)">number of flips n →</text>
</svg>

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

<div style="display:flex;flex-wrap:wrap;gap:10px;margin:12px 0;">
  <figure style="margin:0;text-align:center;flex:1;min-width:120px;">
    <svg width="120" height="110" viewBox="0 0 120 110" role="img" aria-label="One die: uniform distribution, six equal bars">
      <g transform="translate(8,15)">
        <rect x="10" y="0" width="12" height="70" fill="var(--accent)" /><rect x="24" y="0" width="12" height="70" fill="var(--accent)" /><rect x="38" y="0" width="12" height="70" fill="var(--accent)" />
        <rect x="52" y="0" width="12" height="70" fill="var(--accent)" /><rect x="66" y="0" width="12" height="70" fill="var(--accent)" /><rect x="80" y="0" width="12" height="70" fill="var(--accent)" />
        <line x1="0" y1="70" x2="105" y2="70" stroke="var(--border)" stroke-width="1" />
      </g>
    </svg>
    <figcaption style="font-size:11px;color:var(--text-muted);">1 die · uniform</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;flex:1;min-width:120px;">
    <svg width="120" height="110" viewBox="0 0 120 110" role="img" aria-label="Sum of two dice: triangular distribution">
      <g transform="translate(5,15)">
        <rect x="6" y="58" width="11" height="12" fill="var(--accent)" /><rect x="18" y="44" width="11" height="26" fill="var(--accent)" /><rect x="30" y="28" width="11" height="42" fill="var(--accent)" />
        <rect x="42" y="12" width="11" height="58" fill="var(--accent)" /><rect x="54" y="0" width="11" height="70" fill="var(--accent)" /><rect x="66" y="12" width="11" height="58" fill="var(--accent)" />
        <rect x="78" y="28" width="11" height="42" fill="var(--accent)" /><rect x="90" y="44" width="11" height="26" fill="var(--accent)" /><rect x="102" y="58" width="11" height="12" fill="var(--accent)" />
        <line x1="0" y1="70" x2="115" y2="70" stroke="var(--border)" stroke-width="1" />
      </g>
    </svg>
    <figcaption style="font-size:11px;color:var(--text-muted);">2 dice · triangular</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;flex:1;min-width:120px;">
    <svg width="120" height="110" viewBox="0 0 120 110" role="img" aria-label="Sum of three dice: approaching a bell curve">
      <g transform="translate(2,15)">
        <rect x="4" y="58" width="8" height="12" fill="var(--accent)" /><rect x="13" y="50" width="8" height="20" fill="var(--accent)" /><rect x="22" y="40" width="8" height="30" fill="var(--accent)" />
        <rect x="31" y="28" width="8" height="42" fill="var(--accent)" /><rect x="40" y="16" width="8" height="54" fill="var(--accent)" /><rect x="49" y="8" width="8" height="62" fill="var(--accent)" />
        <rect x="58" y="4" width="8" height="66" fill="var(--accent)" /><rect x="67" y="8" width="8" height="62" fill="var(--accent)" /><rect x="76" y="16" width="8" height="54" fill="var(--accent)" />
        <rect x="85" y="28" width="8" height="42" fill="var(--accent)" /><rect x="94" y="40" width="8" height="30" fill="var(--accent)" /><rect x="103" y="50" width="8" height="20" fill="var(--accent)" />
        <rect x="112" y="58" width="8" height="12" fill="var(--accent)" />
        <line x1="0" y1="70" x2="120" y2="70" stroke="var(--border)" stroke-width="1" />
      </g>
    </svg>
    <figcaption style="font-size:11px;color:var(--text-muted);">3 dice · near bell</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;flex:1;min-width:120px;">
    <svg width="120" height="110" viewBox="0 0 120 110" role="img" aria-label="Sum of ten dice: almost normal">
      <g transform="translate(4,15)">
        <rect x="6" y="62" width="6" height="8" fill="var(--accent)" /><rect x="13" y="58" width="6" height="12" fill="var(--accent)" /><rect x="20" y="52" width="6" height="18" fill="var(--accent)" />
        <rect x="27" y="44" width="6" height="26" fill="var(--accent)" /><rect x="34" y="34" width="6" height="36" fill="var(--accent)" /><rect x="41" y="24" width="6" height="46" fill="var(--accent)" />
        <rect x="48" y="14" width="6" height="56" fill="var(--accent)" /><rect x="55" y="8" width="6" height="62" fill="var(--accent)" /><rect x="62" y="4" width="6" height="66" fill="var(--accent)" />
        <rect x="69" y="8" width="6" height="62" fill="var(--accent)" /><rect x="76" y="14" width="6" height="56" fill="var(--accent)" /><rect x="83" y="24" width="6" height="46" fill="var(--accent)" />
        <rect x="90" y="34" width="6" height="36" fill="var(--accent)" /><rect x="97" y="44" width="6" height="26" fill="var(--accent)" /><rect x="104" y="52" width="6" height="18" fill="var(--accent)" />
        <line x1="0" y1="70" x2="112" y2="70" stroke="var(--border)" stroke-width="1" />
      </g>
    </svg>
    <figcaption style="font-size:11px;color:var(--text-muted);">10 dice · near normal</figcaption>
  </figure>
</div>

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
