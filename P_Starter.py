from H_Movement import *

def produceHaySingle(runCondition):
	while (runCondition()):
		while not can_harvest():
			t = 0
		harvest()

def produceHayColumn(runCondition):
	while (runCondition()):
		while not can_harvest():
			t = 0
		harvest()
		move(North)
	
def produceBushes(runCondition):
	while (runCondition()):
		if (get_entity_type() != Entities.Bush or can_harvest()):
			harvest()
			plant(Entities.Bush)
		move(North)	

def produceTriplet(runCondition):
	clear()
	
	column1 = get_world_size() / 3
	column2 = get_world_size() / 3 * 2
	
	while (runCondition()):
		for i in range(get_world_size()):
			for j in range(get_world_size()):
				
				if (i < column1):
					if (get_ground_type() != Grounds.Grassland):
						till()
						
					if (can_harvest()):
						harvest()
				elif (i < column2):
					if num_unlocked(Unlocks.Trees) > 0:
						woodPlant = Entities.Tree
					else:
						woodPlant = Entities.Bush
					if (can_harvest()):
						harvest()
						plant(woodPlant)
					elif (get_entity_type() != woodPlant):
						plant(woodPlant)

				else:
					if (get_ground_type() == Grounds.Grassland):
						till()

					if (can_harvest()):
						harvest()
						if (num_items(Items.Wood) > 0 and num_items(Items.Hay) > 0):
							plant(Entities.Carrot)
					elif (get_entity_type() != Entities.Carrot):
						if (num_items(Items.Wood) > 0 and num_items(Items.Hay) > 0):
							plant(Entities.Carrot)

				
				move(East)
			move(North)	