## Interactive: The Intuition Lab of Graph Theory

### Try It 1: Can It Be Drawn in One Stroke?

Can the following figures be drawn without lifting the pen? Euler's rule decides.

- Figure A: a "tian" grid (3×3 lattice — boundary and internal cross)
- Figure B: a five-pointed star
- Figure C: three squares sharing one corner, forming no closed loop

<details>
<summary>Answer</summary>
- Figure A (3×3 lattice): four corners have degree 2, four edge-midpoints degree 3 (the internal cross passes through), center degree 4. Odd-degree count = 4 → **cannot**.
- Figure B (star): 5 vertices of degree 2 → odd count 0 → **can** (Euler circuit).
- Figure C (three squares sharing a corner): each square's corners share edges — all degrees are even → **can**.
</details>

### Try It 2: Verify the Tree Properties

Which of the following are trees?

- Graph A: three vertices, two edges, a straight chain
- Graph B: four vertices, three edges, an "L" shape
- Graph C: four vertices, three edges, but split into two groups (two isolated vertices + one edge)

<details>
<summary>Answer</summary>
- Graph A: connected + 3 vertices 2 edges → **tree** ✓
- Graph B: connected + 4 vertices 3 edges → **tree** ✓
- Graph C: has 4 vertices 3 edges but is disconnected → **not a tree** ($n-1$ edges is not enough; connectivity is also required)

Key: tree = connected AND edges = vertices − 1; both conditions are necessary.
</details>

### Try It 3: Map Coloring

This "map" has 4 regions; adjacent regions cannot share a color. How few colors are needed?

- Region A borders B and C
- Region B borders A, C, D
- Region C borders A, B, D
- Region D borders B and C

<details>
<summary>Answer</summary>
Draw regions as vertices and borders as edges: you get A–B, A–C, B–C, B–D, C–D (a 4-cycle plus a diagonal). Greedy coloring: A=1, B=2, C must be 3 (borders both A and B), D borders B and C but A is free → D=1. **Only 3 colors** (A and D share). Note this is not the worst planar case — some maps need 4 colors, but the four color theorem guarantees never more than 4.
</details>

### Try It 4: Minimum Spanning Tree

Distances among four cities: AB=2, AC=5, AD=4, BC=3, BD=7, CD=6. To lay pipe connecting all cities with minimum total length, which roads do you choose?

<details>
<summary>Answer</summary>
Use Kruskal's algorithm — pick edges smallest-first, avoiding cycles: pick AB(2) → pick BC(3) → next AD(4) (CD=5, AC=5 are larger) → now all 4 vertices are connected (AB, BC, AD = three edges, 4 vertices, 3 edges = a tree). Total $2+3+4=9$. Verify: this is a minimum spanning tree; any other combination of three edges has total length ≥ 9.
</details>
