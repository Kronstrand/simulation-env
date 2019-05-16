import engine as e
import numpy as np
import time
from termcolor import colored
import colorama
import sys 
import random as rnd
import rl
import trajectory_tree as tt

colorama.init()

action_labels = [[0, "move left"],
                   [1, "move right"],
                   [2, "move up"],
                   [3, "move down"],
                   [4, "go into pharmacy"],
                   [5, "go into bank"], #not implemented
                   [6, "go into docter's office"], #not implemented
                   [7, "Customer look for drugs"],
                   [8, "Customer pick up drug"],
                   [9, "Customer stand in line"],
                   [10, "Customer wait"],
                   [11, "Customer order drugs"],
                   [12, "Pharmacist ask for request"],
                   [13, "Pharmacist ask for prescription"],
                   [14, "Customer produce prescription"],
                   [15, "Customer don't produce prescription"],
                   [16, "Pharmacist refuse to sell"],
                   [17, "Customer pay cash"], #not implemented
                   [18, "Pharmacist hand over drugs"], 
                   [19, "Pharmacist hand over receipt"], 
                   [20, "Customer take drugs"], 
                   [21, "Customer take receipt"],
                   [22, "Pharmacist check prescription"],
                   [23, "Customer leave pharmacy"],
                   [24, "Customer skip line"]
                  ] 

class Prop:
  def __init__(self, name, position, symbol):
    self.name = name
    self.x = position[0]
    self.y = position[1]
    self.symbol = symbol
    self.state = "default"
    self.items = list()

  def has_item(self, name):
    for i in self.items:
      if i.name == name:
        return True  
    return False

  def loose_item(self, name):
    for i in range(len(self.items)):
      if self.items[i].name == name:
        self.items.pop(i)
        break

class Exit(Prop):
  def __init__(self, name, position, symbol, location):
    super().__init__(name, position, symbol)
    self.go_to = location

