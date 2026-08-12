## Explore Limits

### Try It 1: Can You Find δ?

For f(x) = 2x + 1, prove that lim(x→3) f(x) = 7.

If ε = 0.1, what δ do you need?

<details>
<summary>Hint</summary>
|f(x) - 7| = |2x+1-7| = |2x-6| = 2|x-3|. So to have |f(x)-7| < 0.1, we need 2|x-3| < 0.1, i.e. |x-3| < 0.05. So δ = 0.05.
</details>

### Try It 2: Does This Limit Exist?

f(x) = |x|/x. As x → 0, does the limit exist?

<svg width="220" height="200" viewBox="0 0 220 200" role="img" aria-label="Graph of f=|x|/x: 1 for x>0, -1 for x<0, a break at x=0; left and right limits differ" style="margin:12px 0;display:block;">
  <g transform="translate(110,100)">
    <line x1="-100" y1="0" x2="100" y2="0" stroke="var(--border)" stroke-width="1.5" />
    <line x1="0" y1="-85" x2="0" y2="85" stroke="var(--border)" stroke-width="1.5" />
    <line x1="0" y1="-65" x2="90" y2="-65" stroke="var(--accent)" stroke-width="3" />
    <line x1="-90" y1="65" x2="0" y2="65" stroke="var(--accent)" stroke-width="3" />
    <circle cx="0" cy="-65" r="4.5" fill="var(--bg-page)" stroke="var(--accent)" stroke-width="2" />
    <circle cx="0" cy="65" r="4.5" fill="var(--bg-page)" stroke="var(--accent)" stroke-width="2" />
    <text x="30" y="-78" font-size="12" fill="var(--accent)">+1 (right)</text>
    <text x="-30" y="86" text-anchor="end" font-size="12" fill="var(--accent)">−1 (left)</text>
    <text x="40" y="40" font-size="11" fill="var(--accent-error)">break at x=0</text>
  </g>
</svg>

<details>
<summary>Think about it</summary>
Approaching from the right: when x > 0, f(x) = 1.
Approaching from the left: when x < 0, f(x) = -1.
The left and right limits are not equal — the limit does not exist!
This is why we need the concept of one-sided limits.
</details>

### Try It 3: Guess the Value

sin(0.01) ≈ ? (No calculator allowed)

<details>
<summary>Answer</summary>
When x is very small, sin(x) ≈ x. In fact sin(0.01) ≈ 0.0099998... very close to 0.01!
This is one of calculus's most important approximations, rooted in the limit lim(x→0) sin(x)/x = 1.
</details>

### Try It 4: The Harmonic Series Surprise

Does 1 + 1/2 + 1/3 + 1/4 + ... converge or diverge? Guess first.

<details>
<summary>Answer</summary>
Diverges! Even though each term approaches 0, the sum is infinite. But it grows incredibly slowly — the first 10⁴³ terms only sum to just over 100.

Compare: 1 + 1/4 + 1/9 + 1/16 + ... = π²/6 ≈ 1.645 (converges!)
</details>
