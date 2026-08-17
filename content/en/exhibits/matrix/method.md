## Key Insights: How to Think About Matrices

### 1. Solving Systems: Elimination vs. Inverse Matrix

Two perspectives on solving $Ax=b$:

- **Elimination**: apply elementary row operations to the augmented matrix, reduce to echelon form → read off the solution (numerically stable; what is actually used)
- **Inverse matrix**: $x = A^{-1}b$ (only when $A$ is invertible, i.e. det ≠ 0)

### 2. Strategies for Computing Determinants

$$|A| = ad - bc \quad (2\times2)$$

For higher-order determinants, prefer simplifying with **elementary operations**:
- Multiplying a row by $k$ multiplies the determinant by $k$
- Swapping two rows changes its sign
- Adding a multiple of one row to another leaves it unchanged
- Reduce to upper triangular form → the determinant is the product of the diagonal entries

### 3. Rank and Invertibility

The **rank** of a matrix is the maximum number of linearly independent rows (or columns):
- Full rank (rank = n): $Ax=b$ has a unique solution, $A$ is invertible
- Rank deficient: infinitely many solutions or none; the number of free variables = $n - \text{rank}$

Invertible ⇔ det ≠ 0 ⇔ full rank ⇔ columns linearly independent.

### 4. The Order of Matrix Multiplication

$AB$ means "first do $B$, then do $A$" — **matrix multiplication is not commutative**: $AB \neq BA$. But it is associative: $(AB)C = A(BC)$, so you may group factors to minimize computation.

### Common Pitfalls

1. **Matrix multiplication is not commutative**: $AB \neq BA$ — the order cannot be changed
2. **Confusing row and column operations in elimination**: only row operations are allowed when solving
3. **Getting the invertibility condition wrong**: invertible ⇔ det ≠ 0 ⇔ full rank ⇔ columns linearly independent
4. **Treating $AB = 0$ as $A=0$ or $B=0$**: matrix multiplication has no "zero-divisor" property — $AB=0$ does not mean either factor is zero
