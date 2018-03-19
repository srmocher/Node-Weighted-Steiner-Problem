import nwst
import networkx as nx
import networkx.algorithms.tree as t
import ilp

# converting set cover example given here
# (https://www.geeksforgeeks.org/set-cover-problem-set-1-greedy-approximate-algorithm/)
# to NWST problem and applying algorithm

test_graph = nx.Graph()
for i in range(1,6):
    test_graph.add_node("t"+str(i),weight=0)
test_graph.add_node('S1',weight=5)
test_graph.add_node('S2',weight=10)
test_graph.add_node('S3',weight=3)

test_graph.add_edge('S1',"t1")
test_graph.add_edge('S1',"t3")
test_graph.add_edge('S1',"t4")

test_graph.add_edge('S2',"t2")
test_graph.add_edge('S2',"t5")

test_graph.add_edge('S3',"t1")
test_graph.add_edge('S3',"t2")
test_graph.add_edge('S3',"t3")
test_graph.add_edge('S3',"t4")

terminals = ["t1","t2","t3","t4","t5"]
steiner_tree,steiner_cost = nwst.approximate_steiner(test_graph,terminals)
if t.is_tree(steiner_tree):
    print("Is a tree")
print(steiner_cost)

print("Testing through ILP")
exact_solver = ilp.NWSTLPSolver(test_graph,terminals)
exact_solver.formulate_problem()
exact_solver.solve_ilp()
