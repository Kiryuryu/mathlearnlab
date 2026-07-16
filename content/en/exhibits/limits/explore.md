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
