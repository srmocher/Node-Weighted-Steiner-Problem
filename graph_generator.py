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
    terminals = alg.maximal_independent_set(graph)

    for node in list(graph.nodes):
        graph.nodes[node]['weight'] = random.uniform(w_min,w_max)

    for i in range(0,levels):
        terminal_sets.append(list(terminals))
        terminals.pop(random.randint(0,len(terminals)-1))

    terminal_sets.reverse()
    return graph,terminal_sets

