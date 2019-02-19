class Plot_Graph():
    def __init__(self):
        self.id_iterator = 0
        self.content = list()

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
        for b in event.before:
            b.after.remove(event)
        #remove after relations
        for a in event.after:
            a.after.remove(event)
        #remove mutial exclution relations
        for me in event.mutual_exclusive_with:
            me.event.mutual_exclusive_with.remove(event)
           

    def get_executable_events(self):
        executable_events = list()
        for i in self.content:
            if len(i.after) == 0:
                executable_events.append(i)
        return executable_events
    
    def update_plot_graph(self, event):
        
        #remove mutual exclusive events because its mutual exclusive counterpart was used
        #propagate: remove all event following dependent on the mutual exclusive removed event
        self.remove_mutual_exclution_with_propagation(event)

        #remove before relations dependet on removed events.
        for before_event in event.before:
            self.remove_event(before_event)
        
        #remove the event itself
        self.remove_event(event)
        
        return self

    
    def remove_mutual_exclution_with_propagation(self, event):

        proceeding_events_of_deleted_events = list()
        proceeding_events_of_deleted_events = propagate_mutual_exclution_removal(event, proceeding_events_of_deleted_events)
    
        def recursivly_remove_mutual_exclution_events(self, event, proceeding_events_of_deleted_events):

            for proceeding_event in event.after:
                # if there is just one preceedence constraint
                if len(proceeding_event.before) == 1:
                    self.recursivly_remove_mutual_exclution_events(proceeding_event, proceeding_events_of_deleted_events)
                    
                    #remove deleted event from proceeding_events of deleted_events
                    if event in proceeding_events_of_deleted_events:
                        proceeding_events_of_deleted_events.remove(event)

                    #remove the event itself
                    self.remove_event(event)
                else:
                    #add proceeding_event to list of proceeding_events_of_deleted_events
                    if proceeding_event not in proceeding_events_of_deleted_events:
                        proceeding_events_of_deleted_events.append(proceeding_event)



class Event():
    def __init__(self, id, label):
        #self.events
        self.id = id
        self.label = label 
        self.available = True
        self.before = list() # list of before relations
        self.after = list() #list of after relations
        self.mutual_exclusive_with = list()
        self.type = "normal" #normal, optinoal, conditional
    def add_mutual_exclusivity(self, event):
        self.mutual_exclusive_with.append(event)
    def set_before(self, event):
        self.before.append(event)
        event.available = False
        event.after.append(self)
    def set_type(self, event_type):
        if event_type != "normal" or event_type != "optional" or event_type != "conditional":
            raise ValueError(str(event_type) + 'not allowed as type')
        else:
            self.type = event_type

