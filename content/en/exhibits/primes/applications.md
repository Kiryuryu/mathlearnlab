## Applications of Number Theory

### 1. RSA Encryption — Guarding Every Online Transaction

When you pay online, your browser and the server exchange RSA-encrypted messages. Its principle rests on a huge asymmetry:

- **Choose two large primes** $p$, $q$, compute $n = p \times q$
- Public key $(n, e)$ is shared; private key $d$ stays secret
- Encryption is easy: $c = m^e \bmod n$; decryption needs the private key $d$
- **Breaking it = factoring $n$** — but factoring a 2048-bit $n$ into $p \times q$ would take today's fastest computers billions of years

The larger the primes, the safer the cipher. This is the flip side of "primes grow sparse": finding large primes is easy, factoring large composites is brutally hard.

### 2. Primality Testing and Hashing

- **Primality testing**: banks and encryption systems need to quickly decide whether a random large number is prime; Miller–Rabin and friends do it in milliseconds
- **Hash tables**: bucket counts are often prime, spreading data more evenly and reducing collisions
- **Pseudorandom numbers**: linear congruential generators rely on modular arithmetic with primes

### 3. Perfect Numbers and Mersenne Primes

$6 = 1+2+3$, $28 = 1+2+4+7+14$ — a **perfect number** equals the sum of its proper divisors. Euclid proved that even perfect numbers correspond one-to-one with Mersenne primes $2^p-1$. The largest known primes are almost all Mersenne primes (found by the GIMPS distributed project); the 2024 record exceeds 100 million digits.

### 4. Goldbach's Conjecture and the Riemann Hypothesis

- **Goldbach's conjecture**: every even number greater than 2 is the sum of two primes. Verified astronomically far, yet unproven (Chen proved "1+2")
- **The Riemann hypothesis**: a conjecture about the zeros of the $\zeta$ function, widely regarded as the most important open problem in mathematics. Its proof would pin down the exact distribution of primes

### 5. A Conversation with the Universe

In 1974, the Arecibo radio telescope sent a message into space containing the prime sequence 1, 3, 5, 7, 11… — because any alien civilization, whatever its language and culture, would recognize this mathematical pattern.

---

**Behind all of these**: primes combine "unique factorization + sparse distribution + fast detection" — common enough to be everywhere, scarce enough to be the bedrock of cryptography.
