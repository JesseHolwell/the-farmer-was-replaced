# OK what if we solve 16 mazes at once

from Movement import *

right_of = {North:East, East:South, South:West, West:North}
left_of = {North:West, West:South, South:East, East:North}
hugSide = {"Left":left_of,"Right":right_of}
altSide = {"Left":right_of,"Right":left_of}

runtime = 300

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
	
	while True:
		search("Left")

def search(wall):
	searching = True
	hug = hugSide[wall]
	alt = altSide[wall]
	currentDir = North
	
	walls = {}
	
	starting = get_pos_x(), get_pos_y()
	s
	
	#walls[(x, y)] = {N, E, S, W}
	#walls[(x, y)] = {0, 1, 1, 0}
	
	while searching:
		
		north = can_move(North)
		east = can_move(East)
		west = can_move(West)
		south = can_move(South)
		x = get_pos_x()
		y = get_pos_y()
		
		walls[(x, y)] = {north, east, south, west}
		
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
			
		# once entire maze has been mapped
		# searching = false
	
	iterations = 0
	
	while iterations <= 300:
		target = measure()
		# DFS to the treasure
		# checking wall positions along the way and updating the map
		
		if get_entity_type() == Entities.Treasure:
			substance = 8 * 2**(num_unlocked(Unlocks.Mazes) - 1)
			use_item(Items.Weird_Substance, substance)
			iterations += 1
	

def produceGoldAsync():
	
	starting = num_items(Items.Gold)
	
	clear()
	resetPosition()
	worker(0)

	ending = num_items(Items.Gold)	
	quick_print("Produced", ending - starting, "in", runtime, "seconds")
	
produceGoldAsync()