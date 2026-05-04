from H_Movement import *

def runWorkers(worker, runCondition):
	
	drones = []		
	
	for i in range(max_drones() - 1):
		spawned = spawn_drone(worker, i, runCondition)
		if spawned:
			drones.append(spawned)
		
	worker(max_drones() - 1, runCondition)
				
	for drone in drones:
		wait_for(drone)

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
		
