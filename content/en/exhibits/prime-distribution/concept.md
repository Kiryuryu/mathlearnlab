## Prime Distribution — Order Within Randomness

Primes seem to scatter at random along the number line: 25 of them among the first 100 numbers, 168 among the first 1000 — increasingly sparse, yet never vanishing. **The distribution of primes** studies exactly this: what deep pattern lies hidden behind that "seemingly random" scattering?

### The Prime Number Theorem

> The number $\pi(x)$ of primes up to $x$ is approximately $\frac{x}{\ln x}$:

$$\pi(x) \sim \frac{x}{\ln x}$$

- Among the first 100 numbers: $\pi(100) = 25$, while $\frac{100}{\ln 100} \approx 21.7$
- Among the first million: $\pi(10^6) = 78498$, while $\frac{10^6}{\ln 10^6} \approx 72382$

**Gauss guessed this theorem at age 15**; it was proved independently by Hadamard and de la Vallée Poussin in 1896. It ties the "random feel" of primes to the certainty of the logarithm.

### How Large Is the n-th Prime?

Read the prime number theorem backwards: the $n$-th prime is roughly $n\ln n$.

$$p_n \sim n\ln n$$

So the millionth prime should be about $10^6 \times \ln(10^6) \approx 13.8 \times 10^6$ — the true value is 15,485,863, so the magnitude is exactly right.

### Euler's Product and the Riemann Zeta Function

Euler discovered a stunning identity connecting **addition with multiplication**:

$$\sum_{n=1}^{\infty}\frac{1}{n^s} = \prod_{p \text{ prime}}\frac{1}{1 - p^{-s}}$$

On the left stands the zeta function (Riemann's ζ), an infinite series; on the right, the product runs over all primes. **The full nature of primes is encoded in this function** — the Riemann hypothesis, which concerns its zeros, remains the most important unsolved problem in mathematics.

### Prime Gaps and Twin Primes

- Gaps between neighboring primes grow and shrink (2, 4, 6, 2, 4, ...) — and yet gaps of any size will eventually appear
- **The twin prime conjecture**: there are infinitely many pairs of primes differing by 2 (3 and 5, 11 and 13, 17 and 19)
- **Yitang Zhang, 2013** proved that infinitely many prime pairs differ by less than 70 million (later narrowed to 246)

---

**From here:** see [Applications](#applications) on how the distribution of primes drives RSA cryptography and supports conjectures in number theory; in [Interactive](#explore), estimate prime counts by hand and feel the rhythm of the gaps.

→ [Continue reading: Back to the Number Theory Overview](/exhibit/primes)
