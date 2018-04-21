import networkx as nx
import networkx.algorithms as alg
import random


def generate_multi_level_graph(n,w_min,w_max,levels,graph_type,params):
    graph = None
    if graph_type == "watts-strogatz":
        graph = nx.connected_watts_strogatz_graph(n,params['neighbors'],params['prob'],params['tries'])
    elif graph_type == "erdos-renyi":
        graph = nx.erdos_renyi_graph(n,params['prob'],params['seed'])
    elif graph_type == "barabasi-albert":
        graph = nx.barabasi_albert_graph(n,params['m'])

    terminal_sets = list()
    num_nodes = len(list(graph.nodes))
    num_edges = len(list(graph.edges))
    print('Graph generated has '+str(num_nodes)+' nodes and '+str(num_edges))
    for node in list(graph.nodes):
        graph.nodes[node]['weight'] = random.randint(w_min,w_max)
    terminals = list(graph.nodes)
    for i in range(levels):
        num_n = int(num_nodes/(i+2))
        print('Level '+str(i)+' has '+str(num_n)+' terminals')
        terminals = random.sample(terminals, num_n)
        terminals.sort()
        terminal_sets.append(terminals)
    terminal_sets.reverse()
    return graph,terminal_sets


def write_to_file(graph,terminal_sets,levels, file_name):

    with open(file_name,"w") as f:
        num_nodes = len(list(graph.nodes))
        num_edges = len(list(graph.edges))
        f.write(str(num_nodes)+'\n')
        weights = nx.get_node_attributes(graph,'weight')
        for node in list(graph.nodes):
            f.write(str(weights[node])+'\n')
        f.write(str(num_edges)+'\n')
        for edge in list(graph.edges):
            f.write(str(edge[0]+1) + ' ' + str(edge[1]+1)+'\n')

        f.write(str(levels)+'\n')
        for i in range(levels):
            terminals = terminal_sets[i]
            terminals_str = ""
            for terminal in terminals:
                terminals_str = terminals_str + str(terminal+1) + ' '
            f.write(str(terminals_str)+'\n')








