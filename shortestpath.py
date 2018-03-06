import networkx as nx


def get_paths(graph,source,target):
    return list(nx.all_simple_paths(graph,source,target))


def get_path_cost(graph,path):
    cost = 0
    weight = nx.get_node_attributes(graph,'weight')
    for node in path:
        cost = cost + weight[node]
    return cost


def get_least_cost_path(graph,paths):
    min_cost_path = None
    min_cost = float("inf")
    for path in paths:
        cost = get_path_cost(graph,path)
        if cost < min_cost:
            min_cost = cost
            min_cost_path = path
    return min_cost_path,min_cost


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
    num_terminals = len(terminals)
    all_terminal_paths = list()
    for i in range(0,num_terminals):
        for j in range(i+1,num_terminals):
            paths = get_paths(graph,terminals[i],terminals[j])
            least_cost_path,least_cost = get_least_cost_path(graph,paths)
            path = dict()
            path['cost'] = least_cost
            path['path'] = least_cost_path
            all_terminal_paths.append(path)

    all_terminal_paths.sort(lambda x:x['cost'])
    for t_path in all_terminal_paths:
        steiner_tree.add_path(t_path)
        if check_terminals_connected(steiner_tree,terminals):
            break

    while True:
        try:
            cycle = nx.find_cycle(steiner_tree)
            edge = cycle[0]
            steiner_tree.remove_edge(edge[0],edge[1])
        except:
            break
    return steiner_tree
