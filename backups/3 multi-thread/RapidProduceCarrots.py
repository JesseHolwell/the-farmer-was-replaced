# Targeting the production achievement farming a grid with an offset grid of trees
# 333m per minute
	
from Movement import *
from MovementAsync import *
from SmartPlanting import *
from Multithreading import *
from Statistics import *

runtime = 120

def runCondition(time):
	if (time == None):
		return num_items(Items.Carrot) < 2000000000
	else:
		return get_time() - time < runtime
		
def fillFieldWithTreesAsync():
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
		
	#while get_water() < 0.75:
	#	use_item(Items.Water)
		
def harvestPoint():
	while not can_harvest():
		if get_water() < 0.75:
			use_item(Items.Water)
	harvest()
		
def worker(id, timeBased):
	
	x, y = 0, id
	
	startTime = None
	if (timeBased):
		startTime = get_time()
	
	while (runCondition(startTime)):
		if (x + y) % 2 == 1:
			goto(x, y)
			if (get_entity_type() == Entities.Carrot):
				harvestPoint()
			plantCarrot()
		x += 1

def produceCarrotsAsync(timeBased):
	
	starting = num_items(Items.Carrot)
	
	clear()
	tillFieldAsync()
	fillFieldWithTreesAsync()
	
	drones = []		
	
	for i in range(31):
		spawned = spawn_drone(worker, i, timeBased)
		if spawned:
			drones.append(spawned)
		
	worker(31, timeBased)
				
	for drone in drones:
		wait_for(drone)
		
	ending = num_items(Items.Carrot)
		
	quick_print("Produced", ending - starting, "in", runtime, "seconds")
	
produceCarrotsAsync(True)

	
	
	
		