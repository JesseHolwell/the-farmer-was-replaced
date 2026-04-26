from Movement import *

directions = [North, East, South, West]
opposite = {North:South, East:West, South:North, West:East}

def initMaze():
	#resetPosition()
	goto(get_world_size() / 2, get_world_size() / 2)
	
	if can_harvest() and get_entity_type() != Entities.Grass:
		harvest()
		
	plant(Entities.Bush)
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)
	
def searchBranch(dir):
	if move(dir):
		search(dir)

def search(currentDir):
	# Collect spawned drones so we can wait for them before returning.
	# Without this, the function returns the moment the main thread hits a
	# dead-end — drones keep exploring async, and focusItem.py / runWithStats
	# fires the next iteration before treasure is harvested.
	drones = []
	while True:

		if get_entity_type() == Entities.Treasure:
			harvest()
			break

		if get_entity_type() != Entities.Hedge:
			break

		validDirs = []

		for dir in directions:
			if currentDir != None and dir == opposite[currentDir]:
				continue

			if can_move(dir):
				validDirs.append(dir)

		if len(validDirs) == 0:
			break

		chosenDir = validDirs[0]

		if currentDir != None:
			for dir in validDirs:
				if dir == currentDir:
					chosenDir = dir

		for dir in validDirs:
			if dir != chosenDir:
				d = spawn_drone(searchBranch, dir)
				if d:
					drones.append(d)

		if move(chosenDir):
			currentDir = chosenDir
		else:
			break

	for d in drones:
		wait_for(d)
			
def produceGoldAsync():
	initMaze()
	search(None)
	
produceGoldAsync()