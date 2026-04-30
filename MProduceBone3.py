# Next-gen bone pathing: MProduceBone2 baseline plus cached plans.

from Movement import *
from MovementAsync import *

def initBone():
	#set_world_size(6)

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

def buildMoveTable(worldSize, cycleIndex, totalTiles):
	moveTable = {}

	for x in range(worldSize):
		for y in range(worldSize):
			currIndex = cycleIndex[(x, y)]

			for direction in directions:
				nextX = x + deltaX[direction]
				nextY = y + deltaY[direction]

				if not inBounds(nextX, nextY, worldSize):
					moveTable[(x, y, direction)] = None
				else:
					nextIndex = cycleIndex[(nextX, nextY)]
					forward = pathDistance(currIndex, nextIndex, totalTiles)
					moveTable[(x, y, direction)] = (nextX, nextY, nextIndex, forward)

	return moveTable

def directionTo(fromX, fromY, toX, toY):
	if toX > fromX:
		return East
	if toX < fromX:
		return West
	if toY > fromY:
		return North
	return South

def liveLength(body, tailIdx):
	return len(body) - tailIdx

def copyBody(body, tailIdx):
	out = []
	for i in range(tailIdx, len(body)):
		out.append(body[i])
	return out

def copySet(values):
	out = set()
	for value in values:
		out.add(value)
	return out

def appendRepeated(path, direction, steps):
	for i in range(steps):
		path.append(direction)

def isBlockedForNextStep(nextPos, simBody, simSet, willEat):
	if not nextPos in simSet:
		return False

	# The tail only moves away on non-eating moves.
	if not willEat and nextPos == simBody[0]:
		return False

	return True

def simulatePath(path, body, tailIdx, bodySet, moveTable, apple):
	if len(path) == 0:
		return None, None, None, None

	simBody = copyBody(body, tailIdx)
	simSet = copySet(bodySet)
	headX, headY = simBody[len(simBody) - 1]
	ateApple = False

	for direction in path:
		moveInfo = moveTable[(headX, headY, direction)]
		if moveInfo == None:
			return None, None, None, None

		nextX, nextY, nextIndex, forward = moveInfo
		nextPos = (nextX, nextY)
		willEat = not ateApple and nextPos == apple

		if isBlockedForNextStep(nextPos, simBody, simSet, willEat):
			return None, None, None, None

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

	return simBody, simSet, (headX, headY), ateApple

def getSafeCycleDistance(headX, headY, currIndex, direction, moveTable,
	targetIndex, tailIndex, totalTiles, bodySet, tail, apple):
	moveInfo = moveTable[(headX, headY, direction)]
	if moveInfo == None:
		return None

	nextX, nextY, nextIndex, stepDistance = moveInfo
	nextPos = (nextX, nextY)

	if nextPos in bodySet:
		if not (nextPos == tail and nextPos != apple):
			return None

	targetDistance = pathDistance(currIndex, targetIndex, totalTiles)
	tailDistance = pathDistance(currIndex, tailIndex, totalTiles)

	if tailDistance == 0:
		tailDistance = totalTiles

	if stepDistance > targetDistance:
		return None

	if stepDistance > tailDistance:
		return None

	return stepDistance

def getBestCycleDirection(headX, headY, cycleIndex, moveTable, totalTiles, body, tailIdx, bodySet):
	global tarX
	global tarY

	currIndex = cycleIndex[(headX, headY)]
	targetIndex = cycleIndex[(tarX, tarY)]
	tail = body[tailIdx]
	tailIndex = cycleIndex[tail]
	apple = (tarX, tarY)

	bestDirection = None
	bestDistance = 0

	for direction in directions:
		distance = getSafeCycleDistance(headX, headY, currIndex, direction, moveTable,
			targetIndex, tailIndex, totalTiles, bodySet, tail, apple)

		if distance == None:
			continue

		if distance > bestDistance:
			bestDistance = distance
			bestDirection = direction

	return bestDirection

