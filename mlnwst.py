import networkx as nx
import random


def generate_graph(num_vertices,a,b):
    graph = nx.complete_graph(num_vertices)
    nodes = list(graph.nodes)
    for node in nodes:
        graph.nodes[node]['weight'] = random.uniform(a,b)
    return graph


def get_path_cost(graph,path,source,target):
    cost = 0
    for node in path:
        if node is not source and node is not target:
            cost = cost + graph.nodes[node]['weight']

    return cost


def get_path_least_cost(graph,paths,source,target):
    min_cost = float("inf")
    min_path = None
    for path in paths:
        cost = get_path_cost(graph,path,source,target)
        if cost < min_cost:
            min_cost = cost
            min_path = path
    return min_path,min_cost

def get_node_tree_distance(graph,tree,node):
    tree_nodes = list(tree.nodes)
    min_cost = float("inf")
    min_path = None
    for tree_node in tree_nodes:
        paths = list(nx.all_simple_paths(graph,node,tree_node))
        path,cost = get_path_least_cost(graph,paths,node,tree_node)
        if cost < min_cost:
            min_cost = cost
            min_path = path

    return min_path,min_cost


def compute_quotient_cost(graph,trees,node):
    distances = []
    for tree in trees:
        path,cost = get_node_tree_distance(graph,tree,node)
        pair = {}
        pair['tree'] = tree
        pair['distance'] = cost
        distances.append(pair)

    # sort distances from node to all trees and then take subsets of trees
    distances.sort(key=lambda x:x.dist)

    # compute min cost node spider ratio

def iterate_steiner(graph,trees):
    graph_nodes = list(graph.nodes)
    for graph_node in graph_nodes:
        compute_quotient_cost(graph,trees,graph_node)

def approximate_steiner(graph,terminals):
    trees = []
    for node in terminals:
        gr = nx.Graph()
        gr.add_node(node)
        trees.append(gr)

    while len(trees) > 1:
        trees = iterate_steiner(graph,trees)