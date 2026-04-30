# Targeting the production achievement farming a single tile with a companion
	
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


def generate_points():

	cols = 8
	rows = 4
	grid = 32
	pts = set()
	for id in range(cols * rows):
		pts.add(getSubSquare(id, cols, rows, grid))
	return pts

def collides(point, points):
	return point in points
	

def getSubSquare(id, cols, rows, grid):

	id -= 1
	x = ((id % cols + 0.5) * grid / cols)
	y = ((id // cols + 0.5) * grid / rows)
	
	return x, y
		
def getPoint(id):
	cols = 8
	rows = 4
	grid = 32

	return getSubSquare(id, cols, rows, grid)
	
points = generate_points()
	
def plantCompanionAtPoint(point, map):
	x, y = point
	goto(x, y)
	
	#plantHay()
	
	companion = get_companion()
	if companion != None:

		nextItem, (x2, y2) = companion
		#goto(x2, y2)

		while (collides((x2, y2), points)):
			till()
			till()
			nextItem, (x2, y2) = get_companion()
			
		if ((x2, y2) not in map or map[(x2, y2)] != nextItem):
			goto(x2, y2)
			plantItem(nextItem)()
			map[(x2, y2)] = nextItem

	return map
		
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
		
def waterPoint(point):
	#x, y = point
	#goto(x, y)
	while get_water() < 0.90:
		use_item(Items.Water)
		
def hayWorker(id, startTime):
	
	x, y = getPoint(id)
	goto(x, y)
	till()
	
	map = {}
	
	map = plantCompanionAtPoint((x, y), map)
	goto(x, y)
	while (runCondition(startTime)):
		#waterPoint((x, y))
		harvestPoint((x, y))
		map = plantCompanionAtPoint((x, y), map)

def producePolycultureAsync():
	
	startingHay = num_items(Items.Hay)
	startTime = get_time()
	
	clear()
	tillFieldAsync()
	#resetPosition()
	drones = []		
	
	for i in range(31):
		spawned = spawn_drone(hayWorker, i, startTime)
		if spawned:
			drones.append(spawned)
		
	hayWorker(31, startTime)
				
	for drone in drones:
		wait_for(drone)
		
	endingHay = num_items(Items.Hay)
		
	quick_print("Produced", endingHay - startingHay, "in", runtime, "seconds")
	
producePolycultureAsync()

	
	
	
		