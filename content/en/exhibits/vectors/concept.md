## Vectors — Coordinates and Directions of Space

An arrow from the origin pointing at a point in space — that is a vector in its simplest form. But linear algebra asks: **why should this one simple object become the starting point for understanding all of space?** The answer lies in "combination": every vector can be assembled from a few basis vectors, and the structure of space is hidden in those assemblies.

### Two Identities of a Vector

A vector $\mathbf{v} = (x, y)$ has a dual identity:

- **Geometrically**: an arrow from the origin with length $\|\mathbf{v}\| = \sqrt{x^2 + y^2}$ pointing toward $(x,y)$
- **Algebraically**: an ordered list of numbers that can be added, subtracted, and scaled

Switching between these two identities — imagining an abstract list of numbers as a directed arrow — is the most important habit of thought in linear algebra.

### Linear Combination: Assembling All of Space

> $$\mathbf{v} = x\mathbf{i} + y\mathbf{j}$$

**Linear combination** is the core operation on vectors: multiply each vector by a scalar, then add. Two basic moves generate everything:

- **Vector addition** $\mathbf{u} + \mathbf{v}$ = translation (place the tip of $\mathbf{u}$ at the start of $\mathbf{v}$)
- **Scalar multiplication** $c\mathbf{v}$ = scaling (stretch or shrink by a factor of $c$; reversed when $c<0$)

### Bases and Linear Independence

If a set of vectors is **linearly independent** (no one of them is a combination of the others) and **spans** the whole space, then it is a **basis**. The standard $\{\mathbf{i}, \mathbf{j}\}$ is the simplest basis, but space has infinitely many.

Key insight: **the number of basis vectors equals the dimension of the space**. The matrix formed by $n$ linearly independent $n$-dimensional vectors must have nonzero determinant.

### From Vectors to Space

$$n \text{ linearly independent vectors } \Rightarrow \text{ span an } n\text{-dimensional space}$$

Once you accept that "a few vectors can span a space," you hold the foundation for understanding matrices, linear transformations, and eigenvalues — because a matrix is nothing but a record of "where the basis vectors were taken."

---

**From here:** see [Applications](#applications) on how vectors describe forces and displacement in physics and features in data; in [Interactive](#explore), combine basis vectors with your own hands and feel how a space is assembled.

→ [Continue reading: Matrices — Deformers of Space](/exhibit/matrix)
