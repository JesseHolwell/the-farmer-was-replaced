# Hamiltonian corridor path with guarded apple shortcuts.

from Movement import *
from MovementAsync import *

worldsize = 6

tarX = 0
tarY = 0

def initBone():
	set_world_size(worldsize)

	change_hat(Hats.Straw_Hat)
	if can_harvest():
		harvest()
	tillFieldAsync()
	resetPosition()

	change_hat(Hats.Dinosaur_Hat)

def exit():
	change_hat(Hats.Wizard_Hat)
	#set_world_size(0)

def liveLength(body, tailIdx):
	return len(body) - tailIdx

def inBounds(x, y, worldSize):
	return x >= 0 and x < worldSize and y >= 0 and y < worldSize

def nextPosition(x, y, direction):
	return x + deltaX[direction], y + deltaY[direction]

def appendRepeated(path, direction, steps):
	for i in range(steps):
		path.append(direction)

def copyLiveBody(body, tailIdx):
	out = []
	for i in range(tailIdx, len(body)):
		out.append(body[i])
	return out

def copySet(values):
	out = set()
	for value in values:
		out.add(value)
	return out

def getCycleDirectionAt(x, y, worldSize):
	topY = worldSize - 1
	innerTopY = worldSize - 2
	rightX = worldSize - 1

	if x == rightX and y < topY:
		return North

	if y == topY and x > 0:
		return West

	if x == 0 and y > 0:
		return South

	if x % 2 == 1:
		if y < innerTopY:
			return North
		return East

	if y == 0 and x < rightX:
		return East

	return South

def getCycleDirection(worldSize):
	return getCycleDirectionAt(get_pos_x(), get_pos_y(), worldSize)

def isCorridorRow(y, worldSize):
	return y == 0 or y == worldSize - 1

def buildShortcutPath(worldSize):
	global tarX
	global tarY

	currX = get_pos_x()
	currY = get_pos_y()
	topY = worldSize - 1
	innerTopY = worldSize - 2
	rightX = worldSize - 1

	if tarX <= 0 or tarX >= rightX:
		return None

	if tarY <= 0 or tarY >= topY:
		return None

	path = []

	if currY == 0:
		if tarX % 2 == 1:
			entryX = tarX
		else:
			entryX = tarX - 1

		if entryX <= currX:
			return None

		appendRepeated(path, East, entryX - currX)

		if tarX % 2 == 1:
			appendRepeated(path, North, tarY)
		else:
			appendRepeated(path, North, innerTopY)
			path.append(East)
			appendRepeated(path, South, innerTopY - tarY)

		return path

	if currY == topY:
		if tarX % 2 == 0:
			entryX = tarX
		else:
			entryX = tarX + 1

		if entryX >= currX:
			return None

		appendRepeated(path, West, currX - entryX)

		if tarX % 2 == 0:
			appendRepeated(path, South, topY - tarY)
		else:
			appendRepeated(path, South, topY)
			path.append(West)
			appendRepeated(path, North, tarY)

		return path

	return None

def simulateStep(direction, worldSize, totalTiles, simBody, simSet, grows):
	headX, headY = simBody[len(simBody) - 1]
	nextX, nextY = nextPosition(headX, headY, direction)

	if not inBounds(nextX, nextY, worldSize):
		return False

	nextPos = (nextX, nextY)
	if nextPos in simSet:
		return False

	simBody.append(nextPos)
	simSet.add(nextPos)

	if not grows:
		removed = simBody.pop(0)
		simSet.remove(removed)

	return len(simBody) <= totalTiles

def shortcutIsSafe(path, worldSize, totalTiles, body, tailIdx, bodySet):
	global tarX
	global tarY

	if path == None or len(path) == 0:
		return False

	simBody = copyLiveBody(body, tailIdx)
	simSet = copySet(bodySet)
	apple = (tarX, tarY)
	ateApple = False

	for direction in path:
		headX, headY = simBody[len(simBody) - 1]
		nextX, nextY = nextPosition(headX, headY, direction)
		grows = not ateApple and (nextX, nextY) == apple

		if not simulateStep(direction, worldSize, totalTiles, simBody, simSet, grows):
			return False

		if grows:
			ateApple = True

	if not ateApple:
		return False

	if len(simBody) >= totalTiles:
		return True

	# After the shortcut, the only safe assumption is that every future
	# Hamiltonian step might also grow the snake. Accept only if that could
	# fill the remaining board before hitting the body.
	for i in range(totalTiles):
		headX, headY = simBody[len(simBody) - 1]
		direction = getCycleDirectionAt(headX, headY, worldSize)
		if not simulateStep(direction, worldSize, totalTiles, simBody, simSet, True):
			return False

		if len(simBody) >= totalTiles:
			return True

	return False

def getNextDirection(worldSize, totalTiles, body, tailIdx, bodySet, plannedPath, plannedIndex):
	if plannedIndex < len(plannedPath):
		return plannedPath[plannedIndex], plannedPath, plannedIndex + 1

	plannedPath = []
	plannedIndex = 0
	path = buildShortcutPath(worldSize)

	if shortcutIsSafe(path, worldSize, totalTiles, body, tailIdx, bodySet):
		plannedPath = path
		return plannedPath[0], plannedPath, 1

	return getCycleDirection(worldSize), plannedPath, plannedIndex

def moveAndCheck(direction, body, tailIdx, bodySet, totalTiles):
	global tarX
	global tarY

	oldTarget = (tarX, tarY)

	if not move(direction):
		return False, False, tailIdx

	newHead = (get_pos_x(), get_pos_y())
	ateApple = newHead == oldTarget

	if ateApple:
		body.append(newHead)
		bodySet.add(newHead)

		if liveLength(body, tailIdx) >= totalTiles:
			return True, True, tailIdx

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
	nextTarget = measure()
	if nextTarget == None:
		exit()
		return

	tarX, tarY = nextTarget

	worldSize = get_world_size()
	totalTiles = worldSize * worldSize

	startPos = (get_pos_x(), get_pos_y())
	body = [startPos]
	tailIdx = 0
	bodySet = set()
	bodySet.add(startPos)
	plannedPath = []
	plannedIndex = 0

	while liveLength(body, tailIdx) < totalTiles:
		direction, plannedPath, plannedIndex = getNextDirection(
			worldSize, totalTiles, body, tailIdx, bodySet,
			plannedPath, plannedIndex)

		moved, ateApple, tailIdx = moveAndCheck(direction, body, tailIdx, bodySet, totalTiles)
		if not moved:
			break

		if ateApple:
			plannedPath = []
			plannedIndex = 0

	exit()

produceBoneAsync()
