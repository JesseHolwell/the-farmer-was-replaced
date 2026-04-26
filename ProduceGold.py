from Movement import *

def produceGold():
	resetPosition()
	if can_harvest() and get_entity_type() != Entities.Grass:
		harvest()
		
	plant(Entities.Bush)
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)
	
	searching = True
	right_of = {North:East, East:South, South:West, West:North}
	left_of = {North:West, West:South, South:East, East:North}
	currentDir = North
	
	while searching:
		
		if can_move(right_of[currentDir]):
			currentDir = right_of[currentDir]
			move(currentDir)
		elif can_move(currentDir):
			move(currentDir)
		elif can_move(left_of[currentDir]):
			currentDir = left_of[currentDir]
			move(currentDir)
		else:
			currentDir = left_of[currentDir]
			currentDir = left_of[currentDir]
			move(currentDir)
		
		if get_entity_type() == Entities.Treasure:
			harvest()
			searching = False
			break
			
#produceGold()