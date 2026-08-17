## Applications of Unique Factorization

The concept panel told us: every integer greater than 1 has a unique "prime recipe." This section follows that recipe through mathematics and daily life — from school arithmetic with fractions to the cryptography guarding the internet.

### 1. GCD and LCM: Take the Smaller — or the Larger — Exponent

Write both numbers in prime-factor form and the answer is visible at a glance. Take 360 and 84:

$$360 = 2^3 \times 3^2 \times 5, \qquad 84 = 2^2 \times 3 \times 7$$

- **Greatest common divisor**: take the **smaller** exponent of each prime, $\gcd(360,84) = 2^2 \times 3 = 12$
- **Least common multiple**: take the **larger** exponent of each prime, $\operatorname{lcm}(360,84) = 2^3 \times 3^2 \times 5 \times 7 = 2520$

Check: $12 \times 2520 = 30240 = 360 \times 84$ — the identity $\gcd(a,b) \times \operatorname{lcm}(a,b) = a \times b$ always holds.

Why is this algorithm reliable? Because "taking the smaller/larger exponent" presupposes that **the factorization itself is unique**. If a number could be written two ways, the gcd and lcm would depend on who did the factoring — unique factorization is what licenses these formulas.

### 2. Counting Divisors: Add One to Each Exponent, Then Multiply

Write $n = p_1^{e_1}p_2^{e_2}\cdots p_k^{e_k}$. The number of divisors of $n$ is:

$$\tau(n) = (e_1+1)(e_2+1)\cdots(e_k+1)$$

For $360 = 2^3 \times 3^2 \times 5$: $\tau(360) = (3+1)(2+1)(1+1) = 24$.

Why (the multiplication principle): to write a divisor, the exponent of 2 may be chosen among $0,1,2,3$ (4 ways), the exponent of 3 has 3 choices, and the exponent of 5 has 2 — **independent choices, any combination**, giving $4 \times 3 \times 2 = 24$. The same idea also computes the **sum of divisors**: $\sigma(360) = (1+2+4+8)(1+3+9)(1+5) = 15 \times 13 \times 6 = 1170$.

### 3. Why Fractions Work: Reducing and Common Denominators

- **Reducing**: $\frac{8}{30} = \frac{4}{15}$, because $\gcd(8,30) = 2$. Unique factorization guarantees that **the simplest form is unique** — you cannot reduce to two different "simplest" fractions
- **Common denominators**: $\frac{1}{6} + \frac{1}{10}$ — the denominators are $6 = 2 \times 3$ and $10 = 2 \times 5$, so $\operatorname{lcm}(6,10) = 2 \times 3 \times 5 = 30$:

$$\frac{1}{6} + \frac{1}{10} = \frac{5}{30} + \frac{3}{30} = \frac{8}{30} = \frac{4}{15}$$

- **Why it is reliable**: two fractions are equal exactly when their cross products are equal, and after full reduction the prime factors of numerator and denominator are uniquely determined. If factorization were not unique, "simplest form" would not be unique either — and the world of fractions would fall apart

### 4. Cryptography: Correctness from Unique Factorization, Security from Hardness

In RSA, the public key is $n = p \times q$ ($p, q$ large primes); encryption is $c = m^e \bmod n$, and decryption needs the private key $d$. **Breaking RSA means factoring $n$** — and splitting a 2048-bit $n$ back into $p \times q$ would take today's fastest computers billions of years.

But RSA's *correctness* also rests on unique factorization: decryption relies on Euler's theorem $m^{\varphi(n)} \equiv 1 \pmod n$, and deriving $\varphi(n) = (p-1)(q-1)$ presupposes that the prime factorization of $n$ is **exactly** $p \times q$ — there is no other way to write it.

The world of **hashing** also leans on primes: hash tables use a prime number of buckets to avoid systematic collisions when keys share a factor with the table size, and many hash and pseudorandom algorithms take a prime as modulus — enjoying the clean property that a prime is coprime to everything else.

### 5. The Foundation of a Whole Building

Nearly every "divisibility" statement in number theory stands on unique factorization:

- Proving $\sqrt{2}$ irrational: suppose $\sqrt{2} = \frac{a}{b}$ in lowest terms; then $2b^2 = a^2$ — the exponent of 2 on the left is odd, on the right even, contradiction
- Congruences, Euler's totient, quadratic residues… all rest on "every integer has exactly one standard form"

---

**Behind this section**: unique factorization is a calculator — it turns properties of numbers into arithmetic on prime exponents. It gives everyday notions like "greatest common divisor," "number of divisors," and "simplest fraction" a definite answer, and gives cryptography a mathematical foundation it can rely on.
