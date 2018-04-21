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
            steiner_tree,steiner_cost = nwst.approximate_steiner(self.graph,self.terminal_sets[i],weights)
            cost = 0
            for node in list(steiner_tree.nodes):
                cost = cost + self.weights[node]
            print('Cost is '+str(cost))
            # for terminal in self.terminal_sets[i]:
            #     if terminal not in steiner_tree.nodes:
            #         print('Fail')
            self.steiner_trees.insert(i, steiner_tree)
            self.steiner_costs.insert(i, steiner_cost)

    def approximate_steiner_bottom_up(self):
        for i in range(self.levels-1,-1,-1):
            weights = self.get_level_weights(i)
            print('Finding NWST for level ' + str(i))
            steiner_tree, steiner_cost = nwst.approximate_steiner(self.graph, self.terminal_sets[i], weights)
            print('Cost is ' + str(steiner_cost))
            # for terminal in self.terminal_sets[i]:
            #     if terminal not in steiner_tree.nodes:
            #         print('Fail')
            self.steiner_trees.insert(i, steiner_tree)
            self.steiner_costs.insert(i, steiner_cost)

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