from H_Movement import *
from H_MovementAsync import *
from H_Multithreading import *

def worker(x, runCondition):
	pumpkins = []
	pumpkinCount = 0
	for y in range(get_world_size()):
		pumpkins.append(0)
		
	while pumpkinCount != get_world_size():	
		for y in range(len(pumpkins)):
				
			if (pumpkins[y] == 1):
				continue
			
			goto(x, y)
				
			if (get_ground_type() == Grounds.Grassland):
				till()
			
			if (can_harvest()):
				pumpkins[y] = 1
				pumpkinCount += 1
			else:
				plant(Entities.Pumpkin)
				
				if (pumpkinCount > get_world_size() / 2):
					use_item(Items.Water)
		
			if pumpkinCount == get_world_size():
				break
	
def producePumpkins(runCondition):
	clear()
	while (runCondition()):
		runWorkers(worker, runCondition)
		harvest()