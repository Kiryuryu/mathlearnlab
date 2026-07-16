## Beauty in Derivatives

### Taylor Series — Any Function Is a Polynomial

$$f(x) = f(a) + f'(a)(x-a) + \frac{f''(a)}{2!}(x-a)^2 + \frac{f'''(a)}{3!}(x-a)^3 + \cdots$$

If infinitely differentiable, any function can be written as an infinite polynomial. sin(x), cos(x), e^x, arctan(x) — each has a "Taylor face."

The most famous expansions:

$$e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots$$

$$\sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \frac{x^7}{7!} + \cdots$$

$$\cos x = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \frac{x^6}{6!} + \cdots$$

### Euler's Identity via Taylor

Substitute ix into the expansion of e^x:

$$e^{ix} = 1 + ix - \frac{x^2}{2!} - i\frac{x^3}{3!} + \frac{x^4}{4!} + i\frac{x^5}{5!} - \cdots$$

Grouping real and imaginary parts yields: $$e^{ix} = \cos x + i\sin x$$

Set x = π: $$e^{i\pi} + 1 = 0$$

Five fundamental constants linked in one equation. Feynman called it "the most beautiful formula in mathematics."

### The Catenary

A uniform chain hanging from two endpoints forms a catenary — hyperbolic cosine:

$$y = a\cosh(x/a) = a\frac{e^{x/a} + e^{-x/a}}{2}$$

It looks like a parabola, but isn't. Arch bridges and power lines follow this shape — under gravity, it's the configuration of minimum potential energy.

### L'Hôpital's Rule

$$\lim_{x \to a} \frac{f(x)}{g(x)} = \lim_{x \to a} \frac{f'(x)}{g'(x)}$$

For 0/0 or ∞/∞ forms, replace the ratio of functions with the ratio of their derivatives. The beauty: a problem becomes simpler by moving to a more complex object (the derivative).
