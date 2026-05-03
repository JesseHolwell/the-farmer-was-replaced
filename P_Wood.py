from H_Movement import *
from H_MovementAsync import *
from H_SmartPlanting import *
from H_Multithreading import *
from H_Statistics import *
		
def collides(point):
	x, y = point
	return (x + y) % 1
		
def plantTree():
	
	viableCompanion = False
	
	while not viableCompanion:
		harvest()
		plant(Entities.Tree)
		nextItem, (x2, y2) = get_companion()
		viableCompanion = not (collides((x2, y2)) or nextItem != Entities.Grass)
		
	while get_water() < 0.75:
		use_item(Items.Water)
		
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
			if (get_entity_type() == Entities.Tree):
				harvestPoint()
			plantTree()
		x += 1

def produceWood(runCondition):
	
	clear()
	drones = []
	
	for i in range(max_drones() - 1):
		spawned = spawn_drone(worker, i, runCondition)
		if spawned:
			drones.append(spawned)
		
	worker(max_drones() - 1, runCondition)
				
	for drone in drones:
		wait_for(drone)