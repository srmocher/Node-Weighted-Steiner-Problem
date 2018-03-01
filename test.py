import nwst

graph = nwst.generate_graph(5,2,4)
terminals = [0,2,4]

steiner_tree = nwst.approximate_steiner(graph,terminals)