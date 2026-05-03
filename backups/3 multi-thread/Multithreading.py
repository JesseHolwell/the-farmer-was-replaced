from Movement import *

def executeTaskByWorldIndex(function):
	drones = []
	
	for i in range(get_world_size()):
		spawned = False
		while not spawned:
			spawned = spawn_drone(function, i)	
			if spawned:
				drones.append(spawned)
	
	for drone in drones:
		wait_for(drone)
		
def executeAndDoTaskByWorldIndex(function, isRow = False):
	drones = []
	
	for i in range(get_world_size()):
		if (isRow):
			goto(0, i)			
		else:
			goto(i, 0)			
		spawned = False
		while not spawned:
			spawned = spawn_drone(function, i)	
			if spawned:
				drones.append(spawned)
			else:
				function(i)
				spawned = True
	
	for drone in drones:
		wait_for(drone)
		
