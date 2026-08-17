## Matrices — Deformers of Space

How can a matrix of four numbers describe rotation, stretching, and shearing — every transformation of space? Because **matrix multiplication is deformation of space**: when $A$ acts on $\mathbf{x}$, it drags the entire coordinate grid around. The key to understanding a matrix is seeing where it moves the basis vectors.

### Matrix Multiplication = Transformation of Space

$$A\mathbf{x} = \mathbf{y}, \qquad \begin{bmatrix}a & b \\ c & d\end{bmatrix}\begin{bmatrix}x \\ y\end{bmatrix} = \begin{bmatrix}ax+by \\ cx+dy\end{bmatrix}$$

In the "3Blue1Brown" way of seeing: the matrix $A$ moves the basis vector $\mathbf{i}=(1,0)$ to $A\mathbf{i}=(a,c)$ and $\mathbf{j}=(0,1)$ to $A\mathbf{j}=(b,d)$; every other vector is carried along with the grid. **To read a matrix is to read where the basis vectors fly.**

### Three Basic Deformations

| Transformation | Matrix | Effect |
|------|------|------|
| **Rotation** | $\begin{bmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{bmatrix}$ | turn by $\theta$ about the origin |
| **Scaling** | $\begin{bmatrix}s_x & 0 \\ 0 & s_y\end{bmatrix}$ | stretch along the axes |
| **Shear** | $\begin{bmatrix}1 & k \\ 0 & 1\end{bmatrix}$ | slide in parallel |

### The Determinant: How Much Area a Deformation Changes

> $$\det(A) = ad - bc$$

The determinant measures the **area of the parallelogram** into which $A$ maps the unit square. It answers: does this deformation "expand space" or "crush it"?

- $\det(A) = 0$: the transformation flattens the plane onto a line (**dimension loss** — information destroyed)
- $\det(A) > 0$: orientation preserved
- $\det(A) < 0$: orientation flipped

A zero determinant means the matrix is not invertible — the deformation cannot be undone, and some information is unrecoverable.

### Matrix Multiplication and the Inverse

- **Composition**: $AB$ means "first apply $B$, then apply $A$" — but $AB \neq BA$, the order cannot be swapped
- **Inverse** $A^{-1}$: undoes $A$'s deformation, $A^{-1}A = I$. $A$ is invertible ⇔ $\det(A) \neq 0$
- **Rank** = dimension of the transformed space: full rank ($n$) preserves dimension; deficient rank collapses it

---

**From here:** see [Applications](#applications) on how matrices drive 3D graphics and compress images; in [Interactive](#explore), drag the entries of a 2×2 matrix by hand and watch the whole grid deform on screen.

→ [Continue reading: Eigenvalues — Invariant Directions](/exhibit/eigenvalue)
