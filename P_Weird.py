from H_Movement import *
from H_MovementAsync import *
from H_SmartPlanting import *
from H_Multithreading import *
from H_Statistics import *

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
	
	companion = get_companion()
	if companion != None:

		nextItem, (x2, y2) = companion

		attempts = 0
		while (collides((x2, y2), points)):
			till()
			till()
			companion = get_companion()
			if companion == None:
				return map
			nextItem, (x2, y2) = companion
			attempts += 1
			if attempts > 16:
				return map

		if ((x2, y2) not in map or map[(x2, y2)] != nextItem):
			goto(x2, y2)
			plantItem(nextItem)()
			map[(x2, y2)] = nextItem

	return map
		
def harvestPoint(point):
	x, y = point
	goto(x, y)

	if num_items(Items.Fertilizer) > 0:
		use_item(Items.Fertilizer)
	harvest()
		
def worker(id, runCondition):
	x, y = getPoint(id)
	goto(x, y)
	till()

	map = {}

	map = plantCompanionAtPoint((x, y), map)
	goto(x, y)

	iterations = 0
	stuckCount = 0
	lastWeird = num_items(Items.Weird_Substance)

	while (runCondition()):
		harvestPoint((x, y))
		map = plantCompanionAtPoint((x, y), map)
		iterations += 1

		if iterations % 50 == 0:
			currentWeird = num_items(Items.Weird_Substance)
			quick_print("weird worker", id, "iter", iterations, "weird", currentWeird, "fert", num_items(Items.Fertilizer))
			if currentWeird <= lastWeird:
				stuckCount += 1
				if stuckCount >= 4:
					quick_print("weird worker", id, "no global progress in 200 iters, bailing")
					return
			else:
				stuckCount = 0
				lastWeird = currentWeird

		if iterations > 2000:
			quick_print("weird worker", id, "hit iter cap, bailing")
			return

def produceWeird(runCondition):
	quick_print("produceWeird start: weird =", num_items(Items.Weird_Substance), "fert =", num_items(Items.Fertilizer), "drones =", num_drones())
	clear()
	tillField()
	runWorkers(worker, runCondition)
	quick_print("produceWeird done: weird =", num_items(Items.Weird_Substance))

	
	
	
		