from Movement import *
from SmartPlanting import *
	
harvestOrder = []
occupied = []
treeMap = []
	
def plantRecusively(point, item):
	x, y = point
	if occupied[x][y] == 1:
		return
		
	goto(x, y)
	
	if (can_harvest() and get_entity_type() != Entities.Grass):
		harvest()

	plantItem(item)()
	
	harvestOrder.append((x, y))
	occupied[x][y] = 1
	
	if (item == Entities.Tree):
		treeMap[x][y] = 1
	
	nextItem, (x2, y2) = get_companion()
	
	plantRecusively((x2, y2), nextItem)
	

def producePolyculture(focusItem):
	global harvestOrder
	global occupied
	global treeMap
	
	resetPosition()
	harvestOrder = []
	occupied = []
	treeMap = []

	for x in range(get_world_size()):
		occupied.insert(x, [])
		treeMap.insert(x, [])
		for y in range(get_world_size()):
			occupied[x].insert(y, 0)
			treeMap[x].insert(y, 0)

	for x in range(get_world_size()):
		for y in range(get_world_size()):
			
			nextItem = focusItem
			
			if (nextItem == Entities.Tree
				and ((x > 0 and treeMap[x-1][y] == 1)
				or (y > 0 and treeMap[x][y-1] == 1)
				or (x < get_world_size() - 1 and treeMap[x+1][y] == 1)
				or (y < get_world_size() - 1 and treeMap[x][y+1] == 1))):
					nextItem = Entities.Bush
			
			plantRecusively((x, y), nextItem)
				
	for i in harvestOrder:
		x, y = i
		goto(x, y)
		harvest()

		
#producePolyculture(Entities.Grass)	

	
	
	
