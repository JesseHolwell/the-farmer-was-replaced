from Movement import *

right_of = {North:East, East:South, South:West, West:North}
left_of = {North:West, West:South, South:East, East:North}
hugSide = {"Left":left_of,"Right":right_of}
altSide = {"Left":right_of,"Right":left_of}

def search(wall):
	searching = True
	hug = hugSide[wall]
	alt = altSide[wall]
	currentDir = North
	
	while searching:
		
		if get_entity_type() == Entities.Treasure:
			harvest()
			searching = False
			break
		elif get_entity_type() != Entities.Hedge:
			searching = False
			break
		
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

def produceGoldAsync():
	resetPosition()
	if can_harvest() and get_entity_type() != Entities.Grass:
		harvest()
		
	plant(Entities.Bush)
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)
	
	spawn_drone(search, "Right")
	search("Left")
	
produceGoldAsync()