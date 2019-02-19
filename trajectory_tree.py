import plot_graph as p

class Tree():
    def __init__(self):
        self.tree = list()
        self.unfinished_branches = list()

    def to_string(self):
        self.tree[0].print_node("", True)

    def add_new_node(self, node):
        self.tree.append(node)
    
    def add_new_child(self, node, child_node):
        node.add_new_child(child_node)
        self.tree.append(child_node)
    
    def generate_tree_from_plot_graph(self, plot_graph, start_point):
        

        self.tree = Tree_Node(start_point.label)
        unfinished_branches.append([self.tree, plot_graph])
        
        #for all paths
        #get get_executable_events()
            #for all executable_events()
                #add new branching path to path node
                #update graph
                # associate graph with new node

        while True:
            new_unfinished_branches = list()
            for unfinsihed_branch_node in unfinished_branches:
                executable_events = unfinsihed_branch_node[1].get_executable_events()

                for executable_event in executable_events:
                    new_node = Tree_Node(executable_event.label)
                    unfinsihed_branch_node[0].add_new_child(new_node)
                    new_unfinished_branches.append([new_node, unfinsihed_branch_node[1].update_plot_graph(executable_event)]) #implement update_plot_graph

    
    
class Tree_Node:
    def __init__(self, label):
        self.label = label
        self.children = list()
    
    def add_new_child(self, child_node):
        self.children.append(child_node)

    def print_node(self, indent, last):

            print(indent, end = '')

            if last:
                print("└╴", end = '')
                indent += "  "
            else:
                print("├╴", end = '') 
                indent = indent + "│ "
            print(self.label)

            children = self.children
            
            for i in range(len(children)):
                children[i].print_node(indent, i == len(children) -1)