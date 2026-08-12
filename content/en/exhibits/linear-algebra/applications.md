## Applications of Linear Algebra

Now that you know vectors, matrices, determinants, and eigenvectors, let's see how this "language of space" powers the modern world.

### 1. PageRank — The Search Engine of the Web

Google treats the entire internet as one **giant matrix**: each row and column is a web page, and the entries encode link relationships. A page's "importance" is the principal eigenvector of this matrix.

- Iterative computation: each page's importance = weighted sum of pages linking to it
- Once converged, the weight vector reaches a steady state — the ranking is fixed

**An eigenvector of one matrix defines the order of the entire internet.**

### 2. PCA Dimensionality Reduction — The Core Tool of Data Science

High-dimensional data (samples with hundreds of features) is hard to analyze and visualize. **Principal Component Analysis (PCA)** finds the eigenvectors of the covariance matrix corresponding to the largest eigenvalues — directions that preserve the most variance (information).

- Projecting 100-dimensional data onto the 2 most important directions loses the least information
- Face recognition, gene analysis, and recommender systems all use PCA for preprocessing

**Dimensionality reduction is about finding the directions in which data changes most.**

### 3. Quantum Mechanics — The World's Eigenvalue Problem

The Schrödinger equation $H\psi = E\psi$ is an **eigenvalue equation**: the Hamiltonian operator $H$ acting on the wavefunction $\psi$ equals a constant $E$ times $\psi$.

- **Energy levels** are the eigenvalues $E$
- **Orbitals** (the shapes of electron clouds) are the eigenvectors $\psi$

Heisenberg even expressed physical quantities directly as matrices — hence **matrix mechanics**. Quantum computing and chemistry simulation are built entirely on this mathematics.

### 4. 3D Graphics — The Skeleton of Game Engines

Every 3D scene you see on screen is a chain of matrix multiplications:

- **Rotation**: turning an object $45°$ around an axis
- **Projection**: flattening 3D coordinates onto the 2D screen (perspective projection)
- **View transform**: converting camera coordinates into world coordinates

Game engines perform tens of millions of matrix multiplications per frame — that is what GPUs are built for.

### 5. Compression and Recommendation — The Wisdom of Matrices

- **Image compression**: treat the image as a matrix and use Singular Value Decomposition (SVD) to keep the largest singular values while discarding fine detail
- **Recommender systems**: factorize the user–item rating matrix to fill in the "unrated" entries

**The intuition behind matrix factorization: decompose complex information into a combination of a few principal components.**

---

Behind all of these is one idea: **the world can be modeled as space, change can be modeled as matrices, and the essence lives in the eigenvectors.** Look back at the definitions in **Core Concepts** with this eye, and the formulas stop being symbols — they become pictures of space.
