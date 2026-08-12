## Key Insights: How to Solve Graph Theory Problems

### 1. Modeling: Translate the Problem into a Graph

The first step in any graph problem is **identifying vertices and edges**:

- Vertices: who? which object? (people, cities, web pages, states)
- Edges: what relation? (friendship, roads, transitions, dependencies)
- Do edges have weights? (distance, cost, capacity)
- Do edges have direction? (one-way or two-way)

Translating a word problem into a graph often wins half the battle.

### 2. Euler Circuits vs. Hamiltonian Circuits

The two most easily confused concepts:

| Concept | Traverses | Criterion |
|---------|-----------|-----------|
| Euler circuit | each edge once | all vertex degrees even |
| Hamiltonian circuit | each vertex once | no simple criterion (NP-complete) |

**Euler cares about edges, Hamilton about vertices** — remembering this distinction avoids the confusion.

### 3. The Tree Toolbox

For tree problems, use its equivalent characterizations directly:

- $n$ vertices ⟺ $n-1$ edges + connected
- Unique path between any two vertices
- Acyclic and connected
- Adding any edge creates a cycle; removing any edge disconnects

Fastest test for "is it a tree": connected AND edges = vertices − 1.

### 4. Graph Coloring

- The **four color theorem** guarantees planar graphs need at most 4 colors
- Greedy algorithm: color vertices in some order with "the first available color," using at most $\Delta+1$ colors ($\Delta$ = max degree)
- Application spotting: scheduling (conflicts = edges), map coloring, register allocation

### 5. Shortest Paths and Connectivity

- **Dijkstra**: single-source shortest path with nonnegative weights (greedy + priority queue)
- **BFS**: shortest paths in unweighted graphs, connected components
- **DFS**: connectivity, topological sorting, cycle detection

"Are two points connected?" → BFS/DFS; "minimum cost" → Dijkstra; "cheapest way to connect everyone" → minimum spanning tree.

### Common Pitfalls

1. **Confusing Euler and Hamiltonian circuits**: the former looks at edges and is easy; the latter at vertices and is NP-complete
2. **Misusing tree theorems**: a graph with $n-1$ edges is not necessarily a tree (it may be disconnected)
3. **Ignoring graph orientation**: naive Dijkstra fails on directed graphs without care
4. **Treating "at least" as "exactly"**: $\Delta+1$ colors is an upper bound, not the precise number; the greedy order affects the result
