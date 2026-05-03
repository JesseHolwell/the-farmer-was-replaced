from Movement import *

# Bubble sort

sizeMap = {}

def produceCactus():
	
	resetPosition()
	
	for x in range(get_world_size()):
		for y in range(get_world_size()):
	
			goto(x, y)
		
			if (can_harvest()
				and get_entity_type() != Entities.Cactus
				and get_entity_type() != Entities.Grass):
				harvest()
						
			if (get_ground_type() == Grounds.Grassland):
				till()
			
			plant(Entities.Cactus)
			
			sizeMap[(x, y)] = measure()
			
	# sort the columns
	for x in range(get_world_size()):
		for i in range(get_world_size()):
			swapped = False
			
			for y in range(get_world_size() - 1 - i):
				left = (x, y)
				right = (x, y + 1)
				
				if sizeMap[left] > sizeMap[right]:
					goto(x, y)
					swap(North)
					temp = sizeMap[left]
					sizeMap[left] = sizeMap[right]
					sizeMap[right] = temp
					swapped = True
					
			if not swapped:
				break
				

	
	# sort the rows
	for y in range(get_world_size()):
		for i in range(get_world_size()):
			swapped = False
			
			for x in range(get_world_size() - 1 - i):
				down = (x, y)
				up = (x + 1, y)
				
				if sizeMap[down] > sizeMap[up]:
					goto(x, y)
					swap(East)
					temp = sizeMap[down]
					sizeMap[down] = sizeMap[up]
					sizeMap[up] = temp
					swapped = True

			if not swapped:
				break
	
	harvest()
			
#produceCactus()