# Multi-level Node Weighted Steiner Tree problem
Multi-level Node weighted Steiner trees - implementation of heuristics to compute them. The dependencies to run the code are Python 2.7/NetworkX/Matplotlib/PuLP.

## 1. A logarithmic bound heuristic (H3)
Extending below O(logn) approximation to multi-level graph representation with nested terminal sets.
https://www.sciencedirect.com/science/article/pii/S0196677485710292

Update: Implemented and tested successfully for graphs with upto 6 levels and 5000 nodes. The complexity depends on the number of terminals at the bottom level.

## 2. Shortest path heuristic (H1)
Steps:
 * Find shortest paths between all pairs of terminals. (short in terms of total path cost)
 * Sort paths by cost
 * Add edges/nodes by considering each path
 * Repeat this until all terminals are connected
 * If any cycles exist, remove one edge in each cycle to make it a tree.
 
 Update: implemented for a single level but correctness not verified.
 
## 3. Naive Greedy heuristic (H2)
Steps:
* Initially consider the terminals as forest of trees
* Add any edges between terminals if already part of graph
* If all terminals are connected, then we have the Steiner tree
* Otherwise, pick a non-terminal node in non-decreasing order of weights and add it to the forest of trees. Also add any edges
connecting the selected node and existing nodes in the forest
* Repeat this until all terminals are connected.

Update: implemented for a single level but correctness not verified.

## 4. 3+ Spider approach (H4)
A better approximation (O(1.6lnk)) based on below paper
https://www.sciencedirect.com/science/article/pii/S0890540198927547

Update: Partil implementation complete, however implementing the contraction functionality has proven to be a challenge. Due to time concerns, this functionality could be not be achieved.

## Files
`greedy.py` - Implements H2 for single level

`nwst.py` - Implements H3 for single level. To run, import this module in code and call `approximate_steiner` with the input graph and list of terminals as inputs. It returns the steiner tree and its cost.

`threeplusspider.py` - Implements H4 for single level

`shortestpath.py` - Implements H1 for single level

`mnwst.py` - Applying particular heuristic to multiple levels

 `test.py` - Test file to illustrate how H3 works for single level correctly
 
 `ilp.py` - Placeholder file for implementing ILP formulation. NOTE: Ignore this ILP implementation, incorrect as it works only in case of bipartite graphs.
