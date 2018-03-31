import threeplusspider
import networkx as nx
import networkx.algorithms.tree as t
import ilp
import random
import matplotlib.pyplot as plt
import math
from networkx.drawing.nx_agraph import write_dot

# converting set cover example given here
# (https://www.geeksforgeeks.org/set-cover-problem-set-1-greedy-approximate-algorithm/)
# to NWST problem and applying algorithm
test_graph = nx.Graph()
#test_graph = nx.connected_watts_strogatz_graph(40, 3, 0.48, tries=100, seed=None)
#nodes = list(test_graph.nodes)
#for node in nodes:
#    test_graph.nodes[node]['weight'] = random.uniform(5,20)
#weights = nx.get_node_attributes(test_graph,'weight')
#terminals = [x for x in list(test_graph.nodes) if test_graph.nodes[x]['weight']>13]
#terminals = nx.algorithms.maximal_independent_set(test_graph)
test_graph.add_node(1,weight=5)
test_graph.add_node(2,weight=10)
test_graph.add_node(3,weight=3)
test_graph.add_node(4,weight=0)
test_graph.add_node(5,weight=0)
test_graph.add_node(6,weight=0)
test_graph.add_node(7,weight=0)
test_graph.add_node(8,weight=0)

test_graph.add_edge(1,4)
test_graph.add_edge(1,6)
test_graph.add_edge(1,7)

test_graph.add_edge(2,5)
test_graph.add_edge(2,8)

test_graph.add_edge(3,4)
test_graph.add_edge(3,5)
test_graph.add_edge(3,6)
test_graph.add_edge(3,7)

terminals = [4,5,6,7,8]
# terminals = ["t1","t2","t3","t4","t5"]
# mapping = dict()
# for terminal in terminals:
#     test_graph.node[terminal]['weight'] = 0
#     mapping[terminal] = "t"+str(terminal)
#
#
# for node in list(test_graph.nodes):
#     if node not in terminals:
#         mapping[node] = "S"+str(node)

#terminals = ["t"+str(x) for x in terminals]

#test_graph = nx.relabel_nodes(test_graph,mapping)
plt.figure()
nx.draw(test_graph,with_labels=True)
#plt.show()
print('The terminals are '+str(terminals))
steiner_tree,steiner_cost = threeplusspider.approximate_steiner(test_graph,terminals)
plt.figure()
nx.draw(steiner_tree,with_labels=True)
plt.show()

if t.is_tree(steiner_tree):
    print("Is a tree")
print(steiner_cost)
write_dot(steiner_tree,"steiner.dot")
print("Testing through ILP")
exact_solver = ilp.NWSTLPSolver(test_graph,terminals)
exact_solver.formulate_problem()
optimal_cost = exact_solver.solve_ilp()
print("Approximation ratio is "+str(steiner_cost/optimal_cost)+" which is within the bound "+str(2*math.log(len(terminals))))
