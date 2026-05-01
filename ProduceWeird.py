from Movement import *

def produceWeird():
	clear()
	resetPosition()

	for x in range(2):
		for i in range(get_world_size()):
			for j in range(get_world_size()):
				
				if (i + j) % 2 == 0:
					goto(i, j)
					
					if (can_harvest() and get_entity_type() != Entities.Grass):
						harvest()
						
					plant(Entities.Tree)
					use_item(Items.Weird_Substance)
				
#produceWeird()