def buildDirectPlan(worldSize, moveTable, body, tailIdx, bodySet):
	global tarX
	global tarY

	headX, headY = body[len(body) - 1]
	apple = (tarX, tarY)

	xDir = None
	if tarX > headX:
		xDir = East
	elif tarX < headX:
		xDir = West

	yDir = None
	if tarY > headY:
		yDir = North
	elif tarY < headY:
		yDir = South

	deltaXAbs = abs(tarX - headX)
	deltaYAbs = abs(tarY - headY)

	firstDir = xDir
	secondDir = yDir
	firstSteps = deltaXAbs
	secondSteps = deltaYAbs

	if deltaYAbs > deltaXAbs:
		firstDir = yDir
		secondDir = xDir
		firstSteps = deltaYAbs
		secondSteps = deltaXAbs

	path = []
	if firstDir != None:
		appendRepeated(path, firstDir, firstSteps)
	if secondDir != None:
		appendRepeated(path, secondDir, secondSteps)

	simBody, simSet, endPos, ateApple = simulatePath(path, body, tailIdx, bodySet, moveTable, apple)
	if ateApple:
		return path

	path = []
	if secondDir != None:
		appendRepeated(path, secondDir, secondSteps)
	if firstDir != None:
		appendRepeated(path, firstDir, firstSteps)

	simBody, simSet, endPos, ateApple = simulatePath(path, body, tailIdx, bodySet, moveTable, apple)
	if ateApple:
		return path

	return None

def buildTopDetourPlan(worldSize, moveTable, body, tailIdx, bodySet):
	global tarX
	global tarY

	headX, headY = body[len(body) - 1]
	topY = worldSize - 1

	if headY != topY or tarY >= topY or tarX >= headX:
		return None

	if tarX <= 0 or tarX >= worldSize - 1:
		return None

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
	appendRepeated(path, South, topY - tarY)

	if tarX == upX:
		path.append(West)

	apple = (tarX, tarY)
	simBody, simSet, endPos, ateApple = simulatePath(path, body, tailIdx, bodySet, moveTable, apple)
	if not ateApple:
		return None

	# Make sure there is a plausible escape after eating.
	if tarX == downX:
		escape = (upX, tarY)
	else:
		escape = (upX, tarY + 1)

	if escape in simSet:
		return None

	return path

def buildBottomDetourPlan(worldSize, moveTable, body, tailIdx, bodySet):
	global tarX
	global tarY

	headX, headY = body[len(body) - 1]

	if headY != 0 or tarY <= 0 or tarX <= headX:
		return None

	if tarX <= 0 or tarX >= worldSize - 1:
		return None

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
	appendRepeated(path, North, tarY)

	if tarX == downX:
		path.append(East)

	apple = (tarX, tarY)
	simBody, simSet, endPos, ateApple = simulatePath(path, body, tailIdx, bodySet, moveTable, apple)
	if not ateApple:
		return None

	# Make sure there is a plausible escape after eating.
	if tarX == upX:
		escape = (downX, tarY)
	else:
		escape = (downX, tarY - 1)

	if escape in simSet:
		return None

	return path

def buildCorridorDetourPlan(worldSize, moveTable, body, tailIdx, bodySet, totalTiles):
	freeTiles = totalTiles - liveLength(body, tailIdx)
	if freeTiles <= worldSize * 2:
		return None

	path = buildTopDetourPlan(worldSize, moveTable, body, tailIdx, bodySet)
	if path != None:
		return path

	return buildBottomDetourPlan(worldSize, moveTable, body, tailIdx, bodySet)

def buildStraightCyclePlan(direction, worldSize, cycleIndex, moveTable, totalTiles, body, tailIdx, bodySet):
	global tarX
	global tarY

	path = []
	simBody = copyBody(body, tailIdx)
	simSet = copySet(bodySet)
	headX, headY = simBody[len(simBody) - 1]
	apple = (tarX, tarY)

	for i in range(worldSize):
		currIndex = cycleIndex[(headX, headY)]
		targetIndex = cycleIndex[apple]
		tail = simBody[0]
		tailIndex = cycleIndex[tail]

		distance = getSafeCycleDistance(headX, headY, currIndex, direction, moveTable,
			targetIndex, tailIndex, totalTiles, simSet, tail, apple)

		if distance == None:
			break

		path.append(direction)
		moveInfo = moveTable[(headX, headY, direction)]
		nextX, nextY, nextIndex, forward = moveInfo
		nextPos = (nextX, nextY)

		if nextPos == apple:
			return path

		removed = simBody.pop(0)
		simSet.remove(removed)
		simBody.append(nextPos)
		simSet.add(nextPos)
		headX = nextX
		headY = nextY

	if len(path) > 0:
		return path

	return None

