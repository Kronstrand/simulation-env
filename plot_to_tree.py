import trajectory_tree as tt
import plot_graph as p


#add events
bank_plot = p.Plot_Graph()
bank_plot.add_new_event("Sally puts money in bag")
bank_plot.add_new_event("Sally gives John bag")
bank_plot.add_new_event("Sally presses alarm")
bank_plot.add_new_event("John takes bag")
bank_plot.add_new_event("John leaves bank")
bank_plot.add_new_event("Police arrives")
bank_plot.add_new_event("Sally calls police")
bank_plot.add_new_event("Police arrests John")

# add before constraints
bank_plot.get_event("Sally puts money in bag").is_before(bank_plot.get_event("Sally gives John bag"))
bank_plot.get_event("Sally puts money in bag").is_before(bank_plot.get_event("Sally presses alarm"))
bank_plot.get_event("Sally gives John bag").is_before(bank_plot.get_event("John takes bag"))
bank_plot.get_event("Sally presses alarm").is_before(bank_plot.get_event("John takes bag"))
bank_plot.get_event("John takes bag").is_before(bank_plot.get_event("John leaves bank"))
bank_plot.get_event("John leaves bank").is_before(bank_plot.get_event("Police arrives"))
bank_plot.get_event("John leaves bank").is_before(bank_plot.get_event("Sally calls police"))
bank_plot.get_event("Sally calls police").is_before(bank_plot.get_event("Police arrests John"))
bank_plot.get_event("Police arrives").is_before(bank_plot.get_event("Police arrests John"))

# add mutual exclution
bank_plot.create_mutual_exclusivity(bank_plot.get_event("Sally presses alarm"), bank_plot.get_event("Sally calls police"))
bank_plot.get_event("Sally presses alarm").set_type("optional")
bank_plot.get_event("Sally calls police").set_type("conditional")
bank_plot.create_mutual_exclusivity(bank_plot.get_event("John leaves bank"), bank_plot.get_event("Police arrives"))
bank_plot.get_event("John leaves bank").set_type("optional")
bank_plot.get_event("Police arrives").set_type("conditional")

#generate bank tree
#bank_tree = tt.Tree()
#bank_tree.generate_tree_from_plot_graph(bank_plot, bank_plot.get_event("Sally puts money in bag"))
#bank_tree.to_string()

prescription_plot = p.Plot_Graph()
prescription_plot.add_new_event("Leave house")
prescription_plot.add_new_event("Go to bank")
prescription_plot.add_new_event("Go to hospital")
prescription_plot.add_new_event("Go to doctor")
prescription_plot.add_new_event("Withdraw money")
prescription_plot.add_new_event("Get prescription hospital")
prescription_plot.add_new_event("Get prescription doctor")
prescription_plot.add_new_event("Don't get prescription hospital")
prescription_plot.add_new_event("Don't get prescription doctor")
prescription_plot.add_new_event("Go to pharmacy")
prescription_plot.add_new_event("Buy strong drugs")
prescription_plot.add_new_event("Buy week drugs")
prescription_plot.add_new_event("Go home")

prescription_plot.get_event("Leave house").is_before(prescription_plot.get_event("Go to bank"))
prescription_plot.get_event("Leave house").is_before(prescription_plot.get_event("Go to hospital"))
prescription_plot.get_event("Leave house").is_before(prescription_plot.get_event("Go to doctor"))
prescription_plot.get_event("Go to bank").is_before(prescription_plot.get_event("Withdraw money"))
prescription_plot.get_event("Go to hospital").is_before(prescription_plot.get_event("Get prescription hospital"))
prescription_plot.get_event("Go to hospital").is_before(prescription_plot.get_event("Don't get prescription hospital"))
prescription_plot.get_event("Go to doctor").is_before(prescription_plot.get_event("Get prescription doctor"))
prescription_plot.get_event("Go to doctor").is_before(prescription_plot.get_event("Don't get prescription doctor"))
prescription_plot.get_event("Withdraw money").is_before(prescription_plot.get_event("Go to pharmacy"))
prescription_plot.get_event("Don't get prescription hospital").is_before(prescription_plot.get_event("Go to pharmacy"))
prescription_plot.get_event("Don't get prescription doctor").is_before(prescription_plot.get_event("Go to pharmacy"))
prescription_plot.get_event("Get prescription hospital").is_before(prescription_plot.get_event("Go to pharmacy"))
prescription_plot.get_event("Get prescription doctor").is_before(prescription_plot.get_event("Go to pharmacy"))
prescription_plot.get_event("Go to pharmacy").is_before(prescription_plot.get_event("Buy strong drugs"))
prescription_plot.get_event("Go to pharmacy").is_before(prescription_plot.get_event("Buy week drugs"))
prescription_plot.get_event("Buy strong drugs").is_before(prescription_plot.get_event("Go home"))
prescription_plot.get_event("Buy week drugs").is_before(prescription_plot.get_event("Go home"))

prescription_plot.create_mutual_exclusivity(prescription_plot.get_event("Get prescription hospital"), \
    prescription_plot.get_event("Don't get prescription hospital"))
prescription_plot.create_mutual_exclusivity(prescription_plot.get_event("Get prescription hospital"), \
    prescription_plot.get_event("Get prescription doctor"))
prescription_plot.create_mutual_exclusivity(prescription_plot.get_event("Don't get prescription doctor"), \
    prescription_plot.get_event("Get prescription doctor"))
prescription_plot.create_mutual_exclusivity(prescription_plot.get_event("Buy strong drugs"), \
    prescription_plot.get_event("Buy week drugs"))
#prescription_plot.create_mutual_exclusivity(prescription_plot.get_event("Get prescription hospital"), \
#    prescription_plot.get_event("Buy week drugs"))
#prescription_plot.create_mutual_exclusivity(prescription_plot.get_event("Get prescription doctor"), \
#    prescription_plot.get_event("Buy week drugs"))

#prescription_tree = tt.Tree()
#prescription_tree.generate_tree_from_plot_graph(prescription_plot, prescription_plot.get_event("Leave house"))
#prescription_tree.to_string()














