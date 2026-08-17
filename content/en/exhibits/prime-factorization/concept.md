## The Fundamental Theorem of Arithmetic — A Unique Decomposition

Break 360 down as far as it can go: $2^3 \times 3^2 \times 5$. No matter which factor you start from, you always arrive at the same collection of prime factors. **The Fundamental Theorem of Arithmetic** guarantees this uniqueness — and in doing so it makes primes the atoms of the number world, giving every integer one and only one "chemical formula."

### Unique Factorization

> Any integer greater than 1 can be written uniquely as a product of primes (up to order).

$$360 = 2^3 \times 3^2 \times 5$$

- **Existence**: keep pulling out factors until none are left
- **Uniqueness**: however you split it, the prime factors and their exponents are the same

This "uniqueness" matters enormously: it means primes act as the "periodic table of elements" for the world of integers — each number has exactly one "chemical formula."

### There Are Infinitely Many Primes

In the *Elements*, Euclid proved: **there are infinitely many primes**.

Proof idea (by contradiction): suppose there are only finitely many primes $p_1, p_2, \dots, p_k$, and consider the number $N = p_1p_2\cdots p_k + 1$. None of the $p_i$ divides $N$ (it leaves a remainder of 1), so $N$ must have a brand-new prime factor — a contradiction. This proof is widely regarded as one of the most elegant in the history of mathematics.

### Testing Primality: Trial Division

To test whether $n$ is prime, it is enough to try dividing by every prime up to $\sqrt{n}$:

$$n \text{ is composite} \iff \exists \text{ a prime factor } p \le \sqrt{n}$$

because if $n = ab$ with $a \le b$, then $a \le \sqrt{n}$. This straightforward method serves well when $n$ is not too large; for bigger numbers, turn to a sieve or a probabilistic test.

### The Sieve of Eratosthenes

Strike out the multiples of each prime, from smallest to largest, and what remains are the primes:

1. Write down the integers from 2 to $n$
2. Cross out all multiples of 2 — 2 is prime
3. Take the next uncrossed number (it must be prime) and cross out its multiples
4. Repeat up to $\sqrt{n}$

The sieve is the classic way to find primes, and the first building block for understanding how they are distributed.

---

**From here:** see [Applications](#applications) on how unique factorization underpins countless results in number theory; in [Interactive](#explore), run the sieve and factor numbers by trial division yourself.

→ [Continue reading: Congruence — The World of Modular Arithmetic](/exhibit/modular-arithmetic)
