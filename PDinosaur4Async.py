# Optimised Hamiltonian Cycle With full-column detours

from Movement import *
from MovementAsync import *

def initBone():
	#set_world_size(10)

	change_hat(Hats.Wizard_Hat)
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

def getCycleDirection(path, cycleIndex):
	currX = get_pos_x()
	currY = get_pos_y()
	currIndex = cycleIndex[(currX, currY)]
	nextIndex = (currIndex + 1) % len(path)
	nextX, nextY = path[nextIndex]
	return directionTo(currX, currY, nextX, nextY)

def copyBody(body):
	out = []
	for pos in body:
		out.append(pos)
	return out

def copySet(values):
	out = set()
	for value in values:
		out.add(value)
	return out

def appendRepeated(path, direction, steps):
	for i in range(steps):
		path.append(direction)

def nextPosition(x, y, direction):
	return x + deltaX[direction], y + deltaY[direction]

def canMoveDirect(direction, worldSize, bodySet, tail, apple):
	currX = get_pos_x()
	currY = get_pos_y()
	nextX, nextY = nextPosition(currX, currY, direction)

	if not inBounds(nextX, nextY, worldSize):
		return False

	nextPos = (nextX, nextY)
	return not (nextPos in bodySet and not (nextPos == tail and nextPos != apple))

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

def getDirectDirection(worldSize, body, bodySet):
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

	tail = body[0]
	apple = (tarX, tarY)

	for direction in preferredDirections:
		if canMoveDirect(direction, worldSize, bodySet, tail, apple):
			return direction

	return None

def simulatePath(path, worldSize, body, bodySet, apple):
	if len(path) == 0:
		return False

	simBody = copyBody(body)
	simSet = copySet(bodySet)
	headX, headY = simBody[len(simBody) - 1]
	ateApple = False

	for direction in path:
		nextX, nextY = nextPosition(headX, headY, direction)

		if not inBounds(nextX, nextY, worldSize):
			return False

		nextPos = (nextX, nextY)
		willEat = not ateApple and nextPos == apple

		if nextPos in simSet and not (nextPos == simBody[0] and not willEat):
			return False

		if willEat:
			simBody.append(nextPos)
			simSet.add(nextPos)
			ateApple = True
		else:
			removed = simBody.pop(0)
			simSet.remove(removed)
			simBody.append(nextPos)
			simSet.add(nextPos)

		headX = nextX
		headY = nextY

	return ateApple

def buildTopDetourPath(worldSize, body, bodySet):
	global tarX
	global tarY

	headX, headY = body[len(body) - 1]
	topY = worldSize - 1

	if headY != topY or tarY >= topY or tarX >= headX:
		return None

	if tarX <= 0 or tarX >= worldSize - 1:
		return None

	# Top row moves left. Descend on an even column, cross left,
	# then rise on the matching odd column.
	if tarX % 2 == 0:
		downX = tarX
		upX = tarX - 1
	else:
		downX = tarX + 1
		upX = tarX

	if upX <= 0 or downX >= worldSize - 1 or headX < downX:
		return None

	path = []
	appendRepeated(path, West, headX - downX)
	appendRepeated(path, South, topY)
	path.append(West)
	appendRepeated(path, North, topY)

	apple = (tarX, tarY)
	if simulatePath(path, worldSize, body, bodySet, apple):
		return path

	return None

def buildBottomDetourPath(worldSize, body, bodySet):
	global tarX
	global tarY

	headX, headY = body[len(body) - 1]
	topY = worldSize - 1

	if headY != 0 or tarY <= 0 or tarX <= headX:
		return None

	if tarX <= 0 or tarX >= worldSize - 1:
		return None

	# Bottom row moves right. Rise on an odd column, cross right,
	# then descend on the matching even column.
	if tarX % 2 == 1:
		upX = tarX
		downX = tarX + 1
	else:
		upX = tarX - 1
		downX = tarX

	if upX <= 0 or downX >= worldSize - 1 or headX > upX:
		return None

	path = []
	appendRepeated(path, East, upX - headX)
	appendRepeated(path, North, topY)
	path.append(East)
	appendRepeated(path, South, topY)

	apple = (tarX, tarY)
	if simulatePath(path, worldSize, body, bodySet, apple):
		return path

	return None

def buildDetourPath(worldSize, body, bodySet):
	path = buildTopDetourPath(worldSize, body, bodySet)
	if path != None:
		return path

	return buildBottomDetourPath(worldSize, body, bodySet)

def getCorridorShortcutDirection(cycleIndex, totalTiles, worldSize, body, bodySet):
	global tarX
	global tarY

	currX = get_pos_x()
	currY = get_pos_y()
	topY = worldSize - 1
	tail = body[0]
	apple = (tarX, tarY)

	if currY == 0 and tarX > currX:
		if canMoveDirect(East, worldSize, bodySet, tail, apple):
			return East

	if currY == topY and tarX < currX:
		if canMoveDirect(West, worldSize, bodySet, tail, apple):
			return West

	return None

def getBestSafeDirection(cyclePath, cycleIndex, totalTiles, worldSize, body, bodySet):
	if len(body) < worldSize:
		direction = getDirectDirection(worldSize, body, bodySet)
		if direction != None:
			return direction

	direction = getCorridorShortcutDirection(cycleIndex, totalTiles, worldSize, body, bodySet)
	if direction != None:
		return direction

	return getCycleDirection(cyclePath, cycleIndex)

def moveAndCheck(dir, body, bodySet):
	global tarX
	global tarY

	oldTarget = (tarX, tarY)

	if not move(dir):
		return False

	newX = get_pos_x()
	newY = get_pos_y()
	newHead = (newX, newY)

	if newHead == oldTarget:
		body.append(newHead)
		bodySet.add(newHead)

		nextTarget = measure()
		if nextTarget == None:
			return False
		tarX, tarY = nextTarget
	else:
		removed = body.pop(0)
		bodySet.remove(removed)
		body.append(newHead)
		bodySet.add(newHead)

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
	bodySet = set()
	bodySet.add(body[0])
	plannedPath = []
	plannedIndex = 0
	
	while True:

		if plannedIndex >= len(plannedPath):
			plannedPath = buildDetourPath(worldSize, body, bodySet)
			plannedIndex = 0

		if plannedPath != None and plannedIndex < len(plannedPath):
			direction = plannedPath[plannedIndex]
			plannedIndex = plannedIndex + 1
		else:
			direction = getBestSafeDirection(cyclePath, cycleIndex, totalTiles, worldSize, body, bodySet)
			
		if not moveAndCheck(direction, body, bodySet):
			change_hat(Hats.Wizard_Hat)
			break

		if plannedPath != None and plannedIndex < len(plannedPath):
			tail = body[0]
			apple = (tarX, tarY)
			if not canMoveDirect(plannedPath[plannedIndex], worldSize, bodySet, tail, apple):
				plannedPath = []
				plannedIndex = 0
	
	#set_world_size(0)

#produceBoneAsync()
