import networkx as nx
import networkx.algorithms as alg
import time
import networkx.algorithms.shortest_paths as sp
from operator import attrgetter,itemgetter



di_graph = None
all_distances = None
all_predecessors = None
all_paths = None


def get_path_cost(graph,path,source,target,weights):
    """
    Gets the cost of the path 'path' excluding the cost of the endpoints in the patg
    :param graph: input graph
    :param path: path between source and target in the input graph
    :param source: one of the endpoints in the path
    :param target: other endpoint in the path
    :return: Cost of path 'path' in input graph
    """
    if path is None:
        return float("inf")
    cost = 0
    for node in path:
        if node is not source and node is not target:
            cost = cost + weights[node]
    return cost


def get_path_least_cost(graph,paths,source,target,weights):
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
        cost = get_path_cost(graph,path,source,target,weights)
        if cost < min_cost:
            min_cost = cost
            min_path = path
    return min_path,min_cost


def get_node_tree_distance(graph,tree,node,weights):
    """
    Get min distance between node 'node' and any node in tree 'tree'
    :param graph: input undirected graph
    :param tree: A tree with a subset of nodes and edges of the input graph
    :param node: A node in the input graph
    :return: Get min distance between node and any node in tree along with the path
    """
    global di_graph,all_predecessors,all_paths
    tree_nodes = tree.nodes()
    min_cost = float("inf")
    min_path = None

    #print("Finding node "+str(node)+" to tree distance")
    for tree_node in tree_nodes:
        # paths = list(nx.shortest_simple_paths(graph,node,tree_node))
        # path,cost = get_path_least_cost(graph,paths,node,tree_node,weights)
        # path1 = alg.shortest_path(di_graph,node,tree_node,weight='weight')
        # path2 = alg.shortest_path(di_graph,tree_node,node,weight='weight')
        # cost1 = get_path_cost(graph,path1,node,tree_node,weights)
        # cost2 = get_path_cost(graph,path2,tree_node,node,weights)
        # # path1 = get_path(node,tree_node)
        # path2 = get_path(tree_node,node)
        path1 = all_paths[node][tree_node]
        path2 = all_paths[tree_node][node]
        cost1 = get_path_cost(graph,path1,node,tree_node,weights)
        cost2 = get_path_cost(graph,path2,tree_node,node,weights)
        # cost1 =  all_distances[node][tree_node]
        # cost2 = all_distances[tree_node][node]
        if cost1 < cost2:
            cost = cost1
            path = path1
        else:
            cost = cost2
            path = path2
        if cost < min_cost:
            min_cost = cost
            min_path = path

    return min_path,min_cost


def compute_quotient_cost(graph,trees,node,weights):
    """
    Compute quotient cost (spider ratio) for vertex 'node' in the graph with respect to the set of trees 'trees'
    :param graph: input graph
    :param trees: set of trees in the Steiner algorithm iteration
    :param node: node in the input graph
    :return: subset of trees corresponding to quotient, trees not part of the subset and the quotient cost value
    """
    distances = []
    for tree in trees:
        path,cost = get_node_tree_distance(graph,tree,node,weights)
        pair = {}
        pair['tree'] = tree
        pair['distance'] = cost
        distances.append(pair)

    # sort distances from node to all trees and then take subsets of trees
    distances.sort(key=itemgetter('distance'))

    # compute min cost node spider ratio - consider subsets of atleast size 2
    subset = list()
    subset.append(distances[0]['tree'])
    subset.append(distances[1]['tree'])

    #weights = nx.get_node_attributes(graph,'weight')

    min_spider_ratio = (weights[node] + distances[0]['distance'] + distances[1]['distance'])/2
    min_subset = list(subset)
    i = 2
    remaining_trees = list()
    tree_distance = list()
    tree_distance.append(distances[0]['distance'])
    for j in range(1,len(trees)):
        tree_distance.append(tree_distance[j-1] + distances[j]['distance'])
    for k in range(2,len(trees)):
        remaining_trees.append(distances[k]['tree'])
    while i < len(trees):
        subset.append(distances[i]['tree'])
        #tree_distance = 0
        # for j in range(0,i+1):
        #     tree_distance = tree_distance + distances[j]['distance']
        spider_ratio = (weights[node] + tree_distance[i])/(i+1)
        if spider_ratio <= min_spider_ratio:
            min_spider_ratio = spider_ratio
            min_subset = list(subset)
            remaining_trees = []
            for k in range(i+1,len(trees)):
                remaining_trees.append(distances[k]['tree'])
        i += 1

    return min_subset,remaining_trees,min_spider_ratio


