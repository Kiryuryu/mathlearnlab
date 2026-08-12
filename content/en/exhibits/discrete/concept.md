## Graph Theory — Networks of Relations

The citizens of Königsberg found they could not cross all seven bridges exactly once. Euler abstracted land into points and bridges into lines, proving this with a simple count — **graph theory was born**. Today, from social networks to navigation maps, from the internet to molecular structures, every relation in the world is captured by "points and lines."

### Graphs: A Language of Points and Lines

A **graph** $G = (V, E)$ consists of a vertex set $V$ and an edge set $E$:

- **Vertices** represent entities (people, cities, web pages, molecules)
- **Edges** represent relations (friendship, roads, hyperlinks, chemical bonds)
- Directed graphs: edges have direction (following, dependency, one-way streets); undirected: no direction (friendship, adjacency)

The **degree** of a vertex is the number of edges meeting it. A seemingly simple definition can describe everything from friendship to gene regulation.

### Euler Circuits: The Mathematics of One-Stroke Drawing

> A connected graph has an **Euler circuit** (traversing every edge exactly once and returning to the start) if and only if all vertex degrees are even.

$$\text{one stroke} \iff \text{number of odd-degree vertices is } 0 \text{ or } 2$$

In the Königsberg problem, the four land masses have degrees 3, 3, 3, 5 — all odd, so there is **no solution**. This necessary-and-sufficient condition is both simple and profound — graph theory's first great theorem.

### Trees: The Most Economical Connectivity

A **tree** is a connected graph with no cycles. It has equivalent characterizations:

- A tree on $n$ vertices has exactly $n-1$ edges
- Any two vertices are connected by a unique path
- Adding any edge creates a cycle

Trees are "the most economical way to connect" — and thus everywhere: file systems, org charts, decision trees, minimum spanning trees (the cheapest highway network joining all cities).

### The Four Color Theorem: Four Colors Are Enough

> Any planar map can be colored with at most **4 colors** so that adjacent regions differ.

Proposed in 1852, proved by Appel and Haken in 1976 with computer assistance — becoming the first famous mathematical proof to depend on a computer. Its graph-theoretic form: planar graphs are 4-colorable.

### The Modern Power of Graphs

- **Shortest paths**: Dijkstra's algorithm drives navigation and routing
- **PageRank**: treating the web as a graph, importance = an eigenvector
- **Social networks**: six degrees of separation, influence spreading, community detection
- **Matching and flow**: bipartite matching for task assignment, max-flow for logistics bottlenecks

---

**From here:** see [Applications](#applications) on how graph theory builds the internet, navigation, and social networks; in [Interactive](#explore), decide whether figures can be drawn in one stroke and color a map yourself.

→ [Continue reading: Back to the exhibits](/gaoshu) to pick a new direction
