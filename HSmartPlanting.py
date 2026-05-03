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

def plantCactus():
	if (can_harvest()
		and get_entity_type() != Entities.Cactus
		and get_entity_type() != Entities.Grass):
		harvest()
					
	if (get_ground_type() == Grounds.Grassland):
		till()
	
	plant(Entities.Cactus)

def plantSunflower():
	if (can_harvest()
		and get_entity_type() != Entities.Sunflower
		and get_entity_type() != Entities.Grass):
		harvest()
					
	if (get_ground_type() == Grounds.Grassland):
		till()
	
	plant(Entities.Sunflower)
	
itemMap = {
	Entities.Grass:plantHay,
	Entities.Tree:plantTree,
	Entities.Bush:plantBush,
	Entities.Carrot:plantCarrot
	}	
	
def plantItem(item):
	return itemMap[item]