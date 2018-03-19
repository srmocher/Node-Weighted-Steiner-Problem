import networkx as nx
from pulp import *
import numpy as np

# Implementing ILP solver for single level to verify correctness/algorithm approximation bound

class NWSTLPSolver:
    def __init__(self,graph,terminals):
        self.graph = graph
        self.t = terminals
        self.s = []
        nodes = list(graph.nodes)
        for node in nodes:
            if node not in terminals:
                self.s.append(node)
        self.ilp = LpProblem("NWST",sense=LpMinimize)

    def formulate_problem(self):
        weights = nx.get_node_attributes(self.graph,'weight')
        vars = dict()
        print('Each steiner node has a variable in the objective function. Terminal nodes have 1 value by default')
        node_variables = list()
        for i in range(0,len(self.s)):
            var =LpVariable(self.s[i],cat=LpBinary)
            vars[var] = weights[self.s[i]]
            node_variables.append(var)

        obj_function = LpAffineExpression(vars)
        self.ilp += obj_function

        # define constraints to ensure terminals are connected
        for i in range(0,len(self.t)):
            constraint_vars = dict()
            for j in range(0,len(self.s)):
                if self.graph.has_edge(self.t[i],self.s[j]):
                    constraint_vars[node_variables[j]] = 1
            constraint = LpConstraint(constraint_vars,sense=LpConstraintGE,rhs=1)
            self.ilp.addConstraint(constraint)

    def solve_ilp(self):
#        self.ilp.writeLP("nwst.lp")
        self.ilp.solve()
        print("The status : "+LpStatus[self.ilp.status])
        print(self.ilp)
        print("The objective value is "+str(self.ilp.objective.value()))
        variables= self.ilp.variables()
        for variable in variables:
            if variable.varValue == 1:
                print(variable)
        return self.ilp.objective.value()






