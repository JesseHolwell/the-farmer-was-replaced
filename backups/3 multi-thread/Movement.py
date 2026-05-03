directions = [North, East, South, West]

deltaX = {East:1, West:-1, North:0, South:0}
deltaY = {North:1, South:-1, East:0, West:0}
ws = get_world_size()

def goto(x2, y2):
	world_size = get_world_size()
	world_half = world_size / 2

	dx = (x2 - get_pos_x() + world_half) % world_size - world_half
	dy = (y2 - get_pos_y() + world_half) % world_size - world_half

	for _ in range(dx):
		move(East)
	for _ in range(-dx):
		move(West)
	for _ in range(dy):
		move(North)
	for _ in range(-dy):
		move(South)
		
def resetPosition():
	#while (get_pos_x() != 0):
	#	move(East)
	#while (get_pos_y() != 0):
	#	move(North)
	goto(0,0)		
	#change_hat(Hats.Gold_Hat)
		
def clearField():
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			goto(i, j)
			
			if (can_harvest() and get_entity_type() != Entities.Grass):
				harvest()
	resetPosition()
	
def tillField():
	for i in range(get_world_size()):
		for j in range(get_world_size()):
			goto(i, j)
			
			if (can_harvest() and get_entity_type() != Entities.Grass):
				harvest()
				
			if get_ground_type() != Grounds.Soil:
				till()
				


def convertCoordsToLinear(x, y):
	return x + y * get_world_size()
	
def convertLinearToCoords(i):
	return (i // get_world_size(), i % get_world_size())	