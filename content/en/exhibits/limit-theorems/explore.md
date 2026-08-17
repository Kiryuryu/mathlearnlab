## Explore: An Intuition Lab for the Laws of Large Numbers

### Try It 1: The Law of Large Numbers

Imagine flipping a coin again and again. Each single flip is random, but as the count grows, the proportion of heads settles closer and closer to 0.5. **How do you think the gap between the proportion of heads and 0.5 changes after 10, 100, and 10,000 flips?**

<svg width="300" height="180" viewBox="0 0 300 180" role="img" aria-label="Line chart of the proportion of heads converging to 0.5 as the number of flips grows; the fluctuation narrows as flips increase" style="margin:12px 0;display:block;">
  <line x1="40" y1="150" x2="290" y2="150" stroke="var(--border)" stroke-width="1.5" />
  <line x1="40" y1="10" x2="40" y2="150" stroke="var(--border)" stroke-width="1.5" />
  <line x1="40" y1="85" x2="290" y2="85" stroke="var(--accent)" stroke-width="1.5" stroke-dasharray="6 5" />
  <text x="290" y="80" text-anchor="end" font-size="11" fill="var(--accent)">0.5</text>
  <polyline points="42,140 55,120 68,135 82,95 96,112 110,80 124,98 138,72 152,88 166,75 180,82 194,70 208,78 222,66 236,74 250,68 264,72 278,70 288,71" fill="none" stroke="var(--accent-warm)" stroke-width="2" />
  <path d="M 42,130 C 80,105 140,95 200,89 250,87 288,86 288,86 L 288,84 C 250,84 200,85 140,87 80,91 42,100 42,130" fill="none" stroke="var(--border-focus)" stroke-width="1" stroke-dasharray="4 4" />
  <text x="150" y="165" text-anchor="middle" font-size="11" fill="var(--text-muted)">Number of flips n →</text>
</svg>

<details>
<summary>Answer</summary>
After 10 flips the gap can be 0.2 or more; after 100 flips it usually stays within 0.05; after 10,000 flips it is very likely to be less than 0.01. Note: it is not that "more flips get closer to 0.5" (that would leave no randomness at all) — rather, **the size of the deviation is shrinking**, a law on the order of $\frac{1}{\sqrt{n}}$.
</details>

### Try It 2: The Magic of the Central Limit Theorem

Whatever distribution a single random variable follows, **just add them up** and the sum turns normal:

<div style="display:flex;flex-wrap:wrap;gap:10px;margin:12px 0;">
  <figure style="margin:0;text-align:center;flex:1;min-width:120px;">
    <svg width="120" height="110" viewBox="0 0 120 110" role="img" aria-label="1 die: uniform distribution, six bars of equal height">
      <g transform="translate(8,15)">
        <rect x="10" y="0" width="12" height="70" fill="var(--accent)" /><rect x="24" y="0" width="12" height="70" fill="var(--accent)" /><rect x="38" y="0" width="12" height="70" fill="var(--accent)" />
        <rect x="52" y="0" width="12" height="70" fill="var(--accent)" /><rect x="66" y="0" width="12" height="70" fill="var(--accent)" /><rect x="80" y="0" width="12" height="70" fill="var(--accent)" />
        <line x1="0" y1="70" x2="105" y2="70" stroke="var(--border)" stroke-width="1" />
      </g>
    </svg>
    <figcaption style="font-size:11px;color:var(--text-muted);">1 die · uniform</figcaption>
  </figure>
  <figure style="margin:0;text-align:center;flex:1;min-width:120px;">
    <svg width="120" height="110" viewBox="0 0 120 110" role="img" aria-label="Sum of 2 dice: triangular distribution">
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
    <svg width="120" height="110" viewBox="0 0 120 110" role="img" aria-label="Sum of 10 dice: almost normal distribution">
      <g transform="translate(4,15)">
        <rect x="6" y="62" width="6" height="8" fill="var(--accent)" /><rect x="13" y="58" width="6" height="12" fill="var(--accent)" /><rect x="20" y="52" width="6" height="18" fill="var(--accent)" />
        <rect x="27" y="44" width="6" height="26" fill="var(--accent)" /><rect x="34" y="34" width="6" height="36" fill="var(--accent)" /><rect x="41" y="24" width="6" height="46" fill="var(--accent)" />
        <rect x="48" y="14" width="6" height="56" fill="var(--accent)" /><rect x="55" y="8" width="6" height="62" fill="var(--accent)" /><rect x="62" y="4" width="6" height="66" fill="var(--accent)" />
        <rect x="69" y="8" width="6" height="62" fill="var(--accent)" /><rect x="76" y="14" width="6" height="56" fill="var(--accent)" /><rect x="83" y="24" width="6" height="46" fill="var(--accent)" />
        <rect x="90" y="34" width="6" height="36" fill="var(--accent)" /><rect x="97" y="44" width="6" height="26" fill="var(--accent)" /><rect x="104" y="52" width="6" height="18" fill="var(--accent)" />
        <line x1="0" y1="70" x2="112" y2="70" stroke="var(--border)" stroke-width="1" />
      </g>
    </svg>
    <figcaption style="font-size:11px;color:var(--text-muted);">10 dice · near-normal</figcaption>
  </figure>
</div>

<details>
<summary>Answer</summary>
Exactly the central limit theorem. Height, weight, and measurement error are each the accumulation of countless tiny, independent factors, so they all approximate a normal distribution. The key lies in the "sum," not in any single factor — **even when a single die's distribution is nothing like a bell, add them up and a bell appears.**
</details>

### Try It 3: Speed of Convergence

You know that with $n=100$ trials the deviation is about 0.1. To halve the error (to 0.05), how many trials do you need?

<details>
<summary>Answer</summary>
Deviation $\sim \frac{\sigma}{\sqrt{n}}$, so halving the error means doubling $\sqrt{n}$ → multiplying $n$ by 4, i.e., $n=400$. That is the "statistical cost": twice the precision, four times the sample.
</details>