def iterate_steiner(graph,trees,weights):
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
        subset,remaining_trees,ratio = compute_quotient_cost(graph,trees,graph_node,weights)
        if ratio < min_ratio:
            min_ratio = ratio
            min_subset_trees = list(subset)
            min_node = graph_node
            min_remaining_trees = list(remaining_trees)
    return min_node,min_remaining_trees,min_subset_trees,min_ratio


def check_cycle(graph):
    try:
        alg.find_cycle(graph)
        return True
    except:
        return False

def merge_node_trees(graph,node,subset,remaining_trees,weights):
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
        min_path,min_cost = get_node_tree_distance(graph,tree,node,weights)
        merged_tree.add_path(min_path)
        for curr_node in list(tree.nodes):
            merged_tree.add_node(curr_node)
        for curr_edge in list(tree.edges):
            merged_tree.add_edge(curr_edge[0],curr_edge[1])

    # Remove any cycles created by merging trees into one
    cycle_exists = True
    while cycle_exists:
        try:
             cycle = alg.find_cycle(merged_tree)
             edge = cycle[0]
             merged_tree.remove_edge(edge[0],edge[1])
        except:
            cycle_exists = False

    merged_trees.append(merged_tree)
    for tree in remaining_trees:
        merged_trees.append(tree)
    return merged_trees


def preprocess_graph(graph,weights):
    global di_graph, all_predecessors, all_distances, all_paths
    di_graph = nx.DiGraph()
    for edge in list(graph.edges):
        di_graph.add_edge(edge[0], edge[1], weight=weights[edge[1]])
        di_graph.add_edge(edge[1], edge[0], weight=weights[edge[0]])

    print('Computing oracle by preprocessing digraph')
    # all_predecessors,all_distances = sp.floyd_warshall_predecessor_and_distance(di_graph)
    # all_predecessors = dict(all_predecessors)
    # all_distances = dict(all_distances)
    start = time.time()
    all_paths = sp.johnson(di_graph, weight='weight')
    nodes = list(graph.nodes)
    all_distances = dict()
    # for node1 in nodes:
    #     for node2 in nodes:
    #             if node1 not in all_distances:
    #                 all_distances[node1] = dict()
    #             all_distances[node1][node2] = get_path_cost(graph,all_paths[node1][node2],node1,node2,weights)
    end = time.time()

    elapsed = end - start
    print('Time taken in seconds to process graph ' + str(elapsed))

    print('Finished computing APSP')

def approximate_steiner(graph,terminals,weights):
    """
    Approximate minimum node-weighted steiner tree for terminal set 'terminals' in input graph
    :param graph: input graph
    :param terminals: set of vertices, subset of vertices in input
    :return: The approximation of the minimum Steiner tree
    """


    print('Computing steiner tree')
    start = time.time()
    trees = []
    for node in terminals:
        gr = nx.Graph()
        gr.add_node(node)
        trees.append(gr)


    while len(trees) > 1:
        node,remaining_trees,subset_trees,min_ratio = iterate_steiner(graph,trees,weights)
        #print("Select node to be merged is "+str(node)+" with subset size "+str(len(subset_trees)))
        trees = merge_node_trees(graph,node,subset_trees,remaining_trees,weights)
        # for tree in trees:
        #     try:
        #         if alg.find_cycle(tree):
        #             print("Cycle exists")
        #     except:
        #         pass

    steiner_tree = trees[0]
    steiner_cost = 0
    #weights = nx.get_node_attributes(graph,'weight')
    for node in list(steiner_tree.nodes):
        steiner_cost = steiner_cost + weights[node]
    # try:
    #     alg.find_cycle(steiner_tree)
    # except:
    #     print('No cycle')
    #
    # for i in range(len(terminals)):
    #     for j in range(i+1,len(terminals)):
    #         if not nx.has_path(steiner_tree,terminals[i],terminals[j]):
    #             print('Error')
    end = time.time()
    elapsed =  end - start
    print ('Computed steiner tree in '+str(elapsed)+' seconds')
    return steiner_tree,steiner_cost