class Agent(Prop):
  def __init__(self, name, position, symbol):
    super().__init__(name, position, symbol)
    self.walkable = True
    self.action_labels = action_labels
  

  def take_possible_action(self, action):
    possible_actions = self.get_possible_actions()
    if action in possible_actions:
      self.take_action(action)
    else:
      e.output_text.add_line("Error: non available action")

  def reward_protagonist(self, action):
    """
    if protagonist.rewards.get(action) != None:
        #print("reward!")
        protagonist.reward = protagonist.reward + protagonist.rewards[action]
    """
    #using hardcoded rewards
    if protagonist.trajectory_tree == None:
      if protagonist.rewards.get(action) != None and protagonist.has_item("drugs") == False:
        protagonist.reward = protagonist.reward + protagonist.rewards[action]
    # using trajectory tree
    elif len(protagonist.current_tree_event.children) > 0:
      action_found = False
      for event in protagonist.current_tree_event.children:
        if event.action_correspondence == action:
          action_found = True
          protagonist.current_tree_event = event
          break
      if action_found == True:
        protagonist.reward = protagonist.reward + 10
      else:
        protagonist.reward = protagonist.reward - 10

    """
    elif len(protagonist.current_tree_event.children) > 0:
      for event in protagonist.current_tree_event.children:
        if event.action_correspondence == action:
          protagonist.reward = protagonist.reward + 10
          protagonist.current_tree_event = event
          print(str(action))
          break
    """ 
    
    
         
  
  def take_action(self, action):
    
    self.reward_protagonist(action)

    #move left
    if action == 0:
      self.x = self.x - 1
      self.state = "default"
    
    #move right
    elif action == 1:
      self.x = self.x + 1
      self.state = "default"
    
    #move up
    elif action == 2:
      self.y = self.y - 1
      self.state = "default"
    
    #move down
    elif action == 3:
      self.y = self.y + 1
      self.state = "default"
    
    #go into pharmacy
    elif action == 4:
      self.print_action(action)
      world.change_location_of_agent(self, world.location, pharmacy, 3, 6)
      world.location = pharmacy
    
    #go into bank
    elif action == 5:
      print("not implemented")
      #e.output_text.add_line(protagonist.action_labels[5][1])
      #world.location = bank
    
    #go into doctor's office
    elif action == 6:
      print("not implemented")
      #e.output_text.add_line(protagonist.action_labels[6][1])
      #world.location = bank
    
    #browse store
    elif action == 7:
      self.print_action(action)
      self.state = "browse"

    #take drug
    elif action == 8:
      self.print_action(action)
      self.items.append(Item("drugs"))
      self.state = "default"
      self.stole = True

    #stand in line
    elif action == 9:
      self.print_action(action)
      self.state ="Customer stand in line"

    #wait
    elif action == 10:
      self.print_action(action)
      customer1.state = "exit pharm"
      self.state = "at counter"
      self.y = self.y - 1
      pharmacist.state = "new customer"
    
    #refuse to sell
    elif action == 16:
      self.print_action(action)
      protagonist.state = "default"
      protagonist.refused_sell = True
      self.state = "default"

    #hand over drugs
    elif action == 18:
      self.print_action(action)
      if self.has_item("drugs") == False:
        self.items.append(Item("drugs"))
    #hand over receipt
    elif action == 19:
      self.print_action(action)
      self.items.append(Item("receipt"))
    
    #take drugs
    elif action == 20:
      self.print_action(action)
      pharmacist.loose_item("drugs")
      self.items.append(Item("drugs"))
      if pharmacist.has_item("receipt") == False:
        self.state = "default"
    #take receipt
    elif action == 21:
      self.print_action(action)
      pharmacist.loose_item("receipt")
      self.items.append(Item("receipt"))
      if pharmacist.has_item("drugs")  == False:
        self.state = "default"
    elif action == 23:
      world.change_location_of_agent(self, world.location, city, pharmacy.x, pharmacy.y - 1)
      world.location = city
    #skip line
    elif action == 24:
      self.print_action(action)
      customer1.state = "exit pharm"
      self.state = "at counter"
      self.y = self.y - 1
      pharmacist.state = "new customer"
      self.line_skipped = True


    #simple action changing state of agent
    else:
      self.print_action(action)
      self.state = self.action_labels[action][1]


  def get_possible_actions(self):
    
    possible_actions = list()
    
    move_left = self.x - 1
    move_right = self.x + 1
    move_up =  self.y - 1 
    move_down = self.y + 1

    if self.walkable == True:
      #move left
      if move_left >= 0 and e.is_colliding(world.location.get_all_props(), move_left, self.y) != True:
        possible_actions.append(0)
      

      #move right
      if move_right < world.location.size and e.is_colliding(world.location.get_all_props(), move_right, self.y) != True:
        possible_actions.append(1)
      
      #move up
      if move_up >= 0 and e.is_colliding(world.location.get_all_props(), self.x, move_up) != True:
        possible_actions.append(2)
        
      #move down
      if move_down < world.location.size and e.is_colliding(world.location.get_all_props(), self.x, move_down) != True:
        possible_actions.append(3)

      #in city
      if world.location.name == "city":

        #go into pharmacy
        if e.proximity([self.x, self.y], [world.location.locations["pharmacy"].x, world.location.locations["pharmacy"].y]):
          possible_actions.append(4)
        """
        #go into bank
        if e.proximity([self.x, self.y], [world.location.locations["bank"].x, world.location.locations["bank"].y]):
          possible_actions.append(5)
        
        #go into doctor's office
        if e.proximity([self.x, self.y], [world.location.locations["doctor"].x, world.location.locations["doctor"].y]):
          possible_actions.append(6)
        """
      if world.location.name == "pharmacy":
        ex = world.location.get_exit("city")
        if ex != None:
          if ex.x == self.x and ex.y == self.y:
            possible_actions.append(23)

    return possible_actions

  def print_action(self, action):
    e.output_text.add_line(protagonist.action_labels[action][1])
  
  def run(self):
    pass
