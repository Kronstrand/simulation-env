import trajectory_tree as tt
import plot_graph as p

'''
#for test
action_labels = [[0, "move left"], 
                   [1, "move right"],
                   [2, "move up"],
                   [3, "move down"],
                   [4, "go into pharmacy"],
                   #[5, "go into bank"], #not implemented
                   #[6, "go into doctor's office"], #not implemented
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
                   #[17, "pay cash"], #not implemented
                   [18, "hand over drugs"], 
                   [19, "hand over receipt"], 
                   [20, "take drugs"], 
                   [21, "take receipt"],
                   [22, "accept prescription"],
                   [23, "leave pharmacy"],
                   [24, "skip line"]
                  ] 
'''
plot_graph = p.Plot_Graph()

#add events

plot_graph.add_new_event("Customer stand in line")
plot_graph.add_new_event("Customer order drugs")
plot_graph.add_new_event("Pharmacist ask prescription")
plot_graph.add_new_event("Customer produce prescription")
plot_graph.add_new_event("Pharmacist check prescription")
plot_graph.add_new_event("Pharmacist deliver drugs")
plot_graph.add_new_event("Customer pay cash")
plot_graph.add_new_event("Customer swipe card")
plot_graph.add_new_event("Customer take change")
plot_graph.add_new_event("Customer take receipt")
plot_graph.add_new_event("Customer leave pharmacy")
plot_graph.add_new_event("Customer can't produce prescription")
plot_graph.add_new_event("Pharmacist refuse to sell")

#add before relations

plot_graph.get_event("Customer stand in line").is_before(plot_graph.get_event("Customer order drugs"))
plot_graph.get_event("Customer order drugs").is_before(plot_graph.get_event("Pharmacist ask prescription"))
plot_graph.get_event("Pharmacist ask prescription").is_before(plot_graph.get_event("Customer produce prescription"))
plot_graph.get_event("Pharmacist ask prescription").is_before(plot_graph.get_event("Customer can't produce prescription"))
plot_graph.get_event("Customer produce prescription").is_before(plot_graph.get_event("Pharmacist check prescription"))
plot_graph.get_event("Pharmacist check prescription").is_before(plot_graph.get_event("Pharmacist deliver drugs"))
plot_graph.get_event("Pharmacist deliver drugs").is_before(plot_graph.get_event("Customer pay cash"))
plot_graph.get_event("Pharmacist deliver drugs").is_before(plot_graph.get_event("Customer swipe card"))
plot_graph.get_event("Customer pay cash").is_before(plot_graph.get_event("Customer take change"))
plot_graph.get_event("Customer take change").is_before(plot_graph.get_event("Customer leave pharmacy"))
plot_graph.get_event("Customer pay cash").is_before(plot_graph.get_event("Customer take receipt"))
plot_graph.get_event("Customer swipe card").is_before(plot_graph.get_event("Customer take receipt"))
plot_graph.get_event("Customer take receipt").is_before(plot_graph.get_event("Customer leave pharmacy"))
plot_graph.get_event("Customer can't produce prescription").is_before(plot_graph.get_event("Pharmacist refuse to sell"))
plot_graph.get_event("Pharmacist refuse to sell").is_before(plot_graph.get_event("Customer leave pharmacy"))

# add mutual exclution
plot_graph.create_mutual_exclusivity(plot_graph.get_event("Customer produce prescription"), plot_graph.get_event("Customer can't produce prescription"))
plot_graph.create_mutual_exclusivity(plot_graph.get_event("Customer pay cash"), plot_graph.get_event("Customer swipe card"))

#plot_graph.trim_to_fit_labels(action_labels, 0.6)

#pharm_tree = tt.Tree()
#pharm_tree.generate_tree_from_plot_graph(plot_graph, plot_graph.get_event("Stand in line"))
#pharm_tree.to_string()