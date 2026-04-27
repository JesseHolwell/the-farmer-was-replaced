# Claudes optimised Hamiltonian Cycle

from Movement import *
from MovementAsync import *


# Build a Hamiltonian cycle on an N×N grid (N must be even).
# Pattern: column 0 going up, then zigzag through inner columns 1..N-2 (each
# only touching rows 1..N-1, never row 0), then last column going down (full
# height including row 0), then row 0 leftward back to (0, 0).
# The reserved row-0 corridor on inner columns is what closes the cycle.
# Returns a dict mapping cell -> cycle-index. The cycle order itself is
# implicit (each cell's neighbour with forward distance 1 is the next one).
def buildHamiltonCycle(worldSize):
	cycleIdx = {}
	i = 0

	# Column 0 going up.
	for y in range(worldSize):
		cycleIdx[(0, y)] = i
		i = i + 1

	# Inner columns: alternate down/up. Never visit row 0.
	for col in range(1, worldSize - 1):
		if col % 2 == 1:
			for y in range(worldSize - 1, 0, -1):
				cycleIdx[(col, y)] = i
				i = i + 1
		else:
			for y in range(1, worldSize):
				cycleIdx[(col, y)] = i
				i = i + 1

	# Last column: full height, going down.
	for y in range(worldSize - 1, -1, -1):
		cycleIdx[(worldSize - 1, y)] = i
		i = i + 1

	# Row 0 going left back to (0, 0).
	for x in range(worldSize - 2, 0, -1):
		cycleIdx[(x, 0)] = i
		i = i + 1

	return cycleIdx


def produceBone():
	set_world_size(8)

	# Hamilton cycles only exist on even-sided grids; round odd N down by one.
	worldSize = get_world_size()
	if worldSize % 2 == 1:
		set_world_size(worldSize - 1)
		worldSize = worldSize - 1

	change_hat(Hats.Wizard_Hat)
	tillFieldAsync()
	resetPosition()
	change_hat(Hats.Dinosaur_Hat)

	cycleIdx = buildHamiltonCycle(worldSize)
	cycleLen = worldSize * worldSize

	# Track snake body so we can compute shortcut safety.
	# `body` is append-only; `tailIdx` is the live tail's index in body; the
	# live snake is body[tailIdx : ]. `bodySet` is the same cells in a set
	# for O(1) collision lookup.
	startPos = (get_pos_x(), get_pos_y())
	body = [startPos]
	tailIdx = 0
	bodySet = set()
	bodySet.add(startPos)
	apple = measure()

	while True:
		# No apple to chase (board is full or measure returned nothing).
		if apple == None:
			change_hat(Hats.Wizard_Hat)
			break

		head = body[len(body) - 1]
		tail = body[tailIdx]
		snakeLen = len(body) - tailIdx

		headCycleIdx = cycleIdx[head]
		appleCycleIdx = cycleIdx[apple]

		# Forward cycle distance from head to apple. The apple always lies in
		# the free arc (cells not occupied by the body), so this is well-defined.
		distToApple = (appleCycleIdx - headCycleIdx) % cycleLen
		if distToApple == 0:
			distToApple = 1

		# Forward cycle distance from head to tail = number of cells we can
		# safely advance the head before overtaking the tail. The tail itself
		# moves out of the way during the move, which is the +1 below.
		# Equivalently: cycleLen - snakeLen + 1.
		distToTail = cycleLen - snakeLen + 1

		# Pick the neighbor that advances the cycle index furthest, capped by
		# both distToApple (don't overshoot) and distToTail (don't overtake).
		# Default fallback is the cycle-next cell (forward = 1), always safe.
		bestForward = 0
		bestDir = None

		for dir in directions:
			nx = head[0] + deltaX[dir]
			ny = head[1] + deltaY[dir]
			if nx < 0 or nx >= worldSize or ny < 0 or ny >= worldSize:
				continue
			neighbor = (nx, ny)
			# Body collision: blocked unless it's the current tail (which is
			# moving away on this same tick).
			if neighbor in bodySet and neighbor != tail:
				continue
			nIdx = cycleIdx[neighbor]
			forward = (nIdx - headCycleIdx) % cycleLen
			if forward == 0:
				continue
			if forward > distToApple:
				continue
			if forward > distToTail:
				continue
			if forward > bestForward:
				bestForward = forward
				bestDir = dir

		if bestDir == None:
			# Hamilton backbone always provides forward=1, so this should be
			# unreachable in practice. Bail out defensively.
			change_hat(Hats.Wizard_Hat)
			break

		if not move(bestDir):
			change_hat(Hats.Wizard_Hat)
			break

		newX = get_pos_x()
		newY = get_pos_y()
		newHead = (newX, newY)

		# Pop tail BEFORE appending the new head: when the head steps into the
		# popping tail's cell (legal under simultaneous tail-pop), append-first
		# would overwrite-then-delete and leave the cell missing from bodySet.
		if newHead == apple:
			body.append(newHead)
			bodySet.add(newHead)
			apple = measure()
		else:
			removed = body[tailIdx]
			bodySet.remove(removed)
			tailIdx = tailIdx + 1
			body.append(newHead)
			bodySet.add(newHead)


produceBone()
	