def buildCycleNextPlan(cyclePath, cycleIndex, moveTable, totalTiles, worldSize, body, tailIdx, bodySet):
	global tarX
	global tarY

	headX, headY = body[len(body) - 1]
	currIndex = cycleIndex[(headX, headY)]
	nextIndex = (currIndex + 1) % totalTiles
	nextX, nextY = cyclePath[nextIndex]
	direction = directionTo(headX, headY, nextX, nextY)

	return buildStraightCyclePlan(direction, worldSize, cycleIndex, moveTable,
		totalTiles, body, tailIdx, bodySet)

def buildShortcutPlan(cycleIndex, moveTable, totalTiles, worldSize, body, tailIdx, bodySet):
	headX, headY = body[len(body) - 1]
	direction = getBestCycleDirection(headX, headY, cycleIndex, moveTable,
		totalTiles, body, tailIdx, bodySet)

	if direction == None:
		return None

	return buildStraightCyclePlan(direction, worldSize, cycleIndex, moveTable,
		totalTiles, body, tailIdx, bodySet)

def buildPlan(cyclePath, cycleIndex, moveTable, totalTiles, worldSize, body, tailIdx, bodySet):
	if liveLength(body, tailIdx) < worldSize:
		path = buildDirectPlan(worldSize, moveTable, body, tailIdx, bodySet)
		if path != None:
			return path

	path = buildCorridorDetourPlan(worldSize, moveTable, body, tailIdx, bodySet, totalTiles)
	if path != None:
		return path

	# Late game: close holes by riding the Hamiltonian backbone more strictly.
	if totalTiles - liveLength(body, tailIdx) <= worldSize * 2:
		path = buildCycleNextPlan(cyclePath, cycleIndex, moveTable,
			totalTiles, worldSize, body, tailIdx, bodySet)
		if path != None:
			return path

	path = buildShortcutPlan(cycleIndex, moveTable, totalTiles, worldSize, body, tailIdx, bodySet)
	if path != None:
		return path

	return buildCycleNextPlan(cyclePath, cycleIndex, moveTable,
		totalTiles, worldSize, body, tailIdx, bodySet)

def moveAndCheck(direction, body, tailIdx, bodySet):
	global tarX
	global tarY

	oldTarget = (tarX, tarY)

	if not move(direction):
		return False, False, tailIdx

	newX = get_pos_x()
	newY = get_pos_y()
	newHead = (newX, newY)
	ateApple = newHead == oldTarget

	if ateApple:
		body.append(newHead)
		bodySet.add(newHead)

		nextTarget = measure()
		if nextTarget == None:
			return False, ateApple, tailIdx
		tarX, tarY = nextTarget
	else:
		removed = body[tailIdx]
		bodySet.remove(removed)
		tailIdx = tailIdx + 1
		body.append(newHead)
		bodySet.add(newHead)

	return True, ateApple, tailIdx

def produceBoneAsync():

	global tarX
	global tarY

	initBone()
	tarX, tarY = measure()
	worldSize = get_world_size()
	cyclePath, cycleIndex = buildHamiltonianCycle(worldSize)
	totalTiles = len(cyclePath)
	moveTable = buildMoveTable(worldSize, cycleIndex, totalTiles)

	startPos = (get_pos_x(), get_pos_y())
	body = [startPos]
	tailIdx = 0
	bodySet = set()
	bodySet.add(startPos)
	plannedPath = []
	plannedIndex = 0
	
	while True:

		if plannedIndex >= len(plannedPath):
			plannedPath = buildPlan(cyclePath, cycleIndex, moveTable,
				totalTiles, worldSize, body, tailIdx, bodySet)
			plannedIndex = 0

			if plannedPath == None or len(plannedPath) == 0:
				change_hat(Hats.Straw_Hat)
				break

		direction = plannedPath[plannedIndex]
		plannedIndex = plannedIndex + 1
			
		moved, ateApple, tailIdx = moveAndCheck(direction, body, tailIdx, bodySet)
		if not moved:
			change_hat(Hats.Wizard_Hat)
			break

		if ateApple:
			plannedPath = []
			plannedIndex = 0

		if liveLength(body, tailIdx) >= totalTiles:
			change_hat(Hats.Wizard_Hat)
			break
	
	#set_world_size(0)

produceBoneAsync()
