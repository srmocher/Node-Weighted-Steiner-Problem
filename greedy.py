# Placeholder for the naive greedy heuristic planned in the initial proposal

import networkx as nx


def check_terminals_connected(tree,terminals):
    num_terminals = len(terminals)
    for i in range(0,num_terminals):
        for j in range(i+1,num_terminals):
            paths = nx.all_simple_paths(tree,terminals[i],terminals[j])
            if paths is None or len(paths)==0:
                return False

    return True


def approx_steiner(graph,terminals):
    steiner_tree = nx.Graph()
    for terminal in terminals:
        steiner_tree.add_node(terminal)

    nodes = list(graph.nodes)
    weights = nx.get_node_attributes(graph,'weight')
    steiner_nodes = list()
    for node in nodes:
        if node not in terminals:
            n = dict()
            n['node'] = node
            n['weight'] = weights[node]
            steiner_nodes.append(n)

    num_terminals = len(terminals)

    # Add edges between terminals if any
    for i in range(0,num_terminals):
        for j in range(i+1,num_terminals):
            if graph.has_edge(terminals[i],terminals[j]):
                steiner_tree.add_edge(terminals[i],terminals[j])

    if check_terminals_connected(steiner_tree,terminals):
        return steiner_tree

    # Sort non-terminal nodes by weight
    steiner_nodes.sort(lambda x:x['weight'])

    for steiner_node in steiner_nodes:
        current_nodes = list(steiner_tree.nodes)
        steiner_tree.add_node(steiner_node)

        # Add any edges between the selected node and existing nodes
        for current_node in current_nodes:
            if graph.has_edge(steiner_node,current_node):
                steiner_tree.add_edge(steiner_node,current_node)
        if check_terminals_connected(steiner_tree,terminals):
            break

    # Remove cycles if any
    while True:
        try:
            cycle = nx.find_cycle(steiner_tree)
            edge = cycle[0]
            steiner_tree.remove_edge(edge[0],edge[1])
        except:
            break

    return steiner_tree



