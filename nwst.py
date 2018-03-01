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

    # compute min cost node spider ratio - consider subsets of atleast size 2
    subset = trees[0:2]

    min_spider_ratio = (node['weight'] + distances[0]['distance'] + distances[0]['distance'])/2
    min_subset = subset
    i = 2
    while i < len(trees):
        subset.append(trees[i])
        tree_distance = 0
        for j in range(0,i+1):
            tree_distance = tree_distance + distances[i]['distance']
        spider_ratio = (node['weight'] + tree_distance)/i
        if spider_ratio < min_spider_ratio:
            min_spider_ratio = spider_ratio
            min_subset = subset

    return min_subset,min_spider_ratio


def iterate_steiner(graph,trees):
    graph_nodes = list(graph.nodes)
    min_ratio = float("inf")
    min_node = None
    min_subset_trees = None
    for graph_node in graph_nodes:
        subset,ratio = compute_quotient_cost(graph,trees,graph_node)
        if ratio < min_ratio:
            min_ratio = ratio
            min_subset_trees = subset
            min_node = graph_node
    return min_node,min_subset_trees


def merge_node_trees(graph,node,trees,subset):
    print("Merging selected node with subset of trees along shortest path from that node")
    for tree in subset:
        trees.remove(tree)

    merged_tree = nx.Graph()
    for tree in subset:
        min_path,min_cost = get_node_tree_distance(graph,tree,node)
        merged_tree.add_path(min_path)

    trees.append(merged_tree)
    return trees


def approximate_steiner(graph,terminals):
    trees = []
    for node in terminals:
        gr = nx.Graph()
        gr.add_node(node)
        trees.append(gr)

    while len(trees) > 1:
        node,subset_trees = iterate_steiner(graph,trees)
        trees = merge_node_trees(graph,node,trees,subset_trees)