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
        for before_event in event.before:
            if event in before_event.after:
                before_event.after.remove(event)
        #remove after relations
        for after_event in event.after:
            if event in after_event.before:
                after_event.before.remove(event)
        #remove mutial exclution relations
        for mutual_exclusive_event in event.mutual_exclusive_with:
            if event in mutual_exclusive_event.mutual_exclusive_with:
                mutual_exclusive_event.mutual_exclusive_with.remove(event)
        #remove event itself
        self.content.remove(event)

    def get_executable_events(self):
        executable_events = list()
        for i in self.content:
            if len(i.before) == 0:
                executable_events.append(i)
        return executable_events
    
    def update_plot_graph(self, event):
        
        #remove mutual exclusive events because its mutual exclusive counterpart was used
        #propagate: remove all event following dependent on the mutual exclusive removed event
        for mutual_exclusive_event in event.mutual_exclusive_with:
            self.remove_mutual_exclution_with_propagation(mutual_exclusive_event)

        #remove before relations dependet on removed events.
        for before_event in event.before:
            self.remove_event(before_event)
        
        #remove the event itself
        self.remove_event(event)
        
        return self

    
    def remove_mutual_exclution_with_propagation(self, event):

        def recursivly_remove_mutual_exclution_events(event, proceeding_events_of_deleted_events):

            for proceeding_event in event.after:
                # if there is just one preceedence constraint
                if len(proceeding_event.before) == 1:
                    recursivly_remove_mutual_exclution_events(proceeding_event, proceeding_events_of_deleted_events)
                    
                    #remove deleted event from the list of proceeding_events of deleted_events
                    if proceeding_event in proceeding_events_of_deleted_events:
                        proceeding_events_of_deleted_events.remove(proceeding_event)

                    #remove the proceeding event itself from the plot graph
                    self.remove_event(proceeding_event)
                else:
                    #add proceeding_event to list of proceeding_events_of_deleted_events
                    if proceeding_event not in proceeding_events_of_deleted_events:
                        proceeding_events_of_deleted_events.append(proceeding_event)
                #remove event istelf
            

        proceeding_events_of_deleted_events = list()
        proceeding_events_of_deleted_events = recursivly_remove_mutual_exclution_events(event, proceeding_events_of_deleted_events)


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
        #event.available = False
        event.before.append(self)
    def set_type(self, event_type):
        if event_type != "normal" or event_type != "optional" or event_type != "conditional":
            raise ValueError(str(event_type) + 'not allowed as type')
        else:
            self.type = event_type

