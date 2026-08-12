## Applications of Graph Theory

### 1. Navigation and Shortest Paths

The map navigation on your phone is essentially Dijkstra's algorithm finding shortest paths on a road-network graph:

- Cities = vertices, roads = weighted edges
- The algorithm expands "cheapest known paths" from the start until it reaches the destination
- Large road networks use A* heuristics plus hierarchical graphs for speed

Google Maps processes millions of such queries per second.

### 2. PageRank and the Internet

Google treats the entire internet as a giant directed graph: web pages are vertices, hyperlinks are edges. **PageRank** iteratively computes each page's "importance" — an important page is one linked by many important pages. This is the mathematical core of search-engine ranking.

### 3. Social Network Analysis

- **Six degrees of separation**: social networks have small diameter — any two people connect in a few steps on average
- **Influence spreading**: how information spreads like a virus (threshold models, independent cascade models)
- **Community detection**: finding tightly-knit "circles of friends" (Facebook friend suggestions, Twitter topic clustering)

### 4. Transportation and Logistics

- **Max flow**: the maximum throughput of goods, data, or traffic through a network
- **Minimum spanning tree**: the cheapest way to lay pipes/cables connecting all nodes
- **Traveling salesman**: courier route optimization (NP-hard, approximated heuristically)

### 5. Biology and Chemistry

- **Metabolic networks**: the graph of chemical reactions inside an organism
- **Protein interactions**: proteins as vertices, interactions as edges
- **Chemical molecules**: atoms as vertices, bonds as edges — graph-isomorphism algorithms compare drug molecules

### 6. Scheduling and Matching

- **Bipartite matching**: assigning employees to positions, patients to organ donations
- **Scheduling**: model course conflicts as graph coloring — colors are time slots

---

**Behind all of these**: graph theory's power is that it captures the most universal structure (relations) with the least abstraction (points and lines), then unleashes decades of algorithmic machinery in service of those relations.
