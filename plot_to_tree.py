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

pharm_tree = tt.Tree()
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
#test_tree.generate_tree_from_plot_graph(pg2, pg2.get_event("katten løber"))
#test_tree.to_string()


#add events
bank_plot = p.Plot_Graph()
bank_plot.add_new_event("Sally puts money in bag")
bank_plot.add_new_event("Sally gives John bag")
bank_plot.add_new_event("Sally presses alarm")
bank_plot.add_new_event("John takes bag")
bank_plot.add_new_event("John leaves bank")
bank_plot.add_new_event("Polices arives")
bank_plot.add_new_event("Sally calls police")
bank_plot.add_new_event("Police arrests John")

# add before constraints
bank_plot.get_event("Sally puts money in bag").is_before(bank_plot.get_event("Sally gives John bag"))
bank_plot.get_event("Sally puts money in bag").is_before(bank_plot.get_event("Sally presses alarm"))
bank_plot.get_event("Sally gives John bag").is_before(bank_plot.get_event("John takes bag"))
bank_plot.get_event("Sally presses alarm").is_before(bank_plot.get_event("John takes bag"))
bank_plot.get_event("John takes bag").is_before(bank_plot.get_event("John leaves bank"))
bank_plot.get_event("John leaves bank").is_before(bank_plot.get_event("Polices arives"))
bank_plot.get_event("John leaves bank").is_before(bank_plot.get_event("Sally calls police"))
bank_plot.get_event("Sally calls police").is_before(bank_plot.get_event("Police arrests John"))
bank_plot.get_event("Polices arives").is_before(bank_plot.get_event("Police arrests John"))

# add mutual exclution
bank_plot.create_mutual_exclusivity(bank_plot.get_event("Sally presses alarm"), bank_plot.get_event("Sally calls police"))
bank_plot.get_event("Sally presses alarm").set_type("optional")
bank_plot.get_event("Sally calls police").set_type("conditional")
bank_plot.create_mutual_exclusivity(bank_plot.get_event("John leaves bank"), bank_plot.get_event("Polices arives"))
bank_plot.get_event("John leaves bank").set_type("optional")
bank_plot.get_event("Polices arives").set_type("conditional")

#generate bank tree
bank_tree = tt.Tree()
bank_tree.generate_tree_from_plot_graph(bank_plot, bank_plot.get_event("Sally puts money in bag"))
bank_tree.to_string()









