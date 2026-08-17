## Key Insights: How to Think About Eigenvalues

### 1. The Eigenproblem in Three Steps

To find the eigenvalues and eigenvectors of $A$:

1. Solve the characteristic equation $|A - \lambda I| = 0$ → eigenvalues $\lambda$
2. For each $\lambda$, solve the homogeneous equation $(A-\lambda I)v = 0$ → eigenvectors
3. The number of eigenvectors ≤ the multiplicity of the eigenvalue; $A$ is diagonalizable ⇔ each eigenvalue has enough linearly independent eigenvectors

### 2. Spot the Eigenvalues of Special Matrices Quickly

- **Diagonal matrix**: eigenvalues = the diagonal entries
- **Triangular matrix**: eigenvalues = the diagonal entries
- **Symmetric matrix**: all eigenvalues are real
- **Identity matrix**: all eigenvalues are 1 (every nonzero vector is an eigenvector)

### 3. Check with Trace and Determinant

$$\text{tr}(A) = \lambda_1 + \cdots + \lambda_n, \qquad \det(A) = \lambda_1 \cdots \lambda_n$$

Two conservation laws for verification: the sum of all eigenvalues is the trace; the product is the determinant.

### 4. Practical Criteria for Eigenvalues

- Computing $A^n$: after diagonalization $A^n = PD^nP^{-1}$, exponentiate only the diagonal entries
- Judging stability: the spectral radius (largest eigenvalue modulus) decides whether a dynamical system converges or diverges
- Invertibility: $A$ is invertible ⇔ 0 is not an eigenvalue of $A$

### Common Pitfalls

1. **Forgetting that eigenvectors must be nonzero**: an eigenvector can never be the zero vector
2. **Counting repeated eigenvalues**: algebraic multiplicity (the power in the characteristic equation) ≠ geometric multiplicity (the number of linearly independent eigenvectors)
3. **The diagonalization condition**: an $n\times n$ matrix is diagonalizable ⇔ it has $n$ linearly independent eigenvectors — repeated eigenvalues can break it
4. **Real matrices need not have real eigenvalues**: the eigenvalues of a rotation matrix are the complex numbers $e^{\pm i\theta}$
