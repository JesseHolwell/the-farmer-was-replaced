from Movement import *

def producePower():
	resetPosition()
	
	sunflowers = []
	sunflowerSizes = {}
	sunflowerCount = 0
	largestSunflower = 0
	
	for i in range(7, 16):
		sunflowerSizes[i] = []
	
	for i in range(get_world_size() * get_world_size()):
		
		goto(i // get_world_size(), i % get_world_size())

		if (can_harvest()):
			harvest()
					
		if (get_ground_type() == Grounds.Grassland):
			till()
		
		plant(Entities.Sunflower)

		size = measure()		
		sunflowerCount = sunflowerCount + 1
		sunflowerSizes[size].append(i)
		
	for i in range(7, 16):
		index = 22 - i
		while sunflowerSizes[index] != []:
			pos = sunflowerSizes[index][0] 
			goto(pos // get_world_size(), pos % get_world_size())
			
			while can_harvest() == False:
				do_a_flip()
				
			harvest()
			sunflowerSizes[index].remove(pos)
		

#producePower()	