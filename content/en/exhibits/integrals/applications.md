## Applications of Integrals

### 1. Probability and Statistics

Under the normal distribution N(μ, σ²), the integral from a to b of the PDF equals the probability the variable falls in that interval. But there's no elementary antiderivative — only numerical integration. All hypothesis tests and confidence intervals rely on such integrals.

### 2. Arc Length

The length of a suspension bridge's main cable isn't the straight-line distance — it follows a catenary curve. The arc length formula:

$$L = \int_a^b \sqrt{1 + [f'(x)]^2} \, dx$$

### 3. Volumes of Revolution

A function rotated around the x-axis sweeps out a solid. Its volume:

$$V = \pi \int_a^b [f(x)]^2 \, dx$$

Ancient potters shaping clay on a wheel used this same principle — radius ρ(z) at height z, volume is the integral of cross-sectional areas.

### 4. Center of Mass and Moment of Inertia

An airplane's center of mass and moment of inertia determine its flight stability. Both are integrals: center of mass is a position-weighted integral, moment of inertia is a distance-squared-weighted integral.

### 5. Signal Energy

A signal f(t) has total energy = ∫|f(t)|² dt. In communications, we want signal energy concentrated in the target frequency band — this is why Fourier transforms use window functions.

### 6. Entropy in Thermodynamics

Entropy change dS = dQ/T. Total entropy change over a process is an integral: $$\Delta S = \int \frac{dQ}{T}$$. The universe's entropy always increases — perhaps physics's deepest law, written as an integral.
