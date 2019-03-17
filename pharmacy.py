import trajectory_tree as tt
import plot_graph as p

#for test
action_labels = [[0, "move left"], 
                   [1, "move right"],
                   [2, "move up"],
                   [3, "move down"],
                   [4, "go into pharmacy"],
                   [5, "go into bank"], #not implemented
                   [6, "go into doctor's office"], #not implemented
                   [7, "look for drugs"],
                   [8, "pick up drug"],
                   [9, "stand in line"],
                   [10, "wait"],
                   [11, "order drugs"],
                   [12, "ask for request"],
                   [13, "ask for prescription"],
                   [14, "produce prescription"],
                   [15, "don't produce prescription"],
                   [16, "refuse to sell"],
                   [17, "pay cash"], #not implemented
                   [18, "hand over drugs"], 
                   [19, "hand over receipt"], 
                   [20, "take drugs"], 
                   [21, "take receipt"],
                   [22, "accept prescription"],
                   [23, "leave pharmacy"],
                   [24, "skip line"]
                  ] 

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
plot_graph.add_new_event("Customer can't produce prescription")
plot_graph.add_new_event("Pharmacist refuses to sell")

#add before relations

plot_graph.get_event("Stand in line").is_before(plot_graph.get_event("Customer order drugs"))
plot_graph.get_event("Customer order drugs").is_before(plot_graph.get_event("Pharmacist asks for prescription"))
plot_graph.get_event("Pharmacist asks for prescription").is_before(plot_graph.get_event("Customer produces prescription"))
plot_graph.get_event("Pharmacist asks for prescription").is_before(plot_graph.get_event("Customer can't produce prescription"))
plot_graph.get_event("Customer produces prescription").is_before(plot_graph.get_event("Pharmacist checks prescription"))
plot_graph.get_event("Pharmacist checks prescription").is_before(plot_graph.get_event("Pharmacist delivers drugs"))
plot_graph.get_event("Pharmacist delivers drugs").is_before(plot_graph.get_event("Customer pays cash"))
plot_graph.get_event("Pharmacist delivers drugs").is_before(plot_graph.get_event("Customer swipes card"))
plot_graph.get_event("Customer pays cash").is_before(plot_graph.get_event("Customer takes change"))
plot_graph.get_event("Customer takes change").is_before(plot_graph.get_event("Customer leaves"))
plot_graph.get_event("Customer pays cash").is_before(plot_graph.get_event("Customer takes receipt"))
plot_graph.get_event("Customer swipes card").is_before(plot_graph.get_event("Customer takes receipt"))
plot_graph.get_event("Customer takes receipt").is_before(plot_graph.get_event("Customer leaves"))
plot_graph.get_event("Customer can't produce prescription").is_before(plot_graph.get_event("Pharmacist refuses to sell"))
plot_graph.get_event("Pharmacist refuses to sell").is_before(plot_graph.get_event("Customer leaves"))

# add mutual exclution
plot_graph.create_mutual_exclusivity(plot_graph.get_event("Customer produces prescription"), plot_graph.get_event("Customer can't produce prescription"))
plot_graph.create_mutual_exclusivity(plot_graph.get_event("Customer pays cash"), plot_graph.get_event("Customer swipes card"))

plot_graph.trim_to_fit_labels(action_labels,0.6)

pharm_tree = tt.Tree()
pharm_tree.generate_tree_from_plot_graph(plot_graph, plot_graph.get_event("Stand in line"))
pharm_tree.to_string()