## What Is Linear Algebra

Linear algebra is the mathematics of **vector spaces and linear transformations**. Its core question: when we stretch, rotate, or compress space, what stays the same?

### Vectors — More Than Just Arrows

A vector is an ordered pair (x, y), but its deepest meaning: **a point's position in space, starting from the origin.**

- Vector addition: translation
- Scalar multiplication: scaling
- Linear combination: representing any point using a few basis vectors

### Matrices — "Transformers" of Space

The product Ax means: **transform vector x to a new location.**

$$
\begin{bmatrix} a & b \\ c & d \end{bmatrix} \begin{bmatrix} x \\ y \end{bmatrix} = \begin{bmatrix} ax + by \\ cx + dy \end{bmatrix}
$$

Think of a matrix as a "space deformer" — the entire coordinate grid gets stretched, rotated, or sheared.

### Determinants — How Area Changes

For a 2×2 matrix, det(A) = ad - bc. Geometrically, it's the **area** of the parallelogram that the unit square becomes after the transformation.

- det(A) = 0 → the transformation flattens space into a line
- det(A) > 0 → orientation preserved
- det(A) < 0 → orientation flipped

### Eigenvalues and Eigenvectors — Directional Invariants

For a matrix A, if there exists a vector v such that Av = λv, then v is an **eigenvector** and λ is an **eigenvalue**.

Eigenvectors under A are only stretched/compressed (by λ), their **direction unchanged**. This reveals the transformation's essential structure.

### Applications

- **PageRank**: Google treats the entire web as a giant matrix, computing its principal eigenvector for search rankings
- **PCA**: Principal Component Analysis finds eigenvectors of the covariance matrix corresponding to the largest eigenvalues
- **Quantum mechanics**: The Schrödinger equation is an eigenvalue problem — energy levels are eigenvalues, orbitals are eigenvectors
- **3D graphics**: Rotation, projection, and perspective in game engines are all matrix multiplications
