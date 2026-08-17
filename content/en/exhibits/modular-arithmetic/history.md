## The History of Congruence: From "Counting in Threes" to RSA

### 3rd–5th Century CE: The "Unknown Number of Things" in the Sunzi Suanjing

> There is an unknown number of things. Counting by threes leaves 2, counting by fives leaves 3, counting by sevens leaves 2. How many things are there?

In today's language, this is the system of congruences $x\equiv2\pmod3$, $x\equiv3\pmod5$, $x\equiv2\pmod7$ — the answer is 23, one of the earliest recorded systems of congruences in the world. The name **Chinese remainder theorem** comes directly from this tradition: in 1247, Qin Jiushao's *Mathematical Treatise in Nine Sections* gave a systematic method (the "Great Extension" procedure, 大衍求一术), roughly 500 years before comparable European work. Around the same era, Indian mathematicians (Aryabhata and Brahmagupta) developed the *kuttaka* ("pulverizer") algorithm for solving linear congruences; even earlier, Euclid's *Elements*, Book VII, recorded the **Euclidean algorithm** — still the foundation for modular inverses today.

### 17th Century: Fermat and the Margin

In 1621, a Latin translation of Diophantus's *Arithmetica* appeared, and Europe rediscovered number theory — it was in this book's margins that Fermat wrote "I have discovered a truly marvelous proof, which this margin is too narrow to contain." In 1640 he announced Fermat's little theorem in a letter:

$$a^{p-1} \equiv 1 \pmod p \quad (p \text{ prime, and } p \nmid a)$$

As usual, Fermat stated the result without a proof; it had to wait a century, for Euler.

### 18th Century: Euler Turns "Remainders" into a Subject

Euler proved Fermat's little theorem and generalized it into **Euler's theorem** $a^{\varphi(n)}\equiv1\pmod n$, introducing the totient $\varphi$; he articulated the notion of congruence clearly, turning "the remainder after dividing by $m$" into an object that can be manipulated like a number. The same century produced **Wilson's theorem** ($p$ prime $\iff (p-1)!\equiv-1\pmod p$) — conjectured by Wilson, proved by Lagrange.

### 19th Century: Gauss's Disquisitiones

In 1801, the 24-year-old Gauss published the *Disquisitiones Arithmeticae*, the founding work of modern number theory. He formally introduced the notation $a\equiv b\pmod m$ and built congruence theory systematically — of the book's seven chapters, the first three are devoted to congruences. Congruence became the standard language of number theory and remains so. He also gave the first complete proof of **quadratic reciprocity** (which he called the "golden theorem") and a full proof and generalization of the Chinese remainder theorem.

### 20th Century to Today

- **1976**: Diffie–Hellman key exchange — modular exponentiation became the star of cryptography
- **1977**: RSA encryption published; modular inverses and powers guard every online transaction
- **1979**: Shamir's secret sharing uses the Chinese remainder theorem to "split" a secret among many people
- **1994**: Shor's algorithm showed quantum computers might factor large numbers quickly — the mathematical arms race continues

> From the "unknown number of things" in the *Sunzi Suanjing* to the RSA guarding the internet — congruence has traveled eighteen centuries, from a "counting game" to the gatekeeper of the digital world.
