from H_Movement import *
from H_MovementAsync import *
from H_SmartPlanting import *
from H_Multithreading import *

def produceSunflowersColumn(x):
	for y in range(get_world_size()):
		goto(x, y)
		plantSunflower()
		if (measure() == 15):
			while get_water() < 0.75:
				use_item(Items.Water)
	
def harvestSunflowersColumn(x, size):
	for y in range(get_world_size()):
		goto(x, y)
		if (measure() == size):
			# this is gross im tired
			if not can_harvest():
				while not can_harvest():
					if get_water() < 0.75:
						use_item(Items.Water)
						
			harvest()
			
def harvestSunflowersColumnTask(index):
	def f(x):
		harvestSunflowersColumn(x, index)
	return f
	
def produceSunflowers(runCondition):
	clear()
	
	while (runCondition()):
		executeAndDoTaskByWorldIndex(produceSunflowersColumn)
		
		#sunflowers range from 7 to 15
		for i in range(7, 16):
			index = 22 - i		
			executeAndDoTaskByWorldIndex(harvestSunflowersColumnTask(index))
	
				
	
		
	