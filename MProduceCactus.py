from Movement import *
from SmartPlanting import *

def produceCactusColumnSorted(x):
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
				
def sortCactusRow(y):
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

def produceCactusAsync():
	resetPosition()
	executeAndDoTaskByWorldIndex(produceCactusColumnSorted)
	executeAndDoTaskByWorldIndex(sortCactusRow)
	harvest()
			
#produceCactus()