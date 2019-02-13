import numpy as np
import time

class Output_Text:
  def __init__(self, string):
    #self.content = string
    self.content = list()
  def add_line(self, string):
    self.content.append(str(string))
  def reset(self):
    self.content = list()
    
  def print(self):
    print(self.content)

def render(delay, world, actions):
  #clear_output()
  print(chr(27) + "[2J")

  for i in actions:
      print(i)
  print()
  outputMap = list()
  outputMap = [". " * world.location.size + "."]

  for i in range(world.location.size):
    outputLine = ""
    for j in range(0, world.location.size):
      outputLine = outputLine + "." + world.rep[i][j]
    outputLine = outputLine + "."
    outputMap.append(outputLine)

  for i in range(len(outputMap)):
      output_index = len(output_text.content) - len(outputMap) + i
      outputEvents = ""
      #avoid index out of bounds
      if(output_index >= 0 and len(output_text.content) > output_index):
          outputEvents = output_text.content[output_index]
      print(outputMap[i] + "\t" + outputEvents)

  time.sleep(delay)

def new2DArray(size, content):
  li = list()
  tempList = list()
  for i in range(size):
    tempList.append(content)
  for i in range(size):
    li.append(tempList.copy())
  return li

def proximity(a,b):
  distance = np.linalg.norm(np.array(a)-np.array(b))
  if distance < 1.5:
    return True
  else:
    return False

def is_colliding(prop_list, x, y):
  for i in prop_list:
    if i.x == x and i.y == y:
      return True
  return False

output_text = Output_Text("Begin:")