import engine as e
import numpy as np
import time
from termcolor import colored
#from IPython.display import clear_output

class Agent:
  def __init__(self, name, pos, symbol, location):
    self.name = name
    self.x = pos[0]
    self.y = pos[1]
    self.symbol = symbol
    self.location = location
  
  action_labels = [[0, "move left"], 
                   [1, "move right"],
                   [2, "move up"],
                   [3, "move down"],
                   [4, "go into hospital"]
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
    
    #go into hospital
    if action == 4:
      e.output_text.add_line("enter hospital")
      #story = story + "\n" + action_labels[4]
  
  
  def get_possible_actions(self):
    
    possible_actions = list()
    
    #move left
    if self.x - 1 >= 0:
      possible_actions.append(0)
      
    #move right
    if self.x + 1 < self.location.size:
      possible_actions.append(1)
    
    #move up
    if self.y - 1 >= 0:
      possible_actions.append(2)
      
    #move down
    if self.y + 1 < self.location.size:
      possible_actions.append(3)


    if (self.location.name == "city"):

      #go into hospital
      if e.proximity([self.x, self.y], [self.location.locations["hospital"].x, self.location.locations["hospital"].y]):
        possible_actions.append(4)
    
    return possible_actions

class Location:
  def __init__(self, name, size, position, symbol):
    self.name = name
    self.size = size
    self.x = position[0]
    self.y = position[1]
    self.locations = dict()
    self.symbol = symbol
  def addLocation(self, location):
    self.locations.append(location)

class World:
  def __init__(self, location, protagonist):
    self.location = location
    self.protagonist = protagonist
    self.update()
    
  def update(self):
    self.rep = e.new2DArray(self.location.size, " ")
    self.rep[self.protagonist.y][self.protagonist.x] = self.protagonist.symbol
    for k, i in self.location.locations.items():
      self.rep[i.y][i.x] = i.symbol

# load props
city = Location("city", 10, [0,0], 'C')
hospital = Location("Hospital", 5, [3, 3], colored('+', 'red'))
bank = Location("Bank", 5, [3, 7], colored('$', 'red'))

city.locations["hospital"] = hospital
city.locations["bank"] = bank

location = city
protagonist = Agent("Joe", [2,2], colored('@', 'blue'), location)

world = World(location, protagonist)

#simulaton loop
while True:

  #protagonist.take_action(1)
  #env.protagonist.take_possible_action(4)

  #engine.render(1, env.world)

  actions = protagonist.get_possible_actions()
  str_actions = list()
  for i in range(0, len(actions)):
      a = actions[i]
      str_actions.append(str(protagonist.action_labels[a]))



  
  world.update()

  e.render(1, world, str_actions)  
  
  choice = int(input())
  protagonist.take_action(choice)



