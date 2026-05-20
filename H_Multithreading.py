from H_Movement import *

def runWorkers(worker, runCondition):
	n = max_drones()
	ws = get_world_size()
	sliceSize = (ws + n - 1) // n

	def runSlice(droneId, runCondition):
		start = droneId * sliceSize
		end = min(start + sliceSize, ws)
		for id in range(start, end):
			if runCondition != None and not runCondition():
				return
			worker(id, runCondition)

	drones = []

	for i in range(n - 1):
		spawned = spawn_drone(runSlice, i, runCondition)
		if spawned:
			drones.append(spawned)

	runSlice(n - 1, runCondition)

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
		
