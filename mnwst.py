import networkx as nx
import nwst


class MultiLevelGraph:
    def __init__(self,levels):
        self.levels = levels
        self.terminal_sets = list()
        self.graph = None
        self.steiner_trees = list()
        self.steiner_costs = list()

    def set_terminal_set(self,level,terminals):
        self.terminal_sets.insert(level,terminals)

    def set_graph(self,g):
        self.graph = g

    def approximate_steiner(self):
        for i in range(0,self.levels):
            steiner_tree,steiner_cost = nwst.approximate_steiner(self.graph,self.terminal_sets[i])
            self.steiner_trees.insert(i,steiner_tree)
            self.steiner_costs.insert(i,steiner_cost)

    def get_steiner_trees(self):
        return self.steiner_trees,self.steiner_costs