## Key Insights: How to Solve Number Theory Problems

### 1. Testing Primality: From Trial Division to Miller–Rabin

- Small numbers: trial divide up to $\sqrt{n}$ (if $n$ has a factor, one is at most $\sqrt{n}$)
- Large numbers: Miller–Rabin primality test (probabilistic, milliseconds, error chance below "being hit by a meteor")
- Fast sieving: the Sieve of Eratosthenes — cross out multiples of each prime in turn

### 2. Congruences: Four Points About Modular Arithmetic

$$a \equiv b \pmod m \iff m \mid (a-b)$$

- Congruences support addition and multiplication (closed under modular arithmetic)
- **Division needs care**: from $ac \equiv bc \pmod m$ you may cancel $c$ only when $\gcd(c,m)=1$
- Inverses: $ax \equiv 1 \pmod m$ has a solution $\iff \gcd(a,m)=1$, found by the extended Euclidean algorithm
- High powers: Fermat's little theorem $a^{p-1}\equiv 1 \pmod p$ reduces the exponent below $p-1$

### 3. GCD: The Euclidean Algorithm

$$\gcd(a,b) = \gcd(b, a \bmod b)$$

Recurse until the remainder is 0, giving $O(\log n)$ complexity. The extended version also finds $x,y$ with $ax+by=\gcd(a,b)$ — the foundation for modular inverses and linear congruences.

### 4. Prime Distribution and Asymptotics

For "approximately how many primes" questions, use the prime number theorem $\pi(x) \sim \frac{x}{\ln x}$. Example: "how many primes below $10^9$" → $\frac{10^9}{\ln 10^9} \approx 4.8 \times 10^7$.

### 5. Standard Moves in Number-Theoretic Proofs

- **Infinite descent**: assume a minimal counterexample, then construct a smaller one (Fermat used it to show $x^4+y^4=z^2$ has no solutions)
- **Contradiction + unique factorization**: assume the equation, split into prime powers, use uniqueness to force a contradiction
- **Residue classification**: sort integers by their remainder mod $m$; splitting into cases often dissolves the problem

### Common Pitfalls

1. **Forgetting $p$ must be prime** for Fermat's little theorem (Carmichael numbers "impersonate" primes)
2. **Cancelling in congruences without checking coprimality**: cancelling $c$ from $ac \equiv bc$ fails when $\gcd(c,m)>1$
3. **Treating $\pi(x)$ as exact**: the prime number theorem is asymptotic (ratio tends to 1), not equality
4. **Trial dividing to $n/2$**: reaching $\sqrt{n}$ is enough — a huge time saver
