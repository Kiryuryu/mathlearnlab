## Series Applications

### 1. Computing π

The Leibniz series gives us an infinite sum for π:

$$\frac{\pi}{4} = 1 - \frac{1}{3} + \frac{1}{5} - \frac{1}{7} + \frac{1}{9} - \cdots$$

This converges very slowly, but it proves that π can be expressed as an infinite sum of rational numbers.

A much faster series (discovered by Ramanujan):

$$\frac{1}{\pi} = \frac{2\sqrt{2}}{9801} \sum_{n=0}^\infty \frac{(4n)! (1103 + 26390n)}{(n!)^4 396^{4n}}$$

### 2. Function Approximation

Any function can be approximated by its Taylor series:

$$f(x) = \sum_{n=0}^\infty \frac{f^{(n)}(a)}{n!} (x-a)^n$$

For example, $e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots$

### 3. Fourier Analysis

Periodic functions can be decomposed into sine and cosine waves:

$$f(x) = a_0 + \sum_{n=1}^\infty a_n \cos(nx) + b_n \sin(nx)$$

This is the foundation of:
- **MP3 compression** — remove inaudible frequencies
- **JPEG compression** — separate high and low frequency components
- **Wireless communication** — 5G uses OFDM (Orthogonal Frequency Division Multiplexing)
- **Medical imaging** — MRI signal processing
