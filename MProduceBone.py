from Movement import *
from MovementAsync import *
#from SnakeComplexity import *

def initBone():
	set_world_size(16)

	change_hat(Hats.Wizard_Hat)

	tillFieldAsync()
	resetPosition()

	change_hat(Hats.Dinosaur_Hat)

def exit():
	change_hat(Hats.Wizard_Hat)
	#set_world_size(0)


def reverseList(lst):
	out = []
	n = len(lst)
	for i in range(n):
		out.append(lst[n - 1 - i])
	return out


# Try a straight L-shape path (X-first, then Y-first).
# Body cells block; the target is allowed through so callers don't have to
# clone the blocked set when tail-following targets the tail.
# Fast path for open boards — avoids any graph search when the route is direct.
def tryStraightPath(start, target, blocked, worldSize):
	sx, sy = start
	tx, ty = target

	if sx == tx and sy == ty:
		return []

	stepX = 0
	if tx > sx:
		stepX = 1
	elif tx < sx:
		stepX = -1

	stepY = 0
	if ty > sy:
		stepY = 1
	elif ty < sy:
		stepY = -1

	dx = abs(tx - sx)
	dy = abs(ty - sy)

	# X-first variant.
	path = []
	cx = sx
	cy = sy
	ok = True
	for i in range(dx):
		cx = cx + stepX
		cell = (cx, cy)
		if cell != target and cell in blocked:
			ok = False
			break
		path.append((stepX, 0))
	if ok:
		for i in range(dy):
			cy = cy + stepY
			cell = (cx, cy)
			if cell != target and cell in blocked:
				ok = False
				break
			path.append((0, stepY))
		if ok:
			return path

	# Y-first variant.
	path = []
	cx = sx
	cy = sy
	ok = True
	for i in range(dy):
		cy = cy + stepY
		cell = (cx, cy)
		if cell != target and cell in blocked:
			ok = False
			break
		path.append((0, stepY))
	if ok:
		for i in range(dx):
			cx = cx + stepX
			cell = (cx, cy)
			if cell != target and cell in blocked:
				ok = False
				break
			path.append((stepX, 0))
		if ok:
			return path

	return None


# A* with Manhattan heuristic. Body cells block; target is allowed through.
# Manhattan is consistent on a unit-cost grid, so each cell only needs to be
# discovered once. Linear-scan priority queue (no heap available).
def astar(start, target, blocked, worldSize):
	if start == target:
		return []

	openList = [start]
	seen = set()
	seen.add(start)
	gScore = {}
	gScore[start] = 0
	fScore = {}
	fScore[start] = abs(start[0] - target[0]) + abs(start[1] - target[1])
	parent = {}

	while len(openList) > 0:
		# Linear scan for the min-f cell in the open list.
		minIdx = 0
		minF = fScore[openList[0]]
		n = len(openList)
		for i in range(1, n):
			f = fScore[openList[i]]
			if f < minF:
				minF = f
				minIdx = i

		cur = openList[minIdx]

		if cur == target:
			path = []
			node = cur
			while node != start:
				p = parent[node]
				path.append((node[0] - p[0], node[1] - p[1]))
				node = p
			return reverseList(path)

		# Swap-and-pop to remove the min-f cell in O(1).
		last = len(openList) - 1
		openList[minIdx] = openList[last]
		openList.pop()

		gCur = gScore[cur]
		x, y = cur

		for dir in directions:
			nx = x + deltaX[dir]
			ny = y + deltaY[dir]

			if nx < 0 or nx >= worldSize or ny < 0 or ny >= worldSize:
				continue

			nextPos = (nx, ny)

			if nextPos in seen:
				continue

			# Body cells block, except the target (so tail-follow can terminate
			# and the safety check can verify head -> tail reachability).
			if nextPos != target and nextPos in blocked:
				continue

			seen.add(nextPos)
			parent[nextPos] = cur
			gNext = gCur + 1
			gScore[nextPos] = gNext
			fScore[nextPos] = gNext + abs(nx - target[0]) + abs(ny - target[1])
			openList.append(nextPos)

	return None


# Manhattan-first, A* fallback.
def findPath(start, target, blocked, worldSize):
	path = tryStraightPath(start, target, blocked, worldSize)
	if path != None:
		return path
	return astar(start, target, blocked, worldSize)


