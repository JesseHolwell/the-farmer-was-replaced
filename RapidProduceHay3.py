# Targeting the production achievement farming a grid with alternating back and forth
# 127m per minute

	
from Movement import *
from MovementAsync import *
from SmartPlanting import *
from Multithreading import *
from Statistics import *

runtime = 60

def runCondition(time):
	if (time):
		return get_time() - time < runtime
#	else
#		return num_items(Items.Hay) < 2000000000
	
def plantCompanionForPoint(point):
	x, y = point
	x2 = 0
	y2 = 0
	nextItem = None
	viableCompanion = False

	goto(x, y)
	
	while (not viableCompanion):
		till()
		till()
		nextItem, (x2, y2) = get_companion()
		viableCompanion = (x == 1 and x2 == 0 and y2 == y) or (x == 2 and x2 == 3 and y2 == y)
		
	goto(x2, y2)
	plantItem(nextItem)()
		
def harvestPoint(point):
	x, y = point
	goto(x, y)
	
	#while not can_harvest():
	#	if (num_items(Items.Fertilizer) > 100
	#		and num_items(Items.Weird_Substance) > 0):
	#		use_item(Items.Fertilizer)
	#		use_item(Items.Weird_Substance)
	while not can_harvest():
		if get_water() < 0.90:
			use_item(Items.Water)
	harvest()
		
def hayPlanter(id, startTime):
	y = id
	
	for x in range(2):
		plantCompanionForPoint((x+1, y))
				
def hayHarvester(id, startTime):
	y = id
	#goto(0, id)
	
	while (runCondition(startTime)):
		for x in range(2):
			harvestPoint((x+1, y))

def producePolycultureAsync():
	
	startingHay = num_items(Items.Hay)
	startTime = get_time()
	
	clear()
	#set_world_size(10)
	#resetPosition()
	drones = []		
	
	for i in range(31):
		spawned = spawn_drone(hayPlanter, i, startTime)
		if spawned:
			drones.append(spawned)
		
	hayPlanter(31, startTime)
				
	for drone in drones:
		wait_for(drone)
		
	drones = []
	startTime = get_time()
		
	for i in range(31):
		spawned = spawn_drone(hayHarvester, i, startTime)
		if spawned:
			drones.append(spawned)
		
	hayHarvester(31, startTime)
	
	for drone in drones:
		wait_for(drone)
		
	endingHay = num_items(Items.Hay)
		
	quick_print("Produced", endingHay - startingHay, "in", runtime, "seconds")
	
producePolycultureAsync()

	
	
	
		