## Linear Algebra — Transformations of Space

What does multiplying a matrix by a vector actually do? Hide the answer in an image: **a matrix is a deformation of space** — stretching, rotating, squeezing. Linear algebra studies what survives when space is deformed this way. The answer lives in the eigenvectors.

### Vectors: "Points" with Direction

A vector $\mathbf{v} = (x, y)$ is an arrow from the origin, and also a position in space. What really matters is the **linear combination**: any vector can be built from basis vectors.

$$\mathbf{v} = x\mathbf{i} + y\mathbf{j}$$

Vector addition is translation; scalar multiplication is scaling. Every vector operation is built from these two moves.

### Matrices: "Deformers" of Space

A matrix $A$ acting on a vector $\mathbf{x}$ produces a new vector $\mathbf{y}$. Geometrically, $A$ deforms the entire coordinate grid:

$$A\mathbf{x} = \mathbf{y}, \qquad \begin{bmatrix}a & b \\ c & d\end{bmatrix}\begin{bmatrix}x \\ y\end{bmatrix} = \begin{bmatrix}ax+by \\ cx+dy\end{bmatrix}$$

The three classic deformations are **rotation** ($\begin{bmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{bmatrix}$), **scaling** ($\begin{bmatrix}s_x & 0 \\ 0 & s_y\end{bmatrix}$), and **shear** ($\begin{bmatrix}1 & k \\ 0 & 1\end{bmatrix}$). Thinking of a matrix as a "space processor" that pulls and pushes the grid makes much of the abstraction concrete.

### Determinants: How Much Area Changes

$$\det(A) = ad - bc$$

The determinant measures the **area of the parallelogram** into which $A$ maps the unit square. It answers: does this deformation expand space or crush it?

- $\det(A) = 0$: the transformation flattens the plane onto a line (**dimension loss** — information destroyed)
- $\det(A) > 0$: orientation preserved
- $\det(A) < 0$: orientation flipped

A zero determinant means the matrix is not invertible — the deformation cannot be undone, and some information is unrecoverable.

### Eigenvectors: Vectors Whose Direction Is Unchanged

$$A\mathbf{v} = \lambda\mathbf{v}$$

If $A$ only stretches or compresses $\mathbf{v}$ by a factor $\lambda$ without changing its direction, then $\mathbf{v}$ is an **eigenvector** and $\lambda$ an **eigenvalue**.

Most vectors in the grid change direction under a deformation, but **eigenvectors do not** — they reveal the transformation's principal axes, the key to its essential structure. From principal stresses in mechanics to Google's page ranking to the shapes of electron clouds in quantum mechanics, eigenvectors are everywhere.

---

**From here:** see [Applications](#applications) on how PageRank, PCA, 3D graphics, and quantum mechanics turn this into the engine of the modern world; in [Interactive](#explore), drag the entries of a 2×2 matrix and watch the grid stretch, rotate, and flatten on screen.

→ [Continue reading: Probability — The Science of Uncertainty](/exhibit/probability)
