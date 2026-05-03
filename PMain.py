from Movement import *

#hay, wood, carrots

def producePolyculture():
	resetPosition()
	
	column1 = get_world_size() / 3
	column2 = get_world_size() / 3 * 2
	
	for x in range(2):
		for i in range(get_world_size()):
			for j in range(get_world_size()):
				
				if (i < column1):
					if (get_ground_type() != Grounds.Grassland):
						till()
						
					if (can_harvest()):
						harvest()
				elif (i < column2):
					#if (get_ground_type() != Grounds.Grassland):
						#till()
						
					if (can_harvest()):
						harvest()
	
					if ((j + i) % 2 == 0):
						plant(Entities.Tree)
						#use_item(Items.Fertilizer)
						
					else:
						plant(Entities.Bush)
					
				else:
					if (get_ground_type() == Grounds.Grassland):
						till()
					
					if (can_harvest()):
						harvest()
						
					plant(Entities.Carrot)

				
				move(North)
			move(East)			
			
			
#producePolyculture()