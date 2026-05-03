from H_Movement import *
from H_MovementAsync import *
from H_SmartPlanting import *
from H_Multithreading import *
from H_Statistics import *
	
def plantRecusively(point, item, isTreeFocus, harvestOrder):
	x, y = point

	goto(x, y)
	
	if get_entity_type() == None:
		if (item == Entities.Tree
			and isTreeFocus
			and (x + y) % 2 == 0):
			item = Entities.Bush
			
		plantItem(item)()
		harvestOrder.append((x, y))
		companion = get_companion()
		if companion != None:
			nextItem, (x2, y2) = companion
			plantRecusively((x2, y2), nextItem, isTreeFocus, harvestOrder)
		
def produceColumn(x, focusItem, isTreeFocus):
	harvestOrder = []
	for y in range(get_world_size()):
		plantRecusively((x, y), focusItem, isTreeFocus, harvestOrder)
		
	for i in harvestOrder:
		x, y = i
		goto(x, y)
		if get_entity_type() != None:
			while get_entity_type() != None and not can_harvest():
				if (get_water() < 0.75):
					use_item(Items.Water)
				do_a_flip()
		harvest()

def producePolycultureAsync(focusItem):
	clear()
	resetPosition()
	tillFieldAsync()
	drones = []		
	isTreeFocus = focusItem == Entities.Tree

	for x in range(get_world_size()):
		spawned = False
		while not spawned:
			spawned = spawn_drone(produceColumn, x, focusItem, isTreeFocus)	
			if spawned:
				drones.append(spawned)
			else:
				produceColumn(x, focusItem, isTreeFocus)
				spawned = True
		
	for drone in drones:
		wait_for(drone)
		
def producePolyTrees():
	producePolycultureAsync(Entities.Tree)	

#runWithStats(producePolyTrees, Items.Wood)

	
	
	
		