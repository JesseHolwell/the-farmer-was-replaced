# Optimised Hamiltonian Cycle With X/Y optimisations

from H_Movement import *
from H_MovementAsync import *

def initBone():
	set_world_size(10)

	change_hat(Hats.Straw_Hat)
	if can_harvest():
		harvest()
	tillFieldAsync()
	resetPosition()

	change_hat(Hats.Dinosaur_Hat)

def exit():
	change_hat(Hats.Wizard_Hat)
	#set_world_size(0)
	
tarX = 0
tarY = 0

def buildHamiltonianCycle(worldSize):
	path = []

	path.append((0, 0))

	for x in range(1, worldSize - 1):
		if x % 2 == 1:
			for y in range(0, worldSize - 1):
				path.append((x, y))
		else:
			for y in range(worldSize - 2, -1, -1):
				path.append((x, y))

	for y in range(0, worldSize):
		path.append((worldSize - 1, y))

	for x in range(worldSize - 2, -1, -1):
		path.append((x, worldSize - 1))

	for y in range(worldSize - 2, 0, -1):
		path.append((0, y))

	cycleIndex = {}
	for i in range(len(path)):
		cycleIndex[path[i]] = i

	return path, cycleIndex

def pathDistance(fromIndex, toIndex, totalTiles):
	if toIndex >= fromIndex:
		return toIndex - fromIndex
	return totalTiles - fromIndex + toIndex

def inBounds(x, y, worldSize):
	return x >= 0 and x < worldSize and y >= 0 and y < worldSize

def getSafeMoveDistance(direction, cycleIndex, totalTiles, worldSize, body):
	global tarX
	global tarY

	if not can_move(direction):
		return None

	currX = get_pos_x()
	currY = get_pos_y()
	nextX = currX + deltaX[direction]
	nextY = currY + deltaY[direction]

	if not inBounds(nextX, nextY, worldSize):
		return None

	currIndex = cycleIndex[(currX, currY)]
	nextIndex = cycleIndex[(nextX, nextY)]
	targetIndex = cycleIndex[(tarX, tarY)]
	tailX, tailY = body[0]
	tailIndex = cycleIndex[(tailX, tailY)]

	stepDistance = pathDistance(currIndex, nextIndex, totalTiles)
	targetDistance = pathDistance(currIndex, targetIndex, totalTiles)
	tailDistance = pathDistance(currIndex, tailIndex, totalTiles)

	if tailDistance == 0:
		tailDistance = totalTiles

	# Do not take a shortcut that jumps past the apple we are chasing.
	if stepDistance > targetDistance:
		return None

	# The current tail cell may move away during this step, but anything beyond
	# it is still occupied snake territory.
	if stepDistance > tailDistance:
		return None

	return stepDistance

def getDirectDirection(cycleIndex, totalTiles, worldSize, body):
	global tarX
	global tarY

	currX = get_pos_x()
	currY = get_pos_y()

	preferredDirections = []

	if tarX > currX:
		preferredDirections.append(East)
	elif tarX < currX:
		preferredDirections.append(West)

	if tarY > currY:
		preferredDirections.append(North)
	elif tarY < currY:
		preferredDirections.append(South)

	for direction in preferredDirections:
		if getSafeMoveDistance(direction, cycleIndex, totalTiles, worldSize, body) != None:
			return direction

	return None

def getBestSafeDirection(cycleIndex, totalTiles, worldSize, body):
	if len(body) < worldSize:
		direction = getDirectDirection(cycleIndex, totalTiles, worldSize, body)
		if direction != None:
			return direction

	bestDirection = None
	bestDistance = 0

	for direction in directions:
		distance = getSafeMoveDistance(direction, cycleIndex, totalTiles, worldSize, body)

		if distance == None:
			continue

		if distance > bestDistance:
			bestDistance = distance
			bestDirection = direction

	return bestDirection

def moveAndCheck(dir, body):
	global tarX
	global tarY

	if not move(dir):
		return False

	newX = get_pos_x()
	newY = get_pos_y()
	newHead = (newX, newY)

	if get_entity_type() == Entities.Apple:
		body.append(newHead)

		nextTarget = measure()
		if nextTarget == None:
			return False
		tarX, tarY = nextTarget
	else:
		body.pop(0)
		body.append(newHead)

	return True

def produceBoneAsync():

	global tarX
	global tarY

	initBone()
	tarX, tarY = measure()
	worldSize = get_world_size()
	cyclePath, cycleIndex = buildHamiltonianCycle(worldSize)
	totalTiles = len(cyclePath)
	body = [(get_pos_x(), get_pos_y())]
	
	while True:

		direction = getBestSafeDirection(cycleIndex, totalTiles, worldSize, body)
		if direction == None:
			change_hat(Hats.Straw_Hat)
			break
			
		if not moveAndCheck(direction, body):
			change_hat(Hats.Wizard_Hat)
			break
	
	#set_world_size(0)

produceBoneAsync()
