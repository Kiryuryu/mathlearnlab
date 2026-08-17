## The History of Prime Distribution

### 3rd Century BCE: Euclid's First Lesson in Infinity

Book IX of the *Elements* contains one of the most celebrated proofs in mathematics: **there are infinitely many primes**. Suppose the primes were only $p_1,p_2,\ldots,p_k$; construct

$$N=p_1p_2\cdots p_k+1$$

Dividing $N$ by any $p_i$ leaves remainder 1, so $N$ is either prime itself or carries a brand-new prime factor — a contradiction. This is humanity's first serious encounter with infinity, and the proof is still ranked among the most elegant in mathematics.

### 18th Century: Euler Turns "Counts" into "Functions"

In 1737 Euler proved that the sum $\sum_p \frac{1}{p}$ of prime reciprocals diverges — primes grow ever sparser, yet **sparse enough that the sum of their reciprocals still flies to infinity**. He also wrote down the miracle linking addition with multiplication:

$$\sum_{n=1}^{\infty}\frac{1}{n^s}=\prod_{p}\frac{1}{1-p^{-s}}$$

All primes are encoded into a single function — the seed of the Riemann zeta function. Euler also found that $n^2+n+41$ is prime for $n=0,1,\ldots,39$, failing only at $n=40$, where it equals $41^2$.

### 18th–19th Century: Gauss and Legendre's Guess

In 1792, 15-year-old Gauss scribbled the conjecture $\pi(x)\approx x/\ln x$ in the margin of a prime table; Legendre published it independently in 1798. **Both guessed right, and neither could prove it.** Gauss also secretly used the more refined "logarithmic integral" $\operatorname{Li}(x)=\int_2^x\frac{dt}{\ln t}$ to check his prime tables, convinced it hugged $\pi(x)$ more closely than $x/\ln x$ — a judgment it would take nearly two centuries of computation to fully confirm.

### 1859: Riemann's Eight Pages

Riemann's "On the Number of Primes Less Than a Given Magnitude" is only 8 pages long, yet it opens an entire era: he analytically continues the zeta function to the complex plane, states the **Riemann hypothesis** (all nontrivial zeros lie on the line $\operatorname{Re}(s)=\frac{1}{2}$), and gives an "explicit formula" that reconstructs the distribution of primes from the positions of those zeros. **The zeros are tuning forks; the primes, their echo.**

### 1896: Hadamard and de la Vallée Poussin — A Century of Waiting

In 1896, Hadamard and de la Vallée Poussin **independently proved** the prime number theorem $\pi(x)\sim\frac{x}{\ln x}$ — Gauss's guess waited a full 104 years for its verdict, and the thread between the "random feel" of primes and the certainty of the logarithm was finally, formally connected. In 1949, Selberg and Erdős gave an "elementary" proof avoiding complex analysis.

### 2013: Yitang Zhang and the 70 Million

The twin prime conjecture (are there infinitely many prime pairs differing by 2?) had seemed untouchable. In 2013, **Yitang Zhang**, an obscure lecturer at the University of New Hampshire, proved that **infinitely many prime pairs differ by less than 70 million**. Within months, the Polymath project pushed the bound down — 4680, then 600… finally **246**. The 24-page paper went to the *Annals of Mathematics*; referees initially doubted it, yet it was accepted within three months — from submission to rewriting mathematical history in a matter of months.

> From Euclid's contradiction to Riemann's zeros, from 1896 to 2013 — every milestone in prime distribution is a record of humanity's negotiations with randomness.
