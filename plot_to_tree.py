import trajectory_tree as tt
import plot_graph as p

plot_graph = p.Plot_Graph()

#add events

plot_graph.add_new_event("Stand in line")
plot_graph.add_new_event("Customer order drugs")
plot_graph.add_new_event("Pharmacist asks for prescription")
plot_graph.add_new_event("Customer produces prescription")
plot_graph.add_new_event("Pharmacist checks prescription")
plot_graph.add_new_event("Pharmacist delivers drugs")
plot_graph.add_new_event("Customer pays cash")
plot_graph.add_new_event("Customer swipes card")
plot_graph.add_new_event("Customer takes change")
plot_graph.add_new_event("Customer takes receipt")
plot_graph.add_new_event("Customer leaves")
plot_graph.add_new_event("Customer cannot produce prescription")
plot_graph.add_new_event("Pharmacist refuses to sell")

#add before relations

plot_graph.get_event("Stand in line").is_before(plot_graph.get_event("Customer order drugs"))
plot_graph.get_event("Customer order drugs").is_before(plot_graph.get_event("Pharmacist asks for prescription"))
plot_graph.get_event("Pharmacist asks for prescription").is_before(plot_graph.get_event("Customer produces prescription"))
plot_graph.get_event("Pharmacist asks for prescription").is_before(plot_graph.get_event("Customer cannot produce prescription"))
plot_graph.get_event("Customer produces prescription").is_before(plot_graph.get_event("Pharmacist checks prescription"))
plot_graph.get_event("Pharmacist checks prescription").is_before(plot_graph.get_event("Pharmacist delivers drugs"))
plot_graph.get_event("Pharmacist delivers drugs").is_before(plot_graph.get_event("Customer pays cash"))
plot_graph.get_event("Pharmacist delivers drugs").is_before(plot_graph.get_event("Customer swipes card"))
plot_graph.get_event("Customer pays cash").is_before(plot_graph.get_event("Customer takes change"))
plot_graph.get_event("Customer takes change").is_before(plot_graph.get_event("Customer leaves"))
plot_graph.get_event("Customer pays cash").is_before(plot_graph.get_event("Customer takes receipt"))
plot_graph.get_event("Customer swipes card").is_before(plot_graph.get_event("Customer takes receipt"))
plot_graph.get_event("Customer takes receipt").is_before(plot_graph.get_event("Customer leaves"))
plot_graph.get_event("Customer cannot produce prescription").is_before(plot_graph.get_event("Pharmacist refuses to sell"))
plot_graph.get_event("Pharmacist refuses to sell").is_before(plot_graph.get_event("Customer leaves"))

# add mutual exclution
plot_graph.create_mutual_exclusivity(plot_graph.get_event("Customer produces prescription"), plot_graph.get_event("Customer cannot produce prescription"))
plot_graph.create_mutual_exclusivity(plot_graph.get_event("Customer pays cash"), plot_graph.get_event("Customer swipes card"))

#pharm_tree = tt.Tree()
#pharm_tree.generate_tree_from_plot_graph(plot_graph, plot_graph.get_event("Stand in line"))
#pharm_tree.to_string()

tree = tt.Tree()

rootNode = tt.Tree_Node("root")
tree.add_new_node(rootNode)
childNode = tt.Tree_Node("child1")
tree.add_new_child(rootNode, childNode)
tree.add_new_child(rootNode, childNode)
tree.add_new_child(rootNode, childNode)
tree.add_new_child(rootNode, childNode)
childNode2 = tt.Tree_Node("child2")
tree.add_new_child(childNode, childNode2)


#tree.to_string()

pg2 = p.Plot_Graph()
pg2.add_new_event("katten løber")
pg2.add_new_event("katten falder")
pg2.get_event("katten løber").is_before(pg2.get_event("katten falder"))

test_tree = tt.Tree()
test_tree.generate_tree_from_plot_graph(pg2, pg2.get_event("katten løber"))
test_tree.to_string()









