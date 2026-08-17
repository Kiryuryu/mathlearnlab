## Congruence — The World of Modular Arithmetic

"What time is it 8 hours after 7 o'clock?" The answer is 3 o'clock — because a clock only cares about the remainder when you divide by 12. **Congruence** (modular arithmetic) turns this "only the remainder matters" habit of mind into a complete and powerful mathematics: many of the deepest results in number theory hide inside "the remainder after dividing by $m$."

### The Definition of Congruence

$$a \equiv b \pmod m \iff m \mid (a-b)$$

"$a$ and $b$ are congruent modulo $m$" means they leave the same remainder when divided by $m$. For example:

$$17 \equiv 5 \pmod{12}, \qquad 100 \equiv 1 \pmod{11}$$

Congruences can be added, subtracted, and multiplied just like equations — a small trick that simplifies calculations enormously.

### Fermat's Little Theorem: A Touchstone for Primes

> If $p$ is prime and $p \nmid a$, then $a^{p-1} \equiv 1 \pmod{p}$

This theorem offers an elegant tool for testing prime-like behavior and is the mathematical cornerstone of RSA cryptography. For example, $2^6 = 64 \equiv 1 \pmod 7$ ✓.

### Modular Inverses and Euclid

Solving $ax \equiv 1 \pmod m$ means finding the modular inverse of $a$:

$$a^{-1} \text{ exists} \iff \gcd(a, m) = 1$$

The **extended Euclidean algorithm** finds it: it produces $x, y$ such that $ax + my = \gcd(a,m) = 1$, and $x$ is exactly the modular inverse.

### Euler's Totient and Euler's Theorem

$$\varphi(n) = \text{the number of integers from } 1 \text{ to } n \text{ coprime to } n$$

- If $p$ is prime: $\varphi(p) = p-1$; and $\varphi(p^k) = p^k - p^{k-1}$
- **Euler's theorem** (the generalization of Fermat's little theorem): $\gcd(a,n)=1 \Rightarrow a^{\varphi(n)} \equiv 1 \pmod n$

Euler's totient function lies at the heart of RSA encryption — generating a key depends on computing $\varphi(n)$.

---

**From here:** see [Applications](#applications) on how congruences guard online transactions and generate random numbers; in [Interactive](#explore), find modular inverses by hand and verify Fermat's little theorem yourself.

→ [Continue reading: Prime Distribution — Order Within Randomness](/exhibit/prime-distribution)
