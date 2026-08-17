## Interactive: The Laboratory of Unique Factorization

The concept panel said "factorization is unique" — seeing is believing. In this section, factor numbers, compare efficiency, and hunt for counterexamples to test the boundary of the theorem yourself.

### Try It 1: Type an Integer, Watch It Factor

Interactive idea: enter an integer $n$ and the page shows a "division ladder" — at each step divide by the smallest prime factor, until a prime remains. For 360:

| Step | Current number | Divide by | Quotient |
|---|---|---|---|
| 1 | 360 | 2 | 180 |
| 2 | 180 | 2 | 90 |
| 3 | 90 | 2 | 45 |
| 4 | 45 | 3 | 15 |
| 5 | 15 | 3 | 5 |
| 6 | 5 | — | prime, stop |

<details>
<summary>Observe</summary>
Dividing by the smallest prime factor at each step guarantees no factor is missed; the exponents accumulate down the ladder, finally assembling $360 = 2^3 \times 3^2 \times 5$. Try another number (say 720) and check whether you get $2^4 \times 3^2 \times 5$. Try 1000 too: $1000 = 2^3 \times 5^3$ — just two prime factors, 2 and 5, each appearing 3 times.
</details>

### Try It 2: Compare the Efficiency of Finding Primes

Four methods, each with its own job — compare them in a table:

| Method | Complexity | At scale $10^6$ (indicative) | Best for |
|---|---|---|---|
| Trial division (single number) | $O(\sqrt{n})$ | about $10^3$ divisions per number | checking a few numbers |
| Sieve of Eratosthenes | $O(n\log\log n)$ | about $3 \times 10^6$ operations total | listing all primes in a range at once |
| Miller–Rabin | $O(k \log^3 n)$ | milliseconds | primality testing of large numbers |
| Pollard's rho | $O(n^{1/4})$ | seconds | factoring large composites |

<details>
<summary>Think about it</summary>
Why is it enough for the sieve to cross out multiples only up to $\sqrt{n}$? Because every composite has a prime factor no larger than its square root — it was already crossed out by a smaller prime.
</details>

### Try It 3: Find Counterexamples — Number Systems Where Factorization Is Not Unique

**Experiment A: the even-number world.** Suppose the only "numbers" allowed are even integers. In this world, 36 has two decompositions:

$$36 = 2 \times 18 = 6 \times 6$$

<details>
<summary>Verify</summary>
In the even world, $2$, $18$, and $6$ are all irreducible: the product of two even numbers always contains a factor of 4, so it can never equal 2, 18, or 6 — they are this system's "primes," yet 36 splits two different ways. Unique factorization fails in the even-number world!
</details>

**Experiment B: the number system $\mathbb{Z}[\sqrt{-5}]$.** Allow numbers of the form $a + b\sqrt{-5}$ ($a, b$ integers). The same 6:

<svg width="420" height="120" viewBox="0 0 420 120" role="img" aria-label="Two factorizations of the same 6: 2×3 and (1+√-5)(1−√-5)" style="margin:12px 0;display:block;">
  <text x="210" y="26" text-anchor="middle" font-size="17" font-weight="700" fill="var(--text)">6</text>
  <path d="M210 34 L120 76 M210 34 L300 76" stroke="var(--text-muted)" stroke-width="1.5" fill="none"/>
  <text x="120" y="94" text-anchor="middle" font-size="13" font-family="var(--font-mono)" fill="var(--accent)">2 × 3</text>
  <text x="300" y="94" text-anchor="middle" font-size="13" font-family="var(--font-mono)" fill="var(--accent)">(1+√-5)(1−√-5)</text>
</svg>

<details>
<summary>Verify</summary>
Multiply it out: $(1+\sqrt{-5})(1-\sqrt{-5}) = 1 - (\sqrt{-5})^2 = 1 + 5 = 6$ ✓. And $2$, $3$, $1\pm\sqrt{-5}$ are all checked with the norm $N(a+b\sqrt{-5}) = a^2+5b^2$: $N(2)=4$, $N(3)=9$, $N(1\pm\sqrt{-5})=6$. If $2$ factored, it would need a factor of norm $2$, but $a^2+5b^2=2$ has no integer solutions; likewise $3$ and $1\pm\sqrt{-5}$ (the required norms $3$ and $2$ do not exist). All four factors are irreducible, yet 6 has two different "atomic combinations" — unique factorization fails.
</details>

Conclusion: **"unique factorization" is not a property every number system gets for free — it is a gift of the boundary of ordinary integers.**

### Try It 4: Guess How Many Divisors 360 Has

Use the formula $\tau(n) = \prod (e_i + 1)$: $360 = 2^3 \times 3^2 \times 5^1$, so $\tau(360) = 4 \times 3 \times 2 = 24$.

<details>
<summary>Expand to verify</summary>
Here are all 24 divisors: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 60, 72, 90, 120, 180, 360 — exactly 24, no more no less. Their "recipes" are precisely the combinations $2^i3^j5^k$ with $i \in \{0,1,2,3\}$, $j \in \{0,1,2\}$, $k \in \{0,1\}$ — which is exactly why we "add one to each exponent and multiply."
</details>
