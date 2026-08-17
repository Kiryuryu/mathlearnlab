## Applications of Vectors

### 1. Forces and Displacement in Physics

Vectors were born for physics: force is a vector (magnitude and direction), displacement is a vector, and so are velocity and acceleration. Decomposing a force into horizontal and vertical components is exactly a linear combination:

$$F = F_x\mathbf{i} + F_y\mathbf{j}$$

Newton's law $\mathbf{F} = m\mathbf{a}$ is a vector equation — it holds component by component.

### 2. Feature Vectors in Data Science

One record (say, a person's height, weight, age) is a vector. A dataset is a collection of vectors.

- Each record is a point; $n$ features = a point in $n$-dimensional space
- Similarity = the angle between, or distance between, vectors
- **Normalization**: scaling a vector to unit length to remove differences in units

### 3. Graphics and Coordinate Systems

- Every vertex position in 3D graphics is a vector
- Converting between camera and world coordinates = expressing vectors in different bases
- Fonts and audio samples are points in vector spaces

### 4. Recommendation Systems

Represent both user preferences and item attributes as vectors; recommendation = finding vectors pointing in "similar directions" (cosine similarity):

$$\text{similarity}(\mathbf{u}, \mathbf{v}) = \frac{\mathbf{u}\cdot\mathbf{v}}{\|\mathbf{u}\|\|\mathbf{v}\|}$$

### 5. Vector Spaces and Bases in Coding Theory

Linear block codes encode information as a subspace of a vector space, and error correction is the search for the "nearest legal codeword" — vector spaces are the skeleton of the entire theory of communication error correction.

---

Behind these applications: vectors abstract "magnitude and direction" into computable arrays, giving physics, data, and graphics a shared mathematical language.
