import networkx as nx
import random
import matplotlib.pyplot as plt


def generate_graph(num_vertices,a,b):
    """
    Generates a complete undirected graph with num_vertices vertices and node weights in the range [a,b)
    :param num_vertices: Number of vertices in the complete graph
    :param a: lower bound for node weight
    :param b: upper bound for node weight
    :return: A complete graph
    """
    graph = nx.complete_graph(num_vertices)
    nodes = list(graph.nodes)
    for node in nodes:
        graph.nodes[node]['weight'] = random.uniform(a,b)
    return graph


def get_path_cost(graph,path,source,target):
    """
    Gets the cost of the path 'path' excluding the cost of the endpoints in the patg
    :param graph: input graph
    :param path: path between source and target in the input graph
    :param source: one of the endpoints in the path
    :param target: other endpoint in the path
    :return: Cost of path 'path' in input graph
    """
    cost = 0
    for node in path:
        if node is not source and node is not target:
            cost = cost + graph.nodes[node]['weight']
    return cost


def get_path_least_cost(graph,paths,source,target):
    """
    Gets path of least cost from all paths in 'paths'
    :param graph: input graph
    :param paths: list of paths in graph from source to target nodes
    :param source: endpoint of path
    :param target: other endpoint in path
    :return: the path with least cost
    """
    min_cost = float("inf")
    min_path = None
    for path in paths:
        cost = get_path_cost(graph,path,source,target)
        if cost < min_cost:
            min_cost = cost
            min_path = path
    return min_path,min_cost


def get_node_tree_distance(graph,tree,node):
    """
    Get min distance between node 'node' and any node in tree 'tree'
    :param graph: input undirected graph
    :param tree: A tree with a subset of nodes and edges of the input graph
    :param node: A node in the input graph
    :return: Get min distance between node and any node in tree along with the path
    """
    tree_nodes = list(tree.nodes)
    min_cost = float("inf")
    min_path = None
    #print("Finding node "+str(node)+" to tree distance")
    for tree_node in tree_nodes:
        paths = list(nx.all_simple_paths(graph,node,tree_node))
        path,cost = get_path_least_cost(graph,paths,node,tree_node)
        if cost < min_cost:
            min_cost = cost
            min_path = path

    return min_path,min_cost


def compute_quotient_cost(graph,trees,node):
    """
    Compute quotient cost (spider ratio) for vertex 'node' in the graph with respect to the set of trees 'trees'
    :param graph: input graph
    :param trees: set of trees in the Steiner algorithm iteration
    :param node: node in the input graph
    :return: subset of trees corresponding to quotient, trees not part of the subset and the quotient cost value
    """
    distances = []
    for tree in trees:
        path,cost = get_node_tree_distance(graph,tree,node)
        pair = {}
        pair['tree'] = tree
        pair['distance'] = cost
        distances.append(pair)

    # sort distances from node to all trees and then take subsets of trees
    distances.sort(key=lambda x:x['distance'])

    # compute min cost node spider ratio - consider subsets of atleast size 2
    subset = list()
    subset.append(distances[0]['tree'])
    subset.append(distances[1]['tree'])

    weights = nx.get_node_attributes(graph,'weight')
    if node not in weights:
        print('Found')
    min_spider_ratio = (weights[node] + distances[0]['distance'] + distances[1]['distance'])/2
    min_subset = list(subset)
    i = 2
    remaining_trees = list()
    for k in range(2,len(trees)):
        remaining_trees.append(distances[k]['tree'])
    while i < len(trees):
        subset.append(distances[i]['tree'])
        tree_distance = 0
        for j in range(0,i+1):
            tree_distance = tree_distance + distances[j]['distance']
        spider_ratio = (weights[node] + tree_distance)/(i+1)
        if spider_ratio <= min_spider_ratio:
            min_spider_ratio = spider_ratio
            min_subset = list(subset)
            remaining_trees = []
            for k in range(i+1,len(trees)):
                remaining_trees.append(distances[k]['tree'])
        i += 1

    return min_subset,remaining_trees,min_spider_ratio


def iterate_steiner(graph,trees):
    """
    Runs an iteration of the approximation algorithm
    :param graph: input graph
    :param trees: set of trees obtained in previous iteration
    :return: the node to be selected with least quotient cost and trees to merge along with it
    """
    graph_nodes = list(graph.nodes)
    min_ratio = float("inf")
    min_node = None
    min_subset_trees = None
    min_remaining_trees = None
    for graph_node in graph_nodes:
        subset,remaining_trees,ratio = compute_quotient_cost(graph,trees,graph_node)
        if ratio < min_ratio:
            min_ratio = ratio
            min_subset_trees = list(subset)
            min_node = graph_node
            min_remaining_trees = list(remaining_trees)
    return min_node,min_remaining_trees,min_subset_trees,min_ratio


def merge_node_trees(graph,node,subset,remaining_trees):
    """
    Merges the node with trees in the subset along paths with lowest cost
    :param graph: input graph
    :param node: node to be merged with trees
    :param subset: subset of trees corresponding to min quotient cost to be merged with node
    :param remaining_trees: trees which were not merged
    :return: set of all trees after merging
    """
    #print("Merging selected node with subset of trees along shortest path from that node")
    merged_trees = list()
    merged_tree = nx.Graph()
    for tree in subset:
        min_path,min_cost = get_node_tree_distance(graph,tree,node)
        merged_tree.add_path(min_path)
        for curr_node in list(tree.nodes):
            merged_tree.add_node(curr_node)
        for curr_edge in list(tree.edges):
            merged_tree.add_edge(curr_edge[0],curr_edge[1])

    merged_trees.append(merged_tree)
    for tree in remaining_trees:
        merged_trees.append(tree)
    return merged_trees


def draw_trees(trees):
    for tree in trees:
        nx.draw(tree,with_labels=True)
    plt.show()


def approximate_steiner(graph,terminals):
    """
    Approximate minimum node-weighted steiner tree for terminal set 'terminals' in input graph
    :param graph: input graph
    :param terminals: set of vertices, subset of vertices in input
    :return: The approximation of the minimum Steiner tree
    """
    trees = []
    for node in terminals:
        gr = nx.Graph()
        gr.add_node(node)
        trees.append(gr)


    while len(trees) > 1:
        node,remaining_trees,subset_trees,min_ratio = iterate_steiner(graph,trees)
        #print("Select node to be merged is "+str(node)+" with subset size "+str(len(subset_trees)))
        trees = merge_node_trees(graph,node,subset_trees,remaining_trees)

    steiner_tree = trees[0]
    steiner_cost = 0
    weights = nx.get_node_attributes(graph,'weight')
    for node in list(steiner_tree.nodes):
        steiner_cost = steiner_cost + weights[node]

    return trees[0],steiner_cost

