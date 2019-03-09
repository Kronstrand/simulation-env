import copy

class Plot_Graph():
    def __init__(self):
        self.id_iterator = 0
        self.content = list()
        self.executable_events = list()

    def create_mutual_exclusivity(self, event1, event2):
        event1.add_mutual_exclusivity(event2)
        event2.add_mutual_exclusivity(event1)

    def new_id(self):
        old_id = self.id_iterator
        self.id_iterator = self.id_iterator + 1
        return old_id

    def add_new_event(self, label):
        evnt = Event(self.new_id(), label)
        self.content.append(evnt)

    def get_event(self, label):
        for i in self.content:
            if i.label == label:
                return i
    
    def remove_event(self, event):

        #remove before relations
        for before_event in event.before:
            for after_event in before_event.after:
                if after_event.id == event.id:
                    before_event.after.remove(after_event)

        #remove after relations
        for after_event in event.after:
            for before_event in after_event.before:
                if before_event.id == event.id:
                    after_event.before.remove(before_event)

        #remove mutial exclution relations
        for mutual_exclusive_event in event.mutual_exclusive_with:
            for me_event_in_me_event in mutual_exclusive_event.mutual_exclusive_with:
                if me_event_in_me_event.id == event.id:
                    mutual_exclusive_event.mutual_exclusive_with.remove(me_event_in_me_event)
        
        #remove the event itself
        for i in self.content:
            if i.id == event.id:
                self.content.remove(i)

    def prepare(self):

        #create links between proceeding and preceeding events of optional events
        for event in self.content:
            if event.type == "optional":
                for before_event in event.before:
                    for after_event in event.after:
                        before_event.is_before(after_event)
                        #print(before_event.label + " is before " + after_event.label)
    
    def get_executable_events(self):
        executable_events = list()

        for i in self.content:
            optional_event_counter = 0
            for before_event in i.before:
                if before_event.type == "optional":
                    optional_event_counter = optional_event_counter + 1
            
            if len(i.before) - optional_event_counter == 0:
                executable_events.append(i)

        return executable_events
    
    def remove_executable_event(self, event):
        
        self.executable_events[-1].remove(event)
        if len(self.executable_events[-1]) == 0:
            del self.executable_events[-1]
    
    def set_executable_events(self, event):
        
        new_executable_events = list()
        for after_event in event.after:
            optional_event_counter = 0
            for before_event in after_event.before:
                if before_event.type == "optional":
                    optional_event_counter = optional_event_counter + 1
            
            if len(after_event.before) - optional_event_counter == 1:
                new_executable_events.append(after_event)
        
        if len(new_executable_events) > 0:
            self.executable_events.append(new_executable_events)
    
    def new_updated_plot_graph(self, event):

        cloned_plot_Graph = copy.deepcopy(self)
        cloned_event = None
        for i in range(len(cloned_plot_Graph.content)):
            if cloned_plot_Graph.content[i].id == event.id:
                cloned_event = cloned_plot_Graph.content[i]

        return cloned_plot_Graph.update_plot_graph(cloned_event)
    
    def update_plot_graph(self, event):
        
        #remove mutual exclusive events because its mutual exclusive counterpart was used
        #propagate: remove all events dependent on the mutual exclusive removed event
        for mutual_exclusive_event in copy.copy(event.mutual_exclusive_with):
            self.remove_mutual_exclution_with_propagation(mutual_exclusive_event)

        #remove previous events that are no more available
        for before_event in copy.copy(event.before):
            self.remove_event(before_event)
        
        
        #update executable events    
        #self.remove_executable_event(event)
        #self.set_executable_events(event)

        self.remove_event(event)
        
        return self

    
    def remove_mutual_exclution_with_propagation(self, event):

        def recursivly_remove_mutual_exclution_events(event, proceeding_events_of_deleted_events):

            for before_event in event.before:
                for after_event in event.after:
                    before_event.is_before(after_event)
            
            proceeding_events = copy.copy(event.after)
            #print(event.label + " is removed recursivly")
            self.remove_event(event)

            for proceeding_event in proceeding_events:
                # if there is just one preceedence constraint
                if len(proceeding_event.before) == 0:
                    recursivly_remove_mutual_exclution_events(proceeding_event, proceeding_events_of_deleted_events)
                    
                    #remove deleted event from the list of proceeding_events that was not deleted
                    if proceeding_event in proceeding_events_of_deleted_events:
                        proceeding_events_of_deleted_events.remove(proceeding_event)

                else:
                    #add proceeding_event to list of proceeding_events that was not deleted
                    if proceeding_event not in proceeding_events_of_deleted_events:
                        proceeding_events_of_deleted_events.append(proceeding_event)
            
            return proceeding_events_of_deleted_events
                    

        proceeding_events_of_deleted_events = list()
        proceeding_events_of_deleted_events = recursivly_remove_mutual_exclution_events(event, proceeding_events_of_deleted_events)

        #keep structural information by linking preceeding events of the deleted events to the proceeding event of first deleted event
        for before_deleted_event in event.before:
            for after_deleted_event in proceeding_events_of_deleted_events:
                before_deleted_event.is_before(after_deleted_event)


class Event():
    def __init__(self, id, label):
        #self.events
        self.id = id
        self.label = label 
        self.available = True
        self.before = list() # these events are positioned before the event
        self.after = list() # these events are positioned after the event
        self.mutual_exclusive_with = list()
        self.type = "normal" #normal, optinoal, conditional
    def add_mutual_exclusivity(self, event):
        self.mutual_exclusive_with.append(event)
    def is_before(self, event):
        self.after.append(event)
        event.before.append(self)
    def set_type(self, event_type):
        if event_type == "normal" or event_type == "optional" or event_type == "conditional":
            self.type = event_type      
        else:
            raise ValueError(str(event_type) + ' not allowed as type')

