from Movement import *
from Multithreading import *

def tillFieldAsync():
	def tillColumn(x):
		for y in range(get_world_size()):
			goto(x, y)
			if get_ground_type() == Grounds.Grassland:
				till()
		
	executeAndDoTaskByWorldIndex(tillColumn)