## Interactive: The Intuition Lab of Complex Analysis

### Try It 1: The Cycle of Powers of i

Compute $i^0, i^1, i^2, i^3, i^4$. What pattern do you see?

<details>
<summary>Answer</summary>
$i^0 = 1$, $i^1 = i$, $i^2 = -1$, $i^3 = -i$, $i^4 = 1$. Then the cycle repeats every 4: $1, i, -1, -i$. Geometrically, multiplying by $i$ is a 90° counterclockwise rotation — you circle the unit circle in the complex plane. That is why "multiplication by $i$ is rotation."
</details>

### Try It 2: Evaluating Euler's Formula

Use $e^{i\theta} = \cos\theta + i\sin\theta$ to compute $e^{i\pi/2}$ and $e^{i\pi}$, then verify $e^{i\pi} + 1 = 0$.

<details>
<summary>Answer</summary>
$e^{i\pi/2} = \cos(\pi/2) + i\sin(\pi/2) = 0 + i\cdot 1 = i$. So $e^{i\pi/2} = i$ — multiplying by $i$ and by $e^{i\pi/2}$ are the same act (a 90° rotation). $e^{i\pi} = \cos\pi + i\sin\pi = -1 + 0i = -1$, hence $e^{i\pi} + 1 = 0$ ✓. On the complex plane, the exponential "spirals forward"; at $\theta=\pi$ it lands exactly on $-1$.
</details>

### Try It 3: The Singularity of 1/(z−1)

At which point is $f(z) = \frac{1}{z-1}$ not analytic? What kind of singularity is it?

<details>
<summary>Answer</summary>
At $z=1$ the denominator vanishes and $f$ is not analytic. It is a **simple pole** (order 1): the Laurent expansion $f(z) = \frac{1}{z-1}$ has a single negative power, with residue $\mathrm{Res}(f, 1) = \lim_{z\to 1}(z-1)\cdot\frac{1}{z-1} = 1$. So $\oint_{|z-1|=r}\frac{dz}{z-1} = 2\pi i \cdot 1 = 2\pi i$ — the integral around a pole always equals $2\pi i$ times the residue.
</details>

### Try It 4: The Residue Theorem Computes a Real Integral

Use the residue theorem to compute $\int_{-\infty}^{\infty} \frac{dx}{1+x^2}$.

<details>
<summary>Answer</summary>
Consider the upper-half-plane contour (real axis $[-R,R]$ + upper semicircle). The function $f(z)=\frac{1}{1+z^2}=\frac{1}{(z+i)(z-i)}$ has only the pole $z=i$ (a simple pole) in the upper half-plane. Residue: $\mathrm{Res}(f,i) = \lim_{z\to i}(z-i)\frac{1}{(z-i)(z+i)} = \frac{1}{2i}$. By the residue theorem, $\oint f = 2\pi i \cdot \frac{1}{2i} = \pi$. Letting $R\to\infty$, the arc contribution vanishes, so $\int_{-\infty}^{\infty}\frac{dx}{1+x^2} = \pi$ ✓. An "infinite-interval" real integral, obtained from a single point ($z=i$) on the complex plane.
</details>
