## Explore Eigenvalues

### Try It 1: Eigenvalues of a Diagonal Matrix

The matrix $A = \begin{bmatrix}2 & 0 \\ 0 & 3\end{bmatrix}$. What are its eigenvalues and eigenvectors?

<details>
<summary>Answer</summary>
The eigenvalues are just the diagonal entries: $\lambda_1 = 2$, $\lambda_2 = 3$. The corresponding eigenvectors are $(1,0)$ (stretched by 2, direction unchanged) and $(0,1)$ (stretched by 3). The eigenvalues of a diagonal matrix can be read off at a glance.
</details>

### Try It 2: Verifying an Eigenvalue

Verify that $\lambda = 5$ is an eigenvalue of $A = \begin{bmatrix}4 & 1 \\ 2 & 3\end{bmatrix}$.

<details>
<summary>Answer</summary>
Compute the characteristic polynomial: $|A - \lambda I| = \begin{vmatrix}4-\lambda & 1 \\ 2 & 3-\lambda\end{vmatrix} = (4-\lambda)(3-\lambda) - 2 = \lambda^2 - 7\lambda + 10 = (\lambda-5)(\lambda-2)$. So the eigenvalues are 5 and 2. Check: $\det(A) = 12-2=10 = 5\times 2$ ✓, $\text{tr}(A) = 7 = 5+2$ ✓.
</details>

### Try It 3: Eigenvalues of a Rotation Matrix

What are the eigenvalues of $R = \begin{bmatrix}0 & -1 \\ 1 & 0\end{bmatrix}$ (a 90° rotation)?

<details>
<summary>Answer</summary>
$|R - \lambda I| = \lambda^2 + 1 = 0$, so $\lambda = \pm i$ — purely imaginary! A 90° rotation has no real vector with unchanged direction (every vector turns 90°), so its eigenvalues are the complex numbers $e^{\pm i\pi/2}$. This reveals that the "essence" of a rotation lives in the complex world.
</details>

### Try It 4: The Convergence of Powers

The matrix $A = \begin{bmatrix}0.5 & 0 \\ 0 & 0.9\end{bmatrix}$. What happens as $A^n$ is iterated many times?

<details>
<summary>Answer</summary>
$A^n = \begin{bmatrix}0.5^n & 0 \\ 0 & 0.9^n\end{bmatrix}$. Both eigenvalues are less than 1, so $A^n \to 0$ — the system converges. Eigenvalues all less than 1 ⇔ the system decays stably. This is the intuitive picture of "eigenvalues determine the long-term behavior of a dynamical system."
</details>