class Protagonist(Agent):

  def __init__(self, name, position, symbol, Q_table):
    super().__init__(name, position, symbol)
    self.rewards = dict()
    self.reward = 0
    self.Q_table = Q_table
    self.initial_curiosity = 0 
    self.curiosity =  self.initial_curiosity #epsilon
    self.trajectory_tree = None
    self.current_tree_event = None
    self.stole = False
    self.refused_sell = False
    self.line_skipped = False
   
  
  def set_rewards(self, reward_structure):
    
    if reward_structure == "get drugs":
      self.rewards[8] = 10
      self.rewards[20] = 10
  
  def take_action(self, action):

    return super().take_action(action)
    

  
  def get_Q_value(self, state, action):
    if self.Q_table.get(state) != None:
      if self.Q_table[state].get(action) != None:
        return self.Q_table[state].get(action)
    return 0.0

  def add_value_to_Q_table(self, state, action, value):
    if self.Q_table.get(state) == None:
      self.Q_table[state] = dict()
    self.Q_table[state][action] = value    
  
  def get_optimal_action(self, state):

    possible_actions = self.get_possible_actions()
    learned_actions = self.Q_table.get(state)
    
    if learned_actions == None:
      return rnd.choice(possible_actions)
    else:
      learned_actions_num = list(learned_actions.keys())
      Q_values = list(learned_actions.values())

      #create a list of trained values that are possible
      possible_Q_values = list()
      possible_learned_actions_num  = list()
      for i in range(len(learned_actions_num)):
        if learned_actions_num[i] in possible_actions:
          possible_learned_actions_num.append(learned_actions_num[i])
          possible_Q_values.append(Q_values[i])


      #add possible choices that are not trained
      for i in range(len(possible_actions)):
        if possible_actions[i] not in learned_actions_num:
          possible_learned_actions_num.append(possible_actions[i])
          possible_Q_values.append(0.0)

      #choose only MAX choices
      all_max_choices = list()
      m = float("-inf")
      for i in range(len(possible_Q_values)):
        if possible_Q_values[i] > m:
          m = possible_Q_values[i]
          all_max_choices = list()
          all_max_choices.append(possible_learned_actions_num[i])
        elif possible_Q_values[i] == m:
          all_max_choices.append(possible_learned_actions_num[i])

      return rnd.choice(all_max_choices)

    #return action
  
  def learn(self, state, action):
    
    new_state = self.generate_state_key()
    Q_value = self.get_Q_value(state, action)
    optimal_action_in_new_state = self.get_optimal_action(new_state)
    new_optimal_Q_value = self.get_Q_value(new_state, optimal_action_in_new_state)

    self.add_value_to_Q_table(state, action, rl.Q_learning_TD(Q_value, new_optimal_Q_value, self.reward))

    self.reward = 0
  
  def generate_state_key(self):
    return str(world.location.name) + str(self.x) + str(self.y) + str(self.state) + str(self.has_item("drugs")) + str(pharmacist.state) + str(self.current_tree_event)

  
  def choose_action(self):

    state = self.generate_state_key()
    possible_actions = self.get_possible_actions()
    if rnd.random() <= self.curiosity: # if not greedy
      action = rnd.choice(possible_actions)
    else:
      action = self.get_optimal_action(state)

    return action


  def get_possible_actions(self):
    
    possible_actions = list()

    if world.location.name == "pharmacy":
      
      if self.state == "default":
        e_x = pharmacy.get_exit("city").x
        e_y = pharmacy.get_exit("city").y
        
        #look for drugs
        if self.y < 2 and self.has_item("drugs") == False:
          possible_actions.append(7)
        #stand in line
        if customer1.x == self.x and customer1.y == self.y - 1 and customer1.state == "Customer wait":
          possible_actions.append(9) #wait in line
          possible_actions.append(24) #skip line

      # pick up drug
      elif self.state == "browse":
        if self.has_item("drugs") == False:
          possible_actions.append(8)

      #wait
      elif self.state == "Customer stand in line":
        possible_actions.append(10)
    
    
      if self.x == pharmacist.x and self.y == pharmacist.y + 2:
      #order drugs
        if pharmacist.state == "Pharmacist ask for request":
          possible_actions.append(11)

        elif pharmacist.state == "Pharmacist ask for prescription":
          #hand over prescription
          if self.has_item("prescription"):
            possible_actions.append(14)
          #dont hand over prescription
          possible_actions.append(15)

        #take drugs and receipt from counter
        elif pharmacist.state == self.action_labels[22][1]:
          if pharmacist.has_item("drugs"):
            possible_actions.append(20) #take drugs
          if pharmacist.has_item("receipt"):
            possible_actions.append(21) #take receipt 

    possible_actions = super().get_possible_actions() + possible_actions

    return possible_actions

class Pharmacist(Agent):
  def __init__(self, name, position, symbol):
    super().__init__(name, position, symbol)

  def run(self):

    #response to customer at counter
    if self.state == "new customer" and protagonist.state == "at counter":
      self.take_action(12)

    #response to customer order drugs
    elif self.state == "Pharmacist ask for request" and protagonist.state == "Customer order drugs":
      self.take_action(13)

    #don't produce prescription
    elif protagonist.state == "Customer don't produce prescription":
      self.take_action(16)
    
    #costumer produces prescription
    elif protagonist.state == self.action_labels[14][1] and self.state != self.action_labels[22][1]:
      self.take_action(22) #accepts prescription
      self.take_action(18) #hand over drugs
      self.take_action(19) #hand over prescription


  def get_possible_actions(self):

    possible_actions = list()
    return possible_actions
  

class Customer(Agent):
  def __init__(self, name, position, symbol):
    super().__init__(name, position, symbol)
    self.move_script = [0, 3, 3, 3,]
    self.state = "default"
  
  def run(self):
    if self.state == "exit pharm" or self.state == "default":
      if len(self.move_script) != 0:
        self.take_action(self.move_script[0])
        self.move_script.pop(0)
      else:
          world.location.agents.remove(self)
            

