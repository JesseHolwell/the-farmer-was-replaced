from Movement import *
from SmartPlanting import *
from Multithreading import *
	
def plantRecusively(point, item, isTreeFocus, harves):
	x, y = point

	goto(x, y)
	
	if get_entity_type() == None:
		if (item == Entities.Tree
			and isTreeFocus
			and (x + y) % 2 == 0):
			item = Entities.Bush
			
		plantItem(item)()
		harvestOrder.append((x, y))
		nextItem, (x2, y2) = get_companion()
		plantRecusively((x2, y2), nextItem, isTreeFocus)
		
	else:
		for i in harvestOrder:
			x, y = i
			goto(x, y)
			harvest()
		
def produceColumn(x, focusItem, isTreeFocus):
	harvestOrder = []
	for y in range(get_world_size()):
		plantRecusively((x, y), focusItem, isTreeFocus, harvestOrder)

def producePolyculture(focusItem):
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
		
	for drone in drones:
		wait_for(drone)
		
producePolyculture(Entities.Tree)	

	
	
	
		