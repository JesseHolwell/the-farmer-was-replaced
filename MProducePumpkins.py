from Movement import *
from Multithreading import *

def producePumpkinColumn(x):
	pumpkins = []
	pumpkinCount = 0
	for y in range(get_world_size()):
		pumpkins.append(0)
		
	while pumpkinCount != get_world_size():	
		for y in range(len(pumpkins)):
				
			if (pumpkins[y] == 1):
				continue
			
			goto(x, y)
			
			if (can_harvest()
				and get_entity_type() != Entities.Grass
				and get_entity_type() != Entities.Pumpkin):
				harvest()
				
			if (get_ground_type() == Grounds.Grassland):
				till()
			
			if (can_harvest()):
				pumpkins[y] = 1
				pumpkinCount = pumpkinCount + 1
			else:
				plant(Entities.Pumpkin)
				#if (pumpkinCount / get_world_size()
					#> get_water()):
					#use_item(Items.Water)
				
				if (pumpkinCount > get_world_size() / 2):
					use_item(Items.Water)
		
			if pumpkinCount == get_world_size():
				break
	

def producePumpkinsAsync():
	resetPosition()
	executeAndDoTaskByWorldIndex(producePumpkinColumn)
	harvest()
			
#producePumpkins()