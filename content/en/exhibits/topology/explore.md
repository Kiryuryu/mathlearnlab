## Interactive: The Intuition Lab of Topology

### Try It 1: Can It Be Drawn in One Stroke?

For each graph below, how many vertices have odd degree (an odd number of edges meeting)? Can it be drawn without lifting the pen?

- Graph A: a square (each vertex has degree 2)
- Graph B: a straight line (endpoints degree 1, middle degree 2)
- Graph C: a five-pointed star (each vertex degree 2)
- Graph D: an "X" (crossing degree 4, four endpoints degree 1)

<details>
<summary>Answer</summary>
- Graph A: all 4 vertices degree 2, odd count 0 → Euler circuit exists ✓
- Graph B: 2 odd vertices → Euler path exists ✓
- Graph C: all 5 vertices degree 2, odd count 0 → Euler circuit exists ✓
- Graph D: 4 odd endpoints (the crossing, degree 4, is even) → Euler path exists ✓
</details>

### Try It 2: The Euler Characteristic

For a cube, count $V$ (vertices), $E$ (edges), $F$ (faces), then compute $V-E+F$.

<details>
<summary>Answer</summary>
Cube: $V=8$, $E=12$, $F=6$ → $8-12+6=2$ ✓. Now imagine squashing the cube into a sphere — triangulate and count again; it is still 2. This is the invariance of the Euler characteristic: $V-E+F$ depends not on shape but only on the number of holes.
</details>

### Try It 3: The Secret of the Möbius Strip

Take a long strip of paper, twist it 180° (half a turn), and glue the ends. Now cut along the middle line. How many strips do you get?

<details>
<summary>Answer</summary>
You get **one longer strip**, not two! Because a Möbius strip has only one edge, cutting along the middle is like laying out that single edge flat — you get a longer strip with four half-twists. If you then cut that new strip down the middle, you finally get two strips linked together — the paper strip hides topology's most famous counterintuition.
</details>

### Try It 4: Brouwer's Fixed Point

Take a glass of water, stir it gently, then look. Physics guarantees: **at least one water molecule ends up almost exactly where it started.**

<details>
<summary>Answer</summary>
This is Brouwer's fixed-point theorem: a continuous map (the displacement field of stirring) acting on the disk-like water surface must have a point returning near its original position (strictly, a fixed point). Mathematically, any continuous map of a disk into itself has a fixed point — stirring, folding a map, crumpling a paper and stacking it back — none can escape this theorem.
</details>
