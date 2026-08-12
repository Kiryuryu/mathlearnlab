## Key Insights: How to Think About Topology

### 1. First Ask: "What Survives Deformation?"

The first question in any topology problem is always: **is this property preserved under continuous deformation?**

- Preserved: connectedness, number of holes, embeddability, Euler characteristic
- Not preserved: length, angle, area, straightness (stretching changes them)

Filter out irrelevant information with this lens, and the problem often simplifies instantly.

### 2. The Euler Characteristic: One Number Decides

$$\chi = V - E + F$$

- Convex polyhedron: $\chi = 2$; torus (donut): $\chi = 0$; $g$ holes: $\chi = 2 - 2g$
- Technique: find any triangulation, count $V-E+F$ — the result is independent of how you triangulate
- Use: "is this surface a sphere or a torus?" — count the holes

### 3. One-Stroke Drawing: Counting Odd Vertices

One-stroke problems (Euler circuits/paths):
- All vertices have even degree → an Euler circuit exists (return to start)
- Exactly two odd-degree vertices → an Euler path exists (from one odd to the other)
- Otherwise → no solution

**The number of odd-degree vertices is always even** — the first "conservation law" of graph theory.

### 4. Deciding Homeomorphism: Find an Invariant

Are two spaces homeomorphic? If some topological invariant differs, they are definitely not. Common invariants:
- Euler characteristic (different → not homeomorphic)
- Number of connected components (different → not homeomorphic)
- Fundamental group $\pi_1$ (different → not homeomorphic)

Invariants are "necessary but not sufficient" discriminators: equal invariants don't guarantee homeomorphism, but unequal ones guarantee it fails.

### 5. Connectedness and Compactness: Two Keys to Analysis Problems

- **Connected**: the space cannot be split into two nonempty open sets. The intermediate value theorem depends on it
- **Compact**: a covering property (or "closed and bounded"). The existence of extrema of continuous functions depends on it

Judging compactness and connectedness often beats analyzing function properties directly.

### Common Pitfalls

1. **Confusing "homeomorphic" with "homotopic"**: homeomorphism is a strong equivalence (bijective and continuous both ways); homotopy only requires continuous deformation (allowing passing through itself)
2. **Counting "indentations" as holes**: holes must be enclosed cavities/loops; indentations don't count
3. **Applying $V-E+F=2$ to non-spherical shapes**: Euler's formula holds for sphere-type ($\chi=2$); a torus needs $\chi=0$
4. **Forgetting the difference between an Euler path and an Euler circuit**: a circuit must return to the start; a path need not
