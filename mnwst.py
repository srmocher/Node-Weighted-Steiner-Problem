import networkx as nx
import nwst


class MultiLevelGraph:
    def __init__(self,graph,terminal_sets,levels):
        self.levels = levels
        self.terminal_sets = terminal_sets
        self.graph = graph
        self.steiner_trees = list()
        self.steiner_costs = list()
        self.weights = nx.get_node_attributes(graph,'weight')
        nwst.preprocess_graph(self.graph,self.weights)

    def approximate_steiner_top_down(self):
        for i in range(self.levels):
            weights = self.get_level_weights(i)
            print('Finding NWST for level '+str(i))
            if i > 0:
                prev_level_nodes = self.steiner_trees[i-1].nodes()
                for n in prev_level_nodes:
                    weights[n] = 0
            steiner_tree,steiner_cost = nwst.approximate_steiner(self.graph,self.terminal_sets[i],weights)
            cost = 0
            for node in list(steiner_tree.nodes):
                cost = cost + self.weights[node]
            print('Cost is '+str(cost))
            self.steiner_trees.insert(i, steiner_tree)
            self.steiner_costs.insert(i, steiner_cost)

    def approximate_steiner_bottom_up(self):
        print('Running heurisitc on bottom level')
        weights = self.get_level_weights(self.levels-1)
        steiner_tree,steiner_cost = nwst.approximate_steiner(self.graph,self.terminal_sets[self.levels-1],weights)
        self.steiner_trees.insert(self.levels-1,steiner_tree)
        self.steiner_costs.insert(self.levels-1,steiner_cost)
        cost = 0
        for node in steiner_tree.nodes():
            cost = cost + self.weights[node]
        print('Cost of bottom level is '+str(cost))
        for i in range(self.levels-2,-1,-1):
            new_steiner_tree = steiner_tree.copy()
            terminals = self.terminal_sets[i]
            for edge in steiner_tree.edges():
                if edge[0] not in terminals and edge[1] not in terminals:
                    new_steiner_tree.remove_edge(edge[0],edge[1])
                    if edge[0] in new_steiner_tree.nodes() and new_steiner_tree.degree[edge[0]] == 0:
                        new_steiner_tree.remove_node(edge[0])
                    if edge[1] in new_steiner_tree.nodes() and new_steiner_tree.degree[edge[1]] == 0:
                        new_steiner_tree.remove_node(edge[1])
            for terminal in terminals:
                if terminal not in steiner_tree.nodes():
                    print("FAiled not a")

            steiner_tree = new_steiner_tree.copy()
            self.steiner_trees.insert(i,steiner_tree)
            cost = 0
            for node in steiner_tree.nodes():
                cost = cost + self.weights[node]
            self.steiner_costs.insert(i,cost)
            print('Cost of level '+str(i)+' is '+str(cost))
        return self.steiner_trees,self.steiner_costs
    def get_level_weights(self,level):
        terminals = self.terminal_sets[level]
        nodes = list(self.graph.nodes)
        weights = dict()
        for node in nodes:
            if node in terminals:
                weights[node] = 0
            else:
                weights[node] = self.weights[node]
        return weights

    def get_steiner_trees(self):
        return self.steiner_trees,self.steiner_costs