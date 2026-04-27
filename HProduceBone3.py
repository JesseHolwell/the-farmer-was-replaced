from Movement import *
from MovementAsync import *

directions = [North, East, South, West]

def initBone():
	change_hat(Hats.Wizard_Hat)
	
	set_world_size(6)
	
	if can_harvest():
		harvest()
	
	tillFieldAsync()
	resetPosition()
	change_hat(Hats.Dinosaur_Hat)


def exitBone():
	change_hat(Hats.Wizard_Hat)


def make2d(size, value):
	grid = []
	for x in range(size):
		column = []
		for y in range(size):
			column.append(value)
		grid.append(column)
	return grid


def buildHamiltonianCycle():
	n = get_world_size()
	path = []

	for x in range(n):
		path.append([x, 0])

	for y in range(1, n):
		path.append([n - 1, y])

	goingUp = True
	
	for x in range(n - 2, 0, -1):
		if goingUp:
			for y in range(n - 1, 0, -1):
				path.append([x, y])
		else:
			for y in range(1, n):
				path.append([x, y])
		
		goingUp = not goingUp

	for y in range(n - 1, 0, -1):
		path.append([0, y])

	indexGrid = make2d(n, 0)

	for i in range(len(path)):
		x = path[i][0]
		y = path[i][1]
		indexGrid[x][y] = i

	return path, indexGrid


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


def nextPosition(x, y, direction):
	if direction == North:
		return x, y + 1
	if direction == South:
		return x, y - 1
	if direction == East:
		return x + 1, y
	if direction == West:
		return x - 1, y
	
	return x, y


def inBounds(x, y):
	n = get_world_size()
	return x >= 0 and x < n and y >= 0 and y < n


def containsPosition(body, x, y):
	for pos in body:
		if pos[0] == x and pos[1] == y:
			return True
	
	return False


def isTail(body, x, y):
	return body[0][0] == x and body[0][1] == y


def getHamiltonianMove(path, indexGrid):
	n = get_world_size()
	totalTiles = n * n
	
	currX = get_pos_x()
	currY = get_pos_y()
	currIndex = indexGrid[currX][currY]

	nextIndex = (currIndex + 1) % totalTiles
	nextX = path[nextIndex][0]
	nextY = path[nextIndex][1]

	return directionTo(currX, currY, nextX, nextY)


def isSafeMove(direction, body, tarX, tarY):
	currX = get_pos_x()
	currY = get_pos_y()

	nextX, nextY = nextPosition(currX, currY, direction)

	if not inBounds(nextX, nextY):
		return False

	if not can_move(direction):
		return False

	willEat = nextX == tarX and nextY == tarY

	if containsPosition(body, nextX, nextY):
		# Moving into the tail is only safe if the tail will move away.
		if isTail(body, nextX, nextY) and not willEat:
			return True
		
		return False

	return True


def getBestSafeMove(path, indexGrid, body, tarX, tarY):
	n = get_world_size()
	totalTiles = n * n
	
	currX = get_pos_x()
	currY = get_pos_y()
	currIndex = indexGrid[currX][currY]
	targetIndex = indexGrid[tarX][tarY]

	freeTiles = totalTiles - len(body)

	bestDirection = None
	bestTargetDistance = None

	for direction in directions:
		if not isSafeMove(direction, body, tarX, tarY):
			continue

		nextX, nextY = nextPosition(currX, currY, direction)
		nextIndex = indexGrid[nextX][nextY]

		skipDistance = pathDistance(currIndex, nextIndex, totalTiles)

		# Only move forward along the Hamiltonian cycle.
		if skipDistance <= 0:
			continue

		# Shortcut only when enough free space exists.
		# The +1 makes this more conservative near endgame.
		if skipDistance > freeTiles + 1:
			continue

		targetDistance = pathDistance(nextIndex, targetIndex, totalTiles)

		if bestDirection == None or targetDistance < bestTargetDistance:
			bestDirection = direction
			bestTargetDistance = targetDistance

	if bestDirection != None:
		return bestDirection

	hamMove = getHamiltonianMove(path, indexGrid)

	if isSafeMove(hamMove, body, tarX, tarY):
		return hamMove

	return None


def updateBody(body, direction, tarX, tarY):
	currX = get_pos_x()
	currY = get_pos_y()

	nextX, nextY = nextPosition(currX, currY, direction)

	willEat = nextX == tarX and nextY == tarY

	body.append([nextX, nextY])

	if not willEat:
		body.pop(0)

	return willEat


def produceBoneAsync():
	initBone()

	path, indexGrid = buildHamiltonianCycle()

	tarX, tarY = measure()

	body = []
	body.append([get_pos_x(), get_pos_y()])

	while True:
		direction = getBestSafeMove(path, indexGrid, body, tarX, tarY)

		if direction == None:
			exitBone()
			break

		ateApple = updateBody(body, direction, tarX, tarY)

		move(direction)

		if ateApple:
			tarX, tarY = measure()

		if len(body) >= get_world_size() * get_world_size():
			exitBone()
			break

		if (not can_move(North) and
			not can_move(East) and
			not can_move(South) and
			not can_move(West)):
			exitBone()
			break


produceBoneAsync()