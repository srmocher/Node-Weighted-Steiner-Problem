# CSC620-Steiner
Multi-level Node weighted Steiner trees - implementation of heuristics to compute them

## 1. A logarithmic bound heuristic
Extending below O(logn) approximation to multi-level graph representation with nested terminal sets.
https://www.sciencedirect.com/science/article/pii/S0196677485710292

## 2. Shortest path heuristic
Steps:
 * Find shortest paths between all pairs of terminals. (short in terms of total path cost)
 * Sort paths by cost
 * Add edges/nodes by considering each path
 * Repeat this until all terminals are connected
 * If any cycles exist, remove one edge in each cycle to make it a tree.
 
## 3. Naive Greedy heuristic (~Kruskal)
Steps:
* Initially consider the terminals as forest of trees
* Add any edges between terminals if already part of graph
* If all terminals are connected, then we have the Steiner tree
* Otherwise, pick a non-terminal node in non-decreasing order of weights and add it to the forest of trees. Also add any edges
connecting the selected node and existing nodes in the forest
* Repeat this until all terminals are connected.

## 4. Branch Spider approach
A better approximation (O(1.5lnk)) based on below paper
https://www.sciencedirect.com/science/article/pii/S0890540198927547