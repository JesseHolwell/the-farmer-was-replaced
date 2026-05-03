# Hamiltonian path optimised for apple spawns
	
from Movement import *
from MovementAsync import *

worldsize = 6

def initBone():
	set_world_size(worldsize)

	change_hat(Hats.Straw_Hat)
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
length = 0
	
def getNextDirection():
	
	direction = None
	currX = get_pos_x()
	currY = get_pos_y()
	worldsize = get_world_size()
	
	# if the snake is short, proceed straight to the apple (avoid tail)
	if length < worldsize:
		if (tarX > currX):
			direction = East
		elif (tarX < currX):
			direction = West
		elif (tarY < currY):
			direction = South
		elif (tarY > currY):
			direction = North
	# else, we hit the main code. follow a hamiltonian path with shortcuts
	# if on the top row but not in the top left corner, move west
	# if on the bottom row but not in the bottom right corner, move east
	# if the apple is on the current column, move north/south toward it
	# once the apple is collected, go back to either the top row or bottom row based on where we came from
	# if on an even numbered column, move south
	# if on an odd numbered column, move north	
	else:
		#TODO:
		direction = None
		
	if direction == None:
		do_a_flip()
		
	return direction
		

	
def moveDirection(dir):
	global length
	global tarX
	global tarY
	
	move(dir)
	
	if get_entity_type() == Entities.Apple:
		nextTarget = measure()
		tarX, tarY = nextTarget
		length += 1
	
def produceBoneAsync():
	
	global tarX
	global tarY
	global length
	
	initBone()
	direction = None

	if get_entity_type() == Entities.Apple:
		nextTarget = measure()
		tarX, tarY = nextTarget
		#length += 1
	
	while True:

		direction = getNextDirection()
		if direction == None:
			exit()
			break
			
		moveDirection(direction)
		
	exit()

produceBoneAsync()
	
	
	