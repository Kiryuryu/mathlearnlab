## Interactive: The Lab of Order Within Randomness

The distribution of primes looks random, yet it can be counted, measured, and checked everywhere. These experiments let you feel three core rules with your own hands: how sieves *generate* primes, how the prime number theorem *predicts* their count, and how prime gaps *breathe*. For each one, guess first with intuition, then check against the answer — you will find order behind all the randomness.

### Try It 1: The Sieve of Eratosthenes, from 1 to 100

List the integers from 1 to 100. Cross out 1, then start at 2: **each time take the first un-crossed number (it is prime) and cross out all its multiples**. The table below shows the finished sieve — bold numbers are prime (1 has been crossed out):

| 1 | **2** | **3** | 4 | **5** | 6 | **7** | 8 | 9 | 10 |
| **11** | 12 | **13** | 14 | 15 | 16 | **17** | 18 | **19** | 20 |
| 21 | 22 | **23** | 24 | 25 | 26 | 27 | 28 | **29** | 30 |
| **31** | 32 | 33 | 34 | 35 | 36 | **37** | 38 | 39 | 40 |
| **41** | 42 | **43** | 44 | 45 | 46 | **47** | 48 | 49 | 50 |
| 51 | 52 | **53** | 54 | 55 | 56 | 57 | 58 | **59** | 60 |
| **61** | 62 | 63 | 64 | 65 | 66 | **67** | 68 | 69 | 70 |
| **71** | 72 | **73** | 74 | 75 | 76 | 77 | 78 | **79** | 80 |
| 81 | 82 | **83** | 84 | 85 | 86 | 87 | 88 | **89** | 90 |
| 91 | 92 | 93 | 94 | 95 | 96 | **97** | 98 | 99 | 100 |

**Question: why is sieving up to $\sqrt{100}=10$ enough?**

<details>
<summary>Answer</summary>
Every composite has a prime factor at most its square root; multiples of primes above 10 (like 97) were already crossed out by smaller primes, so nothing new remains. There are exactly 25 primes between 1 and 100, matching $\pi(100)=25$.
</details>

### Try It 2: Compare $\pi(x)$ with $x/\ln x$

| $x$ | $\pi(x)$ (exact) | $x/\ln x$ | ratio $\pi(x)\ln x / x$ |
|-----|------------------|-----------|------------------------|
| $10^3$ | 168 | 145 | 1.16 |
| $10^4$ | 1229 | 1086 | 1.13 |
| $10^5$ | 9592 | 8686 | 1.10 |
| $10^6$ | 78498 | 72382 | 1.08 |
| $10^7$ | 664579 | 620420 | 1.07 |
| $10^8$ | 5761455 | 5428681 | 1.06 |
| $10^9$ | 50847534 | 48254942 | 1.05 |

Watch the two columns themselves: the difference grows (from 23 to 2.6 million), yet the relative gap shrinks — **asymptotics never claims "equal," only "ratio tending to 1"**.

**Question: which way does the ratio column head? Guess $\pi(10^{10})$.**

<details>
<summary>Answer</summary>
The ratio falls monotonically toward 1 — the very meaning of "asymptotic": the **relative** gap between $\pi(x)$ and $x/\ln x$ keeps shrinking. $\pi(10^{10})=455052511$, where the ratio is about 1.05. Estimation trick: $\ln 10^{10}\approx 23.03$, so $10^{10}/23.03\approx 4.34\times 10^8$ — the true value overshoots it by roughly 5%.
</details>

### Try It 3: Prime Gaps

The first 20 primes are 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, with gaps 1, 2, 2, 4, 2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4. Gaps wax and wane: the largest gap below 100 is 8 (between 89 and 97), below 1000 it is 20 (887 to 907), and below $10^6$ it is 114. By the way, twin pairs with gap 2 appear 7 times among the first 20 primes — rare, yet always present.

**Question: can you build an arbitrarily long run of consecutive composites?**

<details>
<summary>Answer</summary>
Yes! The $k$ numbers $(k+1)!+2,\ (k+1)!+3,\ \ldots,\ (k+1)!+(k+1)$ are divisible by $2,3,\ldots,k+1$ respectively — all composite. So prime gaps can be arbitrarily large: "ever sparser" coexisting with "infinitely many" is exactly the marvel of the distribution.
</details>

### Try It 4: Guess the $n$-th Prime

Use $p_n\approx n\ln n$: the 1000th prime should be about $1000\ln 1000\approx 6908$; the true value is 7919, off by about 13%.

**Question: what about the millionth prime?**

<details>
<summary>Answer</summary>
$10^6\ln 10^6\approx 13.8\times 10^6$; the true value is 15485863 — the magnitude is exactly right (see the concept page). The larger $n$, the smaller the relative error: the value of estimating is precisely "fix the order of magnitude first, worry about the exact value later."

After these four experiments you will probably agree: "random" is only the observer's illusion — every seemingly random landing point obeys the predictions of probability exactly.
</details>
