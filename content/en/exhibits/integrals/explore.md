## Explore Integrals

### Try It 1: Odd Function Integral

Without computing, what's ∫[-1,1] x³ dx?

<details>
<summary>Answer</summary>
0! x³ is an odd function, so its integral over a symmetric interval is always 0. Geometrically: the negative area on the left and positive area on the right exactly cancel. One second to answer.
</details>

### Try It 2: Physics Intuition

An object moves at velocity v(t) = t² for 3 seconds. How far does it travel?

<details>
<summary>Answer</summary>
Displacement = ∫[0,3] t² dt = [t³/3]₀³ = 27/3 = 9 meters.
Physical meaning: the area under the velocity curve equals displacement.
</details>

### Try It 3: The Ungettable Antiderivative

Can you write an antiderivative for e^(-x²)?

<details>
<summary>Answer</summary>
No! e^(-x²) has no elementary antiderivative. But this doesn't stop us from computing the definite integral — ∫[-∞,∞] e^(-x²) dx = √π. Some integrals can only be evaluated numerically, but the results can be extremely precise.
</details>

### Try It 4: Archimedes' Insight

Approximate the area under y = x² from x = 0 to x = 1 using 10 rectangles. Which is more accurate: left endpoints, right endpoints, or midpoints?

<details>
<summary>Answer</summary>
Midpoints are typically far more accurate than left or right endpoints. With 10 midpoint rectangles approximating ∫[0,1] x² dx = 1/3, the midpoint sum gives 0.3325 (error 0.0008), while the right-endpoint sum gives 0.385 (error 0.052).
Try dragging the Riemann sum slider and watch!
</details>