class Location(Prop):
  
  def __init__(self, name, size, position, symbol):
    super().__init__(name, position, symbol)
    self.size = size
    self.locations = dict()
    self.inventory = list()
    self.exits = list()
    self.agents = list()
  
  def get_exit(self, name):
    for i in self.exits:
      if i.name == name:
        return i
      else:
        return None
 
  def addLocation(self, location):
    self.locations.append(location)
  
  def get_all_props(self):
    l = list()
    for v in self.locations.values():
      l.append(v)
    l = l + self.inventory + self.agents
    return l

class Item:
  def __init__(self, name):
    self.name = name

class World:
  def __init__(self, location):
    self.location = location
    #self.protagonist = protagonist
    self.update()
    
  def run_all_agents(self):
    for i in self.location.agents:
      i.run()
  
  def update(self):
    self.rep = e.new2DArray(self.location.size, " ")
    #add protagonist sybol
    #self.rep[self.protagonist.y][self.protagonist.x] = self.protagonist.symbol
    #add location sybol
    for k, i in self.location.locations.items():
      self.rep[i.y][i.x] = i.symbol
    #add inventory symbol
    for i in self.location.inventory:
      self.rep[i.y][i.x] = i.symbol
    #add exit symbol
    for i in self.location.exits:
      self.rep[i.y][i.x] = i.symbol
    #add agents symbol
    for i in self.location.agents:
      self.rep[i.y][i.x] = i.symbol
  
  def change_location_of_agent(self, agent, old_location, new_location, x, y):
    old_location.agents.remove(agent)
    new_location.agents.append(agent)
    agent.x = x
    agent.y = y



def init(Q_table, tree):

  global city
  global doctors_office
  global bank
  global protagonist
  global pharmacy
  global location
  global customer1
  global pharmacist
  global world

  e.output_text.reset()

  city = Location("city", 8, [0,0], 'C')
  doctors_office = Location("doctor's office", 5, [5, 3], colored('D', 'red'))
  bank = Location("bank", 5, [3, 7], colored('$', 'red'))
  pharmacy = Location("pharmacy", 7, [1,2], colored('+', 'red'))

  city.locations["pharmacy"] = pharmacy
  city.locations["doctor"] = doctors_office
  city.locations["bank"] = bank

  #location = city
  location = pharmacy

  protagonist = Protagonist("Joe", [3,5], colored('@', 'blue'), Q_table)
  protagonist.items.append(Item("prescription"))
  protagonist.set_rewards("get drugs")
  protagonist.trajectory_tree = tree
  if tree != None:
    protagonist.current_tree_event = tree.tree[0]
  location.agents.append(protagonist)

  pharmacist = Pharmacist("Pharmacist", [4,1], colored('@', 'red'))
  customer1 = Customer("Customer one", [4,3], colored('@', 'yellow'))
  customer1.state = "Customer wait"
  # pharmacy
  pharmacy.agents.append(pharmacist)
  pharmacy.agents.append(customer1)
  #add counter
  for i in [0, 3, 4, 5, 6]:
    newProp = Prop("counter", [i, 2], "X")
    pharmacy.inventory.append(newProp)
  #add exit
  pharmacy.exits.append(Exit("city", [3,6], colored('E', 'white'), city))

  world = World(location)

def run(Q_table, tree, render, learn, playable):

  init(Q_table, tree)

  #simulaton loop
  for i in range(20):

    actions = protagonist.get_possible_actions()
    str_actions = list()
    for i in range(0, len(actions)):
        a = actions[i]
        str_actions.append(str(protagonist.action_labels[a]))

    world.update()

    if render == True: 
      e.render(1, world, str_actions)
    
    choice = None
    if playable == True: 
      #input from human 
      while True: 
        choice = input()
        if choice == "x":
          sys.exit()
        try:
          choice = int(choice)
          break
        except:
          print("input is not an int")
    else:
      choice = protagonist.choose_action()

    state = protagonist.generate_state_key()

    protagonist.take_possible_action(choice)
    world.run_all_agents()

    if learn == True:
      protagonist.learn(state, choice)

    #when protagonist leaves pharma and has drugs or was refused drugs, then end siumlation
    if (protagonist.has_item("drugs") == True or protagonist.refused_sell == True) and choice == 23:
      break

  result = 0 
  if protagonist.has_item("drugs"):
    if protagonist.stole == True:
      result = 1 # agent stole drugs
    else:
      result = 2 # agent baught drugs
  elif protagonist.refused_sell == True:
      result = 3 # no drugs becauase agent was refused by pharmacist
      
  return [result, protagonist.line_skipped, protagonist.Q_table]



