import env
import pharmacy
import trajectory_tree as tt

saved_Q_table = dict()
plot_graph = pharmacy.plot_graph
train = True

    
# trim plotgraph to fit labels
plot_graph.trim_to_fit_labels(env.action_labels, 0.6)
pharm_tree = tt.Tree()
#generate trajectory tree
pharm_tree.generate_tree_from_plot_graph(plot_graph, plot_graph.get_event("Stand in line"))
#pharm_tree.to_string()




if train:
    #train the model
    for i in range(10000):
        saved_Q_table = env.run(Q_table=saved_Q_table, tree=pharm_tree, render=False, learn=True, playable=False)
    #run the trained model
    env.run(Q_table=saved_Q_table, tree=pharm_tree, render=True, learn=False, playable=False)
else:
    #play the model
    env.run(Q_table=saved_Q_table, tree=pharm_tree, render=True, learn=False, playable=True)

