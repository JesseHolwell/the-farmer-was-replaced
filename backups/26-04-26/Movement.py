def goto(x, y):

	currentX = get_pos_x()
	currentY = get_pos_y()
	
	if (x > get_world_size() or y > get_world_size()):
		return
		
	if (currentX == x and currentY == y):
		return

	# X
	deltaX = abs(currentX - x)

	if (deltaX > get_world_size() / 2):
		if (x > currentX):
			directionX = West
		else:
			directionX = East
		deltaX = get_world_size() - deltaX
	else:
		if (x < currentX):
			directionX = West
		else:
			directionX = East
		
	for i in range(deltaX):
		move(directionX)	
		
	# Y
	deltaY = abs(currentY - y)
	
	if (deltaY > get_world_size() / 2):
		if (y > currentY):
			directionY = South
		else:
			directionY = North
		deltaY = get_world_size() - deltaY
	else:
		if (y < currentY):
			directionY = South
		else:
			directionY = North
		
	for i in range(deltaY):
		move(directionY)	
		
def resetPosition():
	#while (get_pos_x() != 0):
	#	move(East)
	#while (get_pos_y() != 0):
	#	move(North)
	goto(0,0)		
		
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
	