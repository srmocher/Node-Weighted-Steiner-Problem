import graph_generator as gg
import mnwst

params = dict()
params['prob']=0.48
params['neighbors']=3
params['tries']=100
levels = 3
ml_graph, terminal_sets = gg.generate_multi_level_graph(n=20,w_min=2,w_max=10,levels=levels,graph_type="watts-strogatz",params=params)
multi_level_instance = mnwst.MultiLevelGraph(ml_graph,levels=levels,terminal_sets=terminal_sets)
multi_level_instance.approximate_steiner()

