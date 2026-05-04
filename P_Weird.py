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
	
	use_item(Items.Fertilizer)
	harvest()
		
def worker(id, timeBased):
	
	x, y = getPoint(id)
	goto(x, y)
	till()
	
	map = {}
	
	map = plantCompanionAtPoint((x, y), map)
	goto(x, y)
	
	startTime = None
	if (timeBased):
		startTime = get_time()
	
	while (runCondition(startTime)):
		harvestPoint((x, y))
		map = plantCompanionAtPoint((x, y), map)

def produceWeird(runCondition):
	clear()
	tillField()
	runWorkers(worker, runCondition)

	
	
	
		