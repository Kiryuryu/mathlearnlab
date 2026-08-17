## The History of Unique Factorization

"Every integer has exactly one prime-factor recipe" — this theorem looks self-evident today, but it was not always clear. It was argued by Euclid, extended by Gauss, and then suffered a dramatic failure and rescue in the 19th century. The thread running through the story: **wherever the boundary of "number" lies, unique factorization holds exactly there**.

### 3rd Century BCE: Euclid's Argument

Book VII of the *Elements* defines prime and composite numbers and gives the Euclidean algorithm; Book IX completes the proof of unique factorization, in two steps:

1. **Euclid's lemma** (Book VII, Proposition 30): if a prime $p$ divides a product $ab$, then $p$ divides $a$ or $b$
2. **Uniqueness** (Book IX, Proposition 14): if a number is "least measured" by certain primes, it is measured by no other primes

The idea: suppose $n$ has two prime factorizations; use the lemma to cancel common prime factors one by one — any prime appearing in the left factorization must also appear on the right, and the two lists coincide in the end. Euclid wrote in the language of lengths and "measures," but the logic is identical to today's textbooks.

### Early 19th Century: Gauss Opens a New World

The *Disquisitiones Arithmeticae* (1801) founded modern number theory. In 1832, Gauss studied the **Gaussian integers** $\mathbb{Z}[i] = \{a + bi : a, b \in \mathbb{Z}\}$ and found something deeply suggestive:

- In $\mathbb{Z}[i]$, **unique factorization still holds** — e.g., $5 = (2+i)(2-i)$ (in fact it is even a Euclidean domain, stronger than unique factorization)
- But the identity of "prime" changed: $5$ is irreducible in $\mathbb{Z}$ yet factors in $\mathbb{Z}[i]$!

The lesson: **"prime" is not an absolute property of a number, but a property relative to a number system**. Change the system and you change the atoms.

### Mid-19th Century: Failure and Kummer's "Ideal Numbers"

In the 1840s, Kummer studied cyclotomic integers $\mathbb{Z}[\zeta_p]$ ($\zeta_p$ a primitive $p$-th root of unity) to attack Fermat's Last Theorem — and hit a wall: for some $p$ (e.g., 37, 59, 67), **unique factorization fails**.

The simplest example of failure lives in $\mathbb{Z}[\sqrt{-5}]$:

$$6 = 2 \times 3 = (1+\sqrt{-5})(1-\sqrt{-5})$$

All four factors are irreducible (checkable with the norm $N(a+b\sqrt{-5}) = a^2 + 5b^2$), yet 6 has two decompositions. Kummer did not give up: he invented **ideal prime factors** — in the world of "ideals," the numbers can be split properly and unique factorization is restored. In 1871 Dedekind formalized "ideal numbers" as **ideals** and defined the **class number** — the class number is 1 exactly when unique factorization holds, and the larger it is, the more severely uniqueness fails.

### Why the Boundary of "Number" Decides Uniqueness

| Number system | Unique factorization? |
|---|---|
| Ordinary integers $\mathbb{Z}$ | ✅ holds |
| Gaussian integers $\mathbb{Z}[i]$ | ✅ holds |
| $\mathbb{Z}[\sqrt{-5}]$ | ❌ $6 = 2\times3 = (1+\sqrt{-5})(1-\sqrt{-5})$ |
| Ideals (Dedekind) | ✅ every ideal factors uniquely into prime ideals |

> Extend the boundary one step and the theorem may fall; replace "number" with "ideal" and the building stands again. The history of unique factorization reminds us: **the territory of a mathematical theorem is decided by the objects we choose**.
