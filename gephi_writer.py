from simplegexf import Gexf, Edge

def check_node_exists(gexf_graph,node):
    gexf_nodes = gexf_graph.nodes
    for n in gexf_nodes:
        if n.data['@id'] == str(node):
            return True
    return False

def check_edge_exists(gexf_graph,edge):
    gexf_edges = gexf_graph.edges
    for e in gexf_edges:
        if (e.data['@source'] == edge[0] and e.data['@target'] == edge[1]) or (e.data['@source'] == edge[1] and e.data['@target'] == edge[0]):
            return True

    return False


def write_to_gexf(steiner_trees,terminal_sets,graph_name):
    i = 0
    j = 0

    for tree in steiner_trees:
        gexf_file = Gexf(graph_name+'_'+str(i)+'.gexf')
        graph = gexf_file.add_graph(defaultedgetype="undirected",mode="dynamic")

        for node in list(tree.nodes):
            if i == 0:
               n = graph.add_node(id=node,label=node,start=i)
            elif node not in terminal_sets[i-1]:
               n = graph.add_node(id=node,label=node,start=i)
            if node in terminal_sets[i] and n is not None:
                n.set('viz:size', value=10.0)
                n.set('viz:color', r=255, g=0, b=130)
            elif n is not None:
                n.set('viz:size', value=10.0)
                n.set('viz:color', r=128, g=128, b=130)
        for edge in list(tree.edges):
            e = Edge(id=j,source=edge[0],target=edge[1])
            e.data["@start"] = str(i)
            graph.edges.append(e)
            j += 1
        i += 1
        gexf_file.write()
