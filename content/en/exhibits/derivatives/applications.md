## Applications of Derivatives

### 1. Gradient Descent — The Engine of AI

Every neural network trains on one derivative calculation: the gradient. For a loss function L(w), the gradient ∇L(w) points in the direction of steepest increase. Moving parameters in the opposite direction:

$$w_{\text{new}} = w - \eta \nabla L(w)$$

ChatGPT, Stable Diffusion, AlphaFold — all these AI models are essentially computing derivatives and descending gradients.

### 2. Marginal Analysis in Economics

"Marginal cost" is the derivative of the cost function. If C(q) is the cost of producing q units, C'(q) is the additional cost of one more unit. Firms use this to set optimal production levels.

### 3. The Brachistochrone Problem

A bead slides under gravity from A to B (not vertically aligned). What shape of wire gives the shortest travel time? Intuition says a straight line — but the answer is a **cycloid**. This problem birthed the calculus of variations.

### 4. Newton's Method

Solving f(x) = 0 iteratively:

$$x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}$$

Starting from any initial guess, it converges quadratically to the root. This is the core algorithm computers use for nonlinear equations.

### 5. Snell's Law in Optics

Light bends when entering water. Snell's law follows from Fermat's principle: light takes the path of least time — a derivative = 0 (extremum) problem. Derivatives find light's path.
