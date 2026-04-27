# Optimised Hamiltonian Cycle With X optimisations and short direct chase

from Movement import *
from MovementAsync import *

def initBone():
	set_world_size(6)

	change_hat(Hats.Wizard_Hat)
	if can_harvest():
		harvest()
	tillFieldAsync()
	resetPosition()

	change_hat(Hats.Dinosaur_Hat)

def exit():
	change_hat(Hats.Wizard_Hat)
	set_world_size(0)
	
tarX = 0
tarY = 0
tailLength = 0

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

def directionTo(fromX, fromY, toX, toY):
	if toX > fromX:
		return East
	if toX < fromX:
		return West
	if toY > fromY:
		return North
	if toY < fromY:
		return South
	return None

def inBounds(x, y, worldSize):
	return x >= 0 and x < worldSize and y >= 0 and y < worldSize

def getCycleDirection(path, cycleIndex):
	currX = get_pos_x()
	currY = get_pos_y()
	currIndex = cycleIndex[(currX, currY)]
	nextIndex = (currIndex + 1) % len(path)
	nextX, nextY = path[nextIndex]
	return directionTo(currX, currY, nextX, nextY)

def canTakeCycleShortcut(direction, cycleIndex, totalTiles, worldSize):
	global tarX
	global tarY
	global tailLength

	if not can_move(direction):
		return False

	currX = get_pos_x()
	currY = get_pos_y()
	nextX = currX + deltaX[direction]
	nextY = currY + deltaY[direction]

	if not inBounds(nextX, nextY, worldSize):
		return False

	currIndex = cycleIndex[(currX, currY)]
	nextIndex = cycleIndex[(nextX, nextY)]
	targetIndex = cycleIndex[(tarX, tarY)]

	stepDistance = pathDistance(currIndex, nextIndex, totalTiles)
	targetDistance = pathDistance(currIndex, targetIndex, totalTiles)

	# Do not take a shortcut that jumps past the apple we are chasing.
	if stepDistance > targetDistance:
		return False

	# tailLength counts tail pieces; add the head for the live snake length.
	# A shortcut can only jump through currently-free cycle cells. The +1 is
	# the current tail cell moving away during this step.
	snakeLength = tailLength + 1
	distanceToTail = totalTiles - snakeLength + 1
	return stepDistance <= distanceToTail

def getShortcutDirection(cycleIndex, totalTiles, worldSize):
	global tarX
	global tarY

	currX = get_pos_x()
	currY = get_pos_y()

	if tarX > currX and currY == 0:
		if canTakeCycleShortcut(East, cycleIndex, totalTiles, worldSize):
			return East

	if ((tarX < currX or (tarX == currX and tarY == worldSize - 1))
		and currX % 2 == 1 and currY < worldSize - 1):
		if canTakeCycleShortcut(North, cycleIndex, totalTiles, worldSize):
			return North

	return None

def canMoveInBounds(direction, worldSize):
	if not can_move(direction):
		return False

	nextX = get_pos_x() + deltaX[direction]
	nextY = get_pos_y() + deltaY[direction]
	return inBounds(nextX, nextY, worldSize)

def getDirectDirection(worldSize):
	global tarX
	global tarY
	global tailLength

	if tailLength + 1 >= worldSize:
		return None

	currX = get_pos_x()
	currY = get_pos_y()
	deltaToTargetX = abs(tarX - currX)
	deltaToTargetY = abs(tarY - currY)

	xDirection = None
	if tarX > currX:
		xDirection = East
	elif tarX < currX:
		xDirection = West

	yDirection = None
	if tarY > currY:
		yDirection = North
	elif tarY < currY:
		yDirection = South

	if deltaToTargetX >= deltaToTargetY:
		if xDirection != None and canMoveInBounds(xDirection, worldSize):
			return xDirection
		if yDirection != None and canMoveInBounds(yDirection, worldSize):
			return yDirection
	else:
		if yDirection != None and canMoveInBounds(yDirection, worldSize):
			return yDirection
		if xDirection != None and canMoveInBounds(xDirection, worldSize):
			return xDirection

	return None

def moveAndCheck(dir):
	global tarX
	global tarY
	global tailLength

	if not move(dir):
		return False

	if get_entity_type() == Entities.Apple:
		tailLength += 1
		nextTarget = measure()
		if nextTarget == None:
			return False
		tarX, tarY = nextTarget

	return True

def produceBoneAsync():

	global tarX
	global tarY
	global tailLength

	initBone()
	tarX, tarY = measure()
	tailLength = 0
	worldSize = get_world_size()
	cyclePath, cycleIndex = buildHamiltonianCycle(worldSize)
	totalTiles = worldSize * worldSize
	
	while True:

		direction = getDirectDirection(worldSize)
		if direction == None:
			direction = getShortcutDirection(cycleIndex, totalTiles, worldSize)
		if direction == None:
			direction = getCycleDirection(cyclePath, cycleIndex)
			
		if not moveAndCheck(direction):
			change_hat(Hats.Wizard_Hat)
			break
		
		if (not can_move(North) and
			not can_move(East) and
			not can_move(South) and
			not can_move(West)):
			change_hat(Hats.Wizard_Hat)
			break
	
	#set_world_size(0)

produceBoneAsync()
