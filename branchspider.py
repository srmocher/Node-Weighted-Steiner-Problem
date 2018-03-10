# Placeholder for implementing branch spider approach (Guha,Khuller)
import nwst
import networkx as nx
import math


def find_three_plus_min_ratio_spider(graph,trees):
    nodes = list(graph.nodes)
    min_ratio = float("inf")
    min_subset = None
    min_remaining = None
    min_node = None
    for node in nodes:
        if graph.degree[node] >= 3:
           subset,remaining,ratio = nwst.compute_quotient_cost(graph,trees,node)
           if ratio < min_ratio:
                min_ratio = ratio
                min_subset = subset
                min_remaining = remaining
                min_node = node

    return min_node,min_subset,min_remaining,min_ratio


def check_path_exists(paths,path):
    for p in paths:
        if set(p) == set(path):
            return True

    return False


def contract_spider(graph,spider):
    print('Contracting spider...')

def get_path_cost(graph,path):
    cost  = 0
    weights = nx.get_node_attributes(graph,'weight')
    for node in path:
        cost = cost + weights[node]
    return cost


def find_closest_terminal(graph,node,terminals):
    num_terminals = len(terminals)
    nearest_terminal = None
    min_path = None
    min_cost = float("inf")
    for terminal in terminals:
        if terminal is not node:
            paths = list(nx.all_simple_paths(graph,node,terminal))
            path,cost = nwst.get_path_least_cost(graph,paths,node,terminal)
            if cost < min_cost:
                min_cost = cost
                min_path = path
                nearest_terminal = terminal

    return nearest_terminal,min_path,min_cost


def approximate_steiner(graph,terminals):
    trees = list()
    for terminal in terminals:
        tree = nx.Graph()
        tree.add_node(terminal)
        trees.append(tree)

    while len(trees) > 2:
        node, remaining_trees, subset_trees,min_ratio =  nwst.iterate_steiner(graph,trees)
        if graph.degree[node] >=3:
            print('Found 3+ spider')
        else:
            node,remaining_trees,subset_trees,min_three_plus_spider_ratio = find_three_plus_min_ratio_spider(graph,trees)
            term_term_paths = list()
            for terminal in terminals:
                nearest_terminal,min_path,min_cost =  find_closest_terminal(graph,terminal,terminals)
                path = dict()
                path['cost'] = min_cost
                path['source'] = terminal
                path['target'] = nearest_terminal
                path['path'] = min_path
                term_term_paths.append(path)

            term_term_paths.sort(lambda x:x['cost'])
            S = list()
            for j in range(0,len(term_term_paths)):
                path = term_term_paths[j]
                if path['cost'] <= 2*min(4*min_ratio/3,min_three_plus_spider_ratio):
                    S.append(j)
            distinct_paths = list()
            for j in range(0,len(term_term_paths)):
                if j in S:
                    if not check_path_exists(term_term_paths[j],distinct_paths):
                        distinct_paths.append(term_term_paths[j])

            L_i = len(distinct_paths)
            cost_T = 0
            for path in distinct_paths:
                cost_T = cost_T + get_path_cost(graph,path)

            term_1 = cost_T/(-math.log(1 - L_i/len(trees)))
            term_2 = 2*len(trees)*min_ratio
            term_3 = 1.5*len(trees)*min_three_plus_spider_ratio

            min_term = min(term_1,term_2,term_3)
            if min_term == term_1:
                print('Contract paths induced by forest')
            elif min_term == term_2:
                print('Contract minimum ratio spider')
            else:
                print('Contract min ratio 3+ spider')


