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

class Agent(Prop):
  def __init__(self, name, position, symbol):
    super().__init__(name, position, symbol)
  
  action_labels = [[0, "move left"], 
                   [1, "move right"],
                   [2, "move up"],
                   [3, "move down"],
                   [4, "go into pharmacy"],
                   [5, "go into bank"],
                   [6, "go into docter's office"],
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
      e.output_text.add_line(protagonist.action_labels[4][1])
      world.location = pharmacy
    
    #go into bank
    if action == 5:
      e.output_text.add_line(protagonist.action_labels[5][1])
      world.location = bank
    
    #go into doctor's office
    if action == 6:
      e.output_text.add_line(protagonist.action_labels[6][1])
      world.location = bank
  
class Protagonist(Agent):

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

class Pharmacist(Agent):
  
  def get_possible_actions(self):
    print("not implemented")

class Location(Prop):
  def __init__(self, name, size, position, symbol):
    super().__init__(name, position, symbol)
    self.size = size
    self.locations = dict()
    self.inventory = list()
  def addLocation(self, location):
    self.locations.append(location)
  def get_all_props(self):
    l = list()
    for v in self.locations.values():
      l.append(v)
    l = l + self.inventory
    return l



class World:
  def __init__(self, location, protagonist):
    self.location = location
    self.protagonist = protagonist
    self.update()
    
  def update(self):
    self.rep = e.new2DArray(self.location.size, " ")
    #add protagonist sybol
    self.rep[self.protagonist.y][self.protagonist.x] = self.protagonist.symbol
    #add location sybol
    for k, i in self.location.locations.items():
      self.rep[i.y][i.x] = i.symbol
    #add inventory symbol
    for i in self.location.inventory:
      self.rep[i.y][i.x] = i.symbol

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

# pharmacy

#add counter
for i in [0, 1, 3, 4, 5, 6]:
  newProp = Prop("counter", [i, 2], "✖")
  pharmacy.inventory.append(newProp)

world = World(location, protagonist)

#simulaton loop
while True:

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



