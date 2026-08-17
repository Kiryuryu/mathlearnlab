## Key Moves: Factoring and Testing Primality

The concept panel explained *why* factorization is unique; this section solves *how* to factor and how to test primality — a complete ladder from mental arithmetic to modern algorithms.

### 1. Trial Division: Only Up to $\sqrt{n}$

To test whether $n$ is prime, it suffices to try dividing by the primes up to $\sqrt{n}$ — because if $n = ab$ with $a \le b$, then the smaller factor $a \le \sqrt{n}$ hides within the square root.

Example: $n = 143$, $\sqrt{143} \approx 11.9$; try 2, 3, 5, 7, 11 → $143 = 11 \times 13$.

Complexity $O(\sqrt{n})$: for $n = 10^{12}$ that is about $10^6$ divisions — fine by hand or for small numbers.

Trial division is also the starting point of a **full factorization**: once you find the smallest prime factor $p$, keep dividing the quotient $\frac{n}{p}$ until a prime remains — walk the division ladder to the end and you have the complete list of prime factors of $n$.

### 2. The Sieve of Eratosthenes: Sieve Out a Whole Stretch at Once

Trial division handles one number at a time; the sieve handles a whole interval:

1. Write down the integers from 2 to $n$
2. Cross out all multiples of 2
3. Take the next uncrossed number (it must be prime) and cross out its multiples
4. Repeat up to $\sqrt{n}$; everything left is prime

Complexity $O(n \log \log n)$: sieving all primes below $10^7$ takes a modern computer about 0.1 seconds. Use the sieve to "find a batch of primes"; use trial division to "check a single number."

### 3. Pollard's rho: A Probabilistic Weapon for Large Composites

Factoring large composites is the bedrock of RSA security and a battleground for algorithm designers. Pollard's rho (1975) is one of the most elegant weapons:

- Generate a pseudorandom sequence $x_{i+1} = x_i^2 + c \pmod n$; it must eventually cycle
- By the **birthday paradox**, the sequence collides modulo $p$ (a small prime factor of $n$) far earlier than modulo $n$
- Once $x_i \equiv x_j \pmod p$ but $x_i \not\equiv x_j \pmod n$, computing $\gcd(|x_i - x_j|, n)$ catches the factor $p$

Expected complexity $O(n^{1/4})$ — a world away from trial division's $O(\sqrt{n})$. Example: $n = 8051$; rho finds $8051 = 97 \times 83$ within a few steps.

### 4. Quickly Testing Whether a Large Number Is Prime

To test whether a 256-bit number is prime, the full industrial pipeline is:

1. **Trial division by small primes**: the first few hundred primes eliminate the vast majority of composites
2. **Miller–Rabin**: a probabilistic test, milliseconds per run; $k$ rounds fail with probability at most $4^{-k}$ — 40 rounds drops it below "being hit by a meteor"
3. **Deterministic finishing**: below $2^{64}$ fixed base sets give absolute certainty; for larger numbers, BPSW or AKS can add further confirmation

The "random primes" behind bank keys and digital signatures are generated exactly this way, in milliseconds.

By the way: going from trial division to the polynomial-time AKS algorithm for deciding primality took mathematicians over two thousand years — every speedup in large-number primality testing translates directly into safer cryptography.

### Common Pitfalls

1. **Trial dividing to $n/2$ instead of $\sqrt{n}$**: wasting more than half your time
2. **Running only one round of Miller–Rabin**: a single round fails with probability 25% — critical applications need many rounds
3. **Trial dividing large composites**: at $10^{20}$ you would need $10^{10}$ divisions — eliminate small primes first, then bring in Pollard's rho
4. **Forgetting 0 and 1**: they are neither prime nor composite; the Fundamental Theorem speaks only to integers greater than 1
