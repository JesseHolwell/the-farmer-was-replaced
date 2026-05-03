from H_Movement import *

def produceBone():
	
	direction = West
	
	while True:
		
		if (get_pos_y() == get_world_size() - 2):
			move(East)
			direction = South
			
		if (get_pos_y() == 0):
			move(East)
			direction = North

		if (get_pos_x() == get_world_size() - 1):
			move(North)
			direction = North
			
		if (get_pos_y() == get_world_size() - 1):
			move(West)
			direction = West
			
		if (get_pos_x() == 0):
			move(South)
			direction = South
			
		move(direction)
		
		if (not can_move(North) and
			not can_move(East) and
			not can_move(South) and
			not can_move(West)):
			change_hat(Hats.Wizard_Hat)
			break
	
	set_world_size(0)
			
produceBone()