## Explore Vectors

### Try It 1: A Linear Combination of Vectors

Given vectors $\mathbf{u} = (1, 2)$ and $\mathbf{v} = (3, 1)$, write the combination $2\mathbf{u} - \mathbf{v}$. What are its coordinates?

<details>
<summary>Answer</summary>
$2\mathbf{u} - \mathbf{v} = (2, 4) - (3, 1) = (-1, 3)$. Geometrically: walk two steps along $\mathbf{u}$, then one step opposite to $\mathbf{v}$ — that is the "puzzle-assembly" of a linear combination.
</details>

### Try It 2: Testing Linear Independence

Three vectors: $\mathbf{u} = (1, 0)$, $\mathbf{v} = (0, 1)$, $\mathbf{w} = (1, 1)$. Are they linearly independent? Do they span the plane?

<details>
<summary>Answer</summary>
$\mathbf{w} = \mathbf{u} + \mathbf{v}$, so the three vectors are linearly dependent ($\mathbf{w}$ is a combination of the first two). Yet they still span the whole plane (using just $\mathbf{u}, \mathbf{v}$ suffices). Linear independence = no redundancy; spanning = wide enough coverage. The two properties are independent.
</details>

### Try It 3: Inner Product and Angle

Compute the inner product of $\mathbf{u} = (1, 0)$ and $\mathbf{v} = (0, 1)$. Are they orthogonal?

<details>
<summary>Answer</summary>
$\mathbf{u}\cdot\mathbf{v} = 1\times 0 + 0\times 1 = 0$. Inner product 0 ⟺ orthogonal ⟺ angle 90°. Here $\mathbf{u}$ lies along the x-axis and $\mathbf{v}$ along the y-axis, so of course they are perpendicular.
</details>

### Try It 4: Projecting a Vector

Project $\mathbf{v} = (2, 3)$ onto $\mathbf{u} = (1, 0)$. What is the projection vector?

<details>
<summary>Answer</summary>
$\text{proj}_u(v) = \frac{v\cdot u}{u\cdot u}u = \frac{2\times 1 + 3\times 0}{1^2 + 0^2}(1, 0) = 2(1, 0) = (2, 0)$. Projection decomposes $\mathbf{v}$ into "the component along $\mathbf{u}$, $(2,0)$, and the perpendicular component, $(0,3)$" — this is the basis of least squares.
</details>
