import engine as e
import numpy as np
import time
from termcolor import colored
import sys 


class Prop:
  def __init__(self, name, position, symbol):
    self.name = name
    self.x = position[0]
    self.y = position[1]
    self.symbol = symbol
    self.state = "default"
    self.items = list()

class Exit(Prop):
  def __init__(self, name, position, symbol, location):
    super().__init__(name, position, symbol)
    self.go_to = location

class Agent(Prop):
  def __init__(self, name, position, symbol):
    super().__init__(name, position, symbol)
    self.action_labels = [[0, "move left"], 
                   [1, "move right"],
                   [2, "move up"],
                   [3, "move down"],
                   [4, "go into pharmacy"],
                   [5, "go into bank"],
                   [6, "go into docter's office"],
                   [7, "browse store"],
                   [8, "pick up weak drug"],
                   [9, "stand in line"],
                   [10, "wait"],
                   [11, "order drugs"],
                   [12, "ask for request"],
                   [13, "ask prescription"],
                   [14, "produce prescription"],
                   [15, "don't produce prescription"]
                  ] 
  
   
  

  def take_possible_action(self, action):
    possible_actions = self.get_possible_actions()
    if action in possible_actions:
      self.take_action(action)
    else:
      e.output_text.add_line("Error: non available action")
    
  
  def take_action(self, action):
    
    #move left
    if action == 0:
      self.x = self.x - 1
    
    #move right
    if action == 1:
      self.x = self.x + 1
    
    #move up
    if action == 2:
      self.y = self.y - 1
    
    #move down
    if action == 3:
      self.y = self.y + 1
    
    #go into pharmacy
    if action == 4:
      self.print_action(action)
      world.change_location_of_agent(self, world.location, pharmacy, 3, 6)
      world.location = pharmacy
    
    #go into bank
    if action == 5:
      print("not implemented")
      #e.output_text.add_line(protagonist.action_labels[5][1])
      #world.location = bank
    
    #go into doctor's office
    if action == 6:
      print("not implemented")
      #e.output_text.add_line(protagonist.action_labels[6][1])
      #world.location = bank
    
    #browse store
    if action == 7:
      self.print_action(action)
      self.state = "browse"

    #take weak drug
    if action == 8:
      self.print_action(action)
      self.items.append(Item("weak drug"))
      self.state = "default"

    #stand in line
    if action == 9:
      self.print_action(action)
      self.state ="stand in line"

    #wait
    if action == 10:
      self.print_action(action)
      customer1.state = "exit pharm"
      self.state = "at counter"
      self.y = self.y - 1
      pharmacist.state = "new customer"

    #order drugs
    if action == 11:
      self.print_action(action)
      self.state = "order drugs"

    #produce prescription
    if action == 14:
      self.print_action(action)
      self.state = "produce prescription"

    #don't produce prescription
    if action == 15:
      self.print_action(action)
      self.state = "don't produce prescription"
    
    


  def get_possible_actions(self):
    
    possible_actions = list()
    
    move_left = self.x - 1
    move_right = self.x + 1
    move_up =  self.y - 1 
    move_down = self.y + 1


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
      
      #go into bank
      if e.proximity([self.x, self.y], [world.location.locations["bank"].x, world.location.locations["bank"].y]):
        possible_actions.append(5)
      
      #go into doctor's office
      if e.proximity([self.x, self.y], [world.location.locations["doctor"].x, world.location.locations["doctor"].y]):
        possible_actions.append(6)
    
    


    return possible_actions

  def print_action(self, action):
    e.output_text.add_line(protagonist.action_labels[action][1])
  
  def run(self):
    pass
class Protagonist(Agent):

  def get_possible_actions(self):
    
    possible_actions = list()

    if world.location.name == "pharmacy":
      
      if self.state == "default":
        e_x = pharmacy.get_exit("city").x
        e_y = pharmacy.get_exit("city").y
        
        #browse store
        if self.y > 2 and self.y < world.location.size - 1 and ([self.x, self.y] in [[e_x-1, e_y-1],[e_x, e_y-1],[e_x+1, e_y-1]]) == False:
          possible_actions.append(7)
        #stand in line
        if customer1.x == self.x and customer1.y == self.y - 1 and customer1.state == "wait":
          possible_actions.append(9)

      # pick up weak drug
      elif self.state == "browse":
        possible_actions.append(8)

      #stand in line
      elif self.state == "stand in line":
        possible_actions.append(10)
      
     #order drugs
      if pharmacist.state == "ask for request":
        possible_actions.append(11)

      if pharmacist.state == "need prescription":
        possible_actions.append(14)
        possible_actions.append(15)

    possible_actions = super().get_possible_actions() + possible_actions

    return possible_actions

class Pharmacist(Agent):
  def __init__(self, name, position, symbol):
    super().__init__(name, position, symbol)

  def run(self):

    #response to customer at counter
    if self.state == "new customer" and protagonist.state == "at counter":
      self.print_action(12)
      self.state = "ask for request"

    #response to customer order drugs
    elif self.state == "ask for request" and protagonist.state == "order drugs":
      self.print_action(13)
      self.state = "need prescription"

  
  def get_possible_actions(self):

    possible_actions = list()
    if protagonist.state == "order drugs":
      possible_actions.append(12)

    if protagonist.state == "show prescription":
      print("not implemented")
       
    return possible_actions
  

class Customer(Agent):
  def __init__(self, name, position, symbol):
    super().__init__(name, position, symbol)
    self.move_script = [0, 3, 3, 3,]
    self.state = "default"
  
  def run(self):
    if self.state == "exit_pharm":
      if len(self.move_script) != 0:
        if self.move_script[0] in self.get_possible_actions():
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
    


# instantiate
city = Location("city", 10, [0,0], 'C')
doctors_office = Location("doctor's office", 5, [0, 3], colored('D', 'red'))
bank = Location("bank", 5, [3, 7], colored('$', 'red'))
pharmacy = Location("pharmacy", 7, [1,2], colored('+', 'red'))

city.locations["pharmacy"] = pharmacy
city.locations["doctor"] = doctors_office
city.locations["bank"] = bank

location = city
protagonist = Protagonist("Joe", [2,2], colored('@', 'blue'))
location.agents.append(protagonist)
pharmacist = Pharmacist("Pharmacist", [4,1], colored('@', 'red'))
customer1 = Customer("Customer one", [4,3], colored('@', 'yellow'))
customer1.state = "wait"

# pharmacy
pharmacy.agents.append(pharmacist)
pharmacy.agents.append(customer1)
#add counter
for i in [0, 3, 4, 5, 6]:
  newProp = Prop("counter", [i, 2], "✖")
  pharmacy.inventory.append(newProp)
#add exit
pharmacy.exits.append(Exit("city", [3,6], colored('E', 'white'), city))



world = World(location)

#simulaton loop
while True:

  world.run_all_agents()

  actions = protagonist.get_possible_actions()
  str_actions = list()
  for i in range(0, len(actions)):
      a = actions[i]
      str_actions.append(str(protagonist.action_labels[a]))

  world.update()

  e.render(1, world, str_actions)


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

  protagonist.take_possible_action(choice)



