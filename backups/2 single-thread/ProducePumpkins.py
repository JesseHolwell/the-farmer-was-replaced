from Movement import *

def producePumpkins():
	#clear()
	resetPosition()
	#clearField()
	
	pumpkins = []
	pumpkinCount = 0
	for i in range(get_world_size() * get_world_size()):
		pumpkins.append(0)
	
	while True:
		
		for i in range(len(pumpkins)):
			
			if (pumpkins[i] == 1):
				continue
			
			goto(i // get_world_size(), i % get_world_size())
			
			if (can_harvest()
				and get_entity_type() != Entities.Grass
				and get_entity_type() != Entities.Pumpkin):
				harvest()
				
			if (get_ground_type() == Grounds.Grassland):
				till()
			
			if (can_harvest()):
				pumpkins[i] = 1
				pumpkinCount = pumpkinCount + 1
			else:
				plant(Entities.Pumpkin)
				
		if (pumpkinCount == get_world_size() * get_world_size()):
			harvest()
			break
	#		pumpkinCount = 0
	#		for i in range(get_world_size() * get_world_size()):
	#			pumpkins[i] = 0
			
#producePumpkins()