def stepToDir(step):
	dx, dy = step

	if dx == 1:
		return East
	if dx == -1:
		return West
	if dy == 1:
		return North
	return South


# Returns a path from head to apple that's safe to commit to, or None.
# `body` is append-only (oldest first). `tailIdx` indexes the live tail; the
# live snake is `body[tailIdx : ]` with head at `body[-1]`.
def getSafeApplePath(head, apple, body, tailIdx, bodySet, worldSize):
	path = findPath(head, apple, bodySet, worldSize)

	if path == None or len(path) == 0:
		return None

	snakeLen = len(body) - tailIdx

	# Snake too short to trap itself — skip the simulation + second pathfind.
	if snakeLen < worldSize:
		return path

	pathLen = len(path)

	# Short hops barely shift the snake — if we were safe before, we still are.
	if pathLen * 2 < snakeLen:
		return path

	# Simulate body state after following the path and eating the apple.
	# Last step grows; earlier steps pop the tail.

	# Walk the path forward to get every cell the head occupies.
	pathCells = []
	hx = head[0]
	hy = head[1]
	for i in range(pathLen):
		step = path[i]
		hx = hx + step[0]
		hy = hy + step[1]
		pathCells.append((hx, hy))

	newHead = (hx, hy)

	# Build a fresh blocked set for the simulated post-eat snake.
	#   if P <= snakeLen, some original body remains; new tail is inside it.
	#   if P >  snakeLen, every original body cell has been popped and the
	#                     new tail lives inside the path itself.
	newBlocked = set()
	if pathLen <= snakeLen:
		newTailBodyIdx = tailIdx + pathLen - 1
		bodyEnd = len(body)
		for i in range(newTailBodyIdx, bodyEnd):
			newBlocked.add(body[i])
		for i in range(pathLen):
			newBlocked.add(pathCells[i])
		newTail = body[newTailBodyIdx]
	else:
		pathTailIdx = pathLen - snakeLen - 1
		for i in range(pathTailIdx, pathLen):
			newBlocked.add(pathCells[i])
		newTail = pathCells[pathTailIdx]

	if findPath(newHead, newTail, newBlocked, worldSize) != None:
		return path

	return None


def produceBone():
	initBone()

	worldSize = get_world_size()
	# Append-only body: head is body[-1], tail is body[tailIdx].
	# `bodySet` is the set of live body positions, kept in sync for O(1) lookup.
	startPos = (get_pos_x(), get_pos_y())
	body = [startPos]
	tailIdx = 0
	bodySet = set()
	bodySet.add(startPos)
	apple = measure()
	# Single path cache for both apple-chase and tail-chase phases.
	# Snake evolution is deterministic, so a path computed once stays collision-
	# free for its full length — we only re-plan when the path is exhausted.
	plannedPath = []
	plannedPathIdx = 0

	while True:
		# Re-plan only when the cached path is exhausted.
		if plannedPathIdx >= len(plannedPath):
			head = body[len(body) - 1]
			path = getSafeApplePath(head, apple, body, tailIdx, bodySet, worldSize)
			if path == None:
				# No safe apple route — chase the tail until something opens up.
				tail = body[tailIdx]
				path = findPath(head, tail, bodySet, worldSize)
				if path == None or len(path) == 0:
					exit()
					break
			plannedPath = path
			plannedPathIdx = 0

		step = plannedPath[plannedPathIdx]
		plannedPathIdx = plannedPathIdx + 1
		dir = stepToDir(step)

		# Move.
		if not move(dir):
			exit()
			break

		newX = get_pos_x()
		newY = get_pos_y()
		newHead = (newX, newY)

		# Pop tail BEFORE appending new head. When the tail is the target of a
		# tail-follow path of length 1, newHead == removed; appending first
		# would set bodySet membership and the subsequent .remove(removed)
		# would delete it again, leaving the live cell untracked. Pop-first
		# avoids the double-write race entirely.
		if newHead == apple:
			body.append(newHead)
			bodySet.add(newHead)
			apple = measure()
			plannedPath = []
			plannedPathIdx = 0
		else:
			removed = body[tailIdx]
			bodySet.remove(removed)
			tailIdx = tailIdx + 1
			body.append(newHead)
			bodySet.add(newHead)


produceBone()
