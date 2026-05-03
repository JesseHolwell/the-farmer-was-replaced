clear()

while True:
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			
			if (i == 0):
				
				if (j == 0):
					plant(Entities.Bush)
					use_item(Items.Weird_Substance)
				
				if (get_ground_type() != Grounds.Grassland):
					till()
					
				if (can_harvest()):
					harvest()
			elif (i == 1 or i == 2):
				if (get_ground_type() != Grounds.Grassland):
					till()
					
				if (can_harvest()):
					harvest()

				if ((j % 2 == 0) and (i == 1)) or ((j % 2 == 1) and (i == 2)):
					plant(Entities.Tree)
					use_item(Items.Fertilizer)
					
				else:
					plant(Entities.Bush)
					
				
			elif (i == 3 or i == 4 or i == 5 or i == 6):
				if (j < 3):
					if (get_ground_type() == Grounds.Grassland):
						till()
					
					if (can_harvest()):
						harvest()
						
					plant(Entities.Carrot)
				else:
					if (get_ground_type() == Grounds.Grassland):
						till()
				
					if (can_harvest()):
						harvest()
					
					plant(Entities.Pumpkin)
	

				
			elif (i == 7):
				if (get_ground_type() == Grounds.Grassland):
					till()
				
				if (can_harvest()):
					harvest()
					
				plant(Entities.Sunflower)
				
				if (get_water() < 0.5):
					use_item(Items.Water)
			
			move(North)
		move(East)			