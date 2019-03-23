import random
LEFT = 0
DOWN = 1
RIGHT = 2
UP = 3

def getGridPoint(pos): #returns current position in grid format
  x = pos%4
  y = (int)((pos-x)/4) 
  cp = [x,y]  #current position
  return cp

def getValue(value,choice):
  if(choice == 2):
    value = value +1; #right
  if(choice == 1):
    value = value + 4; #down
  if(choice == 0):
    value = value -1; #left
  if(choice == 3):
    value = value -4; #up
  return value


#----------------classes----------
class Node:
  def __init__(self,value):
    self.value = value
    self.connections = []
 
class Map:
  def __init__(self, start, goal, holesAmount):
    self.start = start
    self.goal = goal
    self.nodes = []
    self.holeStates = []
    self.randomizeHoles(holesAmount)
    self.setNodes()
    self.setNodeConnections()
    self.path = []
    self.setupShortestPath()
  
  #-------set up functions--------
  #-------------------------------
  def setNodes(self):
    for i in range(16):
      self.nodes.append(Node(i))

  def setNodeConnections(self):
    for i in self.nodes:
      value = i.value      
      moves = self.getPossibleMoves(getGridPoint(value))
      for j in moves:
        i.connections.append(j)
        
  def randomizeHoles(self,holesAmount=4):
    for i in range(holesAmount):
      x = random.randrange(0,16)
      while(x == self.start or x==self.goal or getGridPoint(x) in self.holeStates):
        x = random.randrange(0,16)
      x = getGridPoint(x)
      self.holeStates.append(x)
       
  def printMap(self):
    truepath = []
    for i in self.path:
      truepath.append(getGridPoint(i))

    map = []
    for x in range(4):
      for y in range(4):
        point = [y,x]
        if (point in self.holeStates):
          map.append('H')
        elif (point == getGridPoint(self.goal)):
          map.append('G')
        elif(point == getGridPoint(self.start)):
          map.append("S")
        elif (point in truepath):
          map.append("P")
        else:
          map.append('-') 

    print("Path =",self.path)
    print(map[0:4])
    print(map[4:8])
    print(map[8:12])
    print(map[12:16])
    print()
  #-------------------------------------------------
  #------class functions to find shortestPath----------
  #------------------------------------------------
  
  def getPossibleMoves(self,cp): #cp=[x,y]
    choices = []  
    #check right
    if(cp[0] < 3):
      temp = cp.copy()
      temp[0] = temp[0] +1
      if(temp not in self.holeStates):
        choices.append(RIGHT)     
    #check down
    if(cp[1] < 3): 
      temp = cp.copy()
      temp[1] = temp[1] +1
      if(temp not in self.holeStates):
        choices.append(DOWN)
    #check left
    if(cp[0] > 0):
      temp = cp.copy()
      temp[0] = temp[0] -1
      if(temp not in self.holeStates):
        choices.append(LEFT)
    #check up
    if(cp[1] > 0): 
      temp = cp.copy()
      temp[1] = temp[1] -1
      if(temp not in self.holeStates):
        choices.append(UP)         
    if(cp in self.holeStates):
      choices = [] #no choices... game over
      
    return choices
  
  #rearrange connections if needed... at begining RIGHT,DOWN,LEFT,UP .. as defined in getPossibleMoves
  #------------------
  def rearrangeConnections(self,goal,value,connections):
    gg = getGridPoint(goal)   
    
    #check all possible connections, and get their distances if you were to make that move
    distanceList=[None]*4
    for i in range(len(connections)):
      temp = getValue(value,connections[i])
      xx = getGridPoint(temp)
      dist = abs(gg[0] -xx[0]) + abs(gg[1]-xx[1])
      distanceList[connections[i]] = [connections[i],dist]
      
    #rearrange based of their distances to goal and prioritize them that way so their called in priority in the recursive function
    for x in range(len(distanceList)):
      if(distanceList[x] != None):
        for y in range(x,len(distanceList)):
          if(distanceList[y] != None):
            if(distanceList[x][1] >= distanceList[y][1]):
              #need to swap x and y values
              t = distanceList[y].copy()
              distanceList[y] = distanceList[x].copy()
              distanceList[x] = t.copy()    
              
    #now alter connection list to reflect this ordering
    c = []
    for i in distanceList:
      if(i != None):
        c.append(i[0]) 
        
    return c
 
  #recursive function-----
  #-----------------------
  def setupShortestPath(self):
    self.findShortestPath(path=[],prepath=[],visited=[],value = self.start, goal = self.goal)
    
  def findShortestPath(self,value=0,path=[],visited=[], prepath=[], goal=15):
    if(path == []):
      path.append(value)
    if(value == goal):
      if(self.path == []): #this way we only get the first path
        self.path = path.copy()
      elif(len(self.path) > len(path) ):
        self.path = path.copy()
    else:
      visited.append(value) 
      
      if(len(self.nodes[value].connections)>1):
        prepath = path.copy()
      
      #rearrange connections if needed... at begining RIGHT is priority... but if tempy > tempx... make DOWN priority)
      self.nodes[value].connections = self.rearrangeConnections(goal,value,self.nodes[value].connections)
    
      #go through each option 
      for i in self.nodes[value].connections:
        newvalue = getValue(value,i)
        if(newvalue not in visited):
          path.append(newvalue)
          self.findShortestPath(newvalue,path,visited,prepath,goal) #RECURSION CALL
          path = prepath

          

  