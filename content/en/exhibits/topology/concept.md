## Topology — The World of Continuous Deformation

Mold a lump of clay into any shape, fold a sheet of paper into a plane — during all these deformations, what stays the same? **Topology studies the properties that survive continuous stretching and twisting (without tearing or gluing).** It ignores length, angle, and area, caring only about "how things connect" and "how many holes."

### Topological Equivalence: Coffee Mugs and Donuts

Topologists have a classic joke: a coffee mug and a donut are "the same thing." Why?

- The handle of a mug is one hole; the hole of a donut is one hole
- A single **hole** (captured by the Euler characteristic) is topologically invariant
- As long as you neither tear nor glue, clay can deform continuously between the two

**In topology's eyes, everything with "one hole" is the same.** This radically changes our idea of "shape" — the essence of a shape is not its size but its connection structure.

### Euler's Characteristic: V − E + F

In 1736, Euler solved the Königsberg bridges problem, founding graph theory and topology. He also discovered a striking invariant:

> For any convex polyhedron: vertices − edges + faces = 2

$$V - E + F = 2$$

This number $2$ is the **Euler characteristic** $\chi$. It does not change however the polyhedron deforms — stretch or squeeze it, $V-E+F$ stays 2. A donut (torus) has $\chi = 0$; a surface with two holes has $\chi = -2$. **More holes, smaller $\chi$.**

### The Möbius Strip: A Miracle with One Side

Take a strip of paper, twist it half a turn, and glue the ends — you get the **Möbius strip**, with only one side and one edge. Cut along its middle line and you get not two strips but one longer one (twisted twice). It shows how counterintuitive the notion of "side" can be.

### Continuity and Homeomorphism: The Language of Topology

Topology is concerned with what is preserved under **continuous maps**. Two spaces are "topologically equivalent" (homeomorphic) when there is a bijective continuous map with a continuous inverse. Open sets, connectedness, compactness — these concepts form the language of topology and underpin analysis, dynamical systems, and data science.

---

**From here:** see [Applications](#applications) on how topology understands the shape of the universe, network structures, and the "shape of data"; in [Interactive](#explore), make a Möbius strip yourself and feel the wonder of one-sidedness.

→ [Continue reading: Complex Analysis — The Kingdom of Imaginary Numbers](/exhibit/complex)
