from Movement import *
from SmartPlanting import *
from Multithreading import *

def producePowerColumn(x):
	for y in range(get_world_size()):
		goto(x, y)
		plantSunflower()
	
def harvestPowerColumn(x, size):
	for y in range(get_world_size()):
		goto(x, y)
		if (measure() == size):
			# this is gross im tired
			if not can_harvest():
				while not can_harvest():
					if get_water() < 0.75:
						use_item(Items.Water)
						
			harvest()
			
def harvestPowerColumnTask(index):
	def f(x):
		harvestPowerColumn(x, index)
	return f
	
def producePowerAsync():
	resetPosition()
	
	executeTaskByWorldIndex(producePowerColumn)
		
	for i in range(7, 16):
		index = 22 - i		
		executeTaskByWorldIndex(harvestPowerColumnTask(index))

#producePower()
	
				
	
		
	