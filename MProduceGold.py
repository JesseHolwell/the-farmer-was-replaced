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
	move(dir)
	search(dir)

def search(currentDir):
	searching = True
	while searching:
		
		if get_entity_type() == Entities.Treasure:
			harvest()
			searching = False
			return
		elif get_entity_type() != Entities.Hedge:
			searching = False
			return
			
		validDirs = []
		
		for dir in directions:
			if currentDir != None and dir == opposite[currentDir]:
				continue
				
			if can_move(dir):
				validDirs.append(dir)
				
		if len(validDirs) == 0:
			return
				
		chosenDir = validDirs[0]
		
		if currentDir != None:
			for dir in validDirs:
				if dir == currentDir:
					chosenDir = dir
			
		for dir in validDirs:
			if dir != chosenDir:
				spawn_drone(searchBranch, dir)
	
		move(chosenDir)
		currentDir = chosenDir
			
def produceGoldAsync():
	initMaze()
	search(None)
	
#produceGoldAsync()