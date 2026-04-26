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
		
def executeAndDoTaskByWorldIndex(function):
	drones = []
	
	for i in range(get_world_size()):
		spawned = False
		while not spawned:
			spawned = spawn_drone(function, i)	
			if spawned:
				drones.append(spawned)
			else:
				function(i)
	
	for drone in drones:
		wait_for(drone)
		
