def plantHay():
	if (get_ground_type() != Grounds.Grassland):
		till()
		
def plantBush():
	plant(Entities.Bush)
	
def plantTree():
	plant(Entities.Tree)
	
def plantCarrot():
	if (get_ground_type() == Grounds.Grassland):
		till()
	
	plant(Entities.Carrot)
	
itemMap = {
	Entities.Grass:plantHay,
	Entities.Tree:plantTree,
	Entities.Bush:plantBush,
	Entities.Carrot:plantCarrot
	}	
	
def plantItem(item):
	return itemMap[item]