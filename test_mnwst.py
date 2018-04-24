import graph_generator as gg
import mnwst
import gephi_writer
import matplotlib.pyplot as plt
import networkx as nx


params = dict()
# params['prob']=0.48
# params['neighbors']=2
# params['tries']=100
params['m'] = 3
levels = 2
ml_graph, terminal_sets = gg.generate_multi_level_graph(n=200,w_min=2,w_max=10,levels=levels,graph_type="barabasi-albert",params=params)
gg.write_to_file(ml_graph,terminal_sets,levels,"graph.txt")
multi_level_instance = mnwst.MultiLevelGraph(ml_graph,levels=levels,terminal_sets=terminal_sets)
multi_level_instance.approximate_steiner_top_down()
steiner_trees,steiner_costs = multi_level_instance.get_steiner_trees()
gephi_writer.write_to_gexf(steiner_trees,terminal_sets,'graph')
# nx.draw(steiner_trees[0])
# plt.show()
# gfx = gexf.Gexf("Sridhar","CSC 620 graph")
# gexf_graph = gfx.addGraph("undirected","dynamic","NWST")
# gexf_graph.addNode("0","hello")
# gexf_graph.addNode("1","e")
# gexf_graph.addEdge("test edge","0","1")
# with open("hello.gexf","w") as f:
#     gexf_graph.write(f)
#for steiner_tree in steiner_trees:




