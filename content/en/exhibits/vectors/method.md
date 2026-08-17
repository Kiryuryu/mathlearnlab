## Key Insights: How to Think About Vectors

### 1. First Ask: Are They Linearly Independent?

To decide whether a set of vectors is linearly independent:
- Test one by one: can it be written as a linear combination of the preceding ones?
- Fast route: arrange them as rows/columns of a matrix and compute the rank — full rank means independent

### 2. Spans and Bases

A set of vectors forms a basis ⇔ **linearly independent + spans the space**. Equivalent test: $n$ vectors in $n$ dimensions are linearly independent ⇔ the matrix they form has determinant ≠ 0.

### 3. Inner Products and Orthogonality

- Orthogonal ⇔ inner product 0
- Projection formula: $\text{proj}_u(v) = \frac{v\cdot u}{u\cdot u}\,u$
- Gram–Schmidt: orthogonalize a set of vectors to obtain an orthonormal basis

### 4. Think Geometrically

When you see a vector operation, draw a picture first: addition is translation, scalar multiplication is scaling, a linear combination is "walking several steps along each direction." **Translate algebra into geometry, and problems often reveal themselves at a glance.**

### Common Pitfalls

1. **Treating vectors as scalars**: $\mathbf{u} \cdot \mathbf{v}$ is a number, $\mathbf{u} \times \mathbf{v}$ is a vector (in 3D) — don't mix them
2. **Forgetting that the zero vector is a vector**: it is linearly dependent with everything, so it can never count as "independent"
3. **Span ≠ linear independence**: a set can span a space yet still be dependent (redundant vectors)
4. **Forgetting dimension**: $n$ dependent vectors in $n$ dimensions span a space of dimension < $n$
