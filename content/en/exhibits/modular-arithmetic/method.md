## Key Insights: A Toolbox for Congruence Problems

### 1. Learn to "Fold" First: The Four Operations

- Addition, subtraction, and multiplication can all be done "reduce first, then compute": $(a+b)\bmod m=((a\bmod m)+(b\bmod m))\bmod m$ — **keep the numbers small, always**
- Negative numbers live in this ring too: $-1\equiv m-1\pmod m$
- The iron rule of division: from $ac\equiv bc\pmod m$ you may infer $a\equiv b$ only if $\gcd(c,m)=1$

### 2. Solving Linear Congruences $ax\equiv b\pmod m$

Let $d=\gcd(a,m)$: a solution exists $\iff d\mid b$. Reduce: divide both sides — and the modulus — by $d$ to get $a'x\equiv b'\pmod{m'}$ (coprime), then invert: $x\equiv a'^{-1}b'\pmod{m'}$; the number of solutions is exactly $d$.

Example: $3x\equiv4\pmod7$: $3^{-1}\equiv5$, so $x\equiv6$ ✓. Another: $4x\equiv8\pmod{12}$ has $d=4\mid8$; reducing gives $x\equiv2\pmod3$, i.e. 4 solutions $2,5,8,11$.

### 3. Three Weapons for Modular Inverses

- **Extended Euclidean algorithm**: solve $ax+my=1$; then $x$ is the inverse
- **Fermat's little theorem** ($p$ prime): $a^{-1}\equiv a^{p-2}\pmod p$
- **Euler's theorem** ($\gcd(a,n)=1$): $a^{-1}\equiv a^{\varphi(n)-1}\pmod n$

Example: from $13=2\times5+3$, $5=3+2$, $3=2+1$, back-substitution gives $1=2\times13-5\times5$, so $5^{-1}\equiv8\pmod{13}$ ✓.

### 4. The Chinese Remainder Theorem: Divide and Conquer

When $m_1,m_2$ are coprime, $x\equiv a_1\pmod{m_1}$ and $x\equiv a_2\pmod{m_2}$ have a unique solution modulo $m_1m_2$:

$$x\equiv a_1M_1M_1^{-1}+a_2M_2M_2^{-1}\pmod M, \qquad M=m_1m_2$$

where $M_i=M/m_i$ and $M_i^{-1}$ is its inverse mod $m_i$. The idea: break into small problems, then stitch the answers back. Example: for $x\equiv2\pmod3$, $x\equiv3\pmod5$: $5^{-1}\equiv2\pmod3$, $3^{-1}\equiv2\pmod5$, so $x\equiv8\pmod{15}$ ✓.

### 5. Fast Modular Exponentiation: Square-and-Multiply

Write the exponent in binary, square repeatedly and multiply on demand, reducing at every step — complexity only $O(\log e)$. Example: $3^{13}\bmod7$, $13=1101_2$, so $3^{13}=3^8\cdot3^4\cdot3^1\equiv2\cdot4\cdot3=24\equiv3\pmod7$ ✓.

### Common Pitfalls

1. Not checking solvability: no solution when $\gcd(a,m)\nmid b$
2. Cancelling without checking coprimality: $ac\equiv bc$ fails to give $a\equiv b$ when $\gcd(c,m)>1$
3. Misusing Fermat's little theorem: $p$ must be prime and $p\nmid a$
4. Forgetting coprimality in CRT: split into prime powers first when $m_1,m_2$ share factors
5. Not reducing intermediate results: letting numbers grow during fast exponentiation defeats the purpose
