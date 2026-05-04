from H_Movement import *
from H_MovementAsync import *
from H_SmartPlanting import *
from H_Multithreading import *
from H_Statistics import *
		
def fillFieldWithTrees():
	def plantAlternatingColumn(x):
		for y in range(get_world_size()):
			if (x + y) % 2 == 0:
				goto(x, y)
				if get_ground_type() == Grounds.Grassland:
					till()
				if get_entity_type() != Entities.Tree:
					plant(Entities.Tree)
		
	executeAndDoTaskByWorldIndex(plantAlternatingColumn)
		
def collides(point):
	x, y = point
	return (x + y) % 1
		
def plantCarrot():
	
	viableCompanion = False
	
	while not viableCompanion:
		harvest()
		plant(Entities.Carrot)
		nextItem, (x2, y2) = get_companion()
		viableCompanion = not (collides((x2, y2)) or nextItem != Entities.Tree)
		
def harvestPoint():
	while not can_harvest():
		if get_water() < 0.75:
			use_item(Items.Water)
	harvest()
		
def worker(id, runCondition):
	x, y = 0, id
	
	while (runCondition()):
		if (x + y) % 2 == 1:
			goto(x, y)
			if (get_entity_type() == Entities.Carrot):
				harvestPoint()
			plantCarrot()
		x += 1

def produceCarrots(runCondition):
	clear()
	tillField()
	fillFieldWithTrees()
	runWorkers(worker, runCondition)