import trajectory_tree as tt
import plot_graph as p


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