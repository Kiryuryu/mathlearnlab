## Eigenvalues — Invariant Directions

Under a matrix, space is stretched, rotated, and squeezed, and the directions of most vectors twist away. But amid all this variation, **some directions never change** — they are merely lengthened or shortened, their directions fixed. These "invariant directions" are the eigenvectors, and the essence of linear algebra often hides within them.

### Eigenvectors and Eigenvalues

> $$A\mathbf{v} = \lambda\mathbf{v}$$

If the matrix $A$ only stretches/compresses the vector $\mathbf{v}$ by a factor $\lambda$ without changing its direction, then $\mathbf{v}$ is an **eigenvector** and $\lambda$ an **eigenvalue**.

Note: $\lambda$ may be negative (direction reversed) or 0 (vector crushed to the zero vector), but $\mathbf{v}$ must be nonzero.

### Geometric Meaning: The "Principal Axes" of a Transformation

Most vectors in the grid change direction after the deformation, but **eigenvectors do not** — they reveal the transformation's "principal axes," the key to understanding its essential structure:

- A pure scaling matrix $\begin{bmatrix}2 & 0 \\ 0 & 3\end{bmatrix}$ has the basis vectors as its eigenvectors
- The eigenvalues of a rotation matrix are usually complex (a rotation has no real invariant direction)
- The larger the eigenvalue, the stronger the "expansion" along that direction

### Computation: Three Steps

To find the eigenvalues and eigenvectors of $A$:

1. Solve the characteristic equation $|A - \lambda I| = 0$ → eigenvalues $\lambda$
2. For each $\lambda$, solve the homogeneous equation $(A-\lambda I)v = 0$ → eigenvectors
3. The number of eigenvectors ≤ the multiplicity of the eigenvalue; $A$ is diagonalizable ⇔ each eigenvalue has enough linearly independent eigenvectors

### Diagonalization: The Art of Simplification

If $A$ has $n$ linearly independent eigenvectors, then:

$$A = PDP^{-1}$$

Decompose a complicated matrix into "eigenvectors ($P$) + scaling ($D$) + undoing ($P^{-1}$)". **Every complex transformation is, at heart, scaling along a few fixed directions** — this is the power of eigenvalues.

---

**From here:** see [Applications](#applications) on how PageRank ranks web pages with a principal eigenvector and why quantum energy levels are an eigenvalue problem; in [Interactive](#explore), watch the invariant directions of a matrix transformation with your own eyes.

→ [Continue reading: Linear Algebra — Transformations of Space](/exhibit/linear-algebra)
