# OK what if we solve 16 mazes at once

from Movement import *

right_of = {North:East, East:South, South:West, West:North}
left_of = {North:West, West:South, South:East, East:North}
hugSide = {"Left":left_of,"Right":right_of}
altSide = {"Left":right_of,"Right":left_of}
delta = {North:(0,1), East:(1,0), South:(0,-1), West:(-1,0)}
dirs = [North, East, South, West]

iterationTarget = 300
startTime = get_time()

def manhattan(a, b):
	dx = a[0] - b[0]
	if dx < 0:
		dx = -dx
	dy = a[1] - b[1]
	if dy < 0:
		dy = -dy
	return dx + dy

def astar(walls, start, goal):
	if start == goal:
		return []

	# Dial's bucket queue: dict of f-score -> list of nodes,
	# heads[f] tracks next unread index in buckets[f].
	buckets = {}
	heads = {}
	came_from = {}
	g_score = {start: 0}
	closed = {}

	h0 = manhattan(start, goal)
	buckets[h0] = [start]
	heads[h0] = 0
	f = h0
	max_f = h0 + 256

	while f <= max_f:
		if f not in buckets or heads[f] >= len(buckets[f]):
			f += 1
			continue

		pos = buckets[f][heads[f]]
		heads[f] += 1

		if pos in closed:
			continue
		closed[pos] = True

		if pos == goal:
			reversed_path = []
			cur = goal
			while cur in came_from:
				prev, dir_taken = came_from[cur]
				reversed_path.append(dir_taken)
				cur = prev
			path = []
			i = len(reversed_path) - 1
			while i >= 0:
				path.append(reversed_path[i])
				i -= 1
			return path

		if pos not in walls:
			continue

		pos_walls = walls[pos]
		g_pos = g_score[pos]
		for d in dirs:
			if not pos_walls[d]:
				continue
			off = delta[d]
			neighbor = (pos[0] + off[0], pos[1] + off[1])
			if neighbor in closed:
				continue
			tentative_g = g_pos + 1
			if neighbor in g_score and g_score[neighbor] <= tentative_g:
				continue
			g_score[neighbor] = tentative_g
			came_from[neighbor] = (pos, d)
			nf = tentative_g + manhattan(neighbor, goal)
			if nf not in buckets:
				buckets[nf] = []
				heads[nf] = 0
			buckets[nf].append(neighbor)
	return []
	
def probe_and_record(walls):
	pos = (get_pos_x(), get_pos_y())
	walls[pos] = {
		North: can_move(North),
		East:  can_move(East),
		South: can_move(South),
		West:  can_move(West),
	}
	return walls

def worker(id):
	
	x = (id % 4) * 8 + 4
	y = (id // 4) * 8 + 4

	goto(x, y)
	
	if (num_drones() < 16):
		spawn_drone(worker, id+1)
		
	for _ in range(3):
		do_a_flip()

	plant(Entities.Bush)
	substance = 8 * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)
	
	solve(id)

def solve(id):
	wall = "Left"
	searching = True
	hug = hugSide[wall]
	alt = altSide[wall]
	currentDir = North
	startGold = num_items(Items.Gold)

	#walls[(x, y)] = {N, E, S, W}
	#walls[(x, y)] = {0, 1, 1, 0}
	walls = {}
	
	startingPos = get_pos_x(), get_pos_y()
	seen = {(startingPos, currentDir): True}

	while searching:
		walls = probe_and_record(walls)

		if can_move(hug[currentDir]):
			currentDir = hug[currentDir]
			move(currentDir)
		elif can_move(currentDir):
			move(currentDir)
		elif can_move(alt[currentDir]):
			currentDir = alt[currentDir]
			move(currentDir)
		else:
			currentDir = hug[currentDir]
			currentDir = hug[currentDir]
			move(currentDir)

		state = ((get_pos_x(), get_pos_y()), currentDir)
		if state in seen:
			searching = False
		else:
			seen[state] = True
	
	iterations = 0

	while iterations <= iterationTarget:
			
#		if (id == 0):
#			if (get_time() - startTime) % 60 < 3:
#				endGold = num_items(Items.Gold)
#				quick_print("Produced", endGold - startGold, "with", iterations, "iterations")
#				startGold = endGold
	
		target = measure()
		start = get_pos_x(), get_pos_y()

		path = astar(walls, start, target)

		for i in path:
			walls = probe_and_record(walls)
			move(i)

		if get_entity_type() == Entities.Treasure:
			substance = 8 * 2**(num_unlocked(Unlocks.Mazes) - 1)
			use_item(Items.Weird_Substance, substance)
			iterations += 1
	

def produceGoldAsync():

	global startTime

	starting = num_items(Items.Gold)
	startTime = get_time()

	clear()
	resetPosition()
	worker(0)

	ending = num_items(Items.Gold)
	runtime = get_time() - startTime	
	quick_print("Produced", ending - starting, "in", runtime, "with", iterationTarget, "iterations")
	
#produceGoldAsync()