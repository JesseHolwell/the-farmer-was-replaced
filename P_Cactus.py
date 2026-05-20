from H_Movement import *
from H_MovementAsync import *
from H_SmartPlanting import *
from P_Pumpkins import *

def workerColumn(x, runCondition = None):
	sizeMap = {}
	for y in range(get_world_size()):
		goto(x, y)
		plantCactus()
		sizeMap[y] = measure()
		
	for i in range(get_world_size()):
		swapped = False
		
		for y in range(get_world_size() - 1 - i):
			down = y
			up = y + 1
			
			if sizeMap[down] > sizeMap[up]:
				goto(x, y)
				swap(North)
				temp = sizeMap[down]
				sizeMap[down] = sizeMap[up]
				sizeMap[up] = temp
				swapped = True
				
		if not swapped:
			break
				
def workerRow(y, runCondition = None):
	sizeMap = {}
	for x in range(get_world_size()):
		goto(x, y)
		sizeMap[x] = measure()
		
	for i in range(get_world_size()):
		swapped = False
		
		for x in range(get_world_size() - 1 - i):
			left = x
			right = x + 1
			
			if sizeMap[left] > sizeMap[right]:
				goto(x, y)
				swap(East)
				temp = sizeMap[left]
				sizeMap[left] = sizeMap[right]
				sizeMap[right] = temp
				swapped = True

		if not swapped:
			break

def produceCactus(runCondition):
	clear()
	while (runCondition()):
		ws = get_world_size()
		seedCost = get_cost(Entities.Cactus)
		if seedCost:
			for seedItem in seedCost:
				if seedItem == Items.Cactus:
					continue
				needed = seedCost[seedItem] * ws * ws
				if num_items(seedItem) < needed:
					if seedItem == Items.Pumpkin:
						def needPumpkin():
							return num_items(Items.Pumpkin) < needed
						producePumpkins(needPumpkin)
						clear()
		before = num_items(Items.Cactus)
		runWorkers(workerColumn, None)
		runWorkers(workerRow, None)
		harvest()
		if num_items(Items.Cactus) <= before:
			return