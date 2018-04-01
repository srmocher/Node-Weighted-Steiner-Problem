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

    def approximate_steiner(self):
        for i in range(0,self.levels):
            weights = self.get_level_weights(i)
            print('Finding NWST for level '+str(i))
            steiner_tree,steiner_cost = nwst.approximate_steiner(self.graph,self.terminal_sets[i],weights)
            self.steiner_trees.insert(i,steiner_tree)
            self.steiner_costs.insert(i,steiner_cost)

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