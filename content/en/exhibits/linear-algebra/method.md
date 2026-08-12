## Key Insights: How to Think About Linear Algebra

### 1. First Decide: Linear or Not?

A linear system satisfies two laws: closed under addition and under scalar multiplication. Seeing $Ax=b$, matrices, or vector spaces means linearity. **Linearity means superposition — and matrices handle it uniformly.**

### 2. Solving Systems: Elimination vs. Inverse Matrix

Two perspectives on solving $Ax=b$:

- **Elimination**: apply row operations to the augmented matrix, reduce to echelon form → read off the solution
- **Inverse matrix**: $x = A^{-1}b$ (only when $A$ is invertible, i.e. det ≠ 0)

In practice elimination is more common (numerically stable); the inverse suits theoretical derivation.

### 3. Computing Determinants

$$|A| = ad - bc \quad (2\times2)$$

For higher-order determinants, simplify with **elementary operations**:
- Multiplying a row by $k$ multiplies the determinant by $k$
- Swapping two rows changes its sign
- Adding a multiple of one row to another leaves it unchanged
- Reduce to upper triangular form → the determinant is the product of the diagonal entries

### 4. Eigenproblems in Three Steps

To find eigenvalues and eigenvectors of $A$:

1. Solve the characteristic equation $|A - \lambda I| = 0$ → eigenvalues $\lambda$
2. For each $\lambda$, solve the homogeneous system $(A-\lambda I)v = 0$ → eigenvectors
3. The number of eigenvectors ≤ the multiplicity of the eigenvalue; $A$ is diagonalizable ⇔ each eigenvalue has enough linearly independent eigenvectors

### 5. Rank and Free Variables

The **rank** of a matrix is the maximum number of linearly independent rows (or columns):
- Full rank (rank = n): a unique solution
- Rank deficient: infinitely many solutions, with $n - \text{rank}$ free variables

### 6. Vector Spaces and Bases

A set of vectors forms a basis if it is linearly independent and spans the space. Equivalently, $n$ vectors in $n$ dimensions are linearly independent ⇔ the matrix they form has nonzero determinant.

### 7. Orthogonality and Projection

Orthogonal vectors have dot product 0. The projection formula:

$$\text{proj}_u(v) = \frac{v\cdot u}{u\cdot u}\,u$$

Least squares, orthogonal decomposition, and Gram–Schmidt are all extensions — **projection decomposes a vector onto the direction that keeps the most information.**

### Common Pitfalls

1. **Matrix multiplication is not commutative**: $AB \neq BA$ — the order matters
2. **Confusing row and column operations in elimination**: only row operations are allowed when solving
3. **Forgetting the zero vector**: an eigenvector must be nonzero
4. **Getting the invertibility conditions wrong**: invertible ⇔ det ≠ 0 ⇔ full rank ⇔ columns linearly independent
