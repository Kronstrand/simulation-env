import copy
import plot_graph as p


class Tree():
    def __init__(self):
        self.n_stories = 0
        self.tree = list()

    def to_string(self):
        self.tree[0].print_node("", True)

    def add_new_node(self, node):
        self.tree.append(node)
    
    def add_new_child(self, node, child_node):
        node.add_new_child(child_node)
        self.tree.append(child_node)
    
    def generate_tree_from_plot_graph(self, plot_graph, start_point):
        
        print("generating tree from plot graph...")
        
        plot_graph.prepare()
        
        #self.add_new_node(Tree_Node(start_point.label))
        self.add_new_node(Tree_Node("Root", None))

        unfinished_branches = list() #[tree node, plot graph]
        unfinished_branches.append([self.tree[0], plot_graph])

        while len(unfinished_branches) > 0:
            new_unfinished_branches = list()
            for unfinished_branch_node in unfinished_branches:
                plot_graph = unfinished_branch_node[1]
                executable_events = plot_graph.get_executable_events()

                for executable_event in executable_events:
                    new_node = Tree_Node(executable_event.label, executable_event.action_corr)
                    self.add_new_child(unfinished_branch_node[0], new_node)
                    #unfinished_branch_node[0].add_new_child(new_node)
                    if len(executable_event.after) != 0: # if node is an end node
                        new_updated_plot_graph = plot_graph.new_updated_plot_graph(executable_event)
                        new_unfinished_branches.append([new_node, new_updated_plot_graph])
            
            unfinished_branches = new_unfinished_branches
        
        print("Tree generation completed.")

    def generate_tree_from_plot_graph2(self, plot_graph, start_point):
        
        plot_graph.prepare()
        
        self.add_new_node(Tree_Node(start_point.label))
        #plot_graph.executable_events.append([start_point])

        unfinished_branches = list() #[tree node, plot graph]
        unfinished_branches.append([self.tree[0], plot_graph.update_plot_graph(start_point)])

        while len(unfinished_branches) > 0:
            new_unfinished_branches = list()
            for unfinished_branch_node in unfinished_branches:
                plot_graph = unfinished_branch_node[1]
                executable_events = plot_graph.get_executable_events()

                for executable_event in executable_events:
                    new_node = Tree_Node(executable_event.label)
                    unfinished_branch_node[0].add_new_child(new_node)
                    if len(executable_event.after) != 0: # if node is an end node
                        new_updated_plot_graph = plot_graph.new_updated_plot_graph(executable_event)
                        new_unfinished_branches.append([new_node, new_updated_plot_graph])
            
            unfinished_branches = new_unfinished_branches



class Tree_Node:
    def __init__(self, label, action_corr):
        self.label = label
        self.children = list()
        self.action_correspondence = action_corr #map nodes to actions in agents
    
    def add_new_child(self, child_node):
        self.children.append(child_node)

    def print_node(self, indent, last):

            print(indent, end = '')

            if last:
                print("+-", end = '')
                indent += "  "
            else:
                print("+-", end = '') 
                indent = indent + "| "
            print(self.label)

            children = self.children
            
            for i in range(len(children)):
                children[i].print_node(indent, i == len(children) -1)