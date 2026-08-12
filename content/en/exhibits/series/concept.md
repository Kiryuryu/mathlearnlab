## Infinite Series — The Puzzle of Infinity

Cut a cake in half, then half again… if you eat every piece, how much do you get in total? The answer is the whole cake: $\frac12+\frac14+\frac18+\cdots = 1$. **Infinitely many numbers can add to a finite result.** Series study when such infinite sums converge, what they converge to, and how they approximate complicated functions.

### Convergence: The Limit of Partial Sums

Whether $\sum_{n=1}^{\infty} a_n$ converges is decided by the **partial sums** $S_N = a_1 + \cdots + a_N$:

> A series converges ⇔ its partial-sum sequence $\{S_N\}$ has a limit.

Note that $a_n \to 0$ is a **necessary but not sufficient** condition — the harmonic series $\sum \frac1n$ has terms tending to $0$ yet diverges. For positive terms, four weapons decide convergence:

| Test | Idea |
|------|------|
| **Comparison** | compare with a known series, $a_n \le Cb_n$ |
| **Ratio** | $\lim \left|\frac{a_{n+1}}{a_n}\right| = \rho < 1$ converges |
| **Root** | $\lim \sqrt[n]{|a_n|} = \rho < 1$ converges |
| **Integral** | compare with an improper integral $\int_1^\infty f(x)\,dx$ |

### Power Series: A Function Inside Its Radius

$$f(x) = \sum_{n=0}^{\infty} c_n(x-a)^n$$

Every power series has a **radius of convergence** $R$: absolutely convergent for $|x-a| < R$, divergent for $|x-a| > R$, and requiring separate checks at $|x-a| = R$. Inside its convergence domain, this infinite polynomial is completely a function — the Taylor series $f(x)=\sum \frac{f^{(n)}(a)}{n!}(x-a)^n$ is its special case, approximating a function point by point with polynomials.

### Fourier Series: Sculpting Any Periodic Function with Sines

$$f(x) = \frac{a_0}{2} + \sum_{n=1}^{\infty}\left[a_n\cos(nx) + b_n\sin(nx)\right]$$

Any "reasonable" periodic function can be written as a sum of sine and cosine waves at different frequencies. With each added harmonic, the sum approaches the target waveform — but at a discontinuity a persistent overshoot of about **9%** never disappears, no matter how many terms you add: the **Gibbs phenomenon**.

This is the mathematical foundation of signal processing, image compression, and sound synthesis.

---

**From here:** see [Applications](#applications) on Fourier transforms compressing photos and series approximating π; in [Interactive](#explore), drag the harmonic-count slider and sculpt a square wave out of sines.

→ [Continue reading: Multivariable Calculus — From Plane to Space](/exhibit/multivariable)
