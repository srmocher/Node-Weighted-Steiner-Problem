import nwst
import networkx as nx

# converting set cover example given here
# (https://www.geeksforgeeks.org/set-cover-problem-set-1-greedy-approximate-algorithm/)
# to NWST problem and applying algorithm

test_graph = nx.Graph()
for i in range(1,6):
    test_graph.add_node(i,weight=0)
test_graph.add_node('S1',weight=5)
test_graph.add_node('S2',weight=10)
test_graph.add_node('S3',weight=3)

test_graph.add_edge('S1',1)
test_graph.add_edge('S1',3)
test_graph.add_edge('S1',4)

test_graph.add_edge('S2',2)
test_graph.add_edge('S2',5)

test_graph.add_edge('S3',1)
test_graph.add_edge('S3',2)
test_graph.add_edge('S3',3)
test_graph.add_edge('S3',4)

terminals = [1,2,3,4,5]
steiner_tree,steiner_cost = nwst.approximate_steiner(test_graph,terminals)
print(steiner_cost)
