from H_Orchestration import *

def any_short(cost):
	for item in cost:
		if num_items(item) < cost[item]:
			return True
	return False

def itemsSnapshot(cost):
	snap = {}
	for item in cost:
		snap[item] = num_items(item)
	return snap

def makeRunCondition(cost):
	def runCondition():
		return any_short(cost)
	return runCondition

def makeItemRunCondition(item, target_amount):
	def runCondition():
		return num_items(item) < target_amount
	return runCondition

def isUnlocked(unlockItem, level):
	return num_unlocked(unlockItem) >= level

def scaleCost(baseCost, multiplier):
	scaled = {}
	for seedItem in baseCost:
		scaled[seedItem] = baseCost[seedItem] * multiplier
	return scaled

def ensureItems(cost):
	for item in cost:
		target_amount = cost[item]
		while num_items(item) < target_amount:
			shortfall = target_amount - num_items(item)
			if item in perPlantSeedEntity:
				seedCost = get_cost(perPlantSeedEntity[item])
				if seedCost:
					safeCost = {}
					for k in seedCost:
						if k != item:
							safeCost[k] = seedCost[k]
					if safeCost:
						ensureItems(scaleCost(safeCost, shortfall))
			producer = selectProducer(item)
			before = num_items(item)
			producer(makeItemRunCondition(item, target_amount))
			after = num_items(item)
			if after <= before:
				quick_print("stuck producing", item, "- have", after, "need", target_amount)
				break

def targetWith(unlockItem, level, producer):
	if isUnlocked(unlockItem, level):
		return

	cost = get_cost(unlockItem)
	if cost == None:
		return

	ensureItems(cost)

	if any_short(cost):
		producer(makeRunCondition(cost))

	unlock(unlockItem)

def target(unlockItem, level):
	if isUnlocked(unlockItem, level):
		return

	cost = get_cost(unlockItem)
	if cost == None:
		return

	quick_print("target", unlockItem, "cost", cost)

	ensureItems(cost)

	if any_short(cost) and unlockItem in initialMap:
		producer = initialMap[unlockItem]
		producer(makeRunCondition(cost))

	unlock(unlockItem)
