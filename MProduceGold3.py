from Movement import *

directions = [North, East, South, West]
opposite = {North:South, East:West, South:North, West:East}
run = 300

# TODO: we need to define how to know once 300 iterations of a maze have been completed
# is this just num_items(Items.Gold) incremented by 9863168

# TODO: it would be great to remember the state of the walls
# each drone has its own memory? how do we stop drones colliding

# TODO: we need to continuously run this as long as possible

def mazeWorker(id, target):
	
	# form a grid pattern
	goto((id % 6) * 5 + 3, (id // 5) * 6 + 3)
		
	while (get_entity_type() != Entities.Bush):
		do_a_flip()
		
	# maze is ready
	gold = measure()
	
	while (num_items < target):
		#if gold is within our grid pattern (30 divided into 30 equal squares)
		# go and find it
		# otherwise, just keep running measure until we have a new gold
		do_a_flip()
	
def initMaze():
	if can_harvest() and get_entity_type() != Entities.Grass:
		harvest()
		
	plant(Entities.Bush)
	substance = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
	use_item(Items.Weird_Substance, substance)

def init():
	
	startingGold = num_items(Items.Gold)
	target = startingGold + 9863168
	
	if can_harvest() and get_entity_type() != Entities.Grass:
		harvest()
	
	while (num_drones() < 30):
		spawn_drone(mazeWorker, num_drones(), target)
		
	goto(32,32)
	
	for i in range(5):
		do_a_flip()
	
	# TODO: wait for all drones to be in position
	
	initMaze()

def produceGoldAsync():
	init()
	
produceGoldAsync()