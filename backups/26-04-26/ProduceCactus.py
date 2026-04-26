from Movement import *

def produceCactus():
	
	#set_world_size(6)
	
	resetPosition()
	
	# PLANT
	for x in range(get_world_size()):
		for y in range(get_world_size()):
	
			goto(x, y)
		
			if (can_harvest()):
				harvest()
						
			if (get_ground_type() == Grounds.Grassland):
				till()
			
			plant(Entities.Cactus)
		
	sorted = False

	while not sorted:
		
		changed = False
		# SORT X
		for x in range(get_world_size()):
			for y in range(get_world_size()):
		
				goto(x, y)
				
				if (measure() > measure(East) and x < get_world_size() - 1):
					swap(East)
					changed = True
					
				if (measure(West) > measure() and x > 0):
					swap(West)
					changed = True	
					
				if (measure() > measure(North) and y < get_world_size() - 1):
					swap(North)
					changed = True
					
				if (measure(South) > measure() and y > 0):
					swap(South)
					changed = True
		
		# SORT Y		
		#for y in range(get_world_size()):
		#	for x in range(get_world_size()):
		
		#		goto(x, y)
				
		#		if (measure() > measure(North) and y < get_world_size() - 1):
		#			swap(North)
		#			changed = True
				
		sorted = not changed
			
	harvest()