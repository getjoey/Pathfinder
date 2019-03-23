#------------------------------------------------        
#----------example for output and testing--------
#------------------------------------------------
#------------------------------------------------
#visual view of map and path
# S = Start
# P = path
# - = walkable area not on apth
# H = Hole
# G = Goal

#ex1
from pathfinder import *
import random

mapsToDisplay = 10
for i in range(mapsToDisplay):
	startValue = random.randrange(0,16)
	goalValue = random.randrange(0,16)
	map = Map(start=startValue,goal=goalValue,holesAmount=4)
	map.printMap()
	del map

