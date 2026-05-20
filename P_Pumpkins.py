from H_Movement import *
from H_MovementAsync import *
from H_Multithreading import *

def plantPumpkinColumn(x, runCondition):
	ws = get_world_size()
	for y in range(ws):
		if num_items(Items.Carrot) <= num_drones():
			return
		goto(x, y)
		entity = get_entity_type()
		if entity == None or entity == Entities.Dead_Pumpkin:
			plant(Entities.Pumpkin)

def harvestPumpkinColumn(x, runCondition):
	ws = get_world_size()
	done = []
	for y in range(ws):
		done.append(False)

	doneCount = 0
	while doneCount < ws:
		if not runCondition():
			return
		for y in range(ws):
			if done[y]:
				continue
			goto(x, y)
			if can_harvest():
				harvest()
				done[y] = True
				doneCount += 1
				continue
			entity = get_entity_type()
			if entity == None or entity == Entities.Dead_Pumpkin:
				if num_items(Items.Carrot) <= num_drones():
					done[y] = True
					doneCount += 1
					continue
				plant(Entities.Pumpkin)
			else:
				if get_water() < 0.5 and num_items(Items.Water) > num_drones():
					use_item(Items.Water)

def producePumpkins(runCondition):
	clear()
	tillField()
	while runCondition():
		if num_items(Items.Carrot) <= num_drones():
			return
		before = num_items(Items.Pumpkin)
		runWorkers(plantPumpkinColumn, runCondition)
		runWorkers(harvestPumpkinColumn, runCondition)
		if num_items(Items.Pumpkin) <= before:
			return
