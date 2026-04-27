# Optimised Hamiltonian Cycle

from Movement import *
from MovementAsync import *

def initBone():
	set_world_size(8)

	change_hat(Hats.Wizard_Hat)
	if can_harvest():
		harvest()
	tillFieldAsync()
	resetPosition()

	change_hat(Hats.Dinosaur_Hat)

def exit():
	change_hat(Hats.Wizard_Hat)
	set_world_size(0)
	
tarX = 0
tarY = 0
tailLength = 0

def moveAndCheck(dir):
	global tarX
	global tarY
	global tailLength

	move(dir)
	if get_entity_type() == Entities.Apple:
		tarX, tarY = measure()
		tailLength += 1

def produceBoneAsync():

	global tarX
	global tarY
	global tailLength

	initBone()
	tarX, tarY = measure()
	tailLength = 0
	worldSize = get_world_size()
	direction = East
	
	while True:
		
		currX = get_pos_x()
		currY = get_pos_y()
			
		#if (tarX % 2 == 0)
		# its a south column
		#else if x % 2 == 1:
		# its a north column
		
		if tarX < currX and (currX % 2 == 1):
		
			# If the tail is still occupying the top row at this x,
			# do not shortcut yet. Just continue the normal path.
			if not tailLength > worldSize - 1 - currX:
		
				while currY != worldSize - 1:
					moveAndCheck(North)
					currY = get_pos_y()
		
				direction = West
		
		if tarX > currX and currY == 0:
			# if a shortcut wont result in a tail collision
			# ignore this for the current column
			if tarX % 2 == 1:
				stopX = tarX
			else:
				stopX = tarX - 1

			# each odd column skipped removes 6 cells from the cycle;
			# tailLength + skipped must stay below worldSize*worldSize
			cycleLen = worldSize * worldSize
			while stopX > 1 and 6 * (stopX - 1) + tailLength >= cycleLen:
				stopX -= 2

			while currX < stopX:
				moveAndCheck(East)
				currX = get_pos_x()
			moveAndCheck(North)
			direction = North
			continue
			
		
		if (get_pos_y() == get_world_size() - 2):
			moveAndCheck(East)
			direction = South
			
		if (get_pos_y() == 0):
			moveAndCheck(East)
			direction = North

		if (get_pos_x() == get_world_size() - 1):
			moveAndCheck(North)
			direction = North
			
		if (get_pos_y() == get_world_size() - 1):
			moveAndCheck(West)
			direction = West
			
		if (get_pos_x() == 0):
			moveAndCheck(South)
			direction = South
			
		moveAndCheck(direction)
		
		if (not can_move(North) and
			not can_move(East) and
			not can_move(South) and
			not can_move(West)):
			change_hat(Hats.Wizard_Hat)
			break
	
	#set_world_size(0)

produceBoneAsync()
