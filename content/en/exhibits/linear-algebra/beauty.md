## The Beauty of Linear Algebra

### Matrices: Poets of Space

A single 2×2 matrix is just four numbers, yet it can describe rotation, stretching, shearing, and reflection — **every linear transformation of the entire plane**. The product $A\cdot B$ is "first apply $B$, then apply $A$." A compact symbol, a complete language of transformation.

$$\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \text{ rotates by } 90°$$

### Determinants: Guardians of Area

$$|\det(A)| = \text{area of the transformed parallelogram}$$

The determinant tells us elegantly how a transformation affects area: det = 1 preserves area (rotation), det = 2 doubles it, det = 0 flattens space. **A single number encodes the "scaling" information of the whole space.**

### Eigenvalues: The Unchanging Essence

$$A\mathbf{v} = \lambda\mathbf{v}$$

An eigenvector's direction is unchanged by the transformation; it is only stretched by $\lambda$. **Amid endless variation, certain directions hold their essence** — the deepest beauty of linear algebra. The whole space decomposes into independent one-dimensional directions, each performing a pure scaling.

### Diagonalization: The Art of Simplification

If $A$ has $n$ linearly independent eigenvectors, then:

$$A = PDP^{-1}$$

A complicated matrix decomposes into "eigenvectors ($P$) + scaling ($D$) + un-eigenvectors ($P^{-1}$)." **Every complex transformation is, at heart, scaling along a few fixed directions.**

### Symmetry

A symmetric matrix ($A^T = A$) always has real eigenvalues and orthogonal eigenvectors. Symmetric structure brings clean properties — symmetric matrices are everywhere in physics and data.

### From Vectors to the World

The linear combinations of one vector span a whole vector space; a set of basis vectors spans the coordinates of the universe. **The simplest objects (vectors) × simple operations (addition, scalar multiplication) = the broadest structures (spaces).**
