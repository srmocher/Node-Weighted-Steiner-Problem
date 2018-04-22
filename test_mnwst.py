import graph_generator as gg
import mnwst
from simplegexf import Gexf, Edge
import matplotlib.pyplot as plt
import networkx as nx


params = dict()
# params['prob']=0.48
# params['neighbors']=2
# params['tries']=100
params['m'] = 3
levels = 3
ml_graph, terminal_sets = gg.generate_multi_level_graph(n=1000,w_min=2,w_max=10,levels=levels,graph_type="barabasi-albert",params=params)
gg.write_to_file(ml_graph,terminal_sets,levels,"test.txt")
multi_level_instance = mnwst.MultiLevelGraph(ml_graph,levels=levels,terminal_sets=terminal_sets)
multi_level_instance.approximate_steiner_top_down()
steiner_trees,steiner_costs = multi_level_instance.get_steiner_trees()
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

def check_node_exists(gexf_graph,node):
    gexf_nodes = gexf_graph.nodes
    for n in gexf_nodes:
        if n.data['@id'] == str(node):
            return True
    return False

def check_edge_exists(gexf_graph,edge):
    gexf_edges = gexf_graph.edges
    for e in gexf_edges:
        if (e.data['@source'] == edge[0] and e.data['@target']==edge[1]) or (e.data['@source'] == edge[1] and e.data['@target']==edge[0]):
            return True

    return False


gexf = Gexf('nwst.gexf')
gexf_graph = gexf.add_graph(defaultedgetype="undirected",mode="dynamic")

for i in range(levels):
    steiner_tree = steiner_trees[i]
    for node in list(steiner_tree.nodes):
        if not check_node_exists(gexf_graph,node):
            gexf_graph.add_node(id=node,label=node,mode="dynamic",start=i,end=levels)

    j = 0
    for edge in list(steiner_tree.edges):
        if not check_edge_exists(gexf_graph,edge):
            e = Edge(id=j,source=edge[0],target=edge[1])
            gexf_graph.edges.append(e)
            e.data['@start'] = str(i)
            e.data['@end'] = str(levels)

gexf.write()



