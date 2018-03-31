# Placeholder for implementing branch spider approach (Guha,Khuller)
import nwst
import networkx as nx
import math

supernode_spider_mapping = dict()

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


def check_path_exists(path,paths):
    for p in paths:
        if set(p['path']) == set(path):
            return True

    return False


def make_terminals_degree_one(graph,terminals):
    print('Converting graph to one with terminals with all degree 1 and return modified graph and terminal set')
    t = list(terminals)
    nodes = list(graph.nodes)
    edges = list(graph.edges)

    new_terminals = list()
    for node in terminals:
        if graph.degree(node) > 1:
            new_node = max(list(graph.nodes)) + 1
            mapping = dict()
            mapping[node] = new_node
            graph = nx.relabel_nodes(graph,mapping)
            graph.add_node(node)
            graph.nodes[new_node]['weight'] = 0
            graph.nodes[node]['weight'] = 0
            graph.add_edge(new_node,node)
            new_terminals.append(node)
        else:
            new_terminals.append(node)

    return graph,new_terminals



def build_spider(graph, center, subset):
    spider = nx.Graph()
    for tree in subset:
        path, cost = nwst.get_node_tree_distance(graph, tree, center)
        spider.add_path(path)
    return spider

def contract_spider(graph,spider, terminals):

  num_nodes = len(list(graph.nodes))
  new_node = max(list(graph.nodes)) + 1
  cut_nodes = list()
  spider_nodes = list(spider.nodes)
  for edge in list(graph.edges):
      if (edge[0] in  spider_nodes or edge[1] in spider_nodes) and (edge[0] not in spider_nodes and edge[1] not in spider_nodes):
          if edge[0] not in spider_nodes:
            cut_nodes.append(edge[0])
      else:
            cut_nodes.append(edge[1])

  for node in spider_nodes:
      if node in terminals:
            terminals.remove(node)
      graph.remove_node(node)

  graph.add_node(new_node)
  supernode_spider_mapping[new_node] = spider
  graph.nodes[new_node]['weight'] = 0
  terminals.append(new_node)
  for cut_node in cut_nodes:
     graph.add_edge(cut_node,new_node)

  graph,terminals = make_terminals_degree_one(graph,terminals)


  return graph,terminals





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


def extract_steiner_nodes(graph, terminals):
    steiner_tree_nodes = list()
    global supernode_spider_mapping
    for steiner_node in supernode_spider_mapping:
        sub_graph = supernode_spider_mapping[steiner_node]
        for node in list(sub_graph.nodes):
                if (node not in supernode_spider_mapping):
                    steiner_tree_nodes.append(node)

    return steiner_tree_nodes


def build_steiner_tree(steiner_tree_nodes, graph_orig):
    return nx.subgraph(graph_orig, steiner_tree_nodes)

def approximate_steiner(graph,terminals):
    trees = list()

    graph,terminals = make_terminals_degree_one(graph,terminals)
    for terminal in terminals:
        tree = nx.Graph()
        tree.add_node(terminal)
        trees.append(tree)
    n_i = len(terminals)

    graph_orig = nx.Graph(incoming_graph_data=graph)
    while n_i > 2:
        node, remaining_trees, subset_trees,min_ratio = nwst.iterate_steiner(graph,trees)
        if graph.degree[node] >=3:
            graph,terminals = contract_spider(graph,build_spider(graph,node,subset_trees),terminals)
            n_i = len(terminals)
        else:
            node_three_plus,remaining_trees_three_plus,subset_trees_three_plus,min_three_plus_spider_ratio = find_three_plus_min_ratio_spider(graph,trees)
            term_term_paths = list()
            for terminal in terminals:
                nearest_terminal,min_path,min_cost =  find_closest_terminal(graph,terminal,terminals)
                path = dict()
                path['cost'] = min_cost
                path['source'] = terminal
                path['target'] = nearest_terminal
                path['path'] = min_path
                term_term_paths.append(path)

            term_term_paths.sort(key=lambda x:x['cost'])
            S = list()
            for j in range(0,len(term_term_paths)):
                path = term_term_paths[j]
                if path['cost'] <= 2*min(4*min_ratio/3,min_three_plus_spider_ratio):
                    S.append(j)
            distinct_paths = list()
            for j in range(0,len(term_term_paths)):
                if j in S:
                    if not check_path_exists(term_term_paths[j],distinct_paths):
                        distinct_paths.append(term_term_paths[j]['path'])

            L_i = len(distinct_paths)
            cost_T = 0
            all_nodes_paths = set()
            for path in distinct_paths:
                for node in path:
                    all_nodes_paths.add(node)
            for node in all_nodes_paths:
                cost_T = cost_T + graph[node]['weight']

            term_1 = cost_T/(-math.log(1 - L_i/n_i))
            term_2 = 2*len(trees)*min_ratio
            term_3 = 1.5*len(trees)*min_three_plus_spider_ratio

            min_term = min(term_1,term_2,term_3)
            if min_term == term_1:
                spider = nx.Graph()
                for path in distinct_paths:
                    spider.add_path(path)
                graph,terminals = contract_spider(graph,spider,terminals)

            elif min_term == term_2:
                graph, terminals = contract_spider(graph, build_spider(graph, node, subset_trees), terminals)
            else:
                graph,terminals = contract_spider(graph,build_spider(graph,node_three_plus,subset_trees_three_plus),terminals)

            n_i = len(terminals)
        trees = list()
        for terminal in terminals:
            tree = nx.Graph()
            tree.add_node(terminal)
            trees.append(tree)

    source = terminals[0]
    destination = terminals[1]
    paths = nx.all_simple_paths(graph,source,destination)
    path,cost = nwst.get_path_least_cost(graph,paths,source,destination)
    graph.add_path(list(path))

    steiner_nodes = extract_steiner_nodes(graph,terminals)
    steiner_tree = build_steiner_tree(steiner_nodes,graph_orig)
    steiner_cost = 0
    for node in list(steiner_tree.nodes):
        steiner_cost = steiner_cost + graph_orig.nodes[node]['weight']
    return steiner_tree, steiner_cost




