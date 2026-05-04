from H_Movement import *
from H_Multithreading import *

def tillField():
	def tillColumn(x):
		for y in range(get_world_size()):
			goto(x, y)
			if get_ground_type() == Grounds.Grassland:
				till()
		
	executeAndDoTaskByWorldIndex(tillColumn)