#starterUnlocks = {
#	{Unlocks.Loops:1} : [{Items.Hay:5}, produceHaySingle],
#	{Unlocks.Speed:1} : [{Items.Hay:20}, produceHaySingle],
#	{Unlocks.Expand:1} : [{Items.Hay:30}, produceHaySingle],
#	{Unlocks.Plant:1} : [{Items.Hay:50}, produceHayColumn],
#	{Unlocks.Carrots:1} : [{Items.Wood:50}, produceBushes]
#}

#unlocks = {
#	{Unlocks.Loops:1} : {Items.Hay:5}
#}

def produce(item):
	resources = {
		Items.Hay:produceHay,
		Items.Wood:produceWood,
		Items.Carrot:produceCarrots,
		Items.Pumpkin:producePumpkins,
		Items.Weird_Substance:produceWeird,
		Items.Gold:produceMaze,
		Items.Power:produceSunflowers,
		Items.Cactus:produceCactus,
		Items.Bone:produceDinosaur
	}
		
	return resources[item]

def getRunCondition(unlockItem):
	cost = get_cost(unlockItem)
	return num_items(cost[0]) < cost[1]

def getFunction(unlockItem):
	cost = get_cost(unlockItem)
	return produce(cost[